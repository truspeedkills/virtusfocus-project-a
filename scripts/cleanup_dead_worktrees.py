#!/usr/bin/env python
"""
cleanup_dead_worktrees.py - manual cleanup of merged Claude Code worktrees.

A worktree is safe to remove only when ALL of these are true:
  1. Its branch is fully merged into origin/master (zero unique commits)
  2. Working tree has no uncommitted changes
  3. It is NOT the worktree currently invoking this script

Also sweeps orphan empty directories under .claude/worktrees/ that have no
.git pointer (leftovers from prior failed cleanups).

Usage:
  python scripts/cleanup_dead_worktrees.py            # do the cleanup
  python scripts/cleanup_dead_worktrees.py --dry-run  # preview only

Exit codes:
  0 - success (or nothing to do)
  1 - one or more worktrees could not be removed (e.g., OneDrive lock)
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


def run(cmd, cwd=None, check=False):
    """Run a command, return (stdout, exit_code, stderr)."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True
    )
    if check and result.returncode != 0:
        print(f"  ERROR: {' '.join(cmd)}")
        print(f"    {result.stderr.strip()}")
    return result.stdout, result.returncode, result.stderr


def list_worktrees():
    """Parse `git worktree list --porcelain` into list of dicts.

    The FIRST entry is always the main worktree (the original repo root).
    Subsequent entries are linked worktrees.
    """
    out, _, _ = run(["git", "worktree", "list", "--porcelain"])
    worktrees = []
    current = {}
    for line in out.splitlines():
        if line.startswith("worktree "):
            if current:
                worktrees.append(current)
            current = {"path": line[len("worktree "):]}
        elif line.startswith("HEAD "):
            current["sha"] = line[len("HEAD "):]
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):].replace("refs/heads/", "")
        elif line == "" and current:
            worktrees.append(current)
            current = {}
    if current:
        worktrees.append(current)
    return worktrees


def get_main_worktree_path():
    """Main folder is always the first entry in git worktree list."""
    wts = list_worktrees()
    if not wts:
        print("ERROR: not inside a git repository.")
        sys.exit(2)
    return Path(wts[0]["path"]).resolve()


def get_current_toplevel():
    """Returns the path of the worktree we're invoked from."""
    out, code, _ = run(["git", "rev-parse", "--show-toplevel"])
    if code != 0 or not out.strip():
        return None
    return Path(out.strip()).resolve()


def is_branch_merged(branch):
    """Return True if branch has zero commits not in origin/master."""
    out, code, _ = run(
        ["git", "log", branch, "--not", "origin/master", "--oneline"]
    )
    return code == 0 and out.strip() == ""


def has_uncommitted(worktree_path):
    """Return True if worktree has any uncommitted changes."""
    out, _, _ = run(["git", "-C", worktree_path, "status", "--porcelain"])
    return out.strip() != ""


def remove_worktree_with_retry(path, branch, dry_run):
    """git worktree remove + git branch -D, with one retry on lock."""
    if dry_run:
        print(f"  [DRY-RUN] would remove worktree: {Path(path).name}")
        print(f"  [DRY-RUN] would delete branch:   {branch}")
        return True

    print(f"  Removing worktree: {Path(path).name}")
    _, code, err = run(["git", "worktree", "remove", path])
    if code != 0:
        lower = err.lower()
        if "permission denied" in lower or "busy" in lower or "locked" in lower:
            print(f"    Locked. Waiting 5s and retrying once...")
            time.sleep(5)
            _, code, err = run(["git", "worktree", "remove", path])

    if code != 0:
        print(f"    SKIPPED (still locked): {err.strip()}")
        print(f"    Manual cleanup needed once OneDrive sync releases lock.")
        return False

    print(f"  Deleting branch:   {branch}")
    _, code2, err2 = run(["git", "branch", "-D", branch])
    if code2 != 0:
        print(f"    Branch deletion failed (non-fatal): {err2.strip()}")
    return True


def sweep_orphan_dirs(worktree_base, registered_paths, dry_run):
    """Remove empty directories under .claude/worktrees/ with no .git pointer."""
    if not worktree_base.exists():
        return 0, 0

    registered = {Path(p).resolve() for p in registered_paths}
    found = 0
    locked = 0

    for d in worktree_base.iterdir():
        if not d.is_dir():
            continue
        if d.resolve() in registered:
            continue

        git_pointer = d / ".git"
        if git_pointer.exists():
            print(f"  Skipping {d.name}: has .git pointer but not registered "
                  "(manual review needed)")
            continue

        try:
            contents = list(d.iterdir())
        except OSError as e:
            print(f"  Skipping {d.name}: cannot read ({e})")
            continue

        if contents:
            print(f"  Skipping {d.name}: not empty (manual review needed)")
            continue

        found += 1
        if dry_run:
            print(f"  [DRY-RUN] would remove orphan: {d.name}")
        else:
            try:
                d.rmdir()
                print(f"  Removed orphan: {d.name}")
            except OSError:
                print(f"  Locked (will release on OneDrive sync or reboot): "
                      f"{d.name}")
                locked += 1

    return found, locked


def main():
    parser = argparse.ArgumentParser(
        description="Cleanup merged Claude Code worktrees."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview only; make no changes."
    )
    args = parser.parse_args()

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN - no changes will be made")
        print("=" * 60)

    main_path = get_main_worktree_path()
    current_wt = get_current_toplevel()
    worktree_base = main_path / ".claude" / "worktrees"

    print("Fetching origin to refresh merge status...")
    run(["git", "fetch", "origin", "master"], cwd=str(main_path))

    print(f"\nMain folder:      {main_path}")
    print(f"Current worktree: {current_wt or '(running outside any worktree)'}\n")

    worktrees = list_worktrees()
    candidates = []
    skipped = []

    for wt in worktrees:
        path = wt["path"]
        branch = wt.get("branch", "(detached)")

        if Path(path).resolve() == main_path:
            continue
        if current_wt and Path(path).resolve() == current_wt:
            skipped.append((path, branch, "currently active session"))
            continue
        if branch == "(detached)" or not branch.startswith("claude/"):
            skipped.append((path, branch, "not a claude/* branch"))
            continue
        if has_uncommitted(path):
            skipped.append((path, branch, "uncommitted changes"))
            continue
        if not is_branch_merged(branch):
            skipped.append((path, branch, "branch has unmerged commits"))
            continue
        candidates.append((path, branch))

    if skipped:
        print("Skipped (with reason):")
        for path, branch, reason in skipped:
            print(f"  {Path(path).name} [{branch}] - {reason}")
        print()

    failures = 0
    if not candidates:
        print("No worktrees safe to remove.")
    else:
        verb = "Would remove" if args.dry_run else "Removing"
        print(f"{verb} {len(candidates)} merged worktree"
              f"{'s' if len(candidates) > 1 else ''}:")
        for path, branch in candidates:
            ok = remove_worktree_with_retry(path, branch, args.dry_run)
            if not ok:
                failures += 1

    print()
    print("Scanning for orphan empty directories...")
    all_registered = [wt["path"] for wt in list_worktrees()]
    _, orphan_locked = sweep_orphan_dirs(worktree_base, all_registered, args.dry_run)
    failures += orphan_locked

    print()
    if args.dry_run:
        print("DRY RUN complete. Re-run without --dry-run to apply.")
    elif failures:
        print(f"Cleanup complete with {failures} item(s) skipped due to locks.")
        sys.exit(1)
    else:
        print("Cleanup complete.")


if __name__ == "__main__":
    main()
