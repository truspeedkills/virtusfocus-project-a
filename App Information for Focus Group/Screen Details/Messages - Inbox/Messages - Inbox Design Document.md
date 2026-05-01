# Messages / Inbox — Design Document

**App**: VirtusFocus — Athlete Mental Performance App
**Screen**: Messages / Inbox
**Phase**: 4, Screen 1
**Status**: Design Complete
**Date**: 2026-03-13
**Session**: 8

---

## 1. Purpose & Context

Messages / Inbox is the delivery endpoint for all coaching output in VirtusFocus. Every other screen in the app captures athlete data — Morning Tune-Up, Evening Review, Journal, Bullseye, Weekly Recap — and feeds it into the AI coaching pipeline. Messages / Inbox is where the athlete receives the coaching that data produces.

This screen completes the core data flow: **athlete input → pipeline processing → coaching output**.

Messages / Inbox is a **one-directional coaching feed**. The system and coaching pipeline send messages to the athlete. The athlete reads. There is no composing, replying, or user-to-user messaging. The athlete's role here is to receive value — not to produce data.

### Role in the App

- **Bottom nav position**: First item (Inbox · Dynamic Action · Home · Bullseye · Journal). Primary destination.
- **Home screen coupling**: The Coaching Feedback Preview card on Home shows a teaser of the most recent message with an "OPEN MESSAGE" CTA that navigates here.
- **Weekly Recap closure**: After submitting a Weekly Recap, the athlete sees "Week closed. Coaching is on its way." — Messages / Inbox is where that coaching arrives.
- **Daily rhythm**: Each morning, a micro coaching message appears here covering the previous day.

---

## 2. Message Types

Six distinct message types arrive in the feed. Content generation for all coaching messages is **pipeline-owned** — the app is a display layer only.

### 2a. Daily Micro Coaching

