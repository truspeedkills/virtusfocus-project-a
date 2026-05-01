# Bullseye Reflection — Standalone Screen Design Document

**Screen**: Bullseye Reflection (Standalone)
**Phase**: 2 — Standalone Tools
**Screen Number**: 2 of 2 (Journal, then Bullseye)
**Session**: 6 (2026-03-12)
**Status**: COMPLETE

---

## 1. Purpose & Context

The Bullseye Reflection is a standalone moment-logging tool available to athletes 24/7 via the bottom navigation bar. It teaches athletes to classify events into three zones — Can Control, Can Influence, Can't Control — building emotional regulation and self-leadership as a daily habit.

It serves two contexts:

1. **Standalone** — Athletes log moments in real-time throughout the day. No gating, no time restrictions, no completion requirements. Something happens, they classify it, they move on. Speed and low friction are the priority.
2. **Evening Review (Step 2)** — The same screen renders inside the Evening Review wizard. The wizard provides transition prompts and a Continue CTA; the Bullseye screen itself is identical.

### Why Bullseye Exists

- Teaches athletes to separate what they can control from what they can't — the core Bullseye Method
- Builds emotional regulation: classify the event, reframe, move forward
- Feeds the AI coaching pipeline with classified, timestamped moment data for pattern analysis (e.g., "athlete consistently puts team dynamics in Can't Control — coaching opportunity for influence reframing")
- Timestamps and tags provide behavioral signal — an athlete who processes moments in real-time tells a different story than one who batches everything at night
- Supports the decompression arc in Evening Review: after assessing (WTD), the athlete re-centers focus (Bullseye) before expressing (Journal) and closing

### How Bullseye Differs from Journal

| Aspect | Journal | Bullseye |
|--------|---------|----------|
| **Nature** | Reflective — process and express | Reactive — classify and reframe |
| **Unit of entry** | Text per life domain (School/Work, Sport, Homelife) | Moment — a specific event classified across zones |
| **Cadence** | Write when something needs processing | Log when something happens (real-time or soon after) |
| **Speed priority** | Moderate — reflective writing takes time | High — 10-second capture during competition/conflict |
| **Structure** | Three independent domain text areas | Grouped moment: event description + 1–3 zone entries + optional tag |
| **Shared patterns** | Auto-save, entry indicators, source tracking, day boundary, 5-min edit window, 2-day lookback | Same |

### Design Philosophy

- **Reflection without rumination** — classify and move forward, don't dwell
- **Data capture without emotional charge** — no grading, no judgment on what goes where
- **Calm, coach-led pacing** — gentle prompts, not demands
- **Fast and low-friction in standalone** — the athlete is busy living; the app gets out of the way
- **Coach-voice**: brief, grounded, no hype
- No streak language, no celebration animations, no score pressure

---

## 2. Screen Architecture

### Layout: Moment-Based Flow, Single Scroll

The Bullseye screen is a single scrollable screen. At the top is the active moment input area (event description + three zone text areas + optional tag). Below it are previous moments for today (as collapsed cards), followed by a collapsible previous-days section.

```
+---------------------------------+
|  <- Bullseye                    |   Top bar (screen title)
+---------------------------------+
|                                 |
|  What happened?                 |   Event prompt
|  +-------------------------+    |
|  | Describe the moment...  |    |   Text area (required)
|  +-------------------------+    |
|                                 |
|  Can Control              [ ]   |   Zone 1 + entry indicator
|  +-------------------------+    |
|  | Attitude, effort,       |    |
|  | choices...              |    |   Placeholder text
|  +-------------------------+    |
|                                 |
|  Can Influence            [ ]   |   Zone 2 + entry indicator
|  +-------------------------+    |
|  | Communication,          |    |
|  | leadership...           |    |
|  +-------------------------+    |
|                                 |
|  Can't Control            [ ]   |   Zone 3 + entry indicator
|  +-------------------------+    |
|  | Others' decisions,      |    |
|  | the past...             |    |
|  +-------------------------+    |
|                                 |
|  [Competition] [School] [Home]  |   Optional tag chips
|  [Social] [Practice/Training]   |
|                                 |
|  ----- Previous moments ------  |
|  +-------------------------+    |
|  | 2:15 PM - competition   |    |   Moment card (locked)
|  | "Ref made a bad call"   |    |
|  | Can't Control: ref call |    |
|  | Can Control: my response|    |
|  +-------------------------+    |
|                                 |
|  + New Moment                   |   New moment button (when
|                                 |   input area is collapsed)
|                                 |
|  > Yesterday - Mar 11          |   Collapsed previous day
|  > Mar 10                       |   Collapsed previous day
|                                 |
+---------------------------------+
|  Inbox - Action - Home - @ - =  |   Bottom nav (Bullseye = active)
+---------------------------------+
```

