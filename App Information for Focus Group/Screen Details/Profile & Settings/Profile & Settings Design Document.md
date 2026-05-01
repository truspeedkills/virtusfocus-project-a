# Profile & Settings — Design Document

**App**: VirtusFocus — Athlete Mental Performance App
**Screens**: Profile, Edit Profile, Deep Dive Archive, Settings
**Phase**: 6 (Final)
**Status**: Design Complete
**Date**: 2026-03-13
**Session**: 10

---

## 1. Purpose & Context

Profile & Settings is the athlete's identity surface and control panel within VirtusFocus. Every other screen in the app is structured around doing — committing (Morning Tune-Up), reflecting (Evening Review, Journal, Bullseye), closing the week (Weekly Recap), and receiving coaching (Messages/Inbox). Profile & Settings is where the athlete sees who they are in the program and adjusts the small number of preferences the system allows.

This is **not a social profile**. There is no bio, no followers, no public-facing persona. It is informational and functional — identity display, coaching archive access, and preference management.

### Role in the App

- **Access point**: Top-right icon on Home screen. Not in the bottom nav. Profile is a secondary surface — the athlete visits occasionally, not daily.
- **Deep dive archive**: The only place to access Weekly Deep Dives older than 3 weeks (the Messages/Inbox feed window).
- **Account management**: Sign out, edit identity fields, change password, delete account.
- **Preference control**: Notifications, appearance, biometric unlock, schedule (D2C only).

### Design Philosophy

- Profile is identity, not performance dashboard. No stats, no streaks, no scores.
- Settings should be minimal — only what the athlete genuinely needs to control.
- No unnecessary options that create decision burden.
- Calm, informational tone throughout.

---

## 2. Profile Screen

### 2a. Entry Points

| Source | Trigger | Notes |
|--------|---------|-------|
| Home — Top-right icon | Athlete taps profile icon | Primary and only entry point |

Profile is accessible from Home only. It is not in the bottom nav and cannot be reached from any other screen directly.

### 2b. Screen Layout

```
┌──────────────────────────────┐
│  ← Back              PROFILE │
├──────────────────────────────┤
│                              │
│         ┌────────┐           │
│         │ Avatar │           │
│         │ (or    │           │
│         │initials│           │
│         └────────┘           │
│                              │
│       Athlete Full Name      │
│  With VirtusFocus since      │
│       March 2026             │
│    athlete@email.com         │
│                              │
├──────────────────────────────┤
│                              │
│  Basketball · Point Guard    │
│  College                     │
│                              │
├──────────────────────────────┤  ← Institutional only
│                              │
│  🏢 Westfield High School    │
│     Varsity Program          │
│                              │
├──────────────────────────────┤
│                              │
│  📝 Edit Profile        →    │
│  📖 Deep Dive Archive   →    │
│  ⚙️ Settings            →    │
│  ↩️ Sign Out                  │
│                              │
└──────────────────────────────┘
```

### 2c. Identity Block

The top section establishes who the athlete is within VirtusFocus.

| Element | Source | Display |
|---------|--------|---------|
| **Avatar** | Uploaded photo, or initials fallback | Circular, centered, prominent. Initials derived from first + last name (e.g., "AP" for Arron Panigall). Default state until athlete uploads a photo via Edit Profile. |
| **Full name** | First Name + Last Name from account | Largest text in the identity block. Centered below avatar. |
| **Tenure line** | Account creation date | "With VirtusFocus since [Month Year]" — muted text, directly below name. Factual timestamp. No milestone styling changes at any duration. |
| **Email** | Account email | Muted/secondary color. Below tenure line. |

**Tenure line rules**:
- Format is always "With VirtusFocus since [Month Year]" — e.g., "With VirtusFocus since March 2026"
- No day precision — month and year only
- No duration count ("6 months", "1 year") — just the start date
- No visual changes at milestones (1 month, 6 months, 1 year). The line looks the same on day 1 and day 365.
- Serves as quiet acknowledgment of commitment. The longer the athlete is in the program, the more weight the date carries on its own.

### 2d. Athletic Context Block

Below the identity block, separated by subtle visual break.

| Element | Source | Display |
|---------|--------|---------|
| **Sport + Position** | Intake Q1 (sport) + Q2 (position) | Single line: "Basketball · Point Guard". Dot separator. |
| **Competition level** | Intake Q3 (or updated via Edit Profile) | Separate line below sport/position: "College" |

