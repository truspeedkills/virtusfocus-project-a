# Journal — Standalone Screen Design Document

**Screen**: Journal (Standalone)
**Phase**: 2 — Standalone Tools
**Screen Number**: 1 of 2 (Journal, then Bullseye)
**Session**: 5 (2026-03-11)
**Status**: COMPLETE

---

## 1. Purpose & Context

The Journal is a standalone reflective writing tool available to athletes 24/7 via the bottom navigation bar. It serves two contexts:

1. **Standalone** — Athletes journal freely throughout the day with no gating, no time restrictions, and no completion requirements. They write when something happens, process it, and move on.
2. **Evening Review (Step 3)** — The same screen renders inside the Evening Review wizard. The wizard provides transition prompts and a Continue CTA; the Journal screen itself is identical.

### Why the Journal Exists

- Gives athletes a structured-but-gentle space to process daily experiences across three life domains
- Feeds the AI coaching pipeline with classified, timestamped reflective data for pattern analysis (e.g., "athlete consistently struggles in school context but thrives in sport")
- Timestamps on discrete entries provide behavioral signal — an athlete who journals at 7 AM, 2 PM, and 9 PM tells a different story than one who writes everything at the deadline
- Supports the decompression arc in Evening Review: after assessing (WTD) and re-centering (Bullseye), the athlete expresses and processes (Journal) before closing

### Design Philosophy

- **Reflection without rumination** — the Journal helps athletes process, not dwell
- **Data capture without emotional charge** — no grading, no word counts, no judgment
- **Calm, coach-led pacing** — gentle prompts, not demands
- **Coach-voice**: "Write what's real. That's enough."
- No streak language, no celebration animations, no score pressure

---

## 2. Screen Architecture

### Layout: Single Scroll, Three Classification Areas

The Journal is a single scrollable screen with three vertically stacked classification sections, followed by a collapsible previous-days section.

```
┌─────────────────────────────────┐
│  ← Journal                      │   Top bar (screen title)
├─────────────────────────────────┤
│                                 │
│  School/Work              [●]   │   Classification header + entry indicator
│  ┌─────────────────────────┐    │
│  │ 7:12 AM                 │    │   Previous entry (read-only, muted)
│  │ "Had a tough quiz in..." │    │   Locked (past edit window)
│  └─────────────────────────┘    │
│  ┌─────────────────────────┐    │
│  │ Classes, homework,      │    │   Active text area (new entry)
│  │ job, projects...        │    │   Placeholder text
│  └─────────────────────────┘    │
│                                 │
│  Sport                    [●]   │   Classification header + entry indicator
│  ┌─────────────────────────┐    │
│  │ Practice, games,        │    │   Active text area (new entry)
│  │ training, competition...│    │   Placeholder text (no prior entries)
│  └─────────────────────────┘    │
│                                 │
│  Homelife                 [ ]   │   Classification header + empty indicator
│  ┌─────────────────────────┐    │
│  │ Family, friends,        │    │   Active text area (new entry)
│  │ downtime, life outside  │    │
│  │ sport...                │    │
│  └─────────────────────────┘    │
│                                 │
│  ▶ Yesterday — Mar 10          │   Collapsed previous day
│  ▶ Mar 9                       │   Collapsed previous day
│                                 │
├─────────────────────────────────┤
│  Inbox · Action · Home · 🎯 · 📓│   Bottom nav (Journal = active)
└─────────────────────────────────┘
```

### Classification Sections

Each of the three sections contains:
1. **Section header**: Classification label + subtle entry indicator
2. **Previous entries** (if any today): Timestamped, read-only cards in chronological order, muted styling
3. **Active text area**: For new entry input, always present at the bottom of each section

### Entry Indicators

Each classification header shows a subtle indicator of today's entry status:
- **Filled indicator** (e.g., small solid dot): At least one entry exists in this classification today
- **Empty indicator** (e.g., small outline dot or no dot): No entries yet today