### Active Moment Input Area

The top section of the screen is the active moment input — where the athlete creates a new moment. It contains:

1. **"What happened?" prompt and text area** — required field, anchors the moment
2. **Three zone text areas** — Can Control, Can Influence, Can't Control. Each with placeholder text. At least one must be filled for the moment to save, but the athlete can fill any combination.
3. **Tag chips** — optional, pre-defined. One tap to select, tap again to deselect. Only one tag per moment.

### Entry Indicators

Each zone header shows a subtle indicator of today's coverage status **across all moments**:
- **Filled indicator** (small solid dot): At least one moment today has text in this zone
- **Empty indicator** (small outline dot): No moments today have text in this zone

These indicators provide at-a-glance zone coverage feedback — especially useful during Evening Review to see which zones still need entries. Not a progress bar or checklist. No color-coding, no checkmarks, no counts.

---

## 3. Moment Model

### What Is a Moment

A moment is the discrete unit of entry in Bullseye. It represents a specific event or situation the athlete is classifying. Each moment contains:

- **Event description** ("What happened?") — required, free text
- **Zone entries** — 1 to 3 free-text fields (Can Control, Can Influence, Can't Control). At least one zone must have content.
- **Tag** — optional, one pre-defined label
- **Timestamp** — set at creation
- **Source** — standalone or evening_review

### Moment Lifecycle

```
Created --> Editable (5-minute window) --> Locked (read-only)
```

1. **Created**: Athlete types in the "What happened?" field. The moment is timestamped when auto-save first fires (2-second debounce after typing stops). Zone entries and tag are attached to this moment.
2. **Editable window**: For 5 minutes after creation, the entire moment remains editable — event description, zone entries, and tag. No visual countdown; the transition is silent.
3. **Locked**: After 5 minutes, the moment becomes read-only. It displays as a collapsed card in the "Previous moments" section. The active input area resets for a new moment.

### What Constitutes "Creating" a Moment

A moment is created (timestamped) when:
- The athlete has typed non-whitespace text in the "What happened?" field AND at least one zone field
- Auto-save fires (debounce or navigation trigger)

If the athlete types only in "What happened?" but no zones (or vice versa), the content is held as a local draft but not persisted as a moment until both conditions are met.

### Moment Boundary — "+ New Moment" Button

After a moment is saved and its edit window expires (or the athlete scrolls past it), the active input area shows the current in-progress moment (if any) or empty fields ready for a new moment.

**When the athlete completes a moment and wants to start another:**
- The saved moment collapses into a card in the "Previous moments" section
- A **"+ New Moment"** button appears where the active input was
- Tapping it opens fresh input fields (empty "What happened?", empty zones, no tag selected)

**Auto-collapse timing**: The active input area collapses into a card when:
- The athlete taps "+ New Moment" (explicit)
- The 5-minute edit window expires on the current moment (automatic — fields reset)
- The athlete navigates away and returns (auto-save fires, moment saved, fresh input on return)

**First visit / no active moment**: The input fields are open and ready by default. No "+ New Moment" button needed — the fields are already there.

---

## 4. Zone Details

### The Three Zones

| Zone | Label | Ring | Description | Placeholder Text |
|------|-------|------|-------------|-----------------|
| 1 | **Can Control** | Center Ring | Things within the athlete's direct power | "Attitude, effort, breathing, choices..." |
| 2 | **Can Influence** | Middle Ring | Things the athlete can affect but not control directly | "Communication, leadership, team culture..." |
| 3 | **Can't Control** | Outer Ring | Things fully outside the athlete's power | "Others' decisions, weather, the past..." |

### Zone Input Rules

- **Free text** — no structured checklists, no dropdowns
- **At least one zone required per moment** — the moment must have at least one zone with non-whitespace text to save
- **Not all zones required per moment in standalone** — the athlete can fill one, two, or all three
- **All three zones required across the day in Evening Review** — gating checks aggregate zone coverage (see Section 7)
- **No maximum length** — text areas auto-expand as the athlete types
- **No word count display** — no visible counters of any kind

### Zone Order

Zones are always displayed in the same order: Can Control (top) → Can Influence (middle) → Can't Control (bottom). This order mirrors the bullseye target from center outward and is consistent across standalone and Evening Review.

---

## 5. Moment Tagging

### Tag Set

Tags are optional metadata that categorize the type of event. Pre-defined set:

| Tag | Description |
|-----|-------------|
| **Competition** | Games, matches, tournaments, races |
| **School** | Classes, homework, exams, projects |
| **Home** | Family, household, personal life |
| **Social** | Friends, relationships, social situations |
| **Practice/Training** | Practice sessions, workouts, skill development |

### Tag Interaction

- Tags are displayed as **tappable chips** in a horizontal row below the zone text areas
- **One tag per moment** — selecting a tag deselects any previously selected tag
- **Tap to select, tap again to deselect** — simple toggle
- **Optional** — a moment with no tag is valid. Default state: no tag selected (null)
- Tags appear in muted/outline style when unselected and filled/highlighted when selected

### Tag Display on Saved Moments

When a moment is saved and displayed as a card, the tag appears next to the timestamp (e.g., "2:15 PM - competition"). If no tag, only the timestamp appears.

### Why Pre-Defined (Not Free-Form)

- Consistent labels enable reliable pattern analysis in the AI pipeline
- Free-form tags create fragmentation ("game" vs "games" vs "match" vs "competition")
- Five options is fast to scan — no typing, one tap
- The tag set covers the major life contexts from the source material

### Future Extensibility

The tag set may expand in future versions (e.g., "Work/Job" for older athletes). The UI should accommodate additional chips without breaking layout. But for v1, this set is locked.

---

## 6. Auto-Save Behavior

### Save Triggers

- **Debounced auto-save**: 2 seconds after the athlete stops typing in any field
- **Navigation away**: Any navigation event (bottom nav tap, back button, app backgrounded, Evening Review Continue CTA)
- **App killed**: Local draft preserved in local storage, synced on next launch

### What Gets Saved

Auto-save persists the entire in-progress moment atomically:
- "What happened?" text
- Zone entries (whichever have content)
- Selected tag (if any)

A moment is only persisted to the server when it meets minimum requirements (non-whitespace "What happened?" + at least one non-whitespace zone entry). Until then, content is held as a local draft.

### Save Indicator

- A subtle **"Saved"** text appears briefly (1.5 seconds) near the active input area after each auto-save
- No spinner, no animation — just quiet confirmation
- If save fails (network error): **"Couldn't save. Will retry."** appears in muted text. Moment preserved locally and retried on next save trigger.

### Local Persistence

- Unsaved moment content held in local storage as a draft until server confirms save
- Prevents data loss on network failure, app crash, or unexpected exit
- Draft cleared once server confirms save

---

## 7. Evening Review Integration

The Bullseye screen renders identically inside the Evening Review wizard (Step 2). The differences are handled by the **wizard wrapper layer**, not the Bullseye screen itself.

### What the Wizard Layer Provides

| Element | Behavior |
|---------|----------|
| **Transition prompt** (above Bullseye) | "Log your controllables from today." (no entries) or "Here's what you've logged. Want to add anything?" (has entries) |
| **Continue CTA** (below Bullseye) | Disabled until all 3 zones have coverage across the day's moments. Enabled once requirement met. |
| **Progress dots** | 4 dots in top bar, dot 2 active |
| **Back arrow** | Exits entire wizard (partial data preserved via auto-save) |

### Gating Logic

The Evening Review Continue CTA is **disabled** until all three zones have at least one entry across the day's moments:

```
Gate condition:
  moments.filter(date == today).some(m => m.can_control is non-empty)
  AND moments.filter(date == today).some(m => m.can_influence is non-empty)
  AND moments.filter(date == today).some(m => m.can_control_not is non-empty)
```

**Key**: The gate checks **aggregate zone coverage across all moments for the day**, not per-moment. If Moment A has "Can Control" filled and Moment B has "Can Influence" filled, the athlete only needs to cover "Can't Control" (in either existing moment's edit window or a new moment).

Entries from earlier standalone usage satisfy the requirement. If the athlete used Bullseye standalone earlier and collectively covered all three zones, they can review and Continue without adding more.

### Entry Indicators in Evening Review

The same subtle entry indicators (filled/empty dots on zone headers) appear in the Evening Review context. This helps the athlete quickly see which zones still need coverage to satisfy the gate.

### Shared Data

Moments created in standalone are visible in Evening Review, and vice versa. There is one unified Bullseye log for the day — the Evening Review simply provides a gated context for accessing it.

### Same Screen, Different Frame

The Evening Review wizard's transition prompt frames the tool for day-level reflection. The athlete can:
- Create one moment covering the whole day ("What happened? → My day overall")
- Create multiple moments for specific events
- Review existing standalone moments and add more if needed
- Proceed immediately if zone coverage is already satisfied

The screen itself does not change between contexts.

---

## 8. Previous Days Display

### Structure

Below today's moments, the screen shows **2 previous days** as collapsible sections:

- **Yesterday** (labeled as "Yesterday — [Day, Mon DD]")
- **Day before** (labeled as "[Day, Mon DD]")

### Collapsed State (Default)

Previous days are collapsed by default. Each shows:
- Date header (tappable to expand/collapse)
- Chevron indicator (> collapsed, v expanded)
- Moment count in muted text (e.g., "3 moments")

### Expanded State

When expanded, a previous day shows all moments for that day as read-only cards:
- Each card shows: timestamp, tag (if any), "What happened?" text, and zone entries
- Muted styling throughout (reduced contrast, lighter text weight)
- Moments in chronological order
- Tapping the date header again collapses the section

### Edge Cases

- **Day with no moments**: Date header still appears. Expanding shows "No moments logged" in muted italic text.
- **Fewer than 2 previous days available** (new user, day 1 or 2): Only show days that exist. No empty placeholder dates.
- **Full history access**: TBD — not in scope for this design. 2-day lookback is the current limit.

---

## 9. Standalone Behavior

### Entry Points

- **Bottom nav**: Bullseye icon (4th item, position 4). Accessible from any screen at any time.
- **No time restrictions**: Unlike Morning Tune-Up (morning only) and Evening Review (evening only), the standalone Bullseye is available 24/7.

### Exit Points

- **Back button**: Returns to previous screen (wherever the athlete navigated from)
- **Bottom nav**: Tap any other nav item to navigate away
- **No explicit "Done" or "Save" CTA**: Auto-save handles persistence. The athlete logs and leaves.

### No Gating

- Standalone Bullseye has no requirements. The athlete can open it, look at previous moments, and leave without logging anything.
- The athlete can fill one zone, two, or all three per moment. No enforcement.
- No "Continue" button, no completion state, no progress tracking.

### Re-Entry

- Returning to Bullseye (standalone) at any point during the day shows the current state:
  - If a moment is within its edit window: that moment's fields are editable
  - If no active moment: fresh input fields ready for a new moment (or "+ New Moment" button if previous moments exist)
  - Previous moments displayed as cards below
  - Previous days collapsed below

---

## 10. Read-Only States

### Previous Days (Standalone)

- Moments from previous days are always read-only
- Muted styling: reduced contrast, lighter text weight
- No edit affordance, no delete option
- Timestamps and tags visible on each moment card

### Today's Locked Moments

- Moments past the 5-minute edit window are read-only
- Displayed as collapsed cards in the "Previous moments" section
- Same muted styling as previous-day moments
- No edit affordance (no pencil icon, no tap-to-edit)

### Moments Within Edit Window

- Same card layout as locked moments BUT with a subtle edit affordance (e.g., tap to re-open for editing)
- No visible timer or countdown — the transition to locked is silent

### Post-Evening Review Completion

When the athlete re-enters the Evening Review via Dynamic Action (moon icon) after completion:
- Bullseye step shows all moments for the day as read-only cards
- No active input area, no ability to create moments
- All zone entries displayed within each moment card
- Muted styling throughout
- Back button returns to Home

### Post-Hard-Out Lockout

After the hard-out time (default 6:00 AM next day):
- Previous day's moments are permanently read-only
- They appear in the "Yesterday" collapsed section in standalone
- No modification possible regardless of context

---

## 11. Empty States

### First-Time User (No Moments Ever)

```
+---------------------------------+
|  <- Bullseye                    |
+---------------------------------+
|                                 |
|  Name what happened. Put it     |   Subheader (first visit only)
|  in the right ring. Move on.   |
|                                 |
|  What happened?                 |
|  +-------------------------+    |
|  | Describe the moment...  |    |
|  +-------------------------+    |
|                                 |
|  Can Control              [ ]   |
|  +-------------------------+    |
|  | Attitude, effort,       |    |
|  | choices...              |    |
|  +-------------------------+    |
|                                 |
|  Can Influence            [ ]   |
|  +-------------------------+    |
|  | Communication,          |    |
|  | leadership...           |    |
|  +-------------------------+    |
|                                 |
|  Can't Control            [ ]   |
|  +-------------------------+    |
|  | Others' decisions,      |    |
|  | the past...             |    |
|  +-------------------------+    |
|                                 |
|  [Competition] [School] [Home]  |
|  [Social] [Practice/Training]   |
|                                 |
|  (no previous moments section)  |
|  (no previous days section)     |
|                                 |
+---------------------------------+
|  Inbox - Action - Home - @ - =  |
+---------------------------------+
```

- **Subheader**: "Name what happened. Put it in the right ring. Move on." — shown on first visit only (once any moment is created, it never appears again)
- **No previous moments section**: Nothing to show.
- **No previous days section**: Nothing to show. Section appears once there's at least one previous day with moments.
- **Placeholder text** in each text area provides gentle zone guidance
- **No tutorial, no onboarding overlay, no coach popup**

### Today Has No Moments Yet (Returning User)

- Same as above but without the first-visit subheader
- Previous days section appears (collapsed) if applicable
- Input fields open and ready

### Evening Review — No Moments Yet

- Wizard transition prompt: "Log your controllables from today."
- Empty input fields. Entry indicators show all zones empty (outline dots).
- Continue CTA disabled.

### Evening Review — Has Moments, All Zones Covered

- Wizard transition prompt: "Here's what you've logged. Want to add anything?"
- Previous moments visible as cards. Entry indicators show all zones filled (solid dots).
- Continue CTA enabled — athlete can proceed immediately or add more.

### Evening Review — Has Moments, Partial Zone Coverage

- Wizard transition prompt: "Here's what you've logged. Want to add anything?"
- Previous moments visible. Entry indicators show which zones are covered (filled) and which still need entries (empty).
- Continue CTA disabled until all three zones have coverage.

---

## 12. Moment Card Layout (Saved/Locked Moments)

### Card Structure

Each saved moment displays as a compact card:

```
+---------------------------------+
| 2:15 PM - competition           |   Timestamp + tag
| "Ref made a bad call during     |   Event description (truncated
|  the second half"               |   to ~2 lines, tap to expand)
|                                 |
| Can Control: Kept my composure  |   Zone entries (only zones
| Can't Control: The ref's call   |   that have content shown)
+---------------------------------+
```

### Card Rules

- **Timestamp** always shown (hour:minute AM/PM)
- **Tag** shown next to timestamp if present; omitted if null
- **Event description** shown in quotes, truncated to ~2 lines with "..." if longer. Tap card to expand full text.
- **Zone entries** listed below event description. Only zones with content are shown (no empty "Can Influence: —" lines).
- **Zone labels** shown as prefixes (e.g., "Can Control: [text]")
- **Muted styling** for locked moments (past edit window). Slightly less muted for moments within edit window (with edit affordance).
- **Chronological order** — newest moment at the top of the list, closest to the active input area

---

## 13. Data Model

### Moment Object

```
BullseyeMoment {
  id: UUID
  athlete_id: UUID
  date: Date (YYYY-MM-DD)
  event_description: String (trimmed, non-empty, required)
  can_control: String | null (trimmed, null if empty)
  can_influence: String | null (trimmed, null if empty)
  cannot_control: String | null (trimmed, null if empty)
  tag: "competition" | "school" | "home" | "social" | "practice_training" | null
  created_at: Timestamp (used for display and edit window)
  updated_at: Timestamp (tracks edits within 5-minute window)
  locked_at: Timestamp (created_at + 5 minutes)
  source: "standalone" | "evening_review"
}
```

### Validation Rules

- `event_description` is required — must contain non-whitespace text
- At least one of `can_control`, `can_influence`, `cannot_control` must be non-null and non-whitespace
- `tag` is optional (null is valid)
- `source` is set automatically based on context

### Key Data Behaviors

- **One Bullseye log per day per athlete**: All moments for a given date belong to the same logical day
- **Day boundary**: Determined by hard-out time (default 6:00 AM). Moments made at 1:00 AM belong to the previous calendar day until hard-out.
- **Zone entries are set per moment**: Each zone field belongs to the moment it was created with. Cannot be reclassified after creation.
- **Source tracking**: Records whether the moment was created in standalone or Evening Review context. Useful for coaching pipeline (behavioral signal: real-time processor vs. end-of-day batcher).
- **No delete**: Athletes cannot delete moments. Data integrity for the coaching pipeline.
- **Soft delete**: If needed in the future, moments would be soft-deleted (hidden, not destroyed).

### Day Boundary Logic

The Bullseye follows the same day-boundary rules as the rest of the app:
- Hard-out time (default 6:00 AM, configurable up to 10:00 AM) defines when a new "day" begins
- A moment created at 11:30 PM belongs to that calendar day
- A moment created at 2:00 AM (before hard-out) belongs to the previous calendar day
- At hard-out, the previous day locks completely. Today's Bullseye starts fresh.

---

## 14. Entry Points & Navigation

### Entry Points

| Source | Behavior |
|--------|----------|
| Bottom nav (Bullseye icon) | Opens standalone Bullseye. Shows active input + today's moments + 2-day lookback. |
| Evening Review Step 2 | Wizard renders Bullseye screen with transition prompt and Continue CTA. |
| Evening Review read-only review | Bullseye step shows all moments read-only after completion. |

### Navigation Within Bullseye

- **Scrolling**: Single continuous scroll through active input, previous moments, and previous days
- **No internal navigation** (no tabs, no pagination, no step indicators)
- **Keyboard**: Text areas focus on tap. Standard mobile keyboard behavior. Keyboard dismiss on scroll or tap outside.

### Navigation Away

| Action | Behavior |
|--------|----------|
| Bottom nav tap (any item) | Auto-save fires. Navigate to tapped screen. |
| Back button (standalone) | Auto-save fires. Return to previous screen. |
| Back arrow (Evening Review) | Auto-save fires. Exit entire wizard. Partial data preserved. |
| Continue CTA (Evening Review) | Auto-save fires. Advance to Step 3 (Journal). |
| App backgrounded | Auto-save fires immediately. State preserved. |
| App killed | Local draft preserved. Syncs on next launch. |

---

## 15. Edge Cases

### Mid-Moment Exit (Standalone)

- Auto-save fires on navigation away
- If moment meets minimum requirements (non-whitespace "What happened?" + at least one zone), it's saved as a moment
- If only partial content (e.g., "What happened?" filled but no zones), content held as local draft. On re-entry, draft restored in the input fields.
- On re-entry with a saved moment: if within edit window, moment is editable. If past edit window, moment is a locked card and fresh input fields appear.

### Mid-Moment Exit (Evening Review)

- Auto-save fires on wizard exit (back arrow)
- Partial moment content saved (either as moment or draft depending on completeness)
- On re-entry to Evening Review, athlete resumes at Bullseye step
- "Welcome back" nudge appears briefly (2 seconds, auto-dismiss): "Pick up where you left off."
- Previously saved moments visible; active input restores any in-progress draft from local storage

### Network Failure During Save

- Moment preserved in local storage
- Muted inline message: "Couldn't save. Will retry."
- Auto-retry on next save trigger (debounce, navigation, etc.)
- No blocking — athlete can continue logging
- In Evening Review: Continue CTA still respects gating based on locally persisted moments. If moments exist locally but haven't synced, the gate considers them valid (optimistic). Server sync happens in background.

### Hard-Out Reached During Evening Review

- Wizard locks immediately per Evening Review design doc rules
- Any content in active input fields is auto-saved before lockout
- Partial moments preserved but cannot be completed
- No modification allowed after lockout

### App Backgrounded / Killed

- **Backgrounded**: Auto-save fires immediately. Full state preserved.
- **Killed**: Local draft preserved in local storage. On next launch, draft syncs to server. If the athlete was in the Evening Review wizard, they resume at the Bullseye step.

### Very Long Zone Entries

- No character limit enforced
- Text areas grow vertically as the athlete types (auto-expanding)
- Scroll within the overall page, not within individual text areas
- Moment cards with long text truncate to ~2 lines with tap-to-expand

### Rapid Multiple Moments

- Athlete saves a moment, edit window starts (5 min), immediately taps "+ New Moment"
- Both moments coexist: the first in its edit window (shown as an editable card), the second being actively written in the input area
- Each has its own independent timestamp and edit window

### Timezone Changes

- Moments are stamped with the device's local time at creation
- Day boundary follows hard-out time in the program's configured timezone
- If athlete travels across timezones, the program timezone governs day boundaries (not device time)

### "+ New Moment" When Current Input Has Unsaved Content

- If the athlete has started typing in the active input but hasn't triggered auto-save yet, and taps "+ New Moment" — auto-save fires first, saving the current content as a moment (if valid) or discarding (if incomplete). Then fresh fields appear.
- If current content is incomplete (e.g., "What happened?" only, no zones), show a brief inline message: "Add at least one ring to save this moment." The input stays open; "+ New Moment" does not fire.

---

## 16. Copy & Placeholder Text

### Screen Header
- **Title**: "Bullseye"

### First-Visit Subheader
- "Name what happened. Put it in the right ring. Move on."

### Event Description Prompt
- **Label**: "What happened?"
- **Placeholder**: "Describe the moment..."

### Zone Placeholder Text

| Zone | Placeholder |
|------|-------------|
| Can Control | "Attitude, effort, breathing, choices..." |
| Can Influence | "Communication, leadership, team culture..." |
| Can't Control | "Others' decisions, weather, the past..." |

### Tag Labels
- Competition, School, Home, Social, Practice/Training

### New Moment Button
- "+ New Moment"

### Save Indicator
- "Saved" (appears briefly after auto-save, 1.5 seconds)

### Save Error
- "Couldn't save. Will retry."

### Incomplete Moment Warning
- "Add at least one ring to save this moment."

### Previous Day — No Moments
- "No moments logged" (muted italic, shown when day is expanded but empty)

### Evening Review Transition Prompts (wizard layer, not Bullseye screen)
- No entries: "Log your controllables from today."
- Has entries: "Here's what you've logged. Want to add anything?"

### Welcome Back Nudge (Evening Review re-entry)
- "Pick up where you left off."

---

## 17. Styling Notes

These are guidelines for the developer, not pixel-perfect specs.

### Active Input Area
- Standard text input styling consistent with app theme
- "What happened?" text area: ~2 visible lines minimum, auto-expanding
- Zone text areas: ~2 visible lines minimum, auto-expanding
- Zone labels above each text area, standard weight
- Placeholder text in muted/light color
- Clear visual grouping of the active input area (the "What happened?" + zones + tags form a single visual block)

### Tag Chips
- Horizontal row, wrapping if needed
- Unselected: outline/muted style
- Selected: filled/highlighted style
- Tappable with adequate touch targets (minimum 36px height)
- One selected at a time (radio behavior)

### Moment Cards (Locked)
- Muted background or reduced opacity
- Timestamp + tag displayed at top
- Event description in quotes, truncated to ~2 lines
- Zone entries listed with labels
- No edit affordance
- Subtle visual separation between cards (spacing or divider)

### Moment Cards (Within Edit Window)
- Same layout as locked cards but slightly less muted
- Subtle edit affordance (e.g., tap to re-open for editing, small pencil icon or "Edit" text)
- No visible timer or countdown

### "+ New Moment" Button
- Subtle, not dominant — secondary action styling
- Positioned between the last moment card and the previous days section
- Only visible when no active input area is open

### Previous Days
- Collapsed: Date header with chevron + moment count, standard text weight
- Expanded: All moment cards in muted/reduced contrast styling
- Clear visual separation from today's section

### Entry Indicators
- Subtle dot on each zone header
- Filled (solid) = at least one moment today has text in this zone
- Empty (outline) = no moments today have text in this zone
- Small, unobtrusive

### Save Indicator
- Small text near the active input area, muted color
- Appears and fades after 1.5 seconds
- No animation, no checkmark — just text

---

## 18. Hard Rules & Constraints

1. **Same screen in both contexts.** The Bullseye screen is identical in standalone and Evening Review. All differences (transition prompts, Continue CTA, gating) are handled by the Evening Review wizard layer.
2. **Moment-based entry model.** Each Bullseye entry is a moment — an event description + zone classifications + optional tag. Not three independent zone text areas.
3. **"What happened?" is required.** Every moment must have an event description. Zones without an anchor event are meaningless.
4. **At least one zone required per moment.** A moment must classify the event into at least one zone to save.
5. **All three zones required across the day in Evening Review.** Continue CTA disabled until Can Control, Can Influence, and Can't Control each have at least one entry across all moments for the day.
6. **Auto-save is mandatory.** No explicit save button. Content preserved on debounce, navigation, backgrounding, and app kill.
7. **5-minute edit window, then locked.** Moments are editable for 5 minutes after creation. After that, read-only permanently. No exceptions.
8. **No delete.** Athletes cannot delete moments. Data integrity for the coaching pipeline.
9. **Explicit "+ New Moment" trigger.** Moment boundaries are intentional, not implicit. The athlete actively starts a new moment.
10. **Tags are optional.** No enforcement. A moment without a tag is valid.
11. **Tags are pre-defined.** No free-form tagging. The set is: Competition, School, Home, Social, Practice/Training.
12. **No character/word count display.** No visible counters of any kind.
13. **No emotional grading.** No judgment on what goes in which zone. No corrective language.
14. **No coaching feedback within the screen.** No "Good job putting that in Can Control!" or similar.
15. **No streak language.** No "3-day Bullseye streak!" or similar.
16. **No celebration animations.** No confetti, no fireworks, no "Great job!" on save.
17. **Timestamps are behavioral data.** The time a moment was created matters to the coaching pipeline. Preserve and display.
18. **Day boundary = hard-out time.** Not midnight. Moments before hard-out belong to the previous day.
19. **Moments from standalone count in Evening Review.** Shared data model. No duplication.
20. **Previous days are read-only.** 2-day lookback, collapsed by default, no editing.
21. **Source tracking.** Record whether each moment was created in standalone or Evening Review context.
22. **Zone order is fixed.** Can Control → Can Influence → Can't Control. Always. Both in the input area and on moment cards.

---

## 19. Data Flow Summary

### Upstream (What Bullseye Receives)
- Existing moments for the current day (from standalone or Evening Review)
- Existing moments for the 2 previous days
- Program configuration (hard-out time, for day boundary)

### Downstream (What Bullseye Produces)
- Timestamped, zone-classified moments with optional tags
- Source context (standalone vs. Evening Review)
- Moment creation/update timestamps
- Feeds: AI coaching pipeline, Weekly Recap aggregation, Evening Review gating

### Evening Review Data Contract

The Evening Review wizard checks Bullseye data to determine gating:

```
Gate condition:
  moments.filter(date == today).some(m => m.can_control is non-empty)
  AND moments.filter(date == today).some(m => m.can_influence is non-empty)
  AND moments.filter(date == today).some(m => m.cannot_control is non-empty)
```

If all three conditions are true, Continue CTA is enabled.

### AI Pipeline Data Value

| Data Point | Coaching Insight |
|------------|-----------------|
| Zone distribution over time | Energy leak detection — athlete consistently overloading "Can't Control" |
| Tag patterns | Context-specific struggles (e.g., all "Can't Control" entries tagged "Competition") |
| Timestamps | Real-time processor vs. end-of-day batcher — different coaching approaches |
| Source (standalone vs. ER) | Proactive self-regulation (standalone) vs. prompted reflection (ER) |
| "What happened?" text | Situation context for personalized coaching language |
| Zone text | Classification accuracy — coaching opportunity when items are misclassified |

---

## 20. Relationship to Other Screens

| Screen | Relationship |
|--------|-------------|
| **Home — Daily Hub** | Bottom nav launches Bullseye standalone. No Bullseye preview on Home. |
| **Morning Tune-Up** | No direct relationship. |
| **Evening Review** | Bullseye renders as Step 2. Wizard provides gating, prompts, and Continue CTA. |
| **Journal (standalone)** | Sister tool in bottom nav. Shares patterns (auto-save, entry model, standalone/ER integration). Different entry structure (domain-based vs. moment-based). |
| **Weekly Recap** | Downstream consumer. Uses Bullseye data for coaching analysis and zone pattern summaries. |
| **Messages / Inbox** | No direct relationship. Coaching insights derived from Bullseye data may surface in messages. |

---

## 21. What This Document Does NOT Cover

- **Full history access** beyond 2-day lookback — TBD for a future phase
- **Search or filtering** of moments — not in scope
- **Export of Bullseye data** — may be addressed in Settings screen design
- **Coach/admin view** of Bullseye data — backend concern, not athlete-facing
- **Bullseye visual/target graphic** — may be explored in future iterations as a visualization of zone distribution, but the v1 UI uses text-based zone headers
- **Pixel-perfect visual design** — this document defines structure and behavior, not exact colors/fonts/spacing
- **Tag set expansion** — v1 set is locked. Future versions may add tags.