If position is not applicable (e.g., individual sport like Track & Field), only sport displays. No empty "· " separator.

### 2e. Program Block (Institutional Only)

Visible only for athletes who entered a program code during onboarding. Hidden entirely for D2C athletes.

| Element | Source | Display |
|---------|--------|---------|
| **Team/program name** | Resolved from program code during onboarding | e.g., "Westfield High School — Varsity Program" |

**Rules**:
- Read-only. Athlete cannot change their program association from Profile.
- If the program name changes (admin-side), it updates here automatically.
- No sport coach name displayed. Sport coaches interact through the Coaching Insight Dashboard, not through the athlete app.
- D2C athletes: this entire section is absent — no placeholder, no "Join a team" prompt.

### 2f. Action Menu

Four items, displayed as a simple list with tap targets.

| Item | Destination | Notes |
|------|-------------|-------|
| **Edit Profile** | Edit Profile screen | Arrow indicator (→) |
| **Deep Dive Archive** | Deep Dive Archive screen | Arrow indicator (→) |
| **Settings** | Settings screen | Arrow indicator (→) |
| **Sign Out** | Confirmation → Login screen | No arrow — terminal action |

**Sign Out behavior**:
- Tap triggers a confirmation: "Sign out of VirtusFocus?" with "Sign Out" (destructive style) and "Cancel" options.
- Confirmation clears the session token and navigates to the Login screen.
- No data is lost — all athlete data is server-side.

---

## 3. Deep Dive Archive

### 3a. Purpose

The Deep Dive Archive provides long-term access to all Weekly Deep Dives the athlete has received. The Messages/Inbox feed only shows the current week + 2 previous weeks. Deep dives older than that window are only accessible here.

### 3b. Entry Point

| Source | Trigger |
|--------|---------|
| Profile — Action Menu | Tap "Deep Dive Archive" |

### 3c. Screen Layout

```
┌──────────────────────────────┐
│  ← Back      Deep Dive Archive│
│                              │
│  ┌────────────────────────┐  │
│  │ 📅 Jump to month...    │  │  ← Month picker
│  └────────────────────────┘  │
│                              │
│  ── March 2026 ──────────── │  ← Month section header
│                              │
│  ┌────────────────────────┐  │
│  │ Week of March 9, 2026  │  │
│  │ ● New                  │  │  ← Unread indicator
│  └────────────────────────┘  │
│                              │
│  ┌────────────────────────┐  │
│  │ Week of March 2, 2026  │  │
│  └────────────────────────┘  │
│                              │
│  ── February 2026 ───────── │  ← Month section header
│                              │
│  ┌────────────────────────┐  │
│  │ Week of Feb 23, 2026   │  │
│  └────────────────────────┘  │
│  ...                         │
└──────────────────────────────┘
```

### 3d. List Structure

- **Reverse chronological order** — newest deep dive at the top.
- **Grouped by month** with section headers (e.g., "March 2026", "February 2026"). Headers act as visual landmarks for scrolling.
- **Each list item** displays:
  - Week label: "Week of [Month Day, Year]" — the Monday of that coaching week.
  - "New" indicator if the deep dive hasn't been opened in the full-screen reader (same pattern as Messages/Inbox).
- **Month picker** at top of screen: tappable selector that jumps the list to the selected month. Scrollable month/year selector — not a text search field. Zero typing required.

### 3e. Interaction

- **Tap a list item** → opens the full-screen reader (same reader component used in Messages/Inbox).
- **Full-screen reader**: Clean long-form reading view, section headers preserved (Weekly Overview, Strengths and Wins, Opportunities and Growth Areas, Mindset Summary, Coaching Focus Areas). Back arrow returns to archive list.
- **Scroll position preserved**: If the athlete opens a deep dive and returns, the archive list maintains its scroll position.
- **"New" label clears** when the full-screen reader is opened (same logic as Messages/Inbox — `deepDiveOpened` flag).

### 3f. Rules

- **No search by text content.** Date-based navigation only (month picker + section headers).
- **No filtering.** All deep dives are shown.
- **No deletion.** Consistent with the app's data permanence pattern (Journal, Bullseye, Messages).
- **Read-only.** No bookmarking, no sharing, no downloading.
- **All deep dives included.** Every deep dive ever generated for the athlete appears here — no time boundary (unlike the 3-week Messages feed).

### 3g. Empty State