| Attribute | Detail |
|-----------|--------|
| **Source** | AI coaching pipeline, based on previous day's data (WTD scores, Bullseye, Journal, Tune-Up engagement) |
| **Frequency** | ~1 per day, arrives each morning. Not generated on Mondays (no previous-day Evening Review data from Sunday — Sunday's data feeds the weekly cycle instead). |
| **Content size** | 1–2 sentences |
| **Content ownership** | Pipeline-generated. App renders as-is. |
| **Sender attribution** | Named coach (from athlete's program assignment) |

### 2b. Weekly Coaching Message

| Attribute | Detail |
|-----------|--------|
| **Source** | AI coaching pipeline, triggered by Weekly Recap submission |
| **Frequency** | ~1 per week, arrives asynchronously after Weekly Recap submission (backend-timed, not instant) |
| **Content size** | ~400–500 words. Structured as: narrative body → YOUR ACTION section → NEXT WEEK FOCUS QUESTION |
| **Content ownership** | Pipeline-generated. App renders as-is, preserving internal section structure. |
| **Sender attribution** | Named coach, with sign-off in message body (e.g., "— Coach Arron") |

### 2c. Weekly Deep Dive

| Attribute | Detail |
|-----------|--------|
| **Source** | AI coaching pipeline, arrives bundled with Weekly Coaching Message |
| **Frequency** | ~1 per week, same delivery as Weekly Coaching Message |
| **Content size** | ~1,500+ words. Structured analysis with major sections: Weekly Overview, Strengths and Wins, Opportunities and Growth Areas, Mindset Summary, Coaching Focus Areas |
| **Content ownership** | Pipeline-generated. App renders as-is, preserving section headers and structure. |
| **Sender attribution** | Named coach |
| **Delivery note** | Bundled with Weekly Coaching Message. The coaching message is the "cover letter"; the deep dive is the companion analytical document. |

### 2d. Milestone Acknowledgment

| Attribute | Detail |
|-----------|--------|
| **Source** | System-triggered based on program milestones |
| **Frequency** | Sparse, event-driven (e.g., first full week, 30-day consistency) |
| **Content size** | 1–2 sentences |
| **Tone** | Coach voice — grounded, identity-affirming, no hype. (e.g., "You've completed a full week. The data is building. Coaching gets sharper from here.") Not celebration, not gamification. |
| **Sender attribution** | Named coach |

### 2e. System Notification

| Attribute | Detail |
|-----------|--------|
| **Source** | Backend system events |
| **Frequency** | As needed, rare |
| **Content size** | Short |
| **Examples** | Program configuration changes (hard-out time updated), account-related notices. Not feature tips, not marketing. |
| **Sender attribution** | "VirtusFocus" (not coach-attributed) |

### 2f. Welcome Message

| Attribute | Detail |
|-----------|--------|
| **Source** | System, on account creation |
| **Frequency** | Once per athlete |
| **Content** | "Welcome to VirtusFocus. Your coaching journey starts today." |
| **Sender attribution** | "Coach" (generic until program assignment establishes named coach) |

---

## 3. Screen Architecture

### Layout Model: Feed / Timeline

Messages / Inbox is a **scrollable coaching feed** — all messages display fully inline as you scroll. This is a coaching journal, not an email inbox. The athlete opens the feed and reads. No tapping into detail screens (except the deep dive), no inbox management, no triage.

The feed model was chosen because:
- Daily micro coaching (1–2 sentences) doesn't warrant a detail screen. A feed shows it naturally.
- Message volume is low (~1/day + ~1/week). A feed matches the actual content cadence.
- The interaction is frictionless: open and read. No extra navigation.
- Matches the app's coach-led, calm pacing philosophy.

### Feed Structure

Messages are **grouped by week** with subtle week dividers. Within each week, messages appear in **reverse chronological order** (newest at top).

```
[This Week — Feb 2–8]
  Daily micro coaching (Today)          ← inline
  Daily micro coaching (Yesterday)      ← inline
  Weekly Coaching Message               ← visually elevated card
  Deep Dive Preview Card                ← with "READ FULL ANALYSIS" CTA
  Daily micro coaching (Tuesday)        ← inline
  Daily micro coaching (Monday)         ← inline — not generated (no Monday dailies)
  ...

── week divider ──

[Week 2 — Jan 26 – Feb 1]
  Daily micro coaching (Sunday)
  ...
```

### Feed Depth

The feed shows the **current week plus 2 previous weeks** of messages. Older messages are not available in the feed.

- Daily micro coaching is contextual to that day — snippets from 6 weeks ago have little value in a scrollable feed.
- Weekly coaching messages and deep dives are archived in Profile for long-term access (designed in Phase 6).
- The 3-week window keeps the feed fast and focused.

### End of Feed

When the athlete scrolls past all available messages, a subtle end-of-feed indicator appears:

> "That's everything from the last 3 weeks."

No "load more." No infinite scroll. The 3-week window is the boundary.

---

## 4. Message Display

### 4a. Daily Micro Coaching — Inline

- Simple card with minimal chrome
- **Timestamp**: Relative or absolute date (e.g., "Today, 8:12 AM" or "Tuesday, Jan 14")
- **Coach attribution**: Subtle byline — coach name (e.g., "Coach Arron") beneath timestamp. Not a full signature line.
- **No title/subject line**. The message IS the content. A title on 1–2 sentences is overhead.
- **Body**: 1–2 sentences, rendered as plain text.

### 4b. Weekly Coaching Message — Inline, Visually Elevated

- **Visually distinct card** — differentiated from daily snippets via subtle left-border accent or slightly different background. Signals "this is your weekly coaching."
- **Week label**: "Week 1 — January 12–18, 2026"
- **Coach attribution**: Byline beneath week label.
- **Body**: Full content visible, no truncation. ~400–500 words.
- **Internal structure preserved**: Section headers within the card for YOUR ACTION and NEXT WEEK FOCUS QUESTION. These are meaningful divisions the athlete will reference.
- **Sign-off**: Coach signature in body (e.g., "— Coach Arron") as generated by pipeline.

### 4c. Weekly Deep Dive — Preview Card + Full-Screen Reader

**Preview Card (in feed)**:
- Visually distinct from both daily and weekly coaching — more structured/formal card treatment.
- **Title**: "Weekly Deep Dive — Week 1"
- **Teaser**: 1–2 sentence summary (pulled from the Weekly Overview section of the deep dive content).
- **CTA**: "READ FULL ANALYSIS" button.
- Appears directly below the Weekly Coaching Message in the feed (they are bundled).

**Full-Screen Reader (separate view)**:
- Clean long-form reading view, optimized for ~1,500+ words of structured content.
- **Section headers preserved**: Weekly Overview, Strengths and Wins, Opportunities and Growth Areas, Mindset Summary, Coaching Focus Areas, Baseline Alignment Note — as produced by pipeline.
- **Back arrow** in top bar returns to feed.
- **Scroll position preserved** if the athlete navigates away and returns within the same session.
- Purely read-only. No interaction controls.
- This is the only full-screen reader pattern in the app — reinforcing that the deep dive is special.

**Deep Dive Archive**:
- Previous weeks' deep dives are accessible from the athlete's Profile screen (designed in Phase 6).
- The feed only shows deep dive preview cards within the 3-week window.
- Archive provides long-term access without cluttering the feed.

### 4d. Milestone Acknowledgments — Inline

- Simpler card than coaching messages — subtle styling, small icon.
- **Coach attribution**: Named coach (milestones use coach voice).
- Short, 1–2 sentences.

### 4e. System Notifications — Inline

- Minimal card — no card border, just text with a subtle system icon.
- **"VirtusFocus" attribution** (not coach-attributed).
- Short, informational.

---

## 5. Read / Unread State

### 5a. Feed — "New" Label

- Unread messages display a subtle **"New" label** that draws attention without disrupting the feed.
- The label **disappears when the message enters the viewport for ~1 second**. This prevents drive-by scrolling from marking everything as read.
- **Deep dive exception**: The "New" label on a deep dive preview card persists until the athlete **opens the full-screen reader** — scrolling past the preview card in the feed does not mark the deep dive as read.

### 5b. Bottom Nav — Dot Indicator

- The Inbox icon in the bottom nav shows a **simple dot indicator** when unread messages exist.
- **Not a count**. A dot is calm; a count ("3 unread!") creates urgency and pressure.
- The dot **clears when all messages have been viewed** in the feed (viewport-based) and any deep dive preview cards have been opened.

### 5c. Home Screen — Coaching Feedback Preview Card

- Shows the most recent **unread** message preview.
- If all messages are read, shows the most recent message of any type.
- **Weekly bundle behavior**: When the weekly coaching message + deep dive arrive together, the Home preview card shows the **coaching message** preview (the personal letter), not the deep dive announcement.
- **"OPEN MESSAGE" CTA** navigates to the Messages feed, which **always opens at the top** (newest first). No deep-linking to a specific message.
- **Update timing**: If the athlete is on the Home screen when a new message is delivered, the Coaching Feedback Preview card updates **on next visit** (navigating away and back, or app foreground), not live. The dot appears on the Inbox icon in the bottom nav to signal new content. No disruptive mid-screen refresh.

---

## 6. Empty State & First-Time Experience

### 6a. First-Time User

When the athlete first visits Messages / Inbox after completing onboarding (before any daily cycle):

- **One welcome message is already in the feed**: "Welcome to VirtusFocus. Your coaching journey starts today." Attributed to "Coach."
- **Below the welcome message**, static helper text at the bottom of the feed (not a message): "Coaching messages arrive as you use the program. Complete your first full day to get started."
- This avoids an empty-feeling screen while setting clear expectations.

### 6b. Feed Boundary

When the athlete scrolls past all available messages within the 3-week window:

> "That's everything from the last 3 weeks."

No CTA. No "load more." The 3-week window is the boundary.

---

## 7. Entry Points

Three ways the athlete arrives at Messages / Inbox:

### 7a. Bottom Nav — Inbox Icon

- First item in the 5-item bottom nav (Inbox · Dynamic Action · Home · Bullseye · Journal).
- Envelope icon. Dot indicator when unread messages exist.
- Always available from any screen.
- Opens feed at the top (newest first).

### 7b. Home — Coaching Feedback Preview Card

- "OPEN MESSAGE" CTA on the Coaching Feedback Preview card navigates to Messages / Inbox.
- Opens feed at the top. No deep-linking to the previewed message (it's already at the top).

### 7c. Push Notification

- Tapping a push notification for a coaching message opens Messages / Inbox.
- Opens feed at the top.

---

## 8. Notification Integration

### 8a. Push Notifications

| Message Type | Push Notification | Copy Style |
|-------------|-------------------|------------|
| **Daily micro coaching** | Yes | "Your coaching for today is ready." |
| **Weekly bundle** | Yes (one notification for both coaching message + deep dive) | "Your weekly coaching is ready." |
| **Milestone acknowledgment** | No | Found in feed — pleasant surprise, not pushed |
| **System notification** | No (unless time-sensitive, e.g., hard-out time change) | — |

Push notification copy matches coach voice — calm, no urgency language. Not "You have a new message!" but "Your coaching for today is ready."

### 8b. In-App Badge

- Dot indicator on Inbox icon in bottom nav (see Section 5b).
- Clears when all messages viewed.

### 8c. Home Screen Update

- Coaching Feedback Preview card updates on next visit, not live (see Section 5c).

---

## 9. Interaction Model

**Messages / Inbox is purely read-only.** The athlete reads coaching content. There is no:

- Replying or composing
- Bookmarking or saving
- Reactions (thumbs up, emoji, etc.)
- Dismissing or archiving
- Deleting
- Marking as read/unread manually
- Sorting or filtering

Reasons:
- The app philosophy is coach-led, not athlete-driven. The athlete receives — they don't curate.
- Bookmarking implies some messages are more important. The coach decides what's important.
- Reactions add social media mechanics to a coaching relationship. Doesn't fit.
- Deep dive archive in Profile serves the "save for later" use case.
- No deletion — consistent with Journal, Bullseye (data is permanent).

**The only interactive element** is the "READ FULL ANALYSIS" CTA on the deep dive preview card, which is navigation (not message interaction).

---

## 10. Data Model

### 10a. Message Schema

```
Message {
  id:               UUID
  athleteId:        UUID          — recipient athlete
  type:             Enum          — DAILY_MICRO | WEEKLY_COACHING | WEEKLY_DEEP_DIVE | MILESTONE | SYSTEM | WELCOME
  coachName:        String | null — named coach for coaching/milestone messages, null for system
  senderLabel:      String        — display label ("Coach Arron" or "VirtusFocus")
  weekLabel:        String | null — "Week 1 — January 12–18, 2026" (weekly types only)
  weekNumber:       Integer | null — program week number (weekly types only)
  title:            String | null — used for deep dive preview card title, null for inline messages
  teaser:           String | null — 1–2 sentence preview for deep dive card, null for inline messages
  body:             String        — full message content (rendered as-is, pipeline-formatted)
  bundleId:         UUID | null   — links weekly coaching message and deep dive as a bundle
  readStatus:       Boolean       — false = unread, true = read
  deepDiveOpened:   Boolean       — for WEEKLY_DEEP_DIVE type: true when full reader has been opened
  createdAt:        Timestamp     — message generation time
  deliveredAt:      Timestamp     — message delivery time (may differ from creation)
}
```

### 10b. Key Relationships

- **Weekly bundle**: `WEEKLY_COACHING` and `WEEKLY_DEEP_DIVE` messages share the same `bundleId`. They are delivered together and displayed adjacently in the feed.
- **Coach identity**: `coachName` is sourced from the athlete's program assignment. If the athlete is reassigned, new messages use the new coach name. Historical messages retain original attribution.
- **Week numbering**: `weekNumber` is relative to the athlete's program start, not calendar weeks. Enables consistent labeling ("Week 1," "Week 12") regardless of start date.

### 10c. Read State Logic

- **Inline messages** (daily micro, weekly coaching, milestone, system, welcome): `readStatus` flips to `true` when the message enters the viewport for ~1 second.
- **Deep dive preview card**: `readStatus` flips to `true` when the card enters the viewport. `deepDiveOpened` flips to `true` when the full-screen reader is opened. The "New" label on the card is driven by `deepDiveOpened`, not `readStatus`.
- **Inbox dot indicator**: Visible when any message has `readStatus = false` OR any deep dive has `deepDiveOpened = false`.
- **Home Coaching Feedback Preview**: Queries for the most recent message where `readStatus = false` (excluding deep dives). If none, shows most recent message of any type.

---

## 11. Data Consumed (from Coaching Pipeline)

The AI coaching pipeline generates message content. The app receives finalized messages — it does not process raw athlete data. Content generation, voice, tone, and coaching logic are **pipeline-owned**. The app is a **display layer only**.

For reference, the pipeline consumes data from:

| Source Screen | Data Points |
|--------------|-------------|
| **Morning Tune-Up** | Completion status, on-time/late, Mindset Challenge engagement |
| **Evening Review — WTD** | 5 Yes/No answers, daily score (0–5), weekly score (0–35) — never shown to athlete |
| **Evening Review — Bullseye** | Moments: event descriptions, zone entries, tags, timestamps, source |
| **Evening Review — Journal** | Entries: classifications, content, timestamps, source |
| **Weekly Recap** | Season context, Quick Ratings (Confidence, Habit Consistency, Goal Progress), Motivation Inventory (5 questions), Forward Anchor |
| **Engagement patterns** | Timing (on-time vs. late vs. backfill), consistency, standalone vs. guided usage |

---

## 12. Coach Voice & Sender Identity

### Sender Attribution

- **Coaching messages** (daily micro, weekly coaching, weekly deep dive, milestones): Attributed to the athlete's **named coach** from their program assignment. Displayed as a subtle byline (e.g., "Coach Arron").
- **System notifications**: Attributed to **"VirtusFocus"**. No coach name.
- **Welcome message**: Attributed to **"Coach"** (generic, before program assignment establishes the named coach).

### Content Ownership

All coaching message content — voice, tone, structure, and copy — is **generated and owned by the AI coaching pipeline**. The Messages / Inbox screen renders content as-is. No content rules, tone enforcement, or formatting logic in the app layer.

The pipeline is responsible for:
- Coach voice consistency (grounded, calm, identity-affirming)
- Behavioral evidence references
- Controllable-focused framing
- Score suppression (WTD scores never appear in athlete-facing content)
- Section structure in weekly coaching messages and deep dives

---

## 13. Edge Cases

### 13a. No Messages Yet (First-Time User)

Welcome message is pre-populated. Helper text below: "Coaching messages arrive as you use the program. Complete your first full day to get started." See Section 6a.

### 13b. Offline / No Connectivity

- Previously loaded messages remain visible in the feed (cached).
- New messages delivered while offline appear when connectivity is restored and the feed refreshes.
- No explicit "You're offline" banner — the feed simply shows what's available. The dot indicator on the Inbox icon appears when new messages sync on reconnection.

### 13c. Rapid Message Arrival (Multiple Messages in Quick Succession)

- Each message is a separate item in the feed, displayed in chronological order.
- The Inbox dot indicator appears once for any batch of new messages — it doesn't flash or re-trigger per message.
- Home Coaching Feedback Preview card shows the most recent unread.
- Push notifications: If multiple messages arrive simultaneously, only the most recent triggers a push. No notification bombardment.

### 13d. Weekly Bundle — Partial Delivery

If the pipeline delivers the weekly coaching message but the deep dive is delayed (processing time):
- The weekly coaching message appears in the feed immediately.
- The deep dive preview card appears when the deep dive is delivered.
- The `bundleId` links them. The feed renders them adjacently regardless of delivery order — the coaching message always appears above the deep dive card within the same week group.

### 13e. Coach Reassignment

If an athlete is reassigned to a different coach mid-program:
- New messages use the new coach's name.
- Historical messages retain their original coach attribution. No retroactive renaming.

### 13f. Weekly Recap Not Submitted (Missed)

If the athlete misses the Weekly Recap submission window (Monday hard-out):
- No weekly coaching message or deep dive is generated for that week.
- The pipeline may generate a modified daily micro coaching message acknowledging the gap. Content is pipeline-determined.
- No empty "placeholder" appears in the feed for the missing week.

### 13g. App Killed / Backgrounded While Reading

- Read state based on viewport tracking is best-effort. If the app is killed mid-scroll, messages that were in the viewport may or may not have been marked as read depending on whether the 1-second threshold was met.
- On next app open, any messages not marked as read will still show "New" labels and contribute to the Inbox dot indicator. This is the correct behavior — better to show "New" again than to silently mark something as read that the athlete didn't actually see.

---

## 14. Accessibility

- **Screen reader**: All messages are semantic text content. Feed uses a list/article structure with proper heading hierarchy. Week dividers are labeled for screen readers.
- **Font scaling**: Message content respects system font size settings. Cards and the deep dive reader must accommodate larger text without layout breakage.
- **Color contrast**: "New" labels, dot indicators, and card accent borders meet WCAG AA contrast ratios.
- **Deep dive reader**: Back navigation is accessible via both the back arrow and system back gesture/button.
- **Focus management**: When navigating from Home ("OPEN MESSAGE" CTA) or push notification, focus moves to the feed's first message.
- **Motion**: No animations on message appearance. Messages are present when the feed loads — no fly-in or fade-in effects. Consistent with the app's calm, non-gamified design.

---

## 15. Hard Rules & Constraints

1. **No user-to-user messaging.** Messages / Inbox is one-directional: system/coaching → athlete. No composing, replying, or forwarding. Ever.
2. **No scores displayed.** WTD scores, Quick Ratings, or any quantified performance data must never appear in athlete-facing messages. Pipeline responsibility, but the app must never add score displays of its own.
3. **No deletion.** Athletes cannot delete messages. Consistent with Journal and Bullseye data permanence.
4. **No streak language.** No "5 days in a row!" No "You're on a streak!" Not in messages, not in milestone copy. Pipeline responsibility, but the app must never generate streak-based copy.
5. **No celebration animations.** No confetti, no badge reveals, no achievement pop-ups. Messages appear calmly in the feed.
6. **No notification bombardment.** Maximum one push notification per message delivery event. Milestones and system notifications are silent (in-app only).
7. **Feed depth: 3 weeks.** Current week + 2 previous weeks. No infinite scroll. Deep dive archive lives in Profile.
8. **Read-only.** No bookmarks, reactions, dismissals, or manual read/unread toggling.
9. **Content is pipeline-owned.** The app renders message content as delivered. No content transformation, tone enforcement, or formatting logic in the app layer.
10. **Named coach attribution.** Coaching messages are attributed to the athlete's assigned coach by name, not a generic label. System messages are attributed to "VirtusFocus."

---

## 16. Screen Summary

| Aspect | Detail |
|--------|--------|
| **Screen name** | Messages / Inbox |
| **Layout** | Scrollable feed / coaching journal |
| **Message types** | Daily micro, Weekly coaching, Weekly deep dive, Milestone, System, Welcome |
| **Feed depth** | Current week + 2 previous weeks |
| **Grouping** | By week with subtle dividers, reverse chronological within week |
| **Interaction** | Read-only (one CTA: "READ FULL ANALYSIS" on deep dive card) |
| **Unread indicators** | "New" label on messages (viewport-based), dot on Inbox nav icon |
| **Entry points** | Bottom nav Inbox icon, Home "OPEN MESSAGE" CTA, push notification |
| **Deep dive delivery** | Preview card in feed → full-screen reader |
| **Deep dive archive** | Profile screen (Phase 6) |
| **Push notifications** | Daily micro: yes. Weekly bundle: yes. Milestone/system: no. |
| **Sender** | Named coach (coaching), "VirtusFocus" (system) |
| **Content ownership** | AI coaching pipeline (app is display layer) |
| **Empty state** | Welcome message + helper text |
| **Deletion** | Not allowed |
| **Search** | Not available |
