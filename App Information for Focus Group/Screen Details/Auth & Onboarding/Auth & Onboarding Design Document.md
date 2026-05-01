# Auth & Onboarding — Design Document

**Phase**: 5 — Auth & Onboarding
**Session**: 9 (2026-03-13)
**Status**: COMPLETE
**Screens Covered**: Sign Up, Email Verification, Login, Password Recovery, Program Code, Initial Intake (7 sections), How To, First Day Experience

---

## 1. Overview

Auth & Onboarding is the complete entry experience — from account creation through the athlete's first arrival at Home. It serves two purposes: establish a secure account and collect the baseline data the AI coaching pipeline requires to generate personalized mental performance coaching.

**Core tension**: The pipeline requires a complete 29-question intake to function. Onboarding must collect all of it without the athlete abandoning mid-flow. The design resolves this by presenting the intake as 7 fast, focused sections (~5 minutes total) with auto-save at each section boundary, progress visualization, and coach-voice framing that makes each section feel purposeful rather than bureaucratic.

**Two environments**: VirtusFocus operates in two environments that share the same onboarding flow with one fork point:
- **Institutional** (launch priority): Team/program purchases the service. Athletes receive a program code. Code entry bypasses subscription payment and assigns the athlete to the correct team/coaching hierarchy for data sharing.
- **Direct to Consumer (D2C)** (second rollout): Athlete downloads from app store, self-motivated. Pays for subscription. D2C subscription flow is deferred — not designed in this phase.

**Mental performance coaching source**: All coaching comes from **Coach Arron** — the AI coaching pipeline. Not a human coach. Not the athlete's sport coach. Coach Arron is the named coach for every athlete in both environments.

---

## 2. Auth Flow

### 2.1 Sign Up

**Purpose**: Create an account. Nothing more. No profile data, no sport information — that belongs to the intake.

**Fields**:
| Field | Format | Validation | Required |
|-------|--------|------------|----------|
| First Name | Text input | Non-empty, max 50 chars | Yes |
| Last Name | Text input | Non-empty, max 50 chars | Yes |
| Email | Email input | Valid email format, unique in system | Yes |
| Password | Password input | Minimum 8 characters | Yes |

**Layout** (matching existing mockup patterns):
- Top: Centered "VirtusFocus" logo wordmark with amber accent
- Below logo: Tagline (TBD — e.g., "Train your mind. Own your game.")
- 4 input fields: Dark background (zinc-900), rounded-xl, white text, zinc-600 placeholder text
- Password field: Show/hide toggle icon (eye icon, right side of field)
- Primary CTA: Full-width amber "Create Account" button. Disabled until all fields valid.
- Divider: "or" centered between horizontal rules
- Google OAuth: Outlined zinc-800 button with Google G icon, text "Continue with Google"
- Bottom link: "Already have an account? Sign In" — amber text link

**Behavior**:
- "Create Account" tap: Validates fields → creates account → navigates to Email Verification screen
- Google OAuth tap: Initiates Google OAuth flow → on success, auto-populates first name, last name, and email from Google profile → skips Email Verification entirely → navigates to Program Code screen
- Email uniqueness check: If email already exists, inline error beneath email field: "An account with this email already exists. Sign in instead?" with "Sign in" as amber link.
- Password requirements: Minimum 8 characters. No complexity requirements (uppercase, special char, etc.) — research shows these create friction without meaningful security improvement. If the dev team wants to add strength indicators later, that's a Settings/Phase 6 consideration.

**Legal/Compliance**:
- Below the "Create Account" button: Muted text (zinc-500, small): "By creating an account, you agree to our Terms of Service and Privacy Policy." Both "Terms of Service" and "Privacy Policy" are amber text links opening respective pages in external browser.
- No checkbox — account creation implies acceptance (standard mobile pattern).

**Data written**:
- `user.first_name`
- `user.last_name`
- `user.email`
- `user.password_hash`
- `user.auth_method` (email | google)
- `user.created_at` (timestamp)
- `user.onboarding_state` (set to `email_verification_pending` or `program_code_pending` for OAuth)

---

### 2.2 Email Verification

**Purpose**: Confirm the athlete controls the email address before proceeding. Blocking — the athlete cannot access onboarding until verified.

**Trigger**: Immediately after successful Sign Up (email/password only). Skipped for Google OAuth.

**Layout**:
- Top: VirtusFocus logo (smaller than Sign Up, consistent header)
- Center: Mail icon (simple, not animated — no celebration)
- Headline: **"Check your email"**
- Body text: "We sent a verification link to **[email@example.com]**. Tap the link to continue setting up your account."
- Below body: "Didn't get the email?" — amber text link
- Resend behavior: On tap, sends new verification email. Link text changes to "Email sent. Check your inbox." (zinc-500, non-interactive) for 60 seconds, then reverts to "Didn't get the email?" for re-tap.
- Bottom: "Wrong email? Start over" — muted zinc-500 text link → returns to Sign Up screen with fields cleared

**Verification link behavior**:
- Athlete taps link in email → opens app (deep link) or web fallback
- If app installed: Deep link opens app → verification confirmed → auto-navigate to Program Code screen
- If app not installed (web fallback): Landing page confirms verification with "Open VirtusFocus" button (app store link)
- Link expires after 24 hours. Expired link shows: "This link has expired. Open VirtusFocus to request a new one."

**Edge cases**:
- Athlete opens app without verifying: Shows Email Verification screen. Cannot bypass.
- Athlete verifies on a different device: On next app open, the original device detects verification and proceeds to Program Code screen.
- Email already verified (re-taps link): Graceful handling — "Already verified. You're all set." and proceeds normally.

**Data written**:
- `user.email_verified` (boolean)
- `user.email_verified_at` (timestamp)
- `user.onboarding_state` → `program_code_pending`

---

### 2.3 Login

**Purpose**: Authenticate a returning user with an existing account.