These indicators provide at-a-glance coverage feedback without feeling like a progress tracker or checklist. No color-coding (green/red), no checkmarks, no counts — just presence/absence.

---

## 3. Entry Model

### Discrete Timestamped Entries

Each classification supports **multiple discrete entries per day**. Each entry is:
- **Timestamped** at creation (hour:minute, AM/PM)
- **Immutable after a 5-minute edit window** — once locked, the entry is read-only for the rest of the day and permanently
- **Displayed in chronological order** within its classification section

### Entry Lifecycle

```
Created → Editable (5-minute window) → Locked (read-only)
```

1. **Created**: Athlete types in the active text area. Text is auto-saved on a short debounce (~2 seconds after typing stops) and on navigation away.
2. **Editable window**: For 5 minutes after creation, the entry remains editable. The athlete can revise typos or rephrase. No visual countdown — the transition is silent.
3. **Locked**: After 5 minutes, the entry becomes read-only. It displays with muted styling alongside other locked entries. A new active text area appears below for additional entries.

### What Constitutes "Creating" an Entry

An entry is created (timestamped) when the athlete begins typing in an active text area and the auto-save fires. If the athlete types and then deletes all text before saving, no entry is created.

An entry must contain at least some text to persist. Whitespace-only content does not count as an entry (auto-trimmed).

### One Active Text Area Per Classification

Each classification always shows exactly one active text area at the bottom of its entry list. This is where new content goes. Previous entries (locked or within edit window) appear above it in chronological order.

---

## 4. Auto-Save Behavior

### Save Triggers

- **Debounced auto-save**: 2 seconds after the athlete stops typing
- **Navigation away**: Any navigation event (bottom nav tap, back button, app backgrounded, Evening Review Continue CTA)
- **Classification switch**: Scrolling to another classification section does NOT trigger save (all sections are on one scroll — no tab switching). Auto-save handles it via debounce.

### Save Indicator

- A subtle "Saved" text appears briefly (1.5 seconds) near the active text area after each auto-save
- No spinner, no animation — just quiet confirmation
- If save fails (network error): "Couldn't save. Will retry." appears in muted text. Entry is preserved locally and retried on next save trigger.

### Local Persistence

- Unsaved text is held in local storage as a draft until successfully synced to the server
- Prevents data loss on network failure, app crash, or unexpected exit
- Draft is cleared once server confirms save

---

## 5. Previous Days Display

### Structure

Below today's three classification sections, the screen shows **2 previous days** as collapsible sections:

- **Yesterday** (labeled as "Yesterday — [Day, Mon DD]")
- **Day before** (labeled as "[Day, Mon DD]")

### Collapsed State (Default)

Previous days are collapsed by default. Each shows:
- Date header (tappable to expand/collapse)
- Chevron indicator (▶ collapsed, ▼ expanded)

### Expanded State

When expanded, a previous day shows all three classifications with their entries:
- Classification headers (School/Work, Sport, Homelife)
- All entries for that day, timestamped, read-only
- Muted styling throughout (reduced contrast, lighter text weight)
- Classifications with no entries for that day show "No entries" in muted italic text
- Tapping the date header again collapses the section

### Edge Cases

- **Day with no entries at all**: Date header still appears. Expanding shows "No entries for this day" across all classifications.
- **Fewer than 2 previous days available** (new user, day 1 or 2): Only show days that exist. No empty placeholder dates.
- **Full history access**: TBD — not in scope for this design. The 2-day lookback is the current limit.

---

## 6. Standalone Behavior

### Entry Points

- **Bottom nav**: Journal icon (rightmost item, position 5). Accessible from any screen at any time.
- **No time restrictions**: Unlike Morning Tune-Up (morning only) and Evening Review (evening only), the standalone Journal is available 24/7.

### Exit Points

- **Back button**: Returns to previous screen (wherever the athlete navigated from)
- **Bottom nav**: Tap any other nav item to navigate away
- **No explicit "Done" or "Save" CTA**: Auto-save handles persistence. The athlete writes and leaves whenever they want.

