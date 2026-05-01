# Evening Review: Design Document

**Screen**: Evening Review
**Phase**: 1, Screen 3
**Version**: 1.0
**Date**: 2026-03-11
**Status**: Design Complete — Ready for Development

---

## 1. Purpose & Context

The Evening Review is the most behavior-shaping screen in the app. It walks the athlete through honest self-assessment, focus re-centering, and journaling before clean daily closure.

**By the time the athlete exits, they should feel:**

> "I looked at today clearly. I'm complete. Tomorrow resets."

This is not insight for insight's sake. The goal is:
- Honest self-assessment (Win The Day)
- Emotional regulation and re-centering (Bullseye)
- Reflective expression (Journal)
- Clean psychological closure (Completion)

The Evening Review is a **guided wizard flow** — a sequential progression through four steps. Each step renders the **full standalone version** of its respective tool (Bullseye, Journal). The athlete uses the same screens they'd use independently throughout the day; the wizard simply sequences them and handles transitions.

### What This Screen Is

- A coach walking the athlete through end-of-day processing
- A linear, forward-only wizard with no branching exits
- A data capture pipeline — all five WTD scores, Bullseye entries, and journal text feed into the AI coaching system
- Progressive reveal — one step at a time, not all sections visible at once

### What This Screen Is NOT

- A summary dashboard
- A gamified scoring screen
- A motivational reward system
- A simplified or "lite" version of the standalone tools

---

## 2. Entry & Exit Points

### Entry Points

| Source | Trigger | Notes |
|--------|---------|-------|
| Home — Primary CTA | Athlete taps **REFLECT** on the Evening Review card | Primary entry path |
| Bottom Nav — Dynamic Action | Athlete taps moon icon during evening state | Same destination |

Both entry points lead to the same wizard state. If the athlete has a partially completed session (answered some WTD questions, logged Bullseye entries), they resume at the step where they left off (see Section 9.2).

### Exit Points

| Trigger | Destination | Behavior |
|---------|-------------|----------|
| Wizard completion | Home (auto-return after ~2 seconds) | Completion state shown briefly, then auto-navigate |
| Back arrow (top bar) | Home | Partial data preserved. No warning dialog. |
| Bottom nav tap | Respective destination | Partial data preserved for return. |
| App backgrounded | Stays on current wizard step | On foreground return, state preserved |
| Hard-out lockout | Wizard locked | Partial data preserved but review cannot be completed or modified |

### Post-Completion Re-Entry

After completion, if the athlete taps the Dynamic Action (moon icon) or the completed card on Home:

- **Destination**: Read-only review of all Evening Review responses
- **Content**: WTD answers (with checkmarks), Bullseye entries (if any added during review), Journal text, closing copy
- **Navigation**: Back button returns to Home
- **Score**: NOT displayed in read-only review (consistent with no-score philosophy)

---

## 3. Wizard Architecture

### 3.1 Step Sequence

```
Step 1: Win The Day Review (5 Yes/No questions)
    │ Auto-advance when all 5 answered
    ▼
Step 2: Bullseye Reflection (full standalone screen)
    │ Manual "Continue" CTA
    ▼
Step 3: Journal (full standalone screen)
    │ Manual "Continue" CTA
    ▼
Step 4: Completion & Closure
    │ Auto-return to Home (~2 seconds)
    ▼
[Home — Completed Evening State]
```

### 3.2 Step Order Rationale

- **WTD first**: Non-negotiable anchor. Fast, binary, honest self-assessment. Sets the reflective frame.
- **Bullseye second**: After answering 5 honest questions, the athlete's mind is activated. Bullseye channels that energy into "what can I control?" before it spirals into rumination. This is emotional regulation in action.
- **Journal third**: If the athlete still has something to process after WTD + Bullseye, they write. Journaling is the deepest engagement — placed last as the natural landing pad for extended reflection.
- **Completion last**: Clean closure. No carryover.

This sequence creates a **decompression arc**: assess → re-center → express → close.

### 3.3 Progress Indicators

- **Four small dots** at the top of the wizard, below the top bar
- Current step dot is filled/highlighted; others are outline/muted
- No labels (no "Step 2 of 4" text)
- No step names on the dots
- Purpose: orientation without pressure

### 3.4 Navigation Rules