**Layout** (matching existing mockup patterns):
- Top: Centered "VirtusFocus" logo wordmark with amber accent
- 2 input fields: Email, Password (same styling as Sign Up)
- Password field: Show/hide toggle icon
- "Forgot password?" — amber text link, right-aligned below password field
- Primary CTA: Full-width amber "Sign In" button. Disabled until both fields non-empty.
- Divider: "or"
- Google OAuth: Outlined zinc-800 button with Google G icon, text "Continue with Google"
- Bottom link: "Don't have an account? Sign Up" — amber text link

**Behavior**:
- Successful login → navigate to Home (if onboarding complete) or resume onboarding at saved step (if incomplete)
- Failed login: Inline error below password field: "Incorrect email or password." No indication of which field is wrong (security best practice).
- Google OAuth: If Google account exists in system → login → Home or resume onboarding. If Google account does not exist → create account (auto Sign Up) → Program Code screen.
- Account lockout: After 5 failed attempts, lock account for 15 minutes. Show: "Too many attempts. Try again in 15 minutes, or reset your password."

**Data written**:
- `session.token` (30-day expiry)
- `session.created_at`
- `session.auth_method`

---

### 2.4 Password Recovery

**Purpose**: Allow an athlete to reset a forgotten password via email link.

**Flow**: 3 screens — Request → Check Email → Create New Password

#### Screen 1: Request Reset
- Top: VirtusFocus logo (consistent header)
- Headline: **"Reset your password"**
- Body: "Enter the email address you used to create your account."
- Input: Email field (same styling)
- CTA: Full-width amber "Send Reset Link" button
- Bottom: "Back to Sign In" — amber text link
- On submit: Always shows Screen 2, even if email doesn't exist in system (prevents email enumeration attacks)

#### Screen 2: Check Email
- Same layout pattern as Email Verification screen
- Headline: **"Check your email"**
- Body: "If an account exists for **[email@example.com]**, you'll receive a password reset link."
- "Didn't get the email?" — resend link (same 60-second cooldown as verification)
- "Back to Sign In" — bottom link

#### Screen 3: Create New Password (accessed via email link)
- Top: VirtusFocus logo
- Headline: **"Create a new password"**
- Input: New password field (same styling, show/hide toggle)
- Input: Confirm password field
- CTA: Full-width amber "Reset Password" button. Disabled until both fields match and meet minimum 8 characters.
- On success: Confirmation text "Password updated." Auto-navigate to Login screen after ~2 seconds.
- Reset link expires after 1 hour. Expired link: "This link has expired. Request a new one." with link to Screen 1.

**Data written**:
- `user.password_hash` (updated)
- `user.password_reset_at` (timestamp)

---

## 3. Program Code Screen

**Purpose**: Fork point between Institutional and D2C environments. Determines whether the athlete is part of a team/program or independent.

**Trigger**: After Email Verification (email sign-up) or after Google OAuth (skips verification).

**Layout**:
- Top: VirtusFocus logo (consistent header)
- Headline: **"Are you part of a team or program?"**
- Subheadline (muted): "If your team or program provided a code, enter it below."
- Input: Program code text field. Placeholder: "Enter program code"
- CTA: Full-width amber "Continue" button (below code field). Enabled when code field is non-empty.
- Below CTA, separated by spacing: "I'm here on my own" — amber text link, centered

**Behavior — Code entered**:
- Validates code against the system
- **Valid code**: Assigns athlete to institution/team/program + coaching hierarchy. Navigates to Initial Intake. Subscription bypassed (institution pays).
- **Invalid code**: Inline error below code field: "That code doesn't look right. Check with your coach or program administrator." Field retains entered text for correction.
- Code is case-insensitive. Leading/trailing whitespace trimmed automatically.

**Behavior — "I'm here on my own"**:
- D2C path. In the institutional-first launch, this path leads to a holding screen or waitlist: "VirtusFocus for individual athletes is coming soon. Enter your email to be notified." — with email field and "Notify Me" CTA.
- When D2C launches: This path leads to subscription payment (app store flow, design deferred) → then Initial Intake.

**Data written**:
- `user.environment` (institutional | d2c)
- `user.program_code` (string, institutional only)
- `user.institution_id` (FK, institutional only)
- `user.team_id` (FK, institutional only)
- `user.coaching_hierarchy` (assigned from code mapping, institutional only)
- `user.onboarding_state` → `intake_pending`

---

## 4. Initial Intake

**Purpose**: Collect the complete 29-question baseline assessment the AI coaching pipeline requires to function. The app is a collection device — it does not interpret, generate, or modify the questions. All questions are fixed, defined by the coaching methodology.

**Critical rule**: The intake MUST be completed in full. Without all 29 questions answered, the AI pipeline cannot generate personalized coaching. The intake is non-negotiable and non-skippable.

### 4.1 Presentation Model

**Format**: Section-per-screen, 7 steps. Each section is a self-contained screen displaying all questions for that section. Progress bar across the top (continuous fill, not discrete dots — communicates momentum).

**Navigation**:
- "Continue" CTA at bottom of each section. Gated — all required fields on that section must be completed before "Continue" enables.
- **No back button**. Forward-only (consistent with Evening Review wizard pattern). Answers are locked after advancing. This prevents second-guessing and keeps the athlete moving.
- Top bar: Section number and name (e.g., "1 of 7 — Performance Context"). No back arrow — if the athlete wants to exit, they close the app. Data auto-saves.
- Progress bar: Fills proportionally (1/7 after Section 1, 2/7 after Section 2, etc.). Amber fill on zinc-800 track.

**Auto-save**: All answers save at section boundary (on "Continue" tap). Additionally, individual field values auto-save on change (debounced, 2 seconds after interaction stops) so that mid-section exits preserve partial progress within the current section.

