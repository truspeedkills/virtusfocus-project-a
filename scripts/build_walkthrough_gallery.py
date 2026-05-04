"""
Build Mockup_Walkthrough_Gallery.html from App Information for Focus Group/Scott mockindex.html.

Transforms:
1. Updates <title> and header text for walkthrough context.
2. Removes the right-pane <aside> (Session Notes / Design Notes / Source / Status).
3. Filters the screens[] array to only the 9 walkthrough screens, in walkthrough order.
4. Simplifies selectScreen() to drop right-pane updates and notes auto-save.
5. Removes the saveNotes() function (no longer wired up).
6. Strips the status sub-pill from sidebar nav items (cleaner attendee-facing demo).
7. Removes the 1.0x upper cap on phone-frame scaling so it fills available height on a smart-board.
8. Replaces the renderInboxFeed() function body with the walkthrough version
   (real Athlete A Wk12 CM + DD preview + 2 representative daily snippets) loaded
   from scripts/walkthrough_inbox_feed.js.
9. Personalizes the Home screens for the demo: greeting name "Alex" -> "Grace",
   and the shared Coaching Feedback preview card now shows Grace's Wk12 Thursday
   daily snippet (the same text that appears in the Inbox feed, so the Home
   preview literally matches the Inbox message).

All renderXxx functions in the source are preserved untouched.

Run from project root:
    python scripts/build_walkthrough_gallery.py
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "App Information for Focus Group" / "Scott mockindex.html"
INBOX_FEED = REPO_ROOT / "scripts" / "walkthrough_inbox_feed.js"
OUT = REPO_ROOT / "Focus Group Materials" / "Mockup Walkthrough" / "Mockup_Walkthrough_Gallery.html"

# Walkthrough order (per Phase 4 script)
WALKTHROUGH_IDS = [
    "home-morning-active",  # 1. Home (Morning)
    "tuneup-active",        # 2. Tune-Up (Active)
    "bullseye-mid",         # 3. Bullseye (Mid-Entry)
    "journal-active",       # 4. Journal (Active)
    "home-evening-active",  # 5. Home (Evening)
    "er-wtd",               # 6. Evening Review (WTD)
    "home-sunday-active",   # 7. Home (Sunday Recap)
    "recap-active",         # 8. Weekly Recap (Active)
    "inbox-feed",           # 9. Inbox (Feed)
]


def main() -> None:
    src = SRC.read_text(encoding="utf-8")

    # ---- 1. Title and header text ----
    src = src.replace(
        "<title>VirtusFocus – Design Mockup Gallery (Design Docs)</title>",
        "<title>VirtusFocus – Mockup Walkthrough Gallery</title>",
    )
    src = src.replace(
        '<span class="text-zinc-500 text-sm ml-2">Design Doc Mockups</span>',
        '<span class="text-zinc-500 text-sm ml-2">Mockup Walkthrough</span>',
    )
    src = src.replace(
        "Built from design documents — source of truth",
        "May 9 Focus Group Walkthrough",
    )

    # ---- 2. Remove right-pane aside ----
    # Block runs from the "<!-- Right rail" comment to the closing </aside>
    # right before the closing </div> of the 3-column flex container.
    right_pane = re.compile(
        r"\n    <!-- Right rail.*?</aside>\n",
        re.DOTALL,
    )
    new_src, count = right_pane.subn("", src)
    if count != 1:
        raise RuntimeError(f"Expected 1 right-pane block, found {count}")
    src = new_src

    # ---- 3. Filter and reorder screens array ----
    # The array opens with "const screens = [\n" and closes with "\n  ];\n\n  // ─"
    arr_open = "const screens = [\n"
    arr_close_marker = "\n  ];\n\n  // "
    open_idx = src.find(arr_open)
    if open_idx < 0:
        raise RuntimeError("Could not find screens array opening")
    body_start = open_idx + len(arr_open)
    close_idx = src.find(arr_close_marker, body_start)
    if close_idx < 0:
        raise RuntimeError("Could not find screens array closing")
    body = src[body_start:close_idx]

    # Each screen object is bounded by lines that are exactly "    {" (open)
    # and "    }," (close), at the array-element indent depth.
    screen_objects: dict[str, str] = {}
    lines = body.split("\n")
    current: list[str] = []
    in_obj = False
    for line in lines:
        if line == "    {":
            in_obj = True
            current = [line]
        elif in_obj:
            current.append(line)
            if line == "    },":
                block = "\n".join(current)
                m = re.search(r"id: '([^']+)'", block)
                if m:
                    screen_objects[m.group(1)] = block
                in_obj = False
                current = []

    missing = [sid for sid in WALKTHROUGH_IDS if sid not in screen_objects]
    if missing:
        raise RuntimeError(f"Missing walkthrough screen ids: {missing}")

    new_body = "\n".join(screen_objects[sid] for sid in WALKTHROUGH_IDS)
    src = src[:body_start] + new_body + src[close_idx:]

    # ---- 4. Simplify selectScreen() ----
    sel_open = "  function selectScreen(index) {"
    sel_idx = src.find(sel_open)
    if sel_idx < 0:
        raise RuntimeError("selectScreen function not found")
    # Function close is the first line that's exactly "  }" after sel_idx.
    sel_close_match = re.search(r"\n  \}\n", src[sel_idx:])
    if not sel_close_match:
        raise RuntimeError("selectScreen close not found")
    sel_end = sel_idx + sel_close_match.end()

    new_select = (
        "  function selectScreen(index) {\n"
        "    activeIndex = index;\n"
        "    const screen = screens[index];\n"
        "\n"
        "    // Update nav highlight\n"
        "    document.querySelectorAll('.nav-item').forEach((el, i) => {\n"
        "      el.classList.toggle('active', i === index);\n"
        "    });\n"
        "\n"
        "    // Render screen\n"
        "    const content = document.getElementById('screen-content');\n"
        "    content.innerHTML = screen.render();\n"
        "    content.scrollTop = 0;\n"
        "  }\n"
    )
    src = src[:sel_idx] + new_select + src[sel_end:]

    # ---- 5a. Strip status sub-pill from sidebar nav items ----
    src = src.replace(
        "      item.innerHTML = `\n"
        "        <div class=\"text-sm font-semibold text-zinc-200\">${screen.label}</div>\n"
        "        <div class=\"text-xs mt-0.5\" style=\"color:${statusConfig[screen.status].color};\">${statusConfig[screen.status].label}</div>\n"
        "      `;",
        "      item.innerHTML = `\n"
        "        <div class=\"text-sm font-semibold text-zinc-200\">${screen.label}</div>\n"
        "      `;",
    )

    # ---- 5b. Drop the 1.0x cap on phone-frame scaling ----
    src = src.replace(
        "    const scale = Math.min(1, availableHeight / frameHeight, availableWidth / frameWidth);",
        "    const scale = Math.min(availableHeight / frameHeight, availableWidth / frameWidth);",
    )

    # ---- 5c. Update stale layout comment ----
    src = src.replace(
        "<!-- Main layout: fixed 3-column, fills viewport, no page scroll -->",
        "<!-- Main layout: 2-column (nav + phone), fills viewport, no page scroll -->",
    )

    # ---- 5c2. Personalize Home greetings (Alex -> Grace) ----
    # Touches all 6 home renderers (Morning Active/Done, Evening Active/Done,
    # Sunday Active/Done). Only the 3 active variants appear in the walkthrough,
    # but a global replace keeps the source consistent and is harmless on the
    # variants we don't render.
    src = src.replace("Good morning, Alex", "Good morning, Grace")
    src = src.replace("Good evening, Alex", "Good evening, Grace")

    # ---- 5c3. Coaching Feedback preview card content ----
    # Shared coachingCard() helper — replace the placeholder body with Grace's
    # Wk12 Thursday daily snippet (the same text shown in the Inbox feed). This
    # creates literal cohesion: the preview on Home matches the message in the
    # Inbox feed when attendees navigate there.
    src = src.replace(
        "        Yesterday you showed real discipline in how you handled that second set. That's the version of you that wins when it matters.",
        "        Yesterday you got every bunt down on the first pitch and knew it before anyone said it. That noticing is the rep, and you have the same chance to run it today.",
    )

    # ---- 5c4. Weekly Recap (Active) summary stats ----
    # Match Grace's Wk12: 7/7 Morning Tune-Ups, 7/7 Evening Reviews, full
    # Bullseye/Journal engagement (the CM emphasizes "every day this week paired
    # a prompt with something specific you were working on" — 7/7 baseline).
    src = src.replace(
        "            You completed 5 of 7 Morning Tune-Ups this week.<br>\n"
        "            You logged 6 of 7 Evening Reviews this week.<br>\n"
        "            You created 8 Bullseye moments this week.<br>\n"
        "            You wrote 12 Journal entries this week.",
        "            You completed 7 of 7 Morning Tune-Ups this week.<br>\n"
        "            You logged 7 of 7 Evening Reviews this week.<br>\n"
        "            You created 21 Bullseye moments this week.<br>\n"
        "            You wrote 21 Journal entries this week.",
    )

    # ---- 5d. Replace renderInboxFeed() with walkthrough version ----
    inbox_open = "  function renderInboxFeed() {"
    inbox_idx = src.find(inbox_open)
    if inbox_idx < 0:
        raise RuntimeError("renderInboxFeed function not found")
    # Function close is the first line that's exactly "  }" after inbox_idx.
    inbox_close_match = re.search(r"\n  \}\n", src[inbox_idx:])
    if not inbox_close_match:
        raise RuntimeError("renderInboxFeed close not found")
    inbox_end = inbox_idx + inbox_close_match.end()
    new_inbox = INBOX_FEED.read_text(encoding="utf-8")
    if not new_inbox.endswith("\n"):
        new_inbox += "\n"
    src = src[:inbox_idx] + new_inbox + src[inbox_end:]

    # ---- 6. Remove saveNotes() function ----
    sn_open = "  function saveNotes() {"
    sn_idx = src.find(sn_open)
    if sn_idx >= 0:
        sn_close_match = re.search(r"\n  \}\n", src[sn_idx:])
        if not sn_close_match:
            raise RuntimeError("saveNotes close not found")
        sn_end = sn_idx + sn_close_match.end()
        # Also strip the trailing blank line that separates it from the next block.
        if src[sn_end:sn_end + 1] == "\n":
            sn_end += 1
        src = src[:sn_idx] + src[sn_end:]

    # ---- Write output ----
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(src, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Source: {len(SRC.read_text(encoding='utf-8'))} bytes")
    print(f"Output: {len(src)} bytes")
    print(f"Screens included (in walkthrough order): {len(WALKTHROUGH_IDS)}")
    for i, sid in enumerate(WALKTHROUGH_IDS, 1):
        m = re.search(r"label: '([^']+)'", screen_objects[sid])
        print(f"  {i}. {m.group(1)}  [{sid}]")


if __name__ == "__main__":
    main()