| Rule | Behavior |
|------|----------|
| **Forward-only** | No back button to return to previous steps. Once a step is completed (WTD answered, Bullseye continued, Journal continued), it is locked. |
| **Top bar back arrow** | Exits the entire wizard. Returns to Home. Partial data preserved. |
| **Bottom nav** | Fully functional. Navigating away preserves partial data. |
| **No "Skip" buttons** | Every step is required. No optional exits. |

### 3.5 Transition Between Steps

Each step transition includes a brief **contextual prompt** in the wizard layer (not inside the standalone screen). This prompt introduces the next step:

| Transition | Prompt |
|------------|--------|
| WTD → Bullseye (no entries today) | "Log your controllables from today." |
| WTD → Bullseye (has entries today) | "Here's what you've logged. Want to add anything?" |
| Bullseye → Journal (no entries today) | "What do you want to note about today?" |
| Bullseye → Journal (has entries today) | "Here's what you've written. Anything to add?" |

These prompts appear briefly as a header/introduction when the step loads. They are part of the wizard wrapper, not the standalone screen itself.

---

## 4. Step 1 — Win The Day Review

### 4.1 Purpose

Create a fast, honest snapshot of how the athlete led themselves today. This is the primary action of the Evening Review and the anchor of the daily scoring system.

### 4.2 Layout

- Five stacked Yes/No cards
- One question per card
- Full-width tap targets
- Questions presented in fixed order (see 4.3)

### 4.3 The Five Questions (Fixed Order)

| # | Question Text | Type | Notes |
|---|---------------|------|-------|
| 1 | Did I act with intention today? | Static | Same every day |
| 2 | Did I complete my Mindset Challenge today? | Dynamic context | Same wording every day; challenge text shown beneath (see 4.4) |
| 3 | Did I respond to adversity in a way that aligns with my goals? | Static | Same every day |
| 4 | Did I pursue progress over perfection? | Static | Same every day |
| 5 | Did I end the day with gratitude? | Static | Same every day |

**Question design rationale:**
- Q1 (Intention) opens with the broadest question — sets the reflective frame
- Q2 (Mindset Challenge) is most personal/specific — anchored to the morning's commitment
- Q3 (Adversity) is the hardest to answer honestly — placed mid-flow when engagement is high
- Q4 (Progress) is forward-looking and encouraging
- Q5 (Gratitude) closes with the softest question — natural wind-down

**The 4 static questions (1, 3, 4, 5) are the same every day.** Consistency is intentional — the athlete internalizes these four pillars over time through daily repetition. Only Q2's context varies (driven by the Mindset Challenge).

### 4.4 Question 2 — Mindset Challenge Context

**When Morning Tune-Up WAS completed:**
- Question text: "Did I complete my Mindset Challenge today?"
- Below the question, in smaller muted text: "Today's challenge: [actual challenge text from Morning Tune-Up]"
- Example: *"Today's challenge: Hold your composure during one stressful moment today — no reaction."*
- This surfaces the specific commitment without changing the question wording

**When Morning Tune-Up was NOT completed:**
- Question text: "Did I complete my Mindset Challenge today?" (same wording)
- No challenge text shown beneath (there is no challenge to display)
- The honest answer is No — the athlete did not accept or complete a challenge
- **All 5 questions are always present.** The question count never changes. This is critical for the AI coaching pipeline, which requires consistent 5-point daily scoring data.

### 4.5 Scoring

| Answer | Value |
|--------|-------|
| Yes | 1 point |
| No | 0 points |

- **Daily total**: 0–5 points
- **Weekly total**: 0–35 points (used in Weekly Recap and coaching analysis)
- Score interpretation categories exist for the coaching backend:
  - 4–5 = Win The Day
  - 2–3 = Partial Win
  - 0–1 = Missed The Mark
- **These interpretation labels are NEVER shown to the athlete.** They exist only for AI coaching logic and pattern detection.

### 4.6 Interaction

| Aspect | Specification |
|--------|---------------|
| **Tap targets** | Full-width cards. Minimum 48px height per card. |
| **Yes/No buttons** | Two clearly separated tap areas per card. High-clarity toggle. |
| **Selection feedback** | Immediate visual confirmation on tap. Selected option fills/highlights. |
| **Change answer** | Allowed. Athlete can toggle between Yes and No before advancing. |
| **Auto-save** | Each answer saved individually as tapped. If athlete exits mid-WTD, answered questions are preserved. |
| **Auto-advance** | Once all 5 cards are answered, the wizard automatically advances to Step 2 (Bullseye). No manual "Next" button needed. |