**Opening screen** (before Section 1):
- Headline: **"Let's get to know you."**
- Body: "These questions help us build your personal coaching program. It takes about 5 minutes. Answer honestly — there are no wrong answers."
- CTA: "Let's Go" — full-width amber button → advances to Section 1
- This screen is seen once. Not shown on re-entry after abandonment — athlete resumes at their saved section.

### 4.2 Section Headers

Each section screen includes a brief, coach-voice header that frames the questions. Not instructional, not clinical — conversational and grounding.

| Section | Header |
|---------|--------|
| 1 — Performance Context | *"Let's start with where you are."* |
| 2 — Self-Assessment Scales | *"How do you see yourself right now?"* |
| 3 — Performance Friction | *"What gets in the way?"* |
| 4 — Identity & Pressure | *"Who you are when it counts."* |
| 5 — Behavioral Patterns | *"How you respond to adversity."* |
| 6 — Ecosystem | *"Your support system."* |
| 7 — Goals & Commitment | *"Where you're headed."* |

Headers display in larger text below the progress bar, above the questions. Muted zinc-400 or similar — present but not dominant.

### 4.3 Section 1 — Performance Context (6 questions, ~30 sec)

| # | Question | Format | Required | Field | Notes |
|---|----------|--------|----------|-------|-------|
| Q1 | "What is your primary sport?" | Free text | Yes | `sport` | Single-line input |
| Q2 | "What is your position or event? (if applicable)" | Free text | No | `position` | "(if applicable)" signals optional nature. Single-line input. |
| Q3 | "What is your current team or club? (if applicable)" | Free text | No | `team` | Same as Q2 |
| Q4 | "What is your current competitive level?" | Single-select | Yes | `competitive_level` | Options: Youth, Middle School, High School, College, Professional |
| Q5 | "How many years have you been competing?" | Single-select | Yes | `years_competing` | Options: Less than 1, 1-2, 3-5, 6-8, 9+ |
| Q6 | "What is your current season phase?" | Single-select | Yes | `season_phase` | Options: Preseason, In-season, Offseason, Returning from injury |

**Layout**: All 6 questions visible on a single scrollable screen. Free text fields are single-line inputs (not text areas). Single-select options displayed as tappable pill chips (horizontal row if they fit, vertical stack if not). Selected chip fills amber. Unselected chips are outlined zinc-700.

**Gating**: "Continue" enables when Q1, Q4, Q5, and Q6 are answered. Q2 and Q3 are optional (signaled by "(if applicable)").

**Note for institutional athletes**: Q3 (team/club) may be pre-populated from the program code mapping. If pre-populated, the field displays the value as read-only with a muted label "From your program." The athlete cannot edit it.

### 4.4 Section 2 — Self-Assessment Scales (8 questions, ~60 sec)

All scales run 1 (low/negative anchor) to 5 (high/positive anchor). Displayed as 5 tappable numbered circles in a horizontal row. Selected circle fills amber. Anchor text displayed at endpoints (1 and 5).

**Pillar grouping**: Questions are organized under 4 pillar subheadings within the section. Subheadings are subtle labels (zinc-500, small caps or similar) — not interactive, just visual grouping.

| Pillar | # | Question | Anchors | Field |
|--------|---|----------|---------|-------|
| **Ownership** | Q7 | "How much of your development do you currently drive yourself?" | 1 = Low / 5 = High (default) | `abi_ownership_q1` |
| | Q8 | "How often do you review your own performance after practices or games?" | 1 = Low / 5 = High (default) | `abi_ownership_q2` |
| **Composure** | Q9 | "After a mistake, how quickly do you mentally reset?" | 1 = It sticks with me for a while / 5 = I reset almost immediately | `abi_composure_q1` |
| | Q10 | "How well do you keep your composure during big moments?" | 1 = I struggle a lot / 5 = I stay very composed | `abi_composure_q2` |
| **Focus** | Q11 | "During performance, how well do you maintain your focus?" | 1 = I lose focus very often / 5 = I rarely lose focus | `abi_focus_q1` |
| | Q12 | "How much do outside distractions (phone, social media, life stress) affect your training?" | 1 = Low / 5 = High (default) | `abi_focus_q2` |
| **Structure** | Q13 | "How consistent is your pre-performance mental routine?" | 1 = I don't have one / 5 = Very consistent | `abi_structure_q1` |
| | Q14 | "How consistent is your weekly training and recovery rhythm?" | 1 = Very inconsistent / 5 = Very consistent | `abi_structure_q2` |

**All 8 required.** No default value — athlete must tap a number for each. "Continue" enables when all 8 scales have a selection.

**Scale display pattern**: Question text above. 5 numbered circles (1–5) in a horizontal row, evenly spaced. Left anchor text below circle 1, right anchor text below circle 5. Anchors displayed in zinc-500 small text. Selected circle: amber fill, white number. Unselected: zinc-700 outline, zinc-400 number.

**Note on Q12**: The scale direction for Q12 ("How much do outside distractions affect your training?") is inverted relative to the other questions — a high score (5) means distractions affect training a lot (negative), while other questions use 5 as positive. This is intentional per the coaching methodology. The app displays it as-is. The pipeline interprets the inversion.

### 4.5 Section 3 — Performance Friction (2 questions, ~30 sec)

| # | Question | Format | Required | Field | Notes |
|---|----------|--------|----------|-------|-------|
| Q15 | "What usually gets in the way of your best performance?" | Multi-select, up to 3 | Yes (at least 1) | `performance_friction_selections[]` | 8 options (see below) |
| Q16 | "What situation makes this worse?" | Multi-select, up to 2 | Yes (at least 1) | `trigger_context_selections[]` | 5 options (see below) |

**Q15 options** (8 — one per PPD bucket):
- Overthinking
- Confidence going up and down
- Hard time letting go of mistakes
- Losing focus or getting distracted
- Pressure in big moments
- Staying motivated or disciplined
- Lack of routine or structure
- Pressure from coaches or parents