For new athletes who haven't received any deep dives yet:

> "Your weekly deep dives will appear here. Complete your first full week to get started."

Centered, muted text. No CTA. The athlete will naturally return here once coaching begins.

### 3h. Data Source

The archive reads from the same `Message` data model used by Messages/Inbox, filtered to `type = WEEKLY_DEEP_DIVE` for the current athlete. The full-screen reader renders the same `body` content. No separate data store required.

---

## 4. Edit Profile

### 4a. Entry Point

| Source | Trigger |
|--------|---------|
| Profile — Action Menu | Tap "Edit Profile" |

### 4b. Screen Layout

```
┌──────────────────────────────┐
│  ← Cancel      Edit Profile  │
│                       Save → │
├──────────────────────────────┤
│                              │
│         ┌────────┐           │
│         │ Avatar │           │
│         │        │           │
│         └────────┘           │
│      Change Photo            │
│                              │
├──────────────────────────────┤
│                              │
│  First Name                  │
│  ┌────────────────────────┐  │
│  │ Arron                  │  │
│  └────────────────────────┘  │
│                              │
│  Last Name                   │
│  ┌────────────────────────┐  │
│  │ Panigall               │  │
│  └────────────────────────┘  │
│                              │
│  Email                       │
│  ┌────────────────────────┐  │
│  │ arron@email.com        │  │
│  └────────────────────────┘  │
│  Changing your email will    │
│  require verification.       │
│                              │
│  Competition Level           │
│  ┌────────────────────────┐  │
│  │ College            ▼   │  │
│  └────────────────────────┘  │
│                              │
├──────────────────────────────┤
│                              │
│  Sport · Position · Team     │
│  Read-only. Contact support  │
│  to update.                  │
│                              │
└──────────────────────────────┘
```

### 4c. Editable Fields

| Field | Input Type | Validation | Notes |
|-------|-----------|------------|-------|
| **Avatar/photo** | Photo upload (camera or gallery) | Max file size TBD by implementation. Cropped to square. | "Change Photo" link below avatar. "Remove Photo" appears when a photo exists (reverts to initials). |
| **First Name** | Text input | Required. Non-empty after trimming whitespace. | Pre-populated with current value. |
| **Last Name** | Text input | Required. Non-empty after trimming whitespace. | Pre-populated with current value. |
| **Email** | Text/email input | Required. Valid email format. | Changing email triggers re-verification flow (see Section 4e). Helper text below field: "Changing your email will require verification." |
| **Competition Level** | Dropdown selector | Required. Must select a value. | Same options as intake Q3. Pre-populated with current value. Change takes effect immediately on save — no re-verification needed. Pipeline picks up new value on next coaching cycle. |

### 4d. Read-Only Fields (Not Editable)

These fields are visible on the Profile screen but **do not appear as editable fields** in Edit Profile. Instead, a brief note at the bottom of the form acknowledges their existence:

> "Sport, position, and team are set during onboarding. Contact your program administrator to update." (institutional)

> "Sport and position are set during onboarding. Contact support to update." (D2C)

**Fields locked after onboarding:**
- Sport (intake Q1)
- Position (intake Q2)
- Team/program association (from program code)

**Rationale**: These fields feed the AI coaching pipeline. Casual self-service changes would corrupt coaching data. If an athlete legitimately changes sports or teams, that represents a program-level event requiring new intake data and coaching baseline recalibration — not a Profile edit.

### 4e. Email Change — Re-Verification Flow

When the athlete saves a new email address:

1. **Save is accepted** — Profile updates locally to show the new email.
2. **Verification email sent** to the new address.
3. **Until verified**: A banner appears on Profile: "Verify your new email. Check [new@email.com] for a verification link."
4. **If verification completes**: New email is confirmed. Banner disappears.
5. **If verification expires** (same 1-hour window as onboarding): Old email is restored. No data loss. Athlete can try again via Edit Profile.
6. **Login continues to work** with the old email until the new one is verified.

### 4f. Save Behavior

- **Explicit "Save" CTA** in the top bar (right side). Not auto-save — this is identity data.
- **"Cancel"** in the top bar (left side, replacing the back arrow). Returns to Profile with no changes applied.
- **Save validation**: All required fields must be non-empty and valid. If validation fails, inline error messages appear below the offending field(s). Save CTA remains tappable but triggers validation display.
- **Save success**: Navigates back to Profile. Updated data reflected immediately (except email — see 4e).
- **Save failure** (network): Inline error: "Couldn't save. Check your connection and try again." Stay on Edit Profile.