### 4.7 Hard Rules

- No skipping questions — all 5 must be answered
- No explanations, modals, or tooltips
- No rewording per day (static questions)
- No emotional language tied to answers ("Great job!" on Yes, or shame on No)
- No score display after answering (score is calculated silently)
- Answers are locked after auto-advance to Step 2 — no going back to change

---

## 5. Step 2 — Bullseye Reflection

### 5.1 Purpose

Help the athlete re-center focus by classifying their day's events into what they can control, influence, and cannot control. This builds the Bullseye Method as a daily habit and feeds pattern data into the coaching system.

### 5.2 Screen Rendering

The Evening Review renders the **full standalone Bullseye Reflection screen** — the same screen the athlete uses throughout the day for real-time moment logging. The wizard provides a contextual entry prompt (see 3.5) but the screen itself is identical to standalone usage.

**Implementation note:** The standalone Bullseye screen will be fully designed in Phase 3. The developer builds the wizard shell and transition layer now; the actual Bullseye UI plugs in when the Phase 3 design is complete. The data model and gating requirements defined here are authoritative.

### 5.3 Conditional Entry Behavior

| Condition | Wizard Prompt | Screen State |
|-----------|---------------|--------------|
| **No Bullseye entries today** | "Log your controllables from today." | Empty Bullseye screen. Athlete must create entries. |
| **Has Bullseye entries from earlier** | "Here's what you've logged. Want to add anything?" | Bullseye screen with existing entries visible. Athlete can add more or proceed. |

### 5.4 Three Zones (Required Categories)

The Bullseye Method has three classification zones:

| Zone | Label | Description |
|------|-------|-------------|
| Center Ring | **Can Control** | Attitude, effort, breathing, actions, choices under pressure |
| Middle Ring | **Can Influence** | Communication, leadership, team culture, outcomes indirectly |
| Outer Ring | **Can't Control** | Others' decisions, weather, the past, external opinions |

### 5.5 Gating Logic — Continue CTA

| Condition | Continue CTA State |
|-----------|--------------------|
| Athlete has zero Bullseye entries for the day (none from earlier, none just created) | **Disabled** — must create at least one entry in each category |
| Athlete has entries from earlier in the day (at least one per category) | **Enabled** — can proceed without adding more |
| Athlete just created entries (at least one per category) | **Enabled** |