**Q16 options** (5 — trigger context amplifiers):
- Big competitions or high-stakes moments
- After making a mistake
- When being evaluated (coach, scouts, recruiters)
- During busy or stressful life weeks
- When expectations from others are high

**Multi-select display**: Options displayed as tappable rectangular chips (full-width, stacked vertically). Each chip shows a checkbox indicator (left side) + option text. Selected chips: amber left border + amber checkbox fill + slightly elevated background (zinc-800 → zinc-750 or similar). Unselected: zinc-800 background, zinc-600 checkbox outline.

**Selection limit enforcement**: When the athlete reaches the maximum selections (3 for Q15, 2 for Q16), remaining unselected options become visually muted (zinc-600 text, zinc-900 background) and non-tappable. Deselecting a chip re-enables the others. Subtle helper text below the question: "Choose up to 3" / "Choose up to 2".

**Gating**: "Continue" enables when Q15 has at least 1 selection AND Q16 has at least 1 selection.

### 4.6 Section 4 — Identity & Pressure (3 questions, ~90 sec)

| # | Question | Format | Required | Field | Notes |
|---|----------|--------|----------|-------|-------|
| Q17 | "At my best, I compete like someone who..." | Free-text sentence completion | Yes | `identity_sentence_completion` | Display hint below input (see below) |
| Q18 | "Before a big moment, what thought shows up most often?" | Free-text, short answer | Yes | `pressure_thought_text` | Display hint below input |
| Q19 | "What kind of competitor do you want to become?" | Free-text, short answer | Yes | `competitor_aspiration_text` | No hint |

**Display hints** (shown as muted placeholder-style text below the input field, not inside it):
- Q17: *Examples: "stays calm under pressure" / "attacks every rep" / "trusts my training"*
- Q18: *Examples: "Don't mess this up" / "Let's go" / "I need to prove myself"*
- Q19: No hint. The question is self-explanatory and the answer should be entirely the athlete's own words.

**Input format**: Single-line text inputs (not multi-line text areas). These are short-answer prompts — a sentence or phrase, not paragraphs. Max character limit: 200 characters per field.

**This is the longest section by estimated time (~90 sec)** because free-text requires thought. The section header ("Who you are when it counts.") sets a reflective but forward-facing tone. No rush.

**Gating**: "Continue" enables when all 3 fields are non-empty (trimmed whitespace).

### 4.7 Section 5 — Behavioral Patterns (2 questions, ~15 sec)

| # | Question | Format | Required | Field |
|---|----------|--------|----------|-------|
| Q20 | "When something goes wrong in competition, what do you usually do first?" | Single-select | Yes | `adversity_response_pattern` |
| Q21 | "After a bad performance, how do you usually describe yourself?" | Single-select | Yes | `adversity_self_description` |

**Q20 options**:
- Blame the situation
- Get frustrated
- Try to adjust right away
- Reset and refocus

**Q21 options**:
- I question my ability
- I get frustrated but move forward
- I analyze what happened and adjust
- I stay confident in myself

**Display**: Same tappable chip pattern as Section 1 single-selects. Vertical stack, full-width. One selection per question. Selected: amber fill. Unselected: zinc-700 outline.

**Gating**: "Continue" enables when both questions have a selection.

**Design note**: This is the fastest section (~15 sec). Two quick taps and done. The progress bar jumps noticeably — this creates a sense of momentum heading into the final two sections.

### 4.8 Section 6 — Ecosystem (4 questions, ~30 sec)

| # | Question | Format | Required | Field | Notes |
|---|----------|--------|----------|-------|-------|
| Q22 | "How involved are your parents/guardians in your performance journey?" | Single-select | Yes | `parent_involvement_level` | |
| Q23 | "After games or competitions, conversations at home are usually:" | Single-select | Yes | `home_conversation_pattern` | |
| Q24 | "Would you like to include your parents/guardians in your mindset coaching?" | Yes / No | Yes | `parent_inclusion` | Conditional: If Yes, email field appears |
| Q25 | "When you struggle, who do you usually talk to first?" | Single-select | Yes | `support_network_primary` | |

**Q22 options**: Very involved, Somewhat involved, Not very involved, Prefer not to say

**Q23 options**: Mostly supportive, A lot of analysis or advice, Pressure to perform, We don't discuss performance much

**Q24 special handling**:
- Display note (shown above the Yes/No selection, muted text, zinc-400): "All of your personal coaching and input is private and not shared with anyone other than you! Your parent/guardian will receive weekly updates on how they can support you and help with your mental performance growth!"
- Yes/No displayed as two tappable chips (side by side, equal width). Selected: amber fill.
- **Conditional field**: When "Yes" is selected, an email input field slides in below with smooth animation (200ms ease). Label: "Enter your parent/guardian's email address". Standard email validation. This field becomes required when visible.
- When "No" is selected (or toggled from Yes to No), the email field slides out and any entered value is cleared.

**Q25 options**: No one, A teammate, My coach, A parent, A mentor

**Gating**: "Continue" enables when Q22, Q23, Q24, and Q25 are answered. If Q24 = Yes, parent email must also be non-empty and valid.

**Data written (Q24)**:
- `parent_inclusion` (boolean)
- `parent_email` (string, conditional — only when parent_inclusion = true)
- In D2C environment: parent inclusion may trigger a subscription upgrade flow (deferred — not designed in this phase)
- In Institutional environment: parent inclusion is a free addition

### 4.9 Section 7 — Goals & Commitment (4 questions, ~60 sec)

| # | Question | Format | Required | Field | Notes |
|---|----------|--------|----------|-------|-------|
| Q26 | "What does success look like for you in the next 6 months?" | Free-text, short answer | Yes | `success_vision_text` | |
| Q27 | "On a scale of 1-10, how would you rate your current mental game?" | 1-10 selectable scale | Yes | `mental_game_self_rating` | |
| Q28 | "How committed are you to working on your mental game?" | Single-select | Yes | `commitment_level` | |
| Q29 | "Is there anything else you'd like us to know about you, your goals, or your challenges?" | Free-text, optional | No | `additional_context_text` | Display hint: "Skip if nothing comes to mind." |