### 4g. Intake Questions

All 29 intake questions answered during onboarding are **locked permanently**. They are:
- Not viewable in Profile or Edit Profile
- Not editable by the athlete
- Not re-takeable

The intake is a one-time baseline assessment that feeds the coaching pipeline. Re-taking it would disrupt the coaching model. If an athlete's circumstances change significantly, the pipeline adapts through ongoing data collection (Evening Review, Weekly Recap, Journal, Bullseye) — not through re-assessment.

---

## 5. Settings

### 5a. Entry Point

| Source | Trigger |
|--------|---------|
| Profile — Action Menu | Tap "Settings" |

### 5b. Screen Layout

```
┌──────────────────────────────┐
│  ← Back            Settings  │
├──────────────────────────────┤
│                              │
│  NOTIFICATIONS               │
│  ┌────────────────────────┐  │
│  │ Daily Coaching     [●] │  │
│  │ Weekly Coaching    [●] │  │
│  │ Evening Reminder   [●] │  │
│  │ Morning Reminder   [●] │  │
│  └────────────────────────┘  │
│                              │
│  SECURITY                    │
│  ┌────────────────────────┐  │
│  │ Change Password     →  │  │
│  │ Biometric Unlock   [○] │  │
│  └────────────────────────┘  │
│                              │
│  APPEARANCE                  │
│  ┌────────────────────────┐  │
│  │ Theme                  │  │
│  │ ○ Light ○ Dark ● System│  │
│  └────────────────────────┘  │
│                              │
│  SCHEDULE (D2C only)         │
│  ┌────────────────────────┐  │
│  │ Morning Start   6:00AM │  │
│  │ Evening Start   7:00PM │  │
│  └────────────────────────┘  │
│                              │
│  ABOUT & SUPPORT             │
│  ┌────────────────────────┐  │
│  │ How It Works        →  │  │
│  │ Privacy Policy      →  │  │
│  │ Terms of Service    →  │  │
│  │ Contact Support     →  │  │
│  └────────────────────────┘  │
│                              │
│  ACCOUNT                     │
│  ┌────────────────────────┐  │
│  │ Delete Account      →  │  │
│  └────────────────────────┘  │
│                              │
│  VirtusFocus v1.0.2         │
│                              │
└──────────────────────────────┘
```

### 5c. Section 1 — Notifications

Four toggles controlling push notification delivery.

| Toggle | Default | Controls |
|--------|---------|----------|
| **Daily Coaching** | On | Push notification for Daily Micro Coaching ("Your coaching for today is ready.") |
| **Weekly Coaching** | On | Push notification for weekly bundle — coaching message + deep dive ("Your weekly coaching is ready.") |
| **Evening Review Reminder** | On | Gentle nudge if Evening Review not started by a configurable time |
| **Morning Tune-Up Reminder** | On | Gentle nudge if Morning Tune-Up not completed by a configurable time |