### No Gating

- Standalone Journal has no requirements. The athlete can open it, look at previous entries, and leave without writing anything.
- The athlete can write in one classification, two, or all three. No enforcement.
- No "Continue" button, no completion state, no progress tracking.

### Re-Entry

- Returning to the Journal (standalone) at any point during the day shows the current state:
  - Previous entries (locked or within edit window) visible in their classifications
  - Fresh active text area at the bottom of each classification for new entries
  - Previous days collapsed below

---

## 7. Evening Review Integration

The Journal screen renders identically inside the Evening Review wizard (Step 3). The differences are handled by the **wizard wrapper layer**, not the Journal screen itself.

### What the Wizard Layer Provides

| Element | Behavior |
|---------|----------|
| **Transition prompt** (above Journal) | "What do you want to note about today?" (no entries) or "Here's what you've written. Anything to add?" (has entries) |
| **Continue CTA** (below Journal) | Disabled until all 3 classifications have at least 1 entry. Enabled once requirement met. |
| **Progress dots** | 4 dots in top bar, dot 3 active |
| **Back arrow** | Exits entire wizard (partial data preserved via auto-save) |

### Gating Logic

The Evening Review Continue CTA is **disabled** until:
- **School/Work** has at least 1 entry (from earlier standalone use or written now)
- **Sport** has at least 1 entry (from earlier standalone use or written now)
- **Homelife** has at least 1 entry (from earlier standalone use or written now)

All three classifications must have content. An entry must contain non-whitespace text to count.

**No minimum word count enforced.** The expectation is at least a few meaningful words, not a single character, but the system does not validate length.

### Shared Data

Entries created in standalone are visible in Evening Review, and vice versa. There is one unified journal for the day — the Evening Review simply provides a gated context for accessing it.

If the athlete journaled in Sport and School/Work via standalone earlier but never touched Homelife, they must add at least one Homelife entry during Evening Review to satisfy the gate.

### Entry Indicators in Evening Review

The same subtle entry indicators (filled/empty dots on classification headers) appear in the Evening Review context. This helps the athlete quickly see which classifications still need entries to satisfy the gate.

---

## 8. Read-Only States

### Previous Days (Standalone)

- Entries from previous days are always read-only
- Muted styling: reduced contrast, lighter text weight
- No edit affordance, no delete option
- Timestamps visible on each entry

### Today's Locked Entries

- Entries past the 5-minute edit window are read-only
- Same muted styling as previous-day entries but grouped under today's date
- Displayed above the active text area within their classification

### Post-Evening Review Completion

When the athlete re-enters the Evening Review via Dynamic Action (moon icon) after completion:
- Journal step shows all entries for the day as read-only
- No active text areas, no ability to add entries
- All classifications displayed with their entries
- Muted styling throughout
- Back button returns to Home

### Post-Hard-Out Lockout

After the hard-out time (default 6:00 AM next day):
- Previous day's entries are permanently read-only
- They appear in the "Yesterday" collapsed section in standalone
- No modification possible regardless of context

---

## 9. Data Model

### Entry Object

```
JournalEntry {
  id: UUID
  athlete_id: UUID
  date: Date (YYYY-MM-DD)
  classification: "school_work" | "sport" | "homelife"
  text: String (trimmed, non-empty)
  created_at: Timestamp (used for display and edit window)
  updated_at: Timestamp (tracks edits within 5-minute window)
  locked_at: Timestamp (created_at + 5 minutes)
  source: "standalone" | "evening_review"
}
```

### Key Data Behaviors

- **One journal per day per athlete**: All entries for a given date belong to the same logical day
- **Day boundary**: Determined by hard-out time (default 6:00 AM). Entries made at 1:00 AM belong to the previous calendar day until hard-out.
- **Classification is set at creation**: The entry belongs to whichever classification's text area it was written in. Cannot be reclassified after creation.
- **Source tracking**: Records whether the entry was created in standalone or Evening Review context. Useful for coaching pipeline (behavioral signal).
- **Soft delete**: No user-facing delete. If needed in the future, entries would be soft-deleted (hidden, not destroyed) to preserve data integrity.