**Minimum requirement:** At least one entry in each of the three zones (Can Control, Can Influence, Can't Control) must exist for the day — either from earlier standalone usage or created now within the Evening Review.

### 5.6 Hard Rules

- No skipping — Bullseye is mandatory
- No coaching feedback within this step
- No corrective language
- No required balance across zones (beyond minimum one per zone)
- Entries from earlier in the day count toward the requirement
- Auto-save: any entries created are saved immediately (protected against mid-wizard exit)

---

## 6. Step 3 — Journal

### 6.1 Purpose

Provide a space for reflective expression. Journaling is required — this data feeds directly into the AI coaching pipeline for pattern analysis and personalized coaching.

### 6.2 Screen Rendering

The Evening Review renders the **full standalone Journal screen** — the same screen the athlete uses independently throughout the day. The wizard provides a contextual entry prompt (see 3.5) but the screen itself is identical to standalone usage.

**Implementation note:** The standalone Journal screen will be fully designed in Phase 3. The developer builds the wizard shell and transition layer now; the actual Journal UI plugs in when the Phase 3 design is complete. The data model and gating requirements defined here are authoritative.

### 6.3 Conditional Entry Behavior

| Condition | Wizard Prompt | Screen State |
|-----------|---------------|--------------|
| **No journal entries today** | "What do you want to note about today?" | Empty Journal screen. Athlete must write something. |
| **Has journal entries from earlier** | "Here's what you've written. Anything to add?" | Journal screen with existing entries visible. Athlete can review and proceed, or add more. |

### 6.4 Gating Logic — Continue CTA

| Condition | Continue CTA State |
|-----------|--------------------|
| No journal entries for the day AND text box is empty | **Disabled** — must write something |
| No journal entries for the day AND text box has content (even a few words) | **Enabled** |
| Has journal entries from earlier in the day | **Enabled** — existing content satisfies the requirement |

**Minimum requirement:** At least some text must exist for the day — either from earlier standalone journaling or written now within the Evening Review. No minimum word count, but the fields cannot be blank. The expectation is at least a few words per entry, not a single character.

### 6.5 Hard Rules

- Journaling is required — not optional depth
- No minimum word count enforced by the system
- No emotional grading of content
- No auto-prompts mid-entry
- No character limit (but UI should handle long entries gracefully)
- Entries from earlier in the day count toward the requirement
- Auto-save: text entered is saved on exit (protected against mid-wizard exit)

---

## 7. Step 4 — Completion & Closure

### 7.1 Purpose

End the day cleanly. No motivation. No judgment. No carryover. The athlete should feel psychologically closed.

### 7.2 Layout

```
┌──────────────────────────────┐
│                               │
│      [Completion icon]        │
│   Subtle checkmark or calm    │
│   visual indicator            │
│                               │
│   "You looked at today        │
│    honestly. That's the       │
│    work. Rest up."            │
│                               │
│                               │
│   (auto-return in ~2 sec)     │
│                               │
├──────────────────────────────┤
│  BOTTOM NAVIGATION            │
└──────────────────────────────┘
```

### 7.3 Content

| Element | Specification |
|---------|---------------|
| **Visual** | Full-screen or overlay confirmation. Clean, minimal. Calm visual indicator (subtle checkmark, not celebratory). |
| **Closing copy** | "You looked at today honestly. That's the work. Rest up." |
| **Score display** | **None.** The WTD score is NOT shown to the athlete — not on this screen, not on Home, not anywhere athlete-facing. The score exists only in the backend for coaching analysis. |
| **Transition** | Auto-return to Home after ~2 seconds |
| **Animation** | Subtle fade or slide transition. No celebration animations. |

### 7.4 No Score Display — Rationale

The score isn't what matters for the athlete. What matters is answering the questions honestly. Displaying a score:
- Creates pressure to "win" (chase 5/5)
- Incentivizes dishonest Yes answers
- Contradicts "data capture without emotional charge"
- Undermines the philosophy that reflection itself is the value

The score exists for the AI coaching system to detect patterns, generate insights, and tailor weekly coaching. The athlete never sees a number.

### 7.5 Transition Behavior

| Aspect | Specification |
|--------|---------------|
| **Auto-return** | Navigate to Home after ~2 seconds |
| **Early exit** | Tapping back arrow or anywhere on screen navigates to Home immediately |
| **Bottom nav** | Remains visible and functional during completion state |
| **Screen reader** | Announces: "Evening Review complete. Returning to Home." |

### 7.6 Hard Rules

- No streak language
- No encouragement cliches
- No tomorrow planning
- No score display
- No celebration animations (confetti, fireworks, sounds)
- No "You're on a X-day streak!" or similar
- Auto-return must not exceed 3 seconds

---

## 8. Data Requirements

### 8.1 Data Read on Wizard Load

| Data Point | Source | Used For |
|------------|--------|----------|
| Morning Tune-Up completion status (today) | Activity log | Determines whether Q2 shows challenge context text |
| Mindset Challenge text (today) | Morning Tune-Up completion record | Displayed beneath WTD Q2 as reminder |
| Existing Bullseye entries (today) | Bullseye log | Determines Bullseye step entry prompt and Continue gating |
| Existing journal entries (today) | Journal log | Determines Journal step entry prompt and Continue gating |
| Evening Review partial completion state | Activity log / local state | Resumes at correct step on re-entry |
| WTD answers (if partially completed) | Activity log | Restores answered questions on re-entry |

### 8.2 Data Written Per Step

**Step 1 — Win The Day:**

| Data Point | Destination | Timing |
|------------|-------------|--------|
| Individual question answers (Yes/No × 5) | WTD daily record | Auto-saved as each question is answered |
| Daily WTD score (0–5) | Calculated field | Computed when all 5 answered |

**Step 2 — Bullseye Reflection:**

| Data Point | Destination | Timing |
|------------|-------------|--------|
| New Bullseye entries (if created) | Bullseye log | Auto-saved as created |
| Zone classifications | Bullseye log | Saved with each entry |

**Step 3 — Journal:**

| Data Point | Destination | Timing |
|------------|-------------|--------|
| Journal entry text by classification: School/Work, Sport, Homelife | Journal log (timestamped) | Auto-saved on exit / Continue tap |

**Step 4 — Completion:**

| Data Point | Destination | Timing |
|------------|-------------|--------|
| Evening Review completion timestamp | Activity log | On wizard completion |
| Completion category | Activity log | Derived: on-time / late / backfill |

### 8.3 Data Used Downstream

| Data Point | Consumer | Purpose |
|------------|----------|---------|
| WTD daily score (0–5) | Weekly Recap (Phase 2) | Weekly score aggregation (0–35) |
| WTD individual answers | AI Coaching System | Pattern detection (which pillars are weak) |
| WTD score history | AI Coaching System | Growth/Mixed/Reset week classification |
| Bullseye entries | AI Coaching System | Focus pattern analysis, energy leak detection |
| Journal entries | AI Coaching System | Sentiment analysis, personalized coaching |
| Completion timestamp | Home screen | Completed state display |
| Completion timestamp | Timing system | On-time / late / backfill categorization |

---

## 9. Edge Cases & Special States

### 9.1 Loading State

| Aspect | Behavior |
|--------|----------|
| **Immediate** | Top bar renders with back arrow, title ("Evening Review"), and progress dots |
| **Skeleton** | Placeholder blocks for WTD question cards |
| **Animation** | Subtle pulse/shimmer on skeleton elements (matches app-wide loading pattern) |
| **Content arrival** | Fade in real content, no jarring layout shift |
| **Failure** | Show retry message: "Couldn't load your review. Tap to retry." with RETRY button |

### 9.2 Mid-Wizard Exit & Re-Entry

**Behavior**: Partial data is preserved per step. On re-entry, resume at the step where the athlete left off.

| Scenario | Behavior |
|----------|----------|
| **Exits during WTD (e.g., 3 of 5 answered)** | 3 answered questions saved. On re-entry, WTD loads with those 3 pre-filled. Athlete answers remaining 2. |
| **Exits during Bullseye** | Any new entries saved. On re-entry, resumes at Bullseye step with entries visible. |
| **Exits during Journal** | Text auto-saved. On re-entry, resumes at Journal step with text restored. |
| **Exits via back arrow** | Navigates to Home. Data preserved. |
| **Exits via bottom nav** | Navigates to destination. Data preserved. |
| **App backgrounded** | State preserved in memory. On foreground return, exactly as left. |
| **App killed / force closed** | Depends on local persistence. WTD answers and Bullseye entries are already server-saved (auto-save). Journal text may be lost if not yet saved — implementation team determines local persistence strategy. |

**"Welcome back" nudge**: On re-entry after a mid-wizard exit, show a brief message at the top of the current step: "Pick up where you left off." — auto-dismisses after 2 seconds or on interaction. Same pattern as Morning Tune-Up.

### 9.3 Hard-Out Lockout

| Scenario | Behavior |
|----------|----------|
| **Hard-out reached, wizard not started** | Evening Review locked. Home transitions to next-day Morning state. No guilt messaging. |
| **Hard-out reached, wizard partially completed** | Wizard locked immediately. Partial data preserved (answered WTD questions, Bullseye entries, journal text). Cannot be completed or modified. |
| **Hard-out reached, wizard on completion screen** | Completion fires normally (data already saved). Auto-return to Home proceeds. |

**No "hurry up" warnings.** The app does not warn the athlete that hard-out is approaching. The lockout simply happens. This prevents anxiety-driven rushing through reflection.

### 9.4 Network Error During Step Transitions

| Scenario | Behavior |
|----------|----------|
| **WTD auto-save fails** | Retry silently in background. If persistent failure, show subtle inline message. Do not block advancement — the wizard continues, and answers are retried. |
| **Bullseye entry save fails** | Inline error below the entry: "Couldn't save. Check your connection." Entry preserved locally for retry. |
| **Journal save fails** | Inline error: "Couldn't save your entry. Check your connection and try again." Continue CTA retries save on tap. |
| **Completion save fails** | Show inline error: "Couldn't save. Check your connection and try again." Completion screen stays visible with a RETRY button (overrides auto-return). |

### 9.5 First-Time User (Day 1)

| Step | First-Time Behavior |
|------|---------------------|
| **WTD** | All 5 questions shown as usual. If Morning Tune-Up was not completed (likely on Day 1 if onboarding happens in evening), Q2 has no challenge context — honest answer is No. |
| **Bullseye** | No existing entries. Athlete must create at least one entry per zone. |
| **Journal** | No existing entries. Athlete must write something. |
| **Completion** | Same as always. |

No onboarding overlays or tutorials within the Evening Review wizard. Onboarding happens in the dedicated flow (Phase 5).

### 9.6 Timezone Changes

- State transitions follow device local time (same as Home screen)
- If timezone change causes re-entry into evening window after completion, completion status holds — no re-prompting
- Hard-out evaluation always uses current local time

### 9.7 Multiple Completions (Same Day)

Not possible. Once the wizard reaches Step 4 and saves completion, the Evening Review transitions to read-only mode. There is no "redo" or "undo completion" feature.

---

## 10. Read-Only Review Mode (Post-Completion)

### 10.1 Access Points

| Source | Trigger |
|--------|---------|
| Bottom Nav — Dynamic Action (moon icon) | Tap during evening state after completion |
| Home — Completed Card | Tap the completed Evening Review card (optional — may be non-tappable) |

### 10.2 Layout

A scrollable read-only view of all Evening Review responses:

```
┌──────────────────────────────┐
│  TOP BAR                      │
│  ← Back        Evening Review │
├──────────────────────────────┤
│                               │
│  WIN THE DAY                  │
│  Q1: Did I act with intention │
│       today?            [Yes] │
│  Q2: Did I complete my        │
│       Mindset Challenge  [No] │
│  Q3: ...                [Yes] │
│  Q4: ...                [Yes] │
│  Q5: ...                [Yes] │
│                               │
├──────────────────────────────┤
│                               │
│  BULLSEYE REFLECTION          │
│  [Read-only Bullseye entries] │
│                               │
├──────────────────────────────┤
│                               │
│  JOURNAL                      │
│  [Read-only journal text]     │
│                               │
├──────────────────────────────┤
│                               │
│  Completed at 8:42 PM        │
│                               │
├──────────────────────────────┤
│  BOTTOM NAVIGATION            │
└──────────────────────────────┘
```

### 10.3 Visual Treatment

- Slightly muted overall tone (reduced contrast)
- WTD answers shown as Yes/No labels (not interactive toggles)
- Bullseye entries displayed read-only
- Journal text displayed read-only
- No score displayed anywhere
- Completion timestamp shown at bottom in muted text
- No active CTAs — entirely passive

---

## 11. Timing Categories

### 11.1 Evening Review Windows

| Category | Window (default hard-out 6:00 AM) |
|----------|-----------------------------------|
| **On-time** | Before 10:00 PM |
| **Late** | 10:00 PM to 4:00 AM (hard-out minus 2 hours) |
| **Backfill** | 4:00 AM to 6:00 AM (fixed 2-hour window before hard-out) |
| **Missed** | After 6:00 AM (hard-out) — locked permanently |

### 11.2 Availability

| Parameter | Value |
|-----------|-------|
| **Available from** | Evening release time (default 7:00 PM, configurable per program up to 9:00 PM) |
| **Available until** | Hard-out time next day (default 6:00 AM, configurable per program up to 10:00 AM) |
| **Hard-out behavior** | Locks immediately. Partial data preserved. Cannot be completed or modified. |

---

## 12. Connection to Other Screens

### 12.1 Home — Daily Hub (Upstream & Downstream)

| Aspect | Detail |
|--------|--------|
| **Entry** | Home Primary CTA (REFLECT) or Dynamic Action (moon icon) launches Evening Review |
| **Return** | Completion auto-returns to Home, which shows completed evening card |
| **Home completed card** | "You showed up for yourself today." — no score, muted styling, checkmark |
| **Timing** | Home determines evening state activation (evening release time) |

### 12.2 Morning Tune-Up (Upstream)

| Aspect | Detail |
|--------|--------|
| **Data received** | Mindset Challenge text from today's completed Tune-Up |
| **WTD Q2 integration** | Challenge text shown as context beneath Q2 |
| **If Tune-Up not completed** | Q2 still appears, no context text shown, honest answer is No |

### 12.3 Weekly Recap (Downstream)

| Aspect | Detail |
|--------|--------|
| **Data passed** | Daily WTD score (0–5) feeds into weekly aggregation (0–35) |
| **Sunday trigger** | Completing Sunday's Evening Review activates Weekly Recap state on Home |

### 12.4 Bullseye Reflection — Standalone (Shared)

| Aspect | Detail |
|--------|--------|
| **Shared data** | Bullseye entries from standalone use during the day are visible in the Evening Review Bullseye step |
| **Shared screen** | Same UI — Evening Review renders the full standalone Bullseye screen |
| **Entries created** | Entries created within Evening Review are also visible in standalone mode |

### 12.5 Journal — Standalone (Shared)

| Aspect | Detail |
|--------|--------|
| **Shared data** | Journal entries from standalone use during the day satisfy the Evening Review Journal requirement |
| **Shared screen** | Same UI — Evening Review renders the full standalone Journal screen |
| **Entries created** | Entries created within Evening Review are also visible in standalone mode |

### 12.6 Bottom Nav — Dynamic Action

| State | Dynamic Action Behavior |
|-------|------------------------|
| Evening, Review not started | Navigates to Evening Review (Step 1: WTD) |
| Evening, Review in progress | Navigates to Evening Review (resumes at current step) |
| Evening, Review completed | Navigates to Evening Review (read-only review mode) |
| Sunday, after Evening Review | Icon changes to clipboard, navigates to Weekly Recap |

---

## 13. Copy Reference

### 13.1 Fixed UI Copy

| Location | Copy |
|----------|------|
| Top bar title | Evening Review |
| WTD section header | WIN THE DAY |
| WTD Q1 | Did I act with intention today? |
| WTD Q2 | Did I complete my Mindset Challenge today? |
| WTD Q2 context (if Tune-Up done) | Today's challenge: [challenge text] |
| WTD Q3 | Did I respond to adversity in a way that aligns with my goals? |
| WTD Q4 | Did I pursue progress over perfection? |
| WTD Q5 | Did I end the day with gratitude? |
| Bullseye transition (no entries) | Log your controllables from today. |
| Bullseye transition (has entries) | Here's what you've logged. Want to add anything? |
| Journal transition (no entries) | What do you want to note about today? |
| Journal transition (has entries) | Here's what you've written. Anything to add? |
| Completion closing copy | You looked at today honestly. That's the work. Rest up. |
| Welcome back nudge | Pick up where you left off. |
| Loading error | Couldn't load your review. Tap to retry. |
| Save error | Couldn't save. Check your connection and try again. |
| Read-only mode footer | Completed at [HH:MM AM/PM] |

### 13.2 Home Screen Copy (Completed Evening State)

| Element | Copy |
|---------|------|
| Card title | WIN THE DAY REVIEW checkmark |
| Closing statement | You showed up for yourself today. |

---

## 14. Hard Rules & Constraints

### 14.1 Design Philosophy Rules

| Rule | Enforcement |
|------|-------------|
| Forward-only wizard | No back buttons to previous steps. Answers locked after advancing. |
| All steps required | WTD (5 answers), Bullseye (1+ entry per zone), Journal (non-empty text). No skipping. |
| Reflection without rumination | Decompression arc (assess → re-center → express → close). No dwelling. |
| Data capture without emotional charge | No score display. No judgment language. Yes/No only. |
| Clean closure | One completion endpoint. Auto-return. No carryover. |
| Calm, coach-led pacing | No urgency timers. No countdown. No "time remaining." |
| Identity, not achievement | Closing copy reinforces who the athlete is, not what they scored. |

### 14.2 Prohibited Elements

- No score display to the athlete (not on completion, not on Home, not anywhere)
- No score interpretation labels shown to athlete ("Win", "Missed", etc.)
- No streak language or streak counters
- No celebration animations (confetti, fireworks, sounds)
- No motivational hype copy
- No urgency language ("Time is running out!")
- No comparison to other athletes
- No guilt messaging for missed reviews
- No "Skip" buttons on any step
- No back navigation between wizard steps
- No tomorrow planning language
- No encouragement cliches
- No color-coding of scores or answers

### 14.3 Accessibility Requirements

- All text meets WCAG AA contrast ratios
- All interactive elements have accessible labels
- Yes/No tap targets: minimum 48px height, large enough for confident tapping
- Progress dots have accessible role indicators (e.g., "Step 2 of 4, Bullseye Reflection")
- Screen reader announces step transitions
- Completion auto-return announced: "Evening Review complete. Returning to Home."

---

## 15. Open Items & Future Considerations

| Item | Status | Notes |
|------|--------|-------|
| Bullseye standalone screen design | Phase 3 | Evening Review renders full standalone Bullseye. UI spec comes from Phase 3 design. Developer builds wizard shell now, plugs in Bullseye screen later. |
| Journal standalone screen design | Phase 3 | Same as above — full standalone Journal rendered within wizard. UI spec from Phase 3. |
| Bullseye minimum input validation UX | Phase 3 | How does the UI communicate "at least one entry per zone" requirement? Error state? Zone highlighting? Decided during standalone design. |
| Journal minimum input validation UX | Phase 3 | How does the UI communicate "must write something"? Placeholder behavior? Decided during standalone design. |
| Read-only review — Home card tap behavior | TBD | Should tapping the completed card on Home navigate to read-only review? Or only the Dynamic Action icon? Decide during implementation. |
| Closing copy refinement | Future | "You looked at today honestly. That's the work. Rest up." is locked for v1. May evolve with coaching voice refinement. |
| Hard-out approaching notification | Decided: No | No warnings. Lockout simply happens. Prevents anxiety-driven rushing. |
| Step transition animation style | Implementation | Slide left, fade, or other. Developer chooses. Must be subtle and calm. |

---

## Appendix A: Wizard Flow Diagram

```
[Athlete on Home Screen — Evening State]
        │
        │ Taps REFLECT or moon Dynamic Action
        ▼
[Evening Review Wizard Loads]
        │
        │ Progress dots: ● ○ ○ ○
        ▼
┌─────────────────────────────────┐
│ STEP 1: WIN THE DAY              │
│                                  │
│  Q1: Intention?         [Y] [N] │
│  Q2: Mindset Challenge? [Y] [N] │
│      "Today's challenge: ..."    │
│  Q3: Adversity?         [Y] [N] │
│  Q4: Progress?          [Y] [N] │
│  Q5: Gratitude?         [Y] [N] │
│                                  │
│  (auto-advance when all 5 done)  │
└────────────┬────────────────────┘
             │
             │ Progress dots: ○ ● ○ ○
             ▼
┌─────────────────────────────────┐
│ STEP 2: BULLSEYE REFLECTION      │
│                                  │
│  Transition prompt:              │
│  "Log your controllables..."     │
│                                  │
│  [Full standalone Bullseye UI]   │
│                                  │
│  [CONTINUE] (gated: 1+ per zone)│
└────────────┬────────────────────┘
             │
             │ Progress dots: ○ ○ ● ○
             ▼
┌─────────────────────────────────┐
│ STEP 3: JOURNAL                  │
│                                  │
│  Transition prompt:              │
│  "What do you want to note..."   │
│                                  │
│  [Full standalone Journal UI]    │
│                                  │
│  [CONTINUE] (gated: non-empty)  │
└────────────┬────────────────────┘
             │
             │ Progress dots: ○ ○ ○ ●
             ▼
┌─────────────────────────────────┐
│ STEP 4: COMPLETION               │
│                                  │
│  "You looked at today honestly.  │
│   That's the work. Rest up."    │
│                                  │
│  (auto-return ~2 seconds)        │
└────────────┬────────────────────┘
             │
             ▼
[Home — Completed Evening State]
"You showed up for yourself today."
```

## Appendix B: Data Flow Summary

```
Morning Tune-Up (upstream)
  │
  │ mindset_challenge_text
  ▼
Evening Review Wizard
  │
  ├─ Step 1: WTD
  │   writes → 5 × Yes/No answers, daily score (0-5)
  │   reads  → mindset_challenge_text (for Q2 context)
  │
  ├─ Step 2: Bullseye
  │   writes → new Bullseye entries (zone + text)
  │   reads  → existing Bullseye entries (today)
  │
  ├─ Step 3: Journal
  │   writes → journal entry (timestamped)
  │   reads  → existing journal entries (today)
  │
  └─ Step 4: Completion
      writes → completion_timestamp, completion_category
  │
  ▼
Downstream consumers:
  → Home screen (completed state)
  → Weekly Recap (weekly WTD aggregation)
  → AI Coaching System (all data)
```

## Appendix C: WTD Scoring Quick Reference

```
Daily: 5 questions × Yes(1) / No(0) = 0-5 points
Weekly: 7 days × 0-5 = 0-35 points

Backend interpretation (NEVER shown to athlete):
  4-5 daily  = Win The Day
  2-3 daily  = Neutral / Partial Win
  0-1 daily  = Missed The Mark

  28-35 weekly = Growth Week
  14-27 weekly = Mixed Week
  0-13 weekly  = Reset Week

All 5 questions present every day (no reduction when Tune-Up skipped).
Score is NEVER displayed to the athlete.
```