**Rules**:
- Toggles control push notifications only. In-app message delivery is unaffected — messages always appear in the feed regardless of notification settings.
- Milestones and system notifications do not have toggles (they don't send push notifications — decided in Session 8).
- Changes take effect immediately. No save CTA needed — toggles are their own save action.

**OS Permission Denied State**:

If the athlete denied notification permission during onboarding (or revoked it via device settings), this section displays:

> "Notifications are turned off for VirtusFocus."
> [Open Device Settings]

The button deep-links to the OS notification settings for VirtusFocus. Individual toggles are hidden when OS permission is denied — showing disabled toggles would be confusing.

When the athlete grants permission and returns to the app, the toggles reappear with all defaults set to On.

### 5d. Section 2 — Security

| Item | Type | Behavior |
|------|------|----------|
| **Change Password** | Navigation (→) | Opens a sub-screen: Current Password + New Password + Confirm New Password. Standard validation (minimum length, match confirmation). Save CTA. Success returns to Settings with brief confirmation. |
| **Biometric Unlock** | Toggle | Off by default. When enabled, Face ID / fingerprint replaces credential entry on app launch within the 30-day session window. Enabling triggers a one-time biometric enrollment prompt from the OS. Disabling reverts to standard session behavior (auto-login within 30-day window, no biometric). |

**Change Password sub-screen**:
- Current password field required to prevent unauthorized changes if device is unlocked.
- New password validation: minimum 8 characters (matches sign-up requirements from Session 9).
- Confirm password must match new password.
- On success: "Password updated." confirmation, auto-return to Settings.
- On failure (wrong current password): inline error "Current password is incorrect."
- On failure (network): "Couldn't update password. Check your connection and try again."

**Biometric Unlock**:
- Toggle label adapts to platform: "Face ID" on iOS with Face ID, "Fingerprint" on Android, "Biometric Unlock" as fallback.
- If the device doesn't support biometric authentication, this toggle is hidden entirely.
- Enabling does NOT replace the password — it provides a convenience shortcut for app launch only. Password is still required for: Change Password, Delete Account, and any future sensitive actions.

### 5e. Section 3 — Appearance

| Item | Type | Options | Default |
|------|------|---------|---------|
| **Theme** | 3-way selector | Light / Dark / System Default | System Default |

- **System Default**: Follows the device's light/dark mode setting. If the athlete's phone switches to dark mode at sunset, VirtusFocus follows.
- **Light**: Forces light mode regardless of device setting.
- **Dark**: Forces dark mode regardless of device setting.
- Selection takes effect immediately — no save CTA needed.
- This is the only appearance setting. No font size, no color themes, no layout options.

### 5f. Section 4 — Schedule (D2C Only)

This section is **only visible to D2C athletes**. Institutional athletes' schedules are controlled by their program administrator — this section is completely hidden for them.

| Item | Type | Default | Range |
|------|------|---------|-------|
| **Morning Start** | Time picker | 6:00 AM | 4:30 AM – 10:00 AM |
| **Evening Start** | Time picker | 7:00 PM | 5:00 PM – 9:00 PM |

**Morning Start** is the hard-out time:
- Locks previous day's Evening Review (no more backfill after this time).
- Releases today's Morning Tune-Up.
- Serves as the Weekly Recap submission deadline (Monday hard-out).

**Evening Start** is the evening release time:
- Triggers Morning → Evening state transition on Home.
- Makes Evening Review available.

**Behavior**:
- Time pickers use the device's native time picker (scrollable wheels or equivalent).
- Changes take effect on the **next day boundary** — not immediately. If the athlete changes Morning Start at 3 PM, the new time applies tomorrow morning.
- Helper text below the section: "These times shape your daily rhythm. Most athletes don't need to change them."
- Changes save immediately on selection — no separate save CTA.

**Validation**:
- Morning Start must be earlier than Evening Start (minimum gap enforced — at least 6 hours between them to ensure a meaningful morning window).
- If the athlete selects an invalid combination, the second picker auto-adjusts and a brief inline note explains: "Evening start adjusted to maintain your daily rhythm."

### 5g. Section 5 — About & Support

| Item | Type | Behavior |
|------|------|----------|
| **How It Works** | Navigation (→) | Replays the 3-screen How To walkthrough from onboarding. Same content, same swipeable format. "Done" button on the last screen returns to Settings. |
| **Privacy Policy** | External link (→) | Opens the VirtusFocus privacy policy in the device's default browser. Navigates away from the app. |
| **Terms of Service** | External link (→) | Opens the VirtusFocus terms of service in the device's default browser. Navigates away from the app. |
| **Contact Support** | Email link (→) | Opens the device's default email client with a pre-filled "To" address (support@virtusfocus.com or equivalent). Subject line pre-filled: "VirtusFocus Support Request". Body empty — athlete writes their own message. |
| **App Version** | Static text | Displayed at the bottom of the Settings screen in small, muted text. e.g., "VirtusFocus v1.0.2". Not tappable. |

**How It Works** rules:
- Same 3 screens from onboarding: (1) Daily Rhythm, (2) Tools (Bullseye, Journal), (3) Coach Arron.
- Swipeable with dot indicators. "Skip" link available (same as onboarding).
- "Done" or "Get Started" on the final screen returns to Settings (not Home — the athlete is already onboarded).
- This is the only way to re-access the How To content after onboarding.

### 5h. Section 6 — Account

| Item | Type | Behavior |
|------|------|----------|
| **Delete Account** | Navigation (→) | Opens the Delete Account confirmation flow (see Section 5i). Destructive styling on the list item (red text). |

### 5i. Delete Account — Confirmation Flow

Required for App Store and Play Store compliance. This is a permanent, irreversible action with heavy friction by design.

**Flow**:

```
[Settings → Delete Account]
        │
        ▼
┌──────────────────────────────┐
│  Delete Your Account         │
│                              │
│  This will permanently       │
│  delete:                     │
│  • All coaching messages     │
│  • All journal entries       │
│  • All Bullseye reflections  │
│  • All Weekly Recap data     │
│  • All Evening Review data   │
│  • All Morning Tune-Up       │
│    history                   │
│  • Your coaching relationship│
│    with Coach Arron          │
│                              │
│  This cannot be undone.      │
│  Your data cannot be         │
│  recovered after deletion.   │
│                              │
│  Type DELETE to confirm:     │
│  ┌────────────────────────┐  │
│  │                        │  │
│  └────────────────────────┘  │
│                              │
│  [ Delete My Account ]       │  ← Disabled until "DELETE" typed
│                              │
│  Cancel                      │
└──────────────────────────────┘
```

**Rules**:
- The athlete must type "DELETE" (case-sensitive) in the text field.
- "Delete My Account" button is disabled until the exact string is entered.
- On tap: one final system confirmation dialog ("Are you sure? This is permanent.") with "Delete" (destructive) and "Cancel".
- On confirmation: account deletion is queued server-side. Athlete is signed out and returned to the Sign Up screen. Session token is invalidated.
- **Institutional athletes**: Deletion removes the athlete from the program. The program administrator is notified. Historical aggregate data that has already been anonymized for the Coaching Insight Dashboard may be retained per the privacy policy.
- **D2C athletes**: Full data deletion.
- **Processing time**: Deletion may take up to 30 days to fully propagate (per standard privacy compliance). The account is immediately inaccessible.

---

## 6. Data Model

### 6a. Profile Data (Additions to Existing User Model)

```
UserProfile (extends existing User model) {
  // Identity — editable
  firstName:          String        — editable via Edit Profile
  lastName:           String        — editable via Edit Profile
  email:              String        — editable, triggers re-verification
  avatarUrl:          String | null — photo URL, null = initials fallback
  competitionLevel:   String        — editable via Edit Profile (dropdown)

  // Identity — read-only (from intake/onboarding)
  sport:              String        — locked after onboarding
  position:           String | null — locked after onboarding (null for individual sports)
  programId:          UUID | null   — institutional program association, null for D2C
  programName:        String | null — resolved display name, null for D2C
  environment:        Enum          — INSTITUTIONAL | D2C

  // Metadata
  createdAt:          Timestamp     — account creation (drives tenure display)
  emailVerified:      Boolean       — current verification status
  pendingEmail:       String | null — new email awaiting verification, null when no change pending
}
```

### 6b. Settings Data

```
UserSettings {
  userId:                 UUID

  // Notifications
  pushDailyCoaching:      Boolean     — default true
  pushWeeklyCoaching:     Boolean     — default true
  pushEveningReminder:    Boolean     — default true
  pushMorningReminder:    Boolean     — default true

  // Security
  biometricEnabled:       Boolean     — default false

  // Appearance
  theme:                  Enum        — LIGHT | DARK | SYSTEM — default SYSTEM

  // Schedule (D2C only — ignored for institutional)
  morningStartTime:       Time        — default 06:00, range 04:30–10:00
  eveningStartTime:       Time        — default 19:00, range 17:00–21:00
}
```

### 6c. Deep Dive Archive Data

No new data model required. The archive reads from the existing `Message` model (defined in the Messages/Inbox Design Document, Section 10):
- Filter: `type = WEEKLY_DEEP_DIVE` AND `athleteId = current athlete`
- Sort: `createdAt DESC`
- Read status: Uses existing `deepDiveOpened` flag
- No time boundary — all deep dives returned (unlike the 3-week feed window)

---

## 7. Edge Cases

### 7a. New Athlete — No Deep Dives

Empty state text in archive: "Your weekly deep dives will appear here. Complete your first full week to get started." See Section 3g.

### 7b. Email Change — Verification Expires

If the athlete changes their email and the verification link expires (1 hour):
- Old email is restored as the active email.
- Pending email is cleared.
- No notification to the athlete (they'll see the verification banner persists on Profile until they try again or it naturally clears on next Profile visit).
- The athlete can re-attempt the change via Edit Profile.

### 7c. Email Change — New Email Already in Use

If the athlete enters an email that's already associated with another VirtusFocus account:
- Inline error on the email field: "This email is already associated with an account."
- Save is blocked until a different email is entered.

### 7d. Avatar Upload Failure

If the photo upload fails (network, file too large, unsupported format):
- Inline error below the avatar: "Couldn't upload photo. Try a smaller image or check your connection."
- Previous avatar (or initials) remains unchanged.

### 7e. D2C Athlete — Invalid Schedule Configuration

If the athlete tries to set Morning Start later than Evening Start (or within 6 hours):
- The second picker auto-adjusts to maintain minimum gap.
- Brief inline note: "Evening start adjusted to maintain your daily rhythm."
- No error state — the system prevents invalid configurations proactively.

### 7f. Biometric Enrollment Fails

If the athlete enables biometric unlock but the OS enrollment fails (no biometric data enrolled on device):
- Toggle reverts to Off.
- Inline note: "Set up Face ID (or fingerprint) in your device settings first."

### 7g. Account Deletion — Institutional

When an institutional athlete deletes their account:
- Athlete is removed from the program roster.
- Program administrator receives notification of the departure.
- Any data already aggregated/anonymized for the Coaching Insight Dashboard may be retained per the privacy policy — individual athlete data is deleted.

### 7h. Sign Out — With Unsaved Edit Profile Changes

If the athlete navigates to Edit Profile, makes changes, then somehow reaches Sign Out without saving:
- This path isn't directly possible (Edit Profile has explicit Cancel/Save — Cancel discards, Save persists).
- If the athlete uses the system back gesture to exit Edit Profile without tapping Cancel or Save, treat as Cancel — discard changes.

### 7i. Offline Access

- **Profile screen**: Cached data displays normally. Avatar may show a placeholder if the image isn't cached.
- **Edit Profile**: Save will fail with network error. Changes remain in the form for retry.
- **Deep Dive Archive**: Previously loaded/cached deep dives are viewable. Deep dives never loaded will show loading state.
- **Settings toggles**: Changes are saved locally and synced when connectivity returns.

---

## 8. Accessibility

- **Screen reader**: All sections use semantic heading hierarchy. Action menu items are announced with their labels. Toggles announce their current state ("Daily Coaching, on" / "Daily Coaching, off").
- **Font scaling**: All text respects system font size settings. Profile layout accommodates larger text without truncation or overlap.
- **Color contrast**: All text meets WCAG AA contrast ratios. Muted text (email, tenure line) still meets minimum contrast requirements.
- **Tap targets**: All action menu items, toggles, and buttons have minimum 48px height.
- **Avatar**: Decorative — screen readers announce the athlete's name, not "profile photo."
- **Delete Account**: The destructive nature is communicated through both color (red) and text. Not reliant on color alone.
- **Time pickers**: Use native OS components that support accessibility by default.

---

## 9. Visual Design Notes

- **Profile screen**: Clean, centered layout. No cards wrapping the identity block — text flows directly on the background. Action menu items may use subtle dividers.
- **Deep Dive Archive**: Simple list with generous spacing between items. Month headers have subtle weight/size differentiation.
- **Edit Profile**: Standard form layout with labeled inputs. Consistent with onboarding form styling.
- **Settings**: Grouped sections with uppercase section labels (NOTIFICATIONS, SECURITY, etc.). Standard iOS/Android settings pattern — familiar, not custom.
- **No custom illustrations**: No coaching imagery, no motivational graphics. Clean utility screens.
- **Consistent back navigation**: All sub-screens (Edit Profile, Deep Dive Archive, Settings, Change Password, Delete Account) use a back arrow returning to the parent screen.

---

## 10. Hard Rules & Constraints

1. **No stats on Profile.** No check-in counts, no streaks, no scores, no progress charts. Profile is identity, not a performance dashboard.
2. **No streak language anywhere.** Not on Profile, not in Settings, not in Delete Account copy.
3. **Tenure line is factual only.** "With VirtusFocus since [Month Year]" — no duration counts, no milestone styling changes.
4. **Intake questions are locked.** All 29 questions are permanently locked after onboarding. Not viewable, not editable, not re-takeable from Profile.
5. **Sport, position, and team are locked.** Changes require admin/support intervention. Not self-service.
6. **Competition level is the only intake-derived field that is editable.** It naturally evolves (high school → college).
7. **No coach selection or coaching preferences.** Coach Arron is the coach. There are no alternatives, no preference toggles, no coaching style options.
8. **No sport coach display.** Sport coaches interact through the Coaching Insight Dashboard. Their names do not appear in the athlete app.
9. **Sign out requires confirmation.** One-tap sign out is too easy to trigger accidentally.
10. **Delete Account requires typing "DELETE".** Heavy friction is intentional — this is irreversible.
11. **Email changes require re-verification.** The old email remains active until the new one is confirmed.
12. **D2C schedule changes take effect next day.** Not immediately — prevents mid-day confusion.
13. **Notification toggles control push only.** In-app message delivery is never affected by notification settings.
14. **No data export in v1.** Can be added later if regulations require it.
15. **Settings changes are immediate** (except email and schedule). No global save button — toggles and selectors save on interaction.
16. **Deep Dive Archive has no time boundary.** All deep dives ever generated are accessible (unlike the 3-week Messages feed).

---

## 11. Connection to Other Screens

### 11a. Home — Daily Hub (Upstream)

| Aspect | Detail |
|--------|--------|
| **Profile access** | Top-right icon on Home navigates to Profile. Only entry point. |
| **Schedule dependency** | D2C schedule settings (Morning Start, Evening Start) directly control Home's state transitions. |

### 11b. Messages / Inbox

| Aspect | Detail |
|--------|--------|
| **Deep dive archive** | Deep dives older than the 3-week feed window are accessible only through Profile → Deep Dive Archive. |
| **Shared reader** | Deep Dive Archive uses the same full-screen reader component as Messages/Inbox. |
| **Shared data** | Archive reads from the same Message data model. `deepDiveOpened` flag is shared — opening a deep dive in the archive marks it as read in the feed (and vice versa). |
| **Notification settings** | Settings notification toggles control push delivery for Daily Coaching and Weekly Coaching messages. |

### 11c. Auth Flow

| Aspect | Detail |
|--------|--------|
| **Sign out** | Profile → Sign Out navigates to the Login screen. |
| **Delete account** | Settings → Delete Account navigates to the Sign Up screen after deletion. |
| **Email change** | Edit Profile email change triggers the same verification flow as onboarding (same email template, same expiry). |
| **Password change** | Settings → Change Password is self-contained (no connection to Password Recovery flow — that's for forgotten passwords from the Login screen). |

### 11d. Onboarding

| Aspect | Detail |
|--------|--------|
| **Intake data** | Profile displays sport, position, competition level from intake. Intake questions themselves are locked. |
| **Program code** | Profile displays the program name resolved from the code entered during onboarding. |
| **How It Works** | Settings replays the same 3-screen walkthrough from onboarding. |
| **Avatar** | Not collected during onboarding — athlete adds it via Edit Profile. |

### 11e. Weekly Recap

| Aspect | Detail |
|--------|--------|
| **Season Context** | Weekly Recap asks season context every week. This is NOT duplicated in Profile/Settings. Season context is a coaching data point, not a profile attribute. |

### 11f. Evening Review / Morning Tune-Up

| Aspect | Detail |
|--------|--------|
| **Schedule (D2C)** | Settings Schedule section controls the hard-out and evening release times that govern Morning Tune-Up availability and Evening Review timing windows. |

---

## 12. Screen Summary

| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| **Profile** | Identity display + navigation hub | Avatar, name, tenure, email, sport/position/level, program (institutional), action menu |
| **Deep Dive Archive** | Long-term access to weekly deep dives | Reverse-chronological list, month section headers, month picker, full-screen reader |
| **Edit Profile** | Update identity fields | Avatar, first name, last name, email (re-verification), competition level. Explicit Save. |
| **Settings** | Preference management | 6 sections: Notifications (4 toggles), Security (password + biometric), Appearance (theme), Schedule (D2C only — morning/evening times), About & Support (How It Works, legal links, contact, version), Account (delete) |

| Aspect | Detail |
|--------|--------|
| **Entry point** | Home top-right icon → Profile |
| **Environment differences** | Institutional: shows program name. D2C: no program block, has Schedule section in Settings. |
| **Editable fields** | Avatar, first name, last name, email, competition level |
| **Locked fields** | Sport, position, team/program, all 29 intake questions |
| **Stats displayed** | None |
| **Streaks displayed** | None |
| **Coach selection** | None — Coach Arron is the coach |
| **Data export** | Not in v1 |
| **Account deletion** | Yes — heavy friction confirmation, required for app store compliance |