### Day Boundary Logic

The Journal follows the same day-boundary rules as the rest of the app:
- Hard-out time (default 6:00 AM, configurable up to 10:00 AM) defines when a new "day" begins
- An entry created at 11:30 PM belongs to that calendar day
- An entry created at 2:00 AM (before hard-out) belongs to the previous calendar day
- At hard-out, the previous day locks completely. Today's Journal starts fresh.

---

## 10. Entry Points & Navigation

### Entry Points

| Source | Behavior |
|--------|----------|
| Bottom nav (Journal icon) | Opens standalone Journal. Shows today's entries + 2-day lookback. |
| Evening Review Step 3 | Wizard renders Journal screen with transition prompt and Continue CTA. |
| Evening Review read-only review | Journal step shows all entries read-only after completion. |

### Navigation Within Journal

- **Scrolling**: Single continuous scroll through all three classifications and previous days
- **No internal navigation** (no tabs, no pagination, no step indicators)
- **Keyboard**: Active text area focuses on tap. Standard mobile keyboard behavior. Keyboard dismiss on scroll or tap outside.

### Navigation Away

| Action | Behavior |
|--------|----------|
| Bottom nav tap (any item) | Auto-save fires. Navigate to tapped screen. |
| Back button (standalone) | Auto-save fires. Return to previous screen. |
| Back arrow (Evening Review) | Auto-save fires. Exit entire wizard. Partial data preserved. |
| Continue CTA (Evening Review) | Auto-save fires. Advance to Step 4 (Completion). |
| App backgrounded | Auto-save fires immediately. State preserved. |
| App killed | Local draft preserved. Syncs on next launch. |

---

## 11. Empty States

### First-Time User (No Entries Ever)

```
┌─────────────────────────────────┐
│  ← Journal                      │
├─────────────────────────────────┤
│                                 │
│  A place to note what happened  │   Subheader (first visit only)
│  today. Write what's real.      │
│                                 │
│  School/Work              [ ]   │
│  ┌─────────────────────────┐    │
│  │ Classes, homework,      │    │
│  │ job, projects...        │    │
│  └─────────────────────────┘    │
│                                 │
│  Sport                    [ ]   │
│  ┌─────────────────────────┐    │
│  │ Practice, games,        │    │
│  │ training, competition...│    │
│  └─────────────────────────┘    │
│                                 │
│  Homelife                 [ ]   │
│  ┌─────────────────────────┐    │
│  │ Family, friends,        │    │
│  │ downtime, life outside  │    │
│  │ sport...                │    │
│  └─────────────────────────┘    │
│                                 │
│  (no previous days section)     │
│                                 │
├─────────────────────────────────┤
│  Inbox · Action · Home · 🎯 · 📓│
└─────────────────────────────────┘
```

- **Subheader**: "A place to note what happened today. Write what's real." — shown on first visit only (once any entry is created, it never appears again)
- **No previous days section**: Nothing to show. Section appears once there's at least one previous day with entries.
- **Placeholder text** in each text area provides gentle classification guidance
- **No tutorial, no onboarding overlay, no coach popup**

### Today Has No Entries Yet (Returning User)

- Same as above but without the first-visit subheader
- Previous days section appears (collapsed) if applicable
- Placeholder text visible in all three active text areas

### One or Two Classifications Empty (Partial Day)

- Filled classifications show their entries + fresh active text area
- Empty classifications show only the active text area with placeholder text
- Entry indicators reflect current state (filled vs. empty dots)

---

## 12. Edge Cases

### Mid-Entry Exit (Standalone)

- Auto-save fires on navigation away
- If text exists in the active text area, it's saved as a new entry
- On re-entry, that entry appears as a previous entry (locked or within edit window)
- Fresh active text area available below it

