# Home — Daily Hub: Design Document

**Screen**: Home — Daily Hub
**Phase**: 1, Screen 1
**Version**: 1.0
**Date**: 2026-03-11
**Status**: Design Complete — Ready for Development

---

## 1. Purpose & Context

The Home screen is the athlete's central dashboard and the first screen they see every time they open the app. Its single job:

**Guide the athlete to the single correct action for this moment of the day.**

If the Home screen does more than this, it's wrong.

The athlete never chooses *what* to do — only *when* to do it. The system determines the action based on time of day and day of week. The screen has three time-based states (Morning, Evening, Sunday Recap) that share identical layout architecture — only the copy, CTA, and minor details change between them.

---

## 2. Screen Architecture — Layout Components

All three states share this vertical flow, top to bottom. No component is ever reordered across states.

```
┌─────────────────────────────┐
│  HEADER                     │
│  Logo (left) + Profile (right) │
├─────────────────────────────┤
│  GREETING                   │
│  "Good morning/evening, [Name]" │
│  Contextual subtext         │
├─────────────────────────────┤
│  PRIMARY ACTION CARD        │
│  Label + Title + Content    │
│  + Primary CTA Button       │
│  (Must be visible without   │
│   scrolling)                │
├─────────────────────────────┤
│  PROGRESS STRIP (DEFERRED)  │
│  Reserved space — V2        │
├─────────────────────────────┤
│  BULLSEYE STATUS CARD       │
│  Focus status + LOG CTA     │
├─────────────────────────────┤
│  COACHING FEEDBACK PREVIEW  │
│  Message excerpt + OPEN CTA │
├─────────────────────────────┤
│  BOTTOM NAVIGATION          │
│  Inbox · Action · Home ·    │
│  Bullseye · Journal         │
└─────────────────────────────┘
```

### Visual Hierarchy Rules

1. **Primary Action Card** visually outweighs all other elements — largest, highest contrast, dominant position
2. **No scrolling required** to reach the Primary CTA button — it must be fully visible on initial load
3. **Bullseye Status Card** and **Coaching Feedback Preview** are secondary — supportive, not competing
4. **Bottom Navigation** is persistent across all app screens

---

## 3. Component Specifications

### 3.1 Header

| Element | Behavior |
|---------|----------|
| **Logo** | Static VirtusFocus logo, top-left. Not tappable. |
| **Profile Icon** | Top-right. Taps → navigates to Athlete Profile screen. |

- No other header elements (no notifications badge, no search, no hamburger menu)
- Profile is accessed ONLY from this icon — it is not in the bottom nav

### 3.2 Greeting

| Element | Description |
|---------|-------------|
| **Primary line** | "Good morning, [Name]" or "Good evening, [Name]" — time-of-day appropriate |
| **Subtext** | Contextual copy that sets the tone for the current state (see state details below) |

- `[Name]` is the athlete's first name from their profile
- Greeting changes based on state clock time

### 3.3 Primary Action Card

The dominant UI element on screen. Contains:

| Element | Description |
|---------|-------------|
| **Label** | "TODAY'S ACTION" — consistent across all states |
| **Card Title** | Name of the activity (varies by state) |
| **Card Content** | State-specific content area (Focus Word, support copy, etc.) |
| **Primary CTA Button** | Single action button — the one thing the athlete should do |

**Constraints**:
- This card visually outweighs all other cards on screen
- CTA must be reachable without scrolling on standard mobile viewports (375px width, 667px+ height)
- Only ONE CTA per card — no secondary actions, no "skip" or "later" options

**Completed State** (applies to all states after the activity is done):
- Card shifts to a soft/muted visual treatment (reduced contrast, lighter background)
- Checkmark icon replaces the CTA button
- Copy changes to reflect completion (see state-specific details below)
- No active CTA — card becomes passive
- Card remains in its position — does not collapse or disappear

### 3.4 Progress Strip — DEFERRED

**Status**: Reserved layout position. Not included in v1 release. Pending partner input.

**When implemented (V2)**, this will be a horizontal row of 3 passive data points:
- Streaks (consecutive completion days)
- Weekly Score Tally (aggregated WTD)
- Wins (Quick Wins count)

**V1 behavior**: This space is simply absent — the Bullseye Status Card moves up to fill the gap. No placeholder, no skeleton UI. When Progress Strip is approved, it slots in between Primary Action Card and Bullseye Status Card without restructuring.

