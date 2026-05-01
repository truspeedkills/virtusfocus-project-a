# Weekly Recap — Design Document

**Screen**: Weekly Recap (Screen #16)
**Phase**: 3 — Weekly Cycle
**Session**: 7 (2026-03-12)
**Status**: Design Complete

---

## 1. Purpose & Context

The Weekly Recap is **reflection + transition, not therapy.**

It exists to help the athlete:
- Close the week
- Surface patterns lightly
- Set one clean direction forward

By the time the athlete exits, they should feel:
> "Last week is closed. I know what I'm carrying into next week."

The Weekly Recap is the final piece of the weekly cycle. It consumes data from every daily screen (WTD scores, Bullseye moments, Journal entries, Morning Tune-Up engagement) and produces structured input for the AI coaching pipeline. The resulting weekly coaching analysis is delivered to the athlete through Messages/Inbox — not on this screen.

### When It's Available

- **Sunday only.** Activates immediately after the athlete completes their Sunday Evening Review.
- **Availability window**: From Sunday Evening Review completion until Monday hard-out (default 6:00 AM, configurable per program).
- **After Monday hard-out**: Weekly Recap is locked. Treated as Missed. No backfill.
- The athlete cannot access Weekly Recap if Sunday Evening Review was not completed.

### Entry Points

- **Home — Sunday Recap state**: Primary Action Card with "RECAP" CTA. Card title: "WEEKLY MINDSET RECAP." Support copy: "Unlock your weekly coaching. Log your motivation."
- **Bottom nav — Dynamic Action**: Clipboard icon (📋) navigates to Weekly Recap. Active only in Sunday Recap state.

---

## 2. Screen Architecture

### Layout: Single Scroll with Soft Sections

All sections visible on a single scrollable screen. No wizard, no pagination, no branching. Visual section headers provide structure. Submit CTA at the bottom, disabled until all required fields are complete.

This matches the Morning Tune-Up pattern: single scroll, gated CTA, all content visible.

### Section Order (Top → Bottom)

1. **Weekly Summary** — Non-interactive completion context
2. **Season Context** — Single-select season phase
3. **Quick Ratings** — 3 × 1–10 tap selectors
4. **Motivation Inventory** — 5 text questions
5. **Forward Anchor** — Single-line required text input
6. **Submit & Closure** — Gated CTA + confirmation

### Screen Header

- **Title**: "Weekly Recap"
- **Top bar**: Back arrow (exits to Home, partial data auto-saved)
- **No progress indicators** (single scroll, not a wizard)

### First-Visit Subheader

"Close the week. Set your direction."

Shown once on the athlete's first-ever Weekly Recap. Never shown again after first submission. Consistent with Journal and Bullseye first-visit patterns.

---

## 3. Section 1 — Weekly Summary

### Purpose

Ground the reflection with factual, non-evaluative context about the athlete's week. This is a read-only preamble — no interaction required.

### Content

Completion counts for the week, presented as neutral facts:

- "You completed X of 7 Morning Tune-Ups this week."
- "You logged X of 7 Evening Reviews this week."
- "You created X Bullseye moments this week."
- "You wrote X Journal entries this week."

### Display Rules

- Plain text, muted styling. Not a card, not highlighted.
- Counts only — no content previews, no excerpts.
- No evaluative language. "You completed 2 of 7" is neutral. Never "Only 2 of 7" or "Great — 7 of 7!"
- No comparison to previous weeks.
- No WTD scores. No streak language.
- If a count is zero, display it neutrally: "You completed 0 of 7 Morning Tune-Ups this week."
- Data sourced from the current week (Monday through Sunday, bounded by hard-out times).

### Hard Rules

- ❌ No scores displayed (WTD or otherwise)
- ❌ No evaluative adjectives (great, poor, only, just)
- ❌ No comparison to previous weeks
- ❌ No streak language or counters
- ❌ No color-coding based on counts (no red/green)

---

## 4. Section 2 — Season Context

### Purpose

Identify the athlete's current competitive season phase. This data feeds the AI coaching pipeline so it can calibrate tone, challenge intensity, and focus areas. Asked every weekly submission because season phases change mid-program.

### Input

Single-select with 5 options:

1. Pre-Season
2. In-Season
3. Off-Season
4. Post-Season
5. Year-Round Training

### Interaction

- Tappable option chips or radio buttons. One selection required.
- **Defaults to last week's selection** (since season phase changes infrequently). Athlete can change it any week.
- If no previous submission exists (first-ever Weekly Recap), no default — athlete must select.

### Display

- Section header: "Season Phase"
- Prompt: "What phase of your competitive season are you in right now?"
- Five options displayed as tappable chips or a vertical radio list.

### Hard Rules

- ❌ No free-form input — fixed options only
- ❌ No "Other" option
- Required for submission

### Placement Rationale

Placed before Quick Ratings because season context frames everything that follows. A pre-season "6" on confidence means something different than an in-season "6." Identifying season phase first lets the athlete mentally calibrate before rating and reflecting.

---

## 5. Section 3 — Quick Ratings

### Purpose

Capture high-level self-awareness without cognitive load. These are gut-check signals, not precise measurements. The coaching pipeline uses them for trend detection across weeks.

### Inputs

Three 1–10 selectors:

| Rating | Prompt | Anchors |
|--------|--------|---------|
| Confidence | "How confident did you feel this week?" | Low → High |
| Habit Consistency | "How consistent were your habits this week?" | Low → High |

### Interaction Model

- **Discrete 10-point tap selector.** Ten tappable positions (circles, segments, or dots) arranged horizontally. Tap to select. Not a continuous drag slider — discrete positions prevent false precision and are easier to hit on mobile.
- **No default value.** Each selector starts empty. Athlete must tap to set a value. Prevents passive submission of meaningless middle values.
- **No numeric values displayed.** Visual anchors only: "Low" on the left, "High" on the right. The 1–10 integer is stored in the backend but never shown to the athlete.
- **Visual feedback**: Selected position fills/highlights. Positions to the left of the selection may also fill (like a progress bar) or only the selected position may highlight — implementation detail. Either way, subtle, not celebratory.
- **All three required** for submission.

### Section Header

"Quick Ratings"

### Hard Rules

- ❌ No numeric values shown to athlete
- ❌ No labels like "bad / good" or "poor / excellent"
- ❌ No color-coded success/failure (no red/green gradient)
- ❌ No comparison to previous weeks
- ❌ No commentary or interpretation text beneath ratings

---

## 6. Section 4 — Motivation Inventory

### Purpose

Surface context and patterns in the athlete's own words. These free-text responses are the qualitative core of the weekly coaching analysis. The AI coaching pipeline uses them to identify goal alignment, identity-language strength, emotional and environmental influences, and red flags.

### Questions (Fixed Order)

| # | Question | Required | Input Type | Notes |
|---|----------|----------|------------|-------|
| Q1 | What did you achieve this week? | Required | Multi-line text | Reflects on physical progress, mindset improvements, habit consistency, personal growth, academic wins, leadership behaviors. |
| Q2 | What was your favorite Mindset Challenge from this week's Tune-Ups? | Optional | Multi-line text | Reveals which Tune-Up content resonates. Helps AI detect identity and values. Can be left blank if athlete doesn't remember or didn't engage. |
| Q3 | What are your goals for the upcoming week? | Required | Multi-line text | Tracks forward momentum. Broad, multi-line. Distinct from Forward Anchor (which is one controllable focus). |
| Q4 | Is there anything else we should know about this week? | Optional | Multi-line text | Emotional and environmental context. Reveals obstacles, stressors, health issues, schedule changes. Accepts blank or "nothing." |
| Q5 | Any competitions coming up this week? | Optional | Multi-line text | Identifies competition weeks for tailored coaching. Accepts "none," "N/A," or blank. |

### Input Rules

- Short visible field height (3 lines). Expands as athlete types — no scroll within the field until substantial content.
- No minimum character count on any question.
- No maximum character count (practical limit handled by field height).
- Required questions (Q1, Q3): Submit CTA disabled until these contain at least 1 non-whitespace character.
- Optional questions (Q2, Q4, Q5): May be left blank. Blank is stored as empty string, not null.
- All responses stored verbatim for AI analysis.

### Section Header

"Weekly Reflection"

### Behavioral Rules

- Encourage clarity. Do not invite rumination.
- Questions are simple and direct — no multi-part questions, no "why" follow-ups.

### Hard Rules

- ❌ No repeated "why" prompts
- ❌ No multi-part questions
- ❌ No sentiment scoring or analysis shown to athlete
- ❌ No suggested answers or autocomplete
- ❌ No character counters

---

## 7. Section 5 — Forward Anchor

### Purpose

Create directional clarity going into the next week. This is the single most important coaching input on the screen. It's the psychological bridge between weeks — the one thing the athlete consciously carries forward.

### Prompt

**"One thing you can control next week."**

### Input Rules

- Single-line text input. Not multi-line. Forces brevity and clarity.
- Required for submission. Submit CTA disabled until this contains at least 1 non-whitespace character.
- No minimum or maximum character count.
- The "must be controllable" constraint is prompted by the wording, not validated by the UI. The AI coaching pipeline interprets whether the answer is actually controllable.

### Examples (Not Shown to Athlete)

- "Respond calmly to mistakes."
- "Complete my morning challenge every day."
- "Bring energy to practice."

### Visual Treatment

Visually elevated above the Motivation Inventory questions. Clear spacing and/or a subtle divider separates it from Section 4. The Forward Anchor should feel like the culmination of the reflection — the last thing the athlete writes before closing the week.

### Section Header

"Forward Anchor"

### Hard Rules

- ❌ No outcome goals prompted (wording steers toward controllable actions)
- ❌ No long explanations — single-line input enforces this
- ❌ No skip option — required for submission
- ❌ No examples shown in the UI (avoids anchoring bias)

---

## 8. Section 6 — Submit & Closure

### Submit CTA

- **Button text**: "Submit Weekly Recap"
- **Disabled state**: Grayed out until all required inputs are complete:
  - Season Context: one option selected
  - Quick Ratings: all 3 selectors set
  - Motivation Inventory Q1: non-empty
  - Motivation Inventory Q3: non-empty
  - Forward Anchor: non-empty
- **Enabled state**: Full-color, tappable

### On Submit

1. Save all recap data with `submitted` status
2. Signal AI coaching pipeline to generate weekly analysis
3. Transition to confirmation state

### Confirmation State

- **Copy**: "Week closed. Coaching is on its way."
- **Visual**: Subtle checkmark. Not celebratory — calm, grounded.
- **Behavior**: Auto-return to Home after ~2 seconds
- **Home card updates**: Primary Action Card transitions to completed state. Checkmark + "WEEKLY MINDSET RECAP ✓". Closing statement: "Your week is closed. Coaching is on its way."

### Hard Rules

- ❌ No instant AI feedback
- ❌ No score display (WTD or Quick Ratings)
- ❌ No motivational copy or celebration animations
- ❌ No preview of coaching output
- ❌ No streak language

---

## 9. Save Behavior

### Auto-Save Drafts + Explicit Submit

Weekly Recap uses a hybrid save model: fields auto-save as drafts, but the Submit CTA is required to finalize the week.

### Auto-Save (Draft State)

- **Trigger**: Debounced (2 seconds after typing stops) + on navigation/backgrounding/app kill.
- **Scope**: All field values saved. Season Context selection, Quick Ratings positions, text field content, Forward Anchor text.
- **Indicator**: Subtle "Saved" text, same pattern as Journal and Bullseye. Brief appearance, auto-fades.
- **Status**: Data is in `draft` state. Week is NOT closed. Coaching pipeline is NOT triggered.

### Submit (Submitted State)

- Triggered only by explicit Submit CTA tap.
- Changes status from `draft` to `submitted`.
- Triggers the AI coaching pipeline.
- Screen transitions to read-only.

### Why Both

Auto-save prevents data loss (directly addresses UX Gap #1 from CLAUDE.md). Explicit Submit provides the discrete "week closed" signal the coaching pipeline requires. Without a submission event, the pipeline doesn't know when to generate the weekly analysis.

---

## 10. Mid-Flow Exit & Re-Entry

### Exit Behavior

- **Back arrow**: Returns to Home immediately. All entered data auto-saved as draft.
- **Bottom nav**: Functional throughout. Tapping any nav item auto-saves and navigates. Draft preserved.
- **App backgrounding/kill**: Auto-save triggers on lifecycle events. Draft preserved.

### Re-Entry Behavior

- Athlete returns to the Weekly Recap with all previously entered data populated.
- **"Welcome back" nudge**: Brief message at top — "Pick up where you left off." Auto-dismisses after 2 seconds or on first interaction. Same pattern as Morning Tune-Up and Evening Review.
- Scroll position is NOT preserved (too fragile across app lifecycle events). Athlete re-enters at top of form with data populated.
- Submit CTA state recalculated based on populated data.

### Availability Window

- **Opens**: Immediately after Sunday Evening Review completion.
- **Closes**: Monday hard-out (default 6:00 AM, configurable per program).
- **After close**: Weekly Recap is locked. Status becomes `missed` if not submitted. No backfill.
- If athlete has a draft when the window closes, the draft data is preserved in the database (for coaching pipeline access if needed) but the athlete can no longer interact with it.

---

## 11. Read-Only Review

### Post-Submission Review

After submission, the athlete can review their Weekly Recap responses in read-only mode.

### Access Point

- **Dynamic Action** (clipboard icon 📋) in bottom nav. After submission, tapping the clipboard icon opens the completed Weekly Recap in read-only mode.
- **Access persists** until the next state transition: Monday hard-out → Morning Tune-Up activates → Dynamic Action becomes sun icon (☀️).

### Read-Only Display

- All sections rendered with submitted data
- Season Context: selected option shown, not interactive
- Quick Ratings: selected positions shown, not interactive
- Text fields: submitted text displayed, not editable
- Forward Anchor: submitted text displayed, not editable
- Submit CTA: not present (replaced by subtle "Submitted" indicator with timestamp)
- Muted styling consistent with Morning Tune-Up and Evening Review read-only modes

### Hard Rules

- ❌ No editing after submission
- ❌ No re-submission
- ❌ No score display in read-only view

---

## 12. Data Model

### Weekly Recap Record

```
WeeklyRecap {
  id:                 UUID
  athlete_id:         UUID (FK → Athlete)
  program_id:         UUID (FK → Program)
  week_start:         Date          // Monday of the recap week
  week_end:           Date          // Sunday of the recap week
  status:             Enum          // draft | submitted | missed
  created_at:         Timestamp     // First interaction
  submitted_at:       Timestamp?    // When Submit was tapped (null if draft/missed)
  last_saved_at:      Timestamp     // Most recent auto-save or submission

  // Section 2 — Season Context
  season_phase:       Enum          // pre_season | in_season | off_season | post_season | year_round

  // Section 3 — Quick Ratings (1–10 scale, stored as integers)
  rating_confidence:        Integer?  // 1–10, null if not yet set
  rating_habit_consistency: Integer?  // 1–10, null if not yet set
  rating_goal_progress:     Integer?  // 1–10, null if not yet set

  // Section 4 — Motivation Inventory
  q1_achievements:          String?   // Required for submission
  q2_favorite_challenge:    String?   // Optional
  q3_upcoming_goals:        String?   // Required for submission
  q4_anything_else:         String?   // Optional
  q5_competitions:          String?   // Optional

  // Section 5 — Forward Anchor
  forward_anchor:           String?   // Required for submission
}
```

### Field Constraints

| Field | Required for Submit | Validation |
|-------|-------------------|------------|
| season_phase | Yes | Must be one of 5 enum values |
| rating_confidence | Yes | Integer 1–10 |
| rating_habit_consistency | Yes | Integer 1–10 |
| rating_goal_progress | Yes | Integer 1–10 |
| q1_achievements | Yes | Non-whitespace content |
| q2_favorite_challenge | No | Any string or empty |
| q3_upcoming_goals | Yes | Non-whitespace content |
| q4_anything_else | No | Any string or empty |
| q5_competitions | No | Any string or empty |
| forward_anchor | Yes | Non-whitespace content |

### Status Transitions

```
(no record) → draft       // First interaction with any field
draft       → submitted   // Submit CTA tapped
draft       → missed      // Monday hard-out passes without submission
submitted   → (terminal)  // No further transitions
missed      → (terminal)  // No further transitions
```

---

## 13. Data Consumed (From Other Screens)

The Weekly Recap consumes data from the current week for the Weekly Summary section and for the AI coaching pipeline.

### Weekly Summary Display Data

| Data | Source | Usage |
|------|--------|-------|
| Morning Tune-Up completion count (0–7) | Morning Tune-Up records for the week | Weekly Summary: "You completed X of 7 Morning Tune-Ups this week." |
| Evening Review completion count (0–7) | Evening Review records for the week | Weekly Summary: "You logged X of 7 Evening Reviews this week." |
| Bullseye moment count | Bullseye moments for the week | Weekly Summary: "You created X Bullseye moments this week." |
| Journal entry count | Journal entries for the week | Weekly Summary: "You wrote X Journal entries this week." |

### AI Coaching Pipeline Data (Not Displayed)

| Data | Source | Pipeline Usage |
|------|--------|---------------|
| WTD daily scores (0–5 × 7 days) | Evening Review WTD responses | Weekly score (0–35), growth/mixed/reset classification |
| WTD individual answers | Evening Review WTD responses | Pattern detection across questions |
| Bullseye moment content | Bullseye entries (standalone + Evening Review) | Zone balance analysis, event pattern detection |
| Journal entry content | Journal entries (standalone + Evening Review) | Emotional tone, classification balance, behavioral patterns |
| Morning Tune-Up engagement | Tune-Up completion records | Consistency patterns, on-time vs. late |
| Mindset Challenge responses | WTD Q2 answers for the week | Challenge engagement rate |

---

## 14. Data Produced (For AI Coaching Pipeline)

The Weekly Recap submission triggers the AI coaching pipeline to generate a weekly analysis. The following data is produced and passed downstream:

### Structured Data

| Field | Type | Pipeline Usage |
|-------|------|---------------|
| season_phase | Enum | Calibrates coaching tone, challenge intensity, focus areas |
| rating_confidence | Integer (1–10) | Trend detection, weekly comparison (backend only) |
| rating_habit_consistency | Integer (1–10) | Habit formation tracking |
| rating_goal_progress | Integer (1–10) | Goal alignment analysis |
| q1_achievements | Text | Achievement pattern detection, identity-language analysis |
| q2_favorite_challenge | Text | Content resonance, motivational style detection |
| q3_upcoming_goals | Text | Goal specificity analysis, alignment with Forward Anchor |
| q4_anything_else | Text | Environmental context, stressor detection, red flags |
| q5_competitions | Text | Competition week identification, readiness assessment |
| forward_anchor | Text | Controllability analysis, focus consistency week-over-week |

### Pipeline Trigger

On submission, the system:
1. Saves the Weekly Recap record with `submitted` status
2. Aggregates the week's data (WTD scores, Bullseye, Journal, Tune-Up engagement, Quick Ratings, Motivation Inventory, Forward Anchor)
3. Sends the aggregated payload to the AI coaching pipeline
4. The pipeline generates a weekly coaching analysis
5. The analysis is delivered to the athlete as a message in Messages/Inbox
6. Timing of delivery is backend-determined — not instant, not on this screen

---

## 15. Edge Cases

### No Sunday Evening Review Completed

- Weekly Recap is not accessible. Home remains in Evening state.
- Dynamic Action shows moon icon (Evening Review), not clipboard.
- If Sunday Evening Review is never completed, Weekly Recap status becomes `missed` at Monday hard-out.
- The AI coaching pipeline still generates a weekly analysis using available data (WTD scores, Bullseye, Journal) but without the Motivation Inventory and Forward Anchor inputs. Coaching message notes the absence.

### Partial Completion at Monday Hard-Out

- Draft data is preserved in the database.
- Status transitions to `missed` (not `submitted` — the coaching pipeline needs a discrete submission signal).
- The AI coaching pipeline may still access draft data for context, but the weekly analysis is generated with a "partial" flag.
- Athlete cannot return to complete or edit the recap.

### Network Error on Submit

- Submit CTA shows error state: "Couldn't submit. Check your connection and try again."
- Draft data is preserved locally.
- Submit CTA remains enabled for retry.
- No partial submission — it's all or nothing.

### First-Ever Weekly Recap

- Season Context has no default (athlete must select).
- Weekly Summary shows whatever data exists (could be partial if athlete started mid-week).
- First-visit subheader displayed: "Close the week. Set your direction."

### Athlete Opens Weekly Recap but Doesn't Interact

- No draft record created until the athlete interacts with at least one field.
- If the athlete opens the screen and immediately leaves, no data is saved, no draft is created.
- Status remains as if the screen was never opened.

### Week Boundary Definition

- "The week" for Weekly Recap purposes runs from Monday hard-out to Sunday hard-out (7 days of daily data).
- This aligns with the hard-out time governing all daily boundaries.
- Example: With default 6:00 AM hard-out, the week is Monday 6:00 AM through Sunday 6:00 AM (for daily data), but the Weekly Recap itself is available Sunday evening through Monday 6:00 AM.

---

## 16. Accessibility

- All interactive elements: minimum 48×48px tap targets
- Quick Rating selectors: accessible labels ("Confidence rating, position X of 10")
- Season Context options: standard radio button or chip accessibility
- Text fields: associated labels matching the question text
- Submit CTA: disabled state communicated to screen readers ("Submit Weekly Recap, disabled. Complete all required fields to enable.")
- Section headers: proper heading hierarchy for screen reader navigation
- Confirmation state: screen reader announcement — "Weekly Recap submitted. Returning to Home."
- All text: WCAG AA contrast ratios

---

## 17. Hard Rules & Constraints

### Absolute Prohibitions

- ❌ No WTD score displayed — ever, anywhere on this screen (including read-only review)
- ❌ No Quick Ratings values displayed as numbers to the athlete
- ❌ No comparison to previous weeks' ratings or data
- ❌ No streak language or counters
- ❌ No celebration animations
- ❌ No motivational hype copy
- ❌ No urgency language
- ❌ No guilt messaging for low counts or sparse answers
- ❌ No instant AI coaching feedback on this screen
- ❌ No preview of coaching output
- ❌ No color-coded success/failure indicators
- ❌ No sentiment scoring shown to athlete
- ❌ No skip buttons on required fields

### Behavioral Constraints

- Pattern awareness without over-analysis
- Ownership without pressure
- Calm pacing appropriate for weekly reflection — Sunday wind-down energy
- Encourage clarity, do not invite rumination
- The app does not judge — neutral presentation of facts and open-ended prompts
- Coach-voice: brief, grounded, no hype

### Timing Constraints

- Available only after Sunday Evening Review completion
- Locked at Monday hard-out (default 6:00 AM)
- No backfill after hard-out
- Auto-return to Home after submission (~2 seconds)

---

## 18. Screen Flow Summary

```
[Athlete completes Sunday Evening Review]
        ↓
[Home transitions to Sunday Recap state]
        ↓
[Athlete taps RECAP or clipboard icon]
        ↓
┌─────────────────────────────────┐
│  Weekly Recap (Single Scroll)   │
│                                 │
│  Weekly Summary (read-only)     │
│  ──────────────────────────     │
│  Season Context (single-select) │
│  ──────────────────────────     │
│  Quick Ratings (3 × 1–10)      │
│  ──────────────────────────     │
│  Motivation Inventory (5 Qs)   │
│  ──────────────────────────     │
│  Forward Anchor (1 line)       │
│  ──────────────────────────     │
│  [Submit Weekly Recap]          │
└─────────────────────────────────┘
        ↓
[Confirmation: "Week closed. Coaching is on its way."]
        ↓ (~2 sec)
[Auto-return to Home]
        ↓
[Home card: completed state — "Your week is closed. Coaching is on its way."]
```

No forks. No pagination. No side exits. One submission endpoint.