**Q26**: Single-line text input, max 200 characters.

**Q27**: 10 tappable circles in a horizontal row (1–10). Same visual pattern as Section 2 scales but with 10 points instead of 5. No anchor labels — the question is self-explanatory. Selected circle: amber fill. This mirrors the Quick Ratings pattern from Weekly Recap (discrete 10-point tap selector).

**Q28 options**:
- Just curious
- Pretty serious
- All-in — let's go

**Q29**: Multi-line text area (3–4 visible lines). Optional. Display hint below: *"Skip if nothing comes to mind."* in muted zinc-500 text.

**Gating**: "Continue" (on this final section, the CTA reads **"Finish"**) enables when Q26, Q27, and Q28 are answered. Q29 is optional.

### 4.10 Intake Completion Transition

After the athlete taps "Finish" on Section 7:

- Brief confirmation screen (not a separate step — a transition moment):
  - Headline: **"You're all set."**
  - Body: "Your coaching program is being built. Let's show you how this works."
  - Auto-advances to How To after ~2 seconds. No manual CTA needed.
- This screen is the bridge between data collection and orientation. Tone shift: from "tell us about you" to "here's what's next."

**Data written on completion**:
- All 29 question responses (saved incrementally during the flow, but the completion event marks the intake as finalized)
- `user.intake_completed_at` (timestamp)
- `user.onboarding_state` → `how_to_pending`
- Triggers: Welcome message created in Messages/Inbox ("Welcome to VirtusFocus. Your coaching journey starts today." — attributed to Coach Arron)

---

## 5. How To — Tutorial Walkthrough

**Purpose**: Orient the athlete to the app's daily rhythm and tools before they reach Home for the first time. Brief, visual, skippable.

**Format**: 3-screen swipeable walkthrough. Horizontal pagination dots at bottom. "Skip" text link on every screen (top-right). Final screen has "Get Started" CTA.

### Screen 1: "Your day has a rhythm."
- Visual: Simple illustration or icon representing sunrise → sunset arc
- Headline: **"Your day has a rhythm."**
- Body: "Each morning, you'll start with a Tune-Up — a short mental warm-up for the day. Each evening, you'll reflect on how it went. That's the daily loop."
- Swipe indicator: Right arrow or pagination dots showing 1 of 3

### Screen 2: "Your tools are always here."
- Visual: Simple illustration of bottom nav bar with Bullseye and Journal icons highlighted
- Headline: **"Your tools are always here."**
- Body: "Use the Journal to note what happened. Use the Bullseye to sort what you can and can't control. Both are available anytime from the bottom nav."
- Pagination dots: 2 of 3

### Screen 3: "Your coach is with you."
- Visual: Simple illustration of a message/chat bubble with Coach Arron attribution
- Headline: **"Your coach is with you."**
- Body: "Coach Arron builds your coaching around your data — what you do, what you write, how you reflect. The more you use the app, the sharper the coaching gets."
- CTA: Full-width amber **"Get Started"** button
- Pagination dots: 3 of 3

**"Skip" behavior**: Tapping "Skip" on any screen immediately navigates to Home. The How To is marked as completed regardless of how many screens were viewed. It is not re-shown.

**"Get Started" behavior**: Navigates to Home.

**Re-access**: The How To walkthrough is not accessible from within the app after onboarding. A future "How It Works" option in Settings (Phase 6) could replay it, but this is not a commitment — just a possibility.

**Data written**:
- `user.how_to_completed_at` (timestamp — or null if skipped, which still counts as "done")
- `user.onboarding_state` → `complete`
- `user.onboarding_completed_at` (timestamp)

---

## 6. Complete Flow Sequencing

### 6.1 Institutional Flow (Launch Priority)

```
Sign Up (name, email, password)
  → Email Verification (blocking, check email)
    → Program Code Screen (enter institutional code)
      → [Code validated → team/hierarchy assigned]
        → Initial Intake (7 sections, 29 questions)
          → Intake Completion Transition ("You're all set.")
            → How To (3 screens, skippable)
              → Home
```

### 6.2 Institutional Flow — Google OAuth Variant

```
Google OAuth (name + email auto-populated, email pre-verified)
  → Program Code Screen (enter institutional code)
    → [Code validated → team/hierarchy assigned]
      → Initial Intake (7 sections, 29 questions)
        → Intake Completion Transition ("You're all set.")
          → How To (3 screens, skippable)
            → Home
```

### 6.3 D2C Flow (Deferred — Second Rollout)

```
Sign Up (or Google OAuth)
  → [Email Verification if email sign-up]
    → Program Code Screen → "I'm here on my own"
      → [Subscription Payment — app store flow, design deferred]
        → Initial Intake (7 sections, 29 questions)
          → Intake Completion Transition
            → How To (3 screens, skippable)
              → Home
```

### 6.4 D2C During Institutional-Only Launch

```
Sign Up (or Google OAuth)
  → [Email Verification if email sign-up]
    → Program Code Screen → "I'm here on my own"
      → Holding Screen: "VirtusFocus for individual athletes is coming soon.
         Enter your email to be notified."
         [Email field] [Notify Me CTA]
```

### 6.5 Returning User — Login

```
Login (email + password, or Google OAuth)
  → Onboarding complete? → Home
  → Onboarding incomplete? → Resume at saved step
```

---

## 7. First Day Experience

The first day is special. Normal timing rules are relaxed to ensure the athlete can begin the daily data collection cycle regardless of when they complete onboarding.

### 7.1 Post-Onboarding Landing

The athlete lands on **Home with Morning Tune-Up as the primary action**, regardless of clock time. The first Morning Tune-Up content is pre-generated and stored in the database — it does not depend on pipeline processing of intake data. The intake data feeds future personalized coaching; the first Tune-Up is a starter set.