### Mid-Entry Exit (Evening Review)

- Auto-save fires on wizard exit (back arrow)
- Partial text saved. On re-entry to Evening Review, athlete resumes at Journal step
- "Welcome back" nudge appears briefly (2 seconds, auto-dismiss)
- Previously saved entries visible; active text areas restore any in-progress drafts from local storage

### Network Failure During Save

- Entry preserved in local storage
- Muted inline message: "Couldn't save. Will retry."
- Auto-retry on next save trigger (debounce, navigation, etc.)
- No blocking — athlete can continue writing
- In Evening Review: Continue CTA still respects gating based on locally persisted entries. If entries exist locally but haven't synced, the gate considers them valid (optimistic). Server sync happens in background.

### Hard-Out Reached During Evening Review

- Wizard locks immediately per Evening Review design doc rules
- Any text in active text areas is auto-saved before lockout
- Partial journal entries preserved but cannot be completed
- No modification allowed after lockout

### App Backgrounded / Killed

- **Backgrounded**: Auto-save fires immediately. Full state preserved.
- **Killed**: Local draft preserved in local storage. On next launch, draft syncs to server. If the athlete was in the Evening Review wizard, they resume at the Journal step.

### Very Long Entries

- No character limit enforced
- Text area grows vertically as the athlete types (auto-expanding)
- Scroll within the overall page, not within individual text areas
- Previous entries with long text show full content (no truncation) — the read-only card expands to fit

### Rapid Multiple Entries

- Athlete saves an entry, edit window starts (5 min), immediately starts a new entry in the same classification
- Both entries coexist: the first in its edit window, the second being actively written
- Each has its own independent timestamp and edit window

### Timezone Changes

- Entries are stamped with the device's local time at creation
- Day boundary follows hard-out time in the program's configured timezone
- If athlete travels across timezones, the program timezone governs day boundaries (not device time)

---

## 13. Copy & Placeholder Text

### Screen Header
- **Title**: "Journal"

### First-Visit Subheader
- "A place to note what happened today. Write what's real."

### Classification Placeholder Text

| Classification | Placeholder |
|---------------|-------------|
| School/Work | "Classes, homework, job, projects..." |
| Sport | "Practice, games, training, competition..." |
| Homelife | "Family, friends, downtime, life outside sport..." |

### Save Indicator
- "Saved" (appears briefly after auto-save, 1.5 seconds)

### Save Error
- "Couldn't save. Will retry."

### Previous Day — No Entries
- "No entries" (muted italic, per classification within an expanded previous day)

### Previous Day — No Entries At All
- "No entries for this day" (muted italic, shown when entire day is empty)

### Evening Review Transition Prompts (wizard layer, not Journal screen)
- No entries: "What do you want to note about today?"
- Has entries: "Here's what you've written. Anything to add?"

---

## 14. Styling Notes

These are guidelines for the developer, not pixel-perfect specs.

### Active Text Areas
- Standard text input styling consistent with app theme
- Sufficient height to invite writing (~3 visible lines minimum) but auto-expanding
- Classification label above each text area, standard weight
- Placeholder text in muted/light color

### Locked Entries (Today, Past Edit Window)
- Muted background or reduced opacity
- Timestamp displayed (e.g., "7:12 AM")
- Text is non-selectable or visually distinct from editable areas
- No edit affordance (no pencil icon, no tap-to-edit)

### Entries Within Edit Window
- Same styling as locked entries BUT with a subtle edit affordance (e.g., tap to re-open for editing)
- No visible timer or countdown — the transition to locked is silent

### Previous Days
- Collapsed: Date header with chevron, standard text weight
- Expanded: All content in muted/reduced contrast styling
- Clear visual separation from today's section (e.g., divider line or spacing)

### Entry Indicators
- Subtle dot on each classification header
- Filled (solid) = has entries today
- Empty (outline) = no entries today
- Small, unobtrusive — not a progress bar or checklist