**Design constraint if/when built**: Informational only. No taps, no charts, no color-coded pressure, no streak language. Must not incentivize gaming or inauthentic responses.

### 3.5 Bullseye Status Card

| Element | Description |
|---------|-------------|
| **Label** | "YOUR BULLSEYE TODAY" |
| **Status Indicator** | Dot icon + text describing current focus alignment |
| **Support Line** | Brief context on what the status means |
| **CTA** | "LOG YOUR FOCUS" → navigates to Bullseye Reflection (standalone) |

**States**:
- **Has entries today**: Shows most recent Bullseye zone + alignment summary (e.g., "CENTER RING FOCUS — You've been aligned with attitude + effort")
- **No entries today**: Shows intro prompt — "No focus logged yet today" with "LOG YOUR FOCUS" CTA
- **First-time user (never used Bullseye)**: Shows onboarding prompt — "Track where your focus lands throughout the day" with "LOG YOUR FOCUS" CTA

The Bullseye Status Card appears in ALL states (Morning, Evening, Sunday). It is always interactive — the athlete can log focus at any time of day.

### 3.6 Coaching Feedback Preview

| Element | Description |
|---------|-------------|
| **Label** | "COACHING FEEDBACK" |
| **Preview Text** | First 1–2 lines of the most recent coaching message |
| **CTA** | "OPEN MESSAGE" → navigates to Messages/Inbox |

**Content sources** (all delivered through the messaging system):
- Daily coaching snippet (1–2 sentences about the previous day, arrives each morning)
- Weekly coaching message (generated after Weekly Recap submission)
- System notifications

**States**:
- **Has messages**: Shows preview of most recent unread message. If all read, shows most recent message.
- **No messages (first-time user)**: Shows welcome message from "Coach" — e.g., "Welcome to VirtusFocus. Your coaching journey starts today."

The Coaching Feedback Preview appears in ALL states. It always shows the most recent message regardless of whether the athlete is in morning, evening, or Sunday state.

### 3.7 Bottom Navigation

5-item persistent navigation bar:

| Position | Label | Icon | Destination |
|----------|-------|------|-------------|
| 1 | Inbox | Envelope | Messages/Inbox |
| 2 | Dynamic Action | Context-sensitive (see below) | Context-sensitive destination |
| 3 | Home | House | Home — Daily Hub (current screen) |
| 4 | Bullseye | Target | Bullseye Reflection (standalone) |
| 5 | Journal | Book/Pen | Journal (standalone) |

**Dynamic Action Icon — Context Rules**:

| Current Home State | Icon | Label | Destination |
|---|---|---|---|
| Morning (active or completed) | ☀️ Sun | Morning | Morning Tune-Up |
| Evening (active or completed) | 🌙 Moon | Evening | Evening Review |
| Sunday Recap (active or completed) | 📋 Clipboard | Recap | Weekly Recap |

- The Dynamic Action icon reflects the **current Home screen state**, not the completion status
- If the athlete has completed the Morning Tune-Up, the sun icon still shows until the evening state activates
- Home icon is highlighted/active when on this screen

---

## 4. State Definitions

### 4.1 STATE 1 — Morning

**Activates**: At hard-out time (default 6:00 AM local, configurable per program up to 10:00 AM)
**Deactivates**: At Evening Recap release time (default 7:00 PM local, configurable per program up to 9:00 PM)

#### Greeting
- **Primary**: "Good morning, [Name]"
- **Subtext**: "Win today by controlling what's yours."

#### Primary Action Card — Active (Tune-Up not yet completed)