### 7.2 First Day Timing Rules

| Rule | Normal Behavior | First Day Exception |
|------|----------------|-------------------|
| Morning Tune-Up availability | Available from hard-out time until evening release | Available immediately after onboarding, regardless of time |
| Morning Tune-Up "Late" tag | Applied if completed after noon | **No "Late" tag on Day 1** — it's the inaugural Tune-Up |
| Evening Review availability | Available after evening release time | Available at evening release time, OR immediately if already past evening release time when onboarding completes |
| Hard-out | Locks previous day's Evening Review at hard-out (default 6:00 AM) | Normal — first Evening Review locked at next morning's hard-out |

### 7.3 Time-of-Day Scenarios

**Athlete completes onboarding at 8:00 AM**:
- Home shows Morning Tune-Up (normal morning state)
- Normal day unfolds: Tune-Up → tools available → Evening Review at evening release

**Athlete completes onboarding at 3:00 PM**:
- Home shows Morning Tune-Up (first day exception — still available)
- Athlete completes Tune-Up
- Evening Review becomes available at evening release time (default 7:00 PM)
- Normal evening flow

**Athlete completes onboarding at 9:00 PM** (past evening release):
- Home shows Morning Tune-Up (first day exception — still primary action)
- Athlete completes Tune-Up
- Evening Review immediately available (past evening release time)
- Athlete can do both in one sitting if desired

**Athlete completes onboarding at 11:00 PM**:
- Same as 9:00 PM scenario
- Tight window — hard-out at 6:00 AM next morning
- Athlete can complete both tonight, or skip Evening Review tonight and start fresh tomorrow
- No penalty for Day 1 incomplete Evening Review

### 7.4 What's Ready on Day 1

| Content | Source | Available When |
|---------|--------|---------------|
| Morning Tune-Up (6 components) | Pre-generated, stored in database | Immediately on first Home load |
| Welcome message in Inbox | Created on intake completion | Immediately |
| First Daily Micro Coaching | Pipeline-generated from first Evening Review data | Morning after first completed Evening Review |
| First Weekly Coaching | Pipeline-generated from first week of data | After first Weekly Recap submission |

### 7.5 Home Screen First-Time State

When the athlete arrives at Home for the first time after onboarding:
- **Greeting**: "Good morning, [First Name]" or "Good evening, [First Name]" (based on actual time, not forced morning)
- **Primary Action Card**: Morning Tune-Up with today's Focus Word (pre-generated starter content)
- **Coaching Feedback Preview**: Welcome message — "Welcome to VirtusFocus. Your coaching journey starts today." (Coach Arron attribution)
- **Bullseye Card**: First-time empty state with onboarding prompt
- **Messages/Inbox**: Welcome message + helper text: "Coaching messages arrive as you use the program. Complete your first full day to get started."

---

## 8. Abandoned Onboarding

### 8.1 State Preservation

Onboarding progress is saved at each step boundary. The athlete resumes at the exact step where they left off.

| Exit Point | State Saved | Resume Point |
|------------|-------------|-------------|
| After Sign Up, before Email Verification | Account created, unverified | Email Verification screen |
| After Email Verification, before Program Code | Account verified | Program Code screen |
| After Program Code, before Intake | Program/team assigned (if institutional) | Initial Intake, Section 1 |
| Mid-Intake (between sections) | All completed sections saved | First incomplete section |
| Mid-Intake (within a section) | Individual field values auto-saved | Same section, fields pre-populated |
| After Intake, before How To | Intake complete | How To screen |
| During How To | Intake complete | How To screen (from beginning) |

### 8.2 Re-Entry Experience

When an athlete returns to the app with incomplete onboarding:
- App opens → detects incomplete onboarding state → routes to the correct resume point
- No "welcome back" nudge on the onboarding screens themselves (unlike the daily tools which show "welcome back" nudges). The athlete simply picks up where they left off. The pre-populated fields signal that their previous input was saved.

### 8.3 Push Notification Nudges

If the athlete exits before completing onboarding:

| Timing | Message |
|--------|---------|
| After 1 hour | "You're almost set up. A few more steps and your coaching can begin." |
| After 24 hours | "Your coaching program is waiting. Pick up where you left off." |
| After 72 hours | "Ready when you are. Tap to finish setting up VirtusFocus." |
| After 7 days | "Your account is still here. Complete your setup to start training your mind." |

After the 7-day nudge: silence. No further notifications. The account persists but the athlete is not spammed.

**Nudge prerequisite**: Push notification permission must be requested. See Section 9 (Notification Permission).

---

## 9. Notification Permission

**When**: After intake completion, before How To. The intake completion transition screen ("You're all set.") is followed by the OS-level push notification permission prompt.

**Timing rationale**: Requesting notification permission during onboarding (not on first app open) ensures the athlete understands what the app does before deciding. Placing it after intake (not before) means the athlete is invested — they've completed 29 questions and are committed. This maximizes opt-in rate.

**If denied**: The app functions normally without push notifications. No re-prompting during onboarding. A future "Enable Notifications" option in Settings (Phase 6) can surface the system settings to re-enable.

**If accepted**: Enables Daily Micro Coaching notifications ("Your coaching for today is ready."), Weekly Bundle notifications ("Your weekly coaching is ready."), and abandoned onboarding nudges.

**Sequence adjustment**:
```
Initial Intake → Intake Completion Transition → [OS Notification Permission Prompt] → How To → Home
```

---

## 10. Data Model

### 10.1 User Account