### Save Indicator
- Small text near the active text area, muted color
- Appears and fades after 1.5 seconds
- No animation, no checkmark — just text

---

## 15. Hard Rules & Constraints

1. **Same screen in both contexts.** The Journal screen is identical in standalone and Evening Review. All differences (transition prompts, Continue CTA, gating) are handled by the Evening Review wizard layer.
2. **All three classifications always visible.** No hiding, collapsing, or removing classifications. The athlete always sees School/Work, Sport, and Homelife.
3. **Auto-save is mandatory.** No explicit save button. Text is preserved on debounce, navigation, backgrounding, and app kill.
4. **5-minute edit window, then locked.** Entries are editable for 5 minutes after creation. After that, read-only permanently. No exceptions.
5. **No delete.** Athletes cannot delete journal entries. Data integrity for the coaching pipeline.
6. **All 3 classifications required in Evening Review.** Continue CTA disabled until School/Work, Sport, and Homelife each have at least one entry with non-whitespace text.
7. **No minimum word count.** System does not validate entry length. A few meaningful words is the expectation, not a rule.
8. **No character/word count display.** No visible counters of any kind.
9. **No emotional grading.** No sentiment indicators, mood tags, or judgment of content.
10. **No streak language.** No "3-day journaling streak!" or similar.
11. **No celebration animations.** No confetti, no fireworks, no "Great job!" on save.
12. **Timestamps are behavioral data.** The time an entry was created matters to the coaching pipeline. Preserve and display.
13. **Day boundary = hard-out time.** Not midnight. Entries before hard-out belong to the previous day.
14. **Entries from standalone count in Evening Review.** Shared data model. No duplication.
15. **Previous days are read-only.** 2-day lookback, collapsed by default, no editing.
16. **Source tracking.** Record whether each entry was created in standalone or Evening Review context.

---

## 16. Data Flow Summary

### Upstream (What Journal Receives)
- Existing journal entries for the current day (from standalone or Evening Review)
- Existing journal entries for the 2 previous days
- Program configuration (hard-out time, for day boundary)

### Downstream (What Journal Produces)
- Timestamped, classified journal entries
- Source context (standalone vs. Evening Review)
- Entry creation/update timestamps
- Feeds: AI coaching pipeline, Weekly Recap aggregation, Evening Review gating

### Evening Review Data Contract

The Evening Review wizard checks the Journal's data to determine gating:

```
Gate condition:
  entries.filter(date == today && classification == "school_work").length >= 1
  AND entries.filter(date == today && classification == "sport").length >= 1
  AND entries.filter(date == today && classification == "homelife").length >= 1
```

If all three conditions are true, Continue CTA is enabled.

---

## 17. Relationship to Other Screens

| Screen | Relationship |
|--------|-------------|
| **Home — Daily Hub** | Bottom nav launches Journal standalone. No Journal preview on Home. |
| **Morning Tune-Up** | No direct relationship. Pattern reference for auto-save and single-scroll layout. |
| **Evening Review** | Journal renders as Step 3. Wizard provides gating, prompts, and Continue CTA. |
| **Bullseye (standalone)** | Sister tool in bottom nav. Will follow same patterns (auto-save, entry model, standalone/ER integration). |
| **Weekly Recap** | Downstream consumer. Uses journal data for coaching analysis. |
| **Messages / Inbox** | No direct relationship. Coaching insights derived from journal data may surface in messages. |

---

## 18. What This Document Does NOT Cover

- **Full history access** beyond 2-day lookback — TBD for a future phase
- **Search or filtering** of journal entries — not in scope
- **Export of journal data** — may be addressed in Settings screen design
- **Coach/admin view** of journal entries — backend concern, not athlete-facing
- **Bullseye standalone design** — next screen in Phase 2, will reference patterns established here
- **Pixel-perfect visual design** — this document defines structure and behavior, not exact colors/fonts/spacing