| Element | Content |
|---------|---------|
| **Label** | TODAY'S ACTION |
| **Card Title** | MINDSET TUNE-UP |
| **Focus Word** | [Today's pre-generated Focus Word, displayed large/prominent — e.g., "STALWART"] |
| **Support Line** | [Today's pre-generated coaching phrase — e.g., "Stand Firm. Show Strength."] |
| **Primary CTA** | **START** |

The Focus Word is the visual hook — displayed prominently to grab attention and create curiosity. It is pre-generated by the coaching system and pulled from the database each morning. The athlete taps START to launch the Morning Tune-Up, where they engage with the full pre-generated content set (Focus Word, Mindset Statement, Focus Word Quote, Mindset Challenge, and Quick Wins). All 5 components are system-generated — the athlete reads and commits, they don't create any of the content. Quick Wins (item 5) are static and do not change day to day.

**Data required on load**:
- Athlete's first name (from profile)
- Today's Focus Word (from pre-generated Morning Tune-Up content set)
- Today's support line / coaching phrase (from same content set)
- Morning Tune-Up completion status for today

#### Primary Action Card — Completed

| Element | Content |
|---------|---------|
| **Visual treatment** | Muted/soft card styling, reduced contrast |
| **Checkmark** | Completion indicator icon |
| **Card Title** | MINDSET TUNE-UP ✓ |
| **Focus Word** | [Today's Focus Word — remains visible as the day's anchor] |
| **Support Line** | "Your focus is set for today." |
| **CTA** | None — card is passive |

The completed card serves as a passive reference point for the rest of the day. The Focus Word stays visible so the athlete can glance at it throughout the day as a reminder of their commitment.

#### Morning State Hard Rules
- ❌ No evening language or evening-related content
- ❌ No recap prompts or weekly language
- ❌ No progress graphs or data visualizations
- ❌ No motivational hype, celebration, or gamification
- ❌ No secondary action options (no "skip" or "do later")

#### Bottom Nav — Morning
- Dynamic Action: ☀️ Sun icon (highlighted)
- Home: Active state indicator

---

### 4.2 STATE 2 — Evening

**Activates**: At Evening Recap release time (default 7:00 PM local, configurable per program up to 9:00 PM)
**Deactivates**: At hard-out time next day (default 6:00 AM local) — at which point any incomplete Evening Review is locked

#### Greeting
- **Primary**: "Good evening, [Name]"
- **Subtext**: "Reflect on how you led yourself today."

#### Primary Action Card — Active (Evening Review not yet completed)

| Element | Content |
|---------|---------|
| **Label** | TODAY'S ACTION |
| **Card Title** | WIN THE DAY REVIEW |
| **Support Copy** | "Track your momentum. Reflect on your 5 commitments." |
| **Primary CTA** | **REFLECT** |

Note: The original source spec included "Score your 5 habits" as support copy. This has been updated to "Reflect on your 5 commitments" to avoid score-focused language that could incentivize gaming responses.

**Data required on load**:
- Athlete's first name (from profile)
- Evening Recap completion status for today

#### Primary Action Card — Completed

| Element | Content |
|---------|---------|
| **Visual treatment** | Muted/soft card styling, reduced contrast |
| **Checkmark** | Completion indicator icon |
| **Card Title** | WIN THE DAY REVIEW ✓ |
| **Closing Statement** | "You showed up for yourself today." |
| **CTA** | None — card is passive |

The closing statement echoes the coach-voice closing from the Evening Review completion step. It reinforces identity ("you showed up") without surfacing any scores or data. No WTD score is displayed — this prevents athletes from gaming responses to chase a number.

#### Evening State Hard Rules
- ❌ No Morning Tune-Up access or morning language
- ❌ No Weekly Recap access or weekly language
- ❌ Same visual hierarchy as Morning state
- ❌ No score display on completed card

#### Bottom Nav — Evening
- Dynamic Action: 🌙 Moon icon (highlighted)
- Home: Active state indicator

---

### 4.3 STATE 3 — Sunday Weekly Recap

**Activates**: After Sunday's Evening Review is completed (not time-based — completion-triggered)
**Deactivates**: At next hard-out time (Monday morning, default 6:00 AM local) — OR when Weekly Recap is submitted, whichever comes first

**Critical rule**: Sunday follows the same Morning → Evening flow as every other day. The Weekly Recap state ONLY activates after the Sunday Evening Review is done. There is no special Sunday morning state.

- Sunday 6:00 AM – 6:59 PM: Morning state (same as any other day)
- Sunday 7:00 PM – Evening Review completion: Evening state (same as any other day)
- Sunday after Evening Review completion: **Weekly Recap state** (this section)

#### Greeting
- **Primary**: "Good evening, [Name]"
- **Subtext**: "Reflect on how you led yourself this week."

#### Primary Action Card — Active (Weekly Recap not yet submitted)

| Element | Content |
|---------|---------|
| **Label** | TODAY'S ACTION |
| **Card Title** | WEEKLY MINDSET RECAP |
| **Support Copy** | "Unlock your weekly coaching. Log your motivation." |
| **Primary CTA** | **RECAP** |

**Data required on load**:
- Athlete's first name (from profile)
- Sunday Evening Review completion status (must be true to show this state)
- Weekly Recap submission status

#### Primary Action Card — Completed

| Element | Content |
|---------|---------|
| **Visual treatment** | Muted/soft card styling, reduced contrast |
| **Checkmark** | Completion indicator icon |
| **Card Title** | WEEKLY MINDSET RECAP ✓ |
| **Closing Statement** | "Your week is closed. Coaching is on its way." |
| **CTA** | None — card is passive |

#### Sunday Recap State Hard Rules
- ❌ No Morning Tune-Up CTA (must be completed earlier in the day)
- ❌ No Evening Review CTA (must be completed prior to Weekly Recap)
- ❌ No optional daily action buttons or competing CTAs

#### Bottom Nav — Sunday Recap
- Dynamic Action: 📋 Clipboard icon (highlighted)
- Home: Active state indicator

---

## 5. State Transition Logic

### 5.1 Timing Model

State transitions are governed by the activity release/deadline system, not arbitrary clock times.

#### Key Time Parameters

| Parameter | Default | Configurable? | Notes |
|-----------|---------|---------------|-------|
| **Hard-out time** | 6:00 AM local | Yes — per program, up to 10:00 AM | Locks previous day's Evening Review. Also serves as Morning Tune-Up release time. |
| **Evening Recap release** | 7:00 PM local | Yes — per program, up to 9:00 PM | Triggers transition from Morning state to Evening state. |
| **On-time cutoff (Evening)** | 10:00 PM local | No — fixed | Evening Reviews completed before this are "on-time." |
| **Backfill window** | 2 hours before hard-out | No — fixed constant | Always = hard-out minus 2 hours. |

#### Morning Tune-Up Timing Categories

| Category | Window |
|----------|--------|
| **On-time** | Completed before 12:00 PM (noon) local |
| **Late** | Completed at or after 12:00 PM local |
| **Not completed** | Still available until evening release time; then hard-out on evening release |

No backfill category for Morning Tune-Up — it's either done or not.

#### Evening Review Timing Categories

| Category | Window (default hard-out 6:00 AM) |
|----------|-----------------------------------|
| **On-time** | Before 10:00 PM |
| **Late** | 10:00 PM to 4:00 AM |
| **Backfill** | 4:00 AM to 6:00 AM (hard-out minus 2 hours to hard-out) |
| **Missed** | After 6:00 AM (hard-out) — locked |

**Hard-out lockout behavior**: At hard-out, the app locks the Evening Review. Any component data entered before lockout is preserved (partial saves are kept). The athlete cannot complete or modify the review after lockout.

#### Scaling Examples (Different Hard-Out Times)

| Hard-Out | Late Window | Backfill Window |
|----------|-------------|-----------------|
| 6:00 AM (default) | 10 PM – 4 AM | 4 AM – 6 AM |
| 7:00 AM | 10 PM – 5 AM | 5 AM – 7 AM |
| 5:00 AM | 10 PM – 3 AM | 3 AM – 5 AM |

### 5.2 State Transition Flow

```
[Hard-out time reached (default 6:00 AM)]
        │
        ▼
┌─────────────────────┐
│  MORNING STATE       │
│  Morning Tune-Up     │
│  available            │
└────────┬────────────┘
         │
         │ Evening release time reached (default 7:00 PM)
         ▼
┌─────────────────────┐
│  EVENING STATE       │
│  Evening Review      │
│  available            │
└────────┬────────────┘
         │
         ├── Is it Sunday AND Evening Review just completed?
         │
    YES  ▼                    NO ▼
┌─────────────────────┐   ┌──────────────────────┐
│  SUNDAY RECAP STATE  │   │  Stay in Evening     │
│  Weekly Recap        │   │  (completed state)   │
│  available            │   │  until next hard-out │
└────────┬────────────┘   └──────────────────────┘
         │
         │ Hard-out time reached (Monday AM)
         ▼
┌─────────────────────┐
│  MORNING STATE       │
│  (new week begins)   │
└─────────────────────┘
```

### 5.3 What Happens Between Completion and Next State

| Scenario | Home Screen Shows |
|----------|-------------------|
| Morning Tune-Up completed at 8 AM, app reopened at 2 PM | Morning state with completed card (Focus Word visible, no CTA). Bullseye + Coaching remain interactive. Holds until evening release. |
| Evening Review completed at 8 PM (Mon–Sat) | Evening state with completed card ("You showed up for yourself today"). Holds until next hard-out. |
| Evening Review completed at 8 PM (Sunday) | Transitions immediately to Sunday Recap state. Weekly Recap card shown as active. |
| Weekly Recap submitted Sunday night | Sunday Recap state with completed card ("Your week is closed. Coaching is on its way."). Holds until Monday hard-out. |
| All activities completed for the day | Current state's completed card shown. No "all done" special screen. App is calm — athlete can still use Bullseye, Journal, or read coaching messages. |

---

## 6. Navigation Map

### 6.1 Entry Points (How Athletes Arrive at Home)

| Source | Trigger |
|--------|---------|
| App launch | Default landing screen after authentication |
| Bottom nav | Tap Home icon from any screen |
| Back navigation | Completing Morning Tune-Up → returns to Home |
| Back navigation | Completing Evening Review → returns to Home |
| Back navigation | Submitting Weekly Recap → returns to Home |
| Deep link / notification | Future: push notification taps could open Home |

### 6.2 Exit Points (Where Athletes Go from Home)

| Element | Destination |
|---------|-------------|
| Profile Icon (top-right) | Athlete Profile |
| Primary CTA — Morning | Morning Tune-Up (full flow) |
| Primary CTA — Evening | Evening Review (guided wizard: WTD → Journal → Bullseye → Completion) |
| Primary CTA — Sunday Recap | Weekly Recap (single-scroll flow) |
| "LOG YOUR FOCUS" (Bullseye card) | Bullseye Reflection (standalone) |
| "OPEN MESSAGE" (Coaching card) | Messages / Inbox |
| Bottom Nav — Inbox | Messages / Inbox |
| Bottom Nav — Dynamic Action | Morning Tune-Up / Evening Review / Weekly Recap (matches current state) |
| Bottom Nav — Bullseye | Bullseye Reflection (standalone) |
| Bottom Nav — Journal | Journal (standalone) |

---

## 7. Data Requirements

### 7.1 Data the Home Screen Reads

| Data Point | Source | Used For |
|------------|--------|----------|
| Athlete first name | User profile | Greeting personalization |
| Current local time | Device clock | State determination |
| Current day of week | Device clock | Sunday Recap logic |
| Hard-out time setting | Program config / user setting | State transition timing |
| Evening release time setting | Program config / user setting | State transition timing |
| Today's Focus Word | Pre-generated Tune-Up content (database) | Morning Primary Action Card |
| Today's support line | Pre-generated Tune-Up content (database) | Morning Primary Action Card |
| Morning Tune-Up completion status (today) | Activity log | Card active vs. completed state |
| Evening Review completion status (today) | Activity log | Card active vs. completed state; Sunday Recap trigger |
| Weekly Recap submission status (this week) | Activity log | Sunday Recap card state |
| Latest Bullseye entry (today) | Bullseye log | Bullseye Status Card content |
| Bullseye entry count (today) | Bullseye log | Bullseye Status Card — has entries vs. none |
| Most recent coaching message | Messages system | Coaching Feedback Preview content |
| Unread message count | Messages system | Coaching Feedback Preview — could indicate unread |

### 7.2 Data the Home Screen Does NOT Modify

The Home screen is **read-only**. It does not write, update, or delete any data. All data modifications happen on the destination screens (Morning Tune-Up, Evening Review, etc.). The Home screen simply reads current status and routes the athlete.

---

## 8. Edge Cases & Special States

### 8.1 Loading State

When the Home screen is loading data (Focus Word, completion status, coaching message):
- Show the Header + Greeting immediately (name can be cached locally)
- Show skeleton placeholders for the Primary Action Card, Bullseye Status Card, and Coaching Feedback Preview
- No spinner — use subtle pulse/shimmer animation on skeleton elements
- Transition to real content when data arrives (no jarring layout shift)

### 8.2 Error State

If data fails to load (network error, server down):
- Greeting still shows (name is cached)
- Primary Action Card shows a simple retry message: "Couldn't load your daily action. Tap to retry." with a RETRY button
- Bullseye and Coaching cards show their empty/fallback states
- Bottom nav remains fully functional

### 8.3 First-Time User (Day 1, No History)

| Component | First-Time Behavior |
|-----------|---------------------|
| Greeting | "Good morning, [Name]" — same as always |
| Primary Action Card | Morning Tune-Up with today's Focus Word — same as always (content is pre-generated) |
| Bullseye Status Card | "Track where your focus lands throughout the day" + "LOG YOUR FOCUS" CTA |
| Coaching Feedback Preview | Welcome message from Coach: "Welcome to VirtusFocus. Your coaching journey starts today." + "OPEN MESSAGE" CTA |

No onboarding overlays, tooltips, or tutorials on the Home screen itself. Onboarding happens in the dedicated onboarding flow (Phase 5) before the athlete ever reaches Home.

### 8.4 Evening Review Lockout (Hard-Out Reached)

If the athlete opens the app after hard-out and had not completed the Evening Review:
- Home screen is in **Morning state** (new day has begun)
- Previous day's Evening Review is locked — no access, no prompt, no guilt messaging
- Any partial data from the previous evening is preserved in the system but not surfaced on Home
- Morning Tune-Up card shows as active for the new day
- No "you missed yesterday's review" messaging — the system simply moves forward

### 8.5 Timezone Changes

If the athlete's device timezone changes (travel, DST):
- State transitions follow the device's current local time
- No special handling needed — the timing parameters (hard-out, evening release) are always evaluated against local time
- Edge case: if timezone shift causes a "replay" of a state window (e.g., traveling west), completion status prevents re-prompting

### 8.6 App Opened During Backfill Window (2 AM – 6 AM Default)

- If Evening Review was not completed: Evening state still shows with active Evening Review card. The athlete can still complete it (categorized as "backfill" in the system).
- If Evening Review was completed: Evening completed state shows until hard-out.
- Morning Tune-Up is NOT available during backfill — it only releases at hard-out.

---

## 9. Copy Reference — All States

### 9.1 Greetings

| State | Primary | Subtext |
|-------|---------|---------|
| Morning | Good morning, [Name] | Win today by controlling what's yours. |
| Evening | Good evening, [Name] | Reflect on how you led yourself today. |
| Sunday Recap | Good evening, [Name] | Reflect on how you led yourself this week. |

### 9.2 Primary Action Card — Active

| State | Label | Card Title | Content | CTA |
|-------|-------|------------|---------|-----|
| Morning | TODAY'S ACTION | MINDSET TUNE-UP | [Focus Word — large/prominent] + [Support Line] | **START** |
| Evening | TODAY'S ACTION | WIN THE DAY REVIEW | "Track your momentum. Reflect on your 5 commitments." | **REFLECT** |
| Sunday Recap | TODAY'S ACTION | WEEKLY MINDSET RECAP | "Unlock your weekly coaching. Log your motivation." | **RECAP** |

### 9.3 Primary Action Card — Completed

| State | Card Title | Content | CTA |
|-------|------------|---------|-----|
| Morning | MINDSET TUNE-UP ✓ | [Focus Word — still visible] + "Your focus is set for today." | None |
| Evening | WIN THE DAY REVIEW ✓ | "You showed up for yourself today." | None |
| Sunday Recap | WEEKLY MINDSET RECAP ✓ | "Your week is closed. Coaching is on its way." | None |

### 9.4 Bullseye Status Card

| Scenario | Label | Status Text | Support Line | CTA |
|----------|-------|-------------|--------------|-----|
| Has entries today | YOUR BULLSEYE TODAY | [Zone label — e.g., "CENTER RING FOCUS"] | [Alignment summary — e.g., "You've been aligned with attitude + effort"] | LOG YOUR FOCUS |
| No entries today | YOUR BULLSEYE TODAY | No focus logged yet today | — | LOG YOUR FOCUS |
| First-time user | YOUR BULLSEYE TODAY | Track where your focus lands throughout the day | — | LOG YOUR FOCUS |

### 9.5 Coaching Feedback Preview

| Scenario | Label | Preview Text | CTA |
|----------|-------|--------------|-----|
| Has messages | COACHING FEEDBACK | [First 1–2 lines of most recent message] | OPEN MESSAGE |
| First-time user | COACHING FEEDBACK | "Welcome to VirtusFocus. Your coaching journey starts today." | OPEN MESSAGE |

---

## 10. Hard Rules & Constraints

These rules are absolute and apply across all states.

### 10.1 Design Philosophy Rules

| Rule | Enforcement |
|------|-------------|
| One dominant action per state | Only one Primary CTA visible at any time. No secondary action buttons on the primary card. |
| Athlete never chooses what to do | System determines action by time/day. No action picker, no menu of options. |
| Calm, coach-led pacing | No gamification, no hype language, no urgency countdowns. |
| Reflection without rumination | Completed states are brief, positive, and don't resurface detailed activity data. |
| Identity priming + ownership | Copy uses "you" language focused on who the athlete is, not what they achieved. |
| Data capture without emotional charge | No scores on completed cards. No performance judgment language. |

### 10.2 Prohibited Elements

- ❌ No streak language or streak counters (V1)
- ❌ No celebration animations (confetti, fireworks, etc.)
- ❌ No score display on completed cards
- ❌ No progress graphs or data visualizations (V1)
- ❌ No motivational quotes or hype copy
- ❌ No urgency language ("don't miss your streak!", "time is running out!")
- ❌ No comparison to other athletes
- ❌ No guilt messaging for missed activities
- ❌ No "skip" or "do this later" buttons
- ❌ No branching choices or action menus at the Home level
- ❌ No evening language in morning state (and vice versa)
- ❌ No weekly language in daily states (and vice versa)

### 10.3 Accessibility & Performance

- All text must meet WCAG AA contrast ratios
- All interactive elements must have accessible labels
- Primary CTA must have a minimum tap target of 48x48px
- Screen must render meaningful content within 1 second (skeleton states acceptable)
- Focus Word text should be large enough to read at a glance (display/headline sizing)

---

## 11. Open Items & Future Considerations

| Item | Status | Notes |
|------|--------|-------|
| Progress Strip (Streaks, Score, Wins) | Deferred — V2 | Awaiting partner input. Reserved position in layout between Primary Action Card and Bullseye Status Card. Must not gamify or incentivize inauthentic responses. |
| Push notification deep links | Future | Notifications could open Home to specific state. No design needed now. |
| Coaching message unread indicator | TBD | Should the Coaching Feedback Preview show an unread badge/dot? Not specified. Decide during Messages/Inbox design (Phase 4). |
| Bullseye zone descriptions | TBD | Exact zone labels ("CENTER RING FOCUS", etc.) depend on Bullseye Reflection design (Phase 3). Using examples from source spec for now. |
| Closing statement copy (evening completed) | Finalize | "You showed up for yourself today." is the working copy. May be refined to match the actual Evening Review completion screen's closing statement (Phase 1, Screen 3). |
| CTA time estimates | Removed | Original spec showed "REFLECT · 1-2 MIN" and "RECAP · 1-2 MIN". Time estimates removed from CTAs to avoid setting expectations that could create pressure. Open to discussion. |

---

## Appendix A: State Transition Quick Reference

```
6:00 AM (hard-out) ──────────────────── 7:00 PM (evening release)
     │                                        │
     ▼                                        ▼
 ┌────────┐                              ┌─────────┐
 │MORNING │ ──── (holds all day) ──────▶ │ EVENING │
 │ STATE  │                              │  STATE  │
 └────────┘                              └────┬────┘
                                              │
                                    Sunday + Review done?
                                         YES │
                                              ▼
                                        ┌──────────┐
                                        │  SUNDAY  │
                                        │  RECAP   │
                                        └──────────┘

  All times are defaults. Hard-out and evening release are configurable.
  Sunday Recap is completion-triggered, not time-triggered.
```

## Appendix B: Navigation Quick Reference

```
                    ┌──────────────┐
                    │  PROFILE     │◄──── Profile Icon (top-right)
                    └──────────────┘
                           ▲
┌──────────────┐    ┌──────┴───────┐    ┌──────────────┐
│  MORNING     │◄───│              │───▶│  MESSAGES    │
│  TUNE-UP     │    │    HOME      │    │  / INBOX     │
└──────────────┘    │  DAILY HUB   │    └──────────────┘
                    │              │
┌──────────────┐    │  Primary CTA │    ┌──────────────┐
│  EVENING     │◄───│  Bullseye CTA│───▶│  BULLSEYE    │
│  REVIEW      │    │  Coaching CTA│    │  (standalone) │
└──────────────┘    │  Bottom Nav  │    └──────────────┘
                    │              │
┌──────────────┐    └──────┬───────┘    ┌──────────────┐
│  WEEKLY      │◄──────────┘     └─────▶│  JOURNAL     │
│  RECAP       │                        │  (standalone) │
└──────────────┘                        └──────────────┘
```