| Field | Type | Set During | Notes |
|-------|------|-----------|-------|
| `user_id` | UUID | Sign Up | Primary key |
| `first_name` | String | Sign Up | From form or Google profile |
| `last_name` | String | Sign Up | From form or Google profile |
| `email` | String | Sign Up | Unique, from form or Google profile |
| `password_hash` | String | Sign Up | Null for Google OAuth users |
| `auth_method` | Enum | Sign Up | email, google |
| `email_verified` | Boolean | Email Verification | True for OAuth users automatically |
| `email_verified_at` | Timestamp | Email Verification | |
| `created_at` | Timestamp | Sign Up | |
| `onboarding_state` | Enum | Progressive | email_verification_pending → program_code_pending → intake_pending → intake_in_progress → how_to_pending → complete |
| `onboarding_completed_at` | Timestamp | How To completion | |
| `environment` | Enum | Program Code | institutional, d2c |
| `program_code` | String | Program Code | Institutional only |
| `institution_id` | FK | Program Code | Institutional only, derived from code |
| `team_id` | FK | Program Code | Institutional only, derived from code |
| `coaching_hierarchy` | JSON/FK | Program Code | Institutional only, derived from code |
| `notification_permission` | Boolean | Post-Intake | OS-level permission status |

### 10.2 Intake Responses

All 29 intake responses stored as a single structured record linked to the user.

| Field | Type | Section | Required |
|-------|------|---------|----------|
| `sport` | String | 1 | Yes |
| `position` | String | 1 | No |
| `team` | String | 1 | No |
| `competitive_level` | Enum | 1 | Yes |
| `years_competing` | Enum | 1 | Yes |
| `season_phase` | Enum | 1 | Yes |
| `abi_ownership_q1` | Int (1-5) | 2 | Yes |
| `abi_ownership_q2` | Int (1-5) | 2 | Yes |
| `abi_composure_q1` | Int (1-5) | 2 | Yes |
| `abi_composure_q2` | Int (1-5) | 2 | Yes |
| `abi_focus_q1` | Int (1-5) | 2 | Yes |
| `abi_focus_q2` | Int (1-5) | 2 | Yes |
| `abi_structure_q1` | Int (1-5) | 2 | Yes |
| `abi_structure_q2` | Int (1-5) | 2 | Yes |
| `performance_friction_selections` | Array (max 3) | 3 | Yes (min 1) |
| `trigger_context_selections` | Array (max 2) | 3 | Yes (min 1) |
| `identity_sentence_completion` | String | 4 | Yes |
| `pressure_thought_text` | String | 4 | Yes |
| `competitor_aspiration_text` | String | 4 | Yes |
| `adversity_response_pattern` | Enum | 5 | Yes |
| `adversity_self_description` | Enum | 5 | Yes |
| `parent_involvement_level` | Enum | 6 | Yes |
| `home_conversation_pattern` | Enum | 6 | Yes |
| `parent_inclusion` | Boolean | 6 | Yes |
| `parent_email` | String | 6 | Conditional (if parent_inclusion = true) |
| `support_network_primary` | Enum | 6 | Yes |
| `success_vision_text` | String | 7 | Yes |
| `mental_game_self_rating` | Int (1-10) | 7 | Yes |
| `commitment_level` | Enum | 7 | Yes |
| `additional_context_text` | String | 7 | No |
| `intake_completed_at` | Timestamp | — | Set on final submission |
| `intake_section_progress` | Int (0-7) | — | Tracks furthest completed section |

---

## 11. Edge Cases

### 11.1 Auth Edge Cases

| Scenario | Behavior |
|----------|----------|
| Email already registered (Sign Up) | Inline error: "An account with this email already exists. Sign in instead?" |
| Google OAuth email matches existing email/password account | Link accounts. Athlete can now use either method. No duplicate account created. |
| Google OAuth email matches existing Google account | Normal login. Proceeds to Home or resume onboarding. |
| Password reset for Google-only account | "This account uses Google Sign-In. Use 'Continue with Google' to access your account." |
| Email verification link expired | "This link has expired. Open VirtusFocus to request a new one." |
| Email verification link used twice | Graceful: "Already verified. You're all set." |
| 5 failed login attempts | Account locked 15 minutes. "Too many attempts. Try again in 15 minutes, or reset your password." |

### 11.2 Program Code Edge Cases

| Scenario | Behavior |
|----------|----------|
| Invalid code | Inline error: "That code doesn't look right. Check with your coach or program administrator." |
| Valid code, team already full | If institution has a cap: "This program has reached its enrollment limit. Contact your program administrator." |
| Athlete enters code, then later institution removes them | Account persists. Environment flag updated. Data retained. Coaching continues (Coach Arron is independent of institution). Access to institutional features (coach data sharing) revoked. |
| Athlete enters wrong team's code | Program code screen shows the resolved team name after validation: "You'll be joining [Team Name]." with a "That's not right" link that clears the code and lets them re-enter. Confirmation before proceeding. |

### 11.3 Intake Edge Cases

| Scenario | Behavior |
|----------|----------|
| App killed mid-section | Auto-saved field values restore on re-open. Athlete sees their partial answers pre-populated. |
| Athlete taps "Continue" then loses connection | Optimistic: advance to next section. Queue the save. Retry on reconnection. If save ultimately fails, re-prompt that section on next open. |
| Q24 Yes → enters email → changes to No → changes back to Yes | Email field cleared when toggled to No. Must re-enter on toggle back to Yes. Prevents stale data. |
| Very long free-text answer | Max 200 characters per field (Q17, Q18, Q19, Q26, Q29). Character counter appears when 80% of limit reached. Hard stop at limit. Q29 (the optional open-ended) gets 500 character limit. |

### 11.4 Timing Edge Cases

| Scenario | Behavior |
|----------|----------|
| Onboarding completes at 5:55 AM (5 min before hard-out) | Home shows Morning Tune-Up. First day exception — no hard-out impact on Day 1 Tune-Up. The hard-out that fires at 6:00 AM has no previous-day Evening Review to lock (there is no previous day). |
| Onboarding completes at 2:00 AM | First day exception. Home shows Morning Tune-Up. The athlete can do it now (2 AM counts as the current calendar day per hard-out boundary rules). Evening Review available at evening release time later that day. |
| Athlete signs up, verifies email, then doesn't open app for 3 weeks | On re-open: resumes onboarding at Program Code screen. Nudge notifications sent at 1hr, 24hr, 72hr, 7 days. After 7 days, silence. Account persists indefinitely. |

---

## 12. Accessibility

- All text inputs: Proper labels, not just placeholder text. Labels visible above fields at all times (not placeholder-as-label that disappears on focus).
- Scale selectors (1-5, 1-10): Each circle is a tappable target minimum 44x44pt. Circles have accessible labels (e.g., "1 of 5, It sticks with me for a while" for Q9).
- Multi-select chips: Minimum 44pt tap target height. Selected state communicated via color AND icon (checkbox fill), not color alone.
- Single-select chips: Same tap target requirements. Selected state: amber fill + checkmark or radio dot, not color alone.
- Progress bar: Accessible label ("Step 3 of 7 — Performance Friction").
- "Skip" link on How To: Minimum 44pt tap target despite being styled as a text link.
- All form validation errors: Communicated via text (not color alone), associated with the relevant field via accessibility labels.
- Screen reader: Each intake section announces its header and question count on focus.

---

## 13. Visual Design Notes

**Consistent with existing app patterns**:
- Dark theme: zinc-900 backgrounds, zinc-800 input fields/cards
- Amber accent: CTAs, selected states, links, progress bar fill
- White text: Primary content, input text
- Zinc-400/500: Secondary text, hints, helpers, anchors
- Rounded-xl: Input fields, buttons, chips
- Font: System default (San Francisco on iOS, Roboto on Android)

**New patterns introduced in this phase**:
- **Progress bar**: Continuous amber fill on zinc-800 track. Used for intake only (7 steps). Not used on How To (dots instead).
- **Section headers**: Larger text, coach-voice, muted color. Framing text above question groups.
- **Conditional reveal**: Q24's email field slides in/out (200ms ease) based on Yes/No selection.
- **Confirmation code input**: Program code field — standard text input, no special formatting (not segmented OTP-style).
- **Holding screen (D2C during institutional launch)**: Clean, minimal — logo, message, email capture, single CTA.

---

## 14. Hard Rules

1. **Intake is non-skippable.** All 29 questions (28 required + Q29 optional) must be answered before the athlete reaches Home. No "Skip for now" option. No "Complete later" option. The pipeline cannot function without complete intake data.
2. **Forward-only intake flow.** No back button between sections. Answers are committed when the athlete advances. This is consistent with the Evening Review wizard pattern and prevents over-analysis of responses.
3. **Auto-save everywhere.** Every field value auto-saves. Abandoned onboarding resumes at the exact point of exit. No data loss on app kill, backgrounding, or connection loss (queued for retry).
4. **Email verification is blocking.** No access to onboarding until email is verified. Exception: Google OAuth bypasses this entirely.
5. **Program code validates before proceeding.** Invalid codes show inline errors. The athlete cannot advance without a valid code (institutional) or explicit "I'm here on my own" selection (D2C).
6. **Coach Arron is the only coach.** All coaching attribution is Coach Arron — the AI pipeline. No human coaches provide mental performance coaching through this app. Sport coaches (institutional) receive data insights only, via a separate dashboard.
7. **First day timing is relaxed.** Morning Tune-Up is available immediately after onboarding, regardless of clock time. No "Late" tag on Day 1.
8. **No celebration, no hype, no gamification in onboarding.** No confetti on intake completion. No "Great job!" after each section. The tone is calm, coach-led, grounded. The intake completion transition is simple: "You're all set."
9. **Privacy declaration on Q24 is mandatory display.** The parent inclusion privacy note must always be shown when Q24 is presented. It is not collapsible or dismissable.
10. **Notification permission requested once during onboarding.** After intake, before How To. If denied, no re-prompting during onboarding. Settings (Phase 6) provides the re-enable path.
11. **Abandoned onboarding nudges stop after 7 days.** Four total nudges (1hr, 24hr, 72hr, 7 days), then silence. Account persists but the athlete is not spammed.
12. **D2C holding screen during institutional launch.** "I'm here on my own" leads to a waitlist/notification capture, not the full onboarding flow. When D2C launches, this screen is replaced with the subscription flow.

---

## 15. Open Items for Future Phases

| Item | Phase | Notes |
|------|-------|-------|
| D2C subscription payment flow | Phase 5 addendum or separate | Deferred. Design when D2C rollout approaches. |
| Biometric unlock (Face ID / fingerprint) | Phase 6 — Settings | Configured in Settings, not during onboarding. |
| "How It Works" replay | Phase 6 — Settings | Optional re-access to How To walkthrough from Settings. |
| Avatar / profile photo | Phase 6 — Profile | Athletes can add via Profile screen. Not collected during onboarding. |
| Parent enrollment flow (D2C upgrade) | Future | Q24 parent inclusion may trigger subscription upgrade in D2C. Flow TBD. |
| Institutional athlete removal handling | Future | What happens when an institution removes an athlete from their program. |
| Account deletion | Phase 6 — Settings | Required for app store compliance. Not part of onboarding. |
| Terms of Service / Privacy Policy content | Legal | Links exist on Sign Up screen. Actual content is a legal deliverable, not a design deliverable. |

---

## 16. Session 8 Decision Update — Coach Attribution

**Previous decision (Session 8, Messages / Inbox)**: Welcome message attributed to generic "Coach" until program assignment establishes named coach.

**Updated decision (Session 9)**: Welcome message attributed to **Coach Arron**. There is no "generic Coach → named coach" transition. Coach Arron is the AI coaching pipeline and is the named coach from day one, for all athletes, in both environments. The Messages/Inbox design document should be updated to reflect this: all references to "generic Coach before program assignment" should be changed to "Coach Arron."

This is the only change to a previous design document resulting from this session.
