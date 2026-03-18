# VirtusFocus — App Development Technical Handoff

**Version:** 1.0
**Date:** 2026-03-18
**Audience:** App development team (backend + frontend)
**Purpose:** Everything the development team needs to build the VirtusFocus app backend and rendering layer. This document is self-contained — implement from this document alone.

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Intake Form & Onboarding](#2-intake-form--onboarding)
3. [PPD Scoring (Backend Computation)](#3-ppd-scoring-backend-computation)
4. [ABI Scoring (Backend Computation)](#4-abi-scoring-backend-computation)
5. [Daily Data Collection & Mini-JSON](#5-daily-data-collection--mini-json)
6. [Weekly Data Assembly](#6-weekly-data-assembly)
7. [Execution Signal Computation (Backend)](#7-execution-signal-computation-backend)
8. [Daily Coach Signal — Stage 7 (Backend)](#8-daily-coach-signal--stage-7-backend)
9. [AI Pipeline Interface](#9-ai-pipeline-interface)
10. [Dashboard Rendering](#10-dashboard-rendering)
11. [Data Storage & Retention](#11-data-storage--retention)
12. [Compliance Requirements for Backend](#12-compliance-requirements-for-backend)
13. [Core Foundation Compatibility](#13-core-foundation-compatibility)
14. [Product Tier Activation Matrix](#14-product-tier-activation-matrix)

---

## 1. System Architecture Overview

### 1.1 Data Flow

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────┐
│  App UI  │────▶│ Backend  │────▶│ AI Pipeline  │────▶│ Backend  │────▶│  App UI  │
│(Athlete) │     │(Your Code)│     │(Claude Agents)│     │(Storage) │     │(Delivery)│
└──────────┘     └──────────┘     └──────────────┘     └──────────┘     └──────────┘
```

**What the backend owns:**
- Intake form collection and storage
- PPD scoring (deterministic formula — Section 3)
- ABI scoring (deterministic formula — Section 4)
- Daily event data collection and storage
- Daily Mini-JSON assembly (deterministic extraction — Section 5)
- Weekly Input Object assembly (Section 6)
- Execution signal composite scores (7 formulas — Section 7)
- Coach flags evaluation (15 threshold checks — Section 7)
- Self-ratings alignment classification (Section 7)
- Daily Coach Signal / Stage 7 (full deterministic rules engine — Section 8)
- All data storage and retrieval
- Dashboard rendering (presentation layer — Section 10)
- Scheduling and orchestration of AI pipeline calls

**What the AI pipeline owns:**
- Athlete Snapshot generation (Stage 1 — one-time narrative from intake data)
- Weekly Interpretation JSON (Stage 2 — classifies all weekly signals)
- Coaching Message + Deep Dive + Parent Coaching Message (Stage 3 — narrative coaching output)
- Coach Insights + Parent Insights + Team Snapshot (Stage 4 — institutional dashboards)
- Editorial Audit (Stage 5 — quality gate, internal only)
- Daily Coaching Snippet (Stage 6 — 2-3 sentence daily coaching moment)

### 1.2 Product Tiers

| Tier | Monthly Cost/Athlete | Description |
|------|---------------------|-------------|
| **D2C Base** | ~$0.24 | Daily snippets only (7/week). No weekly pipeline. Standalone. |
| **D2C Premium** | ~$2.64 | Weekly pipeline (Stages 2→3→5) + daily snippets (6/week, Tue-Sun). |
| **D2C Premium + Parent** | ~$2.92 | Premium + parent-facing outputs (Parent CM, Parent Insight, Parent Dashboard). |
| **Institutional** | ~$3.12 | All stages active. Coach dashboards, team snapshots, daily signals for coaches. |

### 1.3 AI Model Assignments

| Stage | Model | Type | Cost Driver |
|-------|-------|------|-------------|
| Stage 1: Athlete Snapshot | Opus | AI (one-time) | Minimal (runs once per athlete) |
| Stage 2: Interpretation Engine | Opus | AI (weekly) | Primary weekly cost |
| Stage 3: Coaching Output | Opus | AI (weekly) | Primary weekly cost |
| Stage 4: Coach Insights | Opus | AI (weekly) | Institutional only |
| Stage 5: Editorial Audit | Opus | AI (weekly) | Internal QA |
| Stage 6: Daily Snippets | Sonnet | AI (daily) | ~10% of total with caching |
| Stage 7: Daily Coach Signal | **None** | **Deterministic** | **Zero AI cost** — backend computes |

### 1.4 Boundary Diagram

```
BACKEND (Your Code)                    │  AI PIPELINE (Claude)
───────────────────────────────────────│────────────────────────────────
Collect intake form responses          │  Generate Athlete Snapshot (Stage 1)
Compute PPD scores (Layers 1,2,4)      │  Classify PPD tie-breaker (Layer 3)
Compute ABI scores                     │  Generate Interpretation JSON (Stage 2)
Collect daily app events               │  Generate Coaching Message (Stage 3)
Assemble Daily Mini-JSON               │  Generate Deep Dive (Stage 3)
Assemble Weekly Input Object           │  Generate Parent CM (Stage 3)
Compute 7 composite scores             │  Generate Coach Insight (Stage 4)
Evaluate 15 coach flags                │  Generate Parent Insight (Stage 4)
Compute self-ratings alignment         │  Generate Team Snapshot (Stage 4)
Compute Daily Coach Signal (Stage 7)   │  Run Editorial Audit (Stage 5)
Render all dashboards                  │  Generate Daily Snippet (Stage 6)
Schedule all pipeline invocations      │
Store all inputs and outputs           │
```

---

## 2. Intake Form & Onboarding

### 2.1 Form Structure

29 questions across 7 sections. Estimated completion: 5-6 minutes.

### 2.2 Complete Question List

#### Section 1: Performance Context (Q1-Q6)

| # | Question | Format | Options/Validation | Routes To |
|---|----------|--------|--------------------|-----------|
| Q1 | What is your primary sport? | Free text | Required | Snapshot |
| Q2 | What is your position or event? (if applicable) | Free text | Required | Snapshot |
| Q3 | What is your current team or club? (if applicable) | Free text | Required | Snapshot |
| Q4 | What is your current competitive level? | Single select | Youth, Middle School, High School, College, Professional | Snapshot, Pipeline (competitive_level calibration) |
| Q5 | How many years have you been competing? | Single select | Less than 1, 1-2, 3-5, 6-8, 9+ | Snapshot |
| Q6 | What is your current season phase? | Single select | Preseason, In-season, Offseason, Returning from injury | Snapshot (baseline_season_phase), Longitudinal |

#### Section 2: Self-Assessment Scales (Q7-Q14) — ABI Input

All questions use a 1-5 scale with question-specific anchors.

| # | Question | Anchors | Pillar | ABI Role |
|---|----------|---------|--------|----------|
| Q7 | How much of your development do you currently drive yourself? | 1 = Others drive most of it / 5 = I drive almost all of it | Ownership | Q_a |
| Q8 | How often do you review your own performance after practices or games? | 1 = Never / 5 = Every time | Ownership | Q_b |
| Q9 | After a mistake, how quickly do you mentally reset? | 1 = It sticks with me for a while / 5 = I reset almost immediately | Composure | Q_a (also PPD amplifier for Mistake Recovery Lag) |
| Q10 | How well do you keep your composure during big moments? | 1 = I struggle a lot / 5 = I stay very composed | Composure | Q_b |
| Q11 | During performance, how well do you maintain your focus? | 1 = I lose focus very often / 5 = I rarely lose focus | Focus | Q_a |
| Q12 | How much do outside distractions (phone, social media, life stress) affect your training? | 1 = They affect me a lot / 5 = They rarely affect me | Focus | Q_b |
| Q13 | How consistent is your pre-performance mental routine? | 1 = I don't have one / 5 = Very consistent | Structure | Q_a (also PPD amplifier for Structure Gap) |
| Q14 | How consistent is your weekly training and recovery rhythm? | 1 = Very inconsistent / 5 = Very consistent | Structure | Q_b |

#### Section 3: Performance Friction (Q15-Q16) — PPD Input

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q15 | What usually gets in the way of your best performance? | Multi-select (1-3) | Overthinking, Confidence going up and down, Hard time letting go of mistakes, Losing focus or getting distracted, Pressure in big moments, Staying motivated or disciplined, Lack of routine or structure, Pressure from coaches or parents | PPD (selection weight +3 per bucket), Snapshot |
| Q16 | What situation makes this worse? | Multi-select (1-2) | Big competitions or high-stakes moments, After making a mistake, When being evaluated (coach, scouts, recruiters), During busy or stressful life weeks, When expectations from others are high | PPD (trigger amplifier), Snapshot |

**Q15 Validation:** Minimum 1, maximum 3 selections. No "Other" option (breaks deterministic PPD scoring).

**Q16 Validation:** Minimum 1, maximum 2 selections.

#### Section 4: Identity & Pressure (Q17-Q19)

| # | Question | Format | Validation | Routes To |
|---|----------|--------|------------|-----------|
| Q17 | At my best, I compete like someone who... | Free text (sentence completion) | Required | Snapshot (identity claim anchor) |
| Q18 | Before a big moment, what thought shows up most often? | Free text (short answer) | Required | PPD (tie-breaker classification), Snapshot |
| Q19 | What kind of competitor do you want to become? | Free text (short answer) | Required | Snapshot (competitor aspiration), Longitudinal |

#### Section 5: Behavioral Patterns (Q20-Q21)

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q20 | When something goes wrong in competition, what do you usually do first? | Single select | Blame the situation, Get frustrated, Try to adjust right away, Reset and refocus | Snapshot (adversity_response_pattern), Pipeline |
| Q21 | After a bad performance, how do you usually describe yourself? | Single select | I question my ability, I get frustrated but move forward, I analyze what happened and adjust, I stay confident in myself | Snapshot (adversity_self_description) |

#### Section 6: Ecosystem (Q22-Q25)

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q22 | How involved are your parents/guardians in your performance journey? | Single select | Very involved, Somewhat involved, Not very involved, Prefer not to say | Snapshot (Ecosystem), Parent Output calibration |
| Q23 | After games or competitions, conversations at home are usually: | Single select | Mostly supportive, A lot of analysis or advice, Pressure to perform, We don't discuss performance much | PPD (ecosystem amplifier), Snapshot (Ecosystem), Parent CM calibration |
| Q24 | Would you like to include your parents/guardians in your mindset coaching? | Yes/No + conditional email | If Yes: email field (validated email format) | Parent Output (gating), Snapshot (parent_inclusion) |
| Q25 | When you struggle, who do you usually talk to first? | Single select | No one, A teammate, My coach, A parent, A mentor | Snapshot (Ecosystem), Parent CM calibration |

#### Section 7: Goals & Commitment (Q26-Q29)

| # | Question | Format | Validation | Routes To |
|---|----------|--------|------------|-----------|
| Q26 | What does success look like for you in the next 6 months? | Free text | Required | Snapshot |
| Q27 | On a scale of 1-10, how would you rate your current mental game? | Scale 1-10 | Required, integer | Snapshot (mental_game_self_rating), Longitudinal |
| Q28 | How committed are you to working on your mental game? | Single select | Just curious, Pretty serious, All-in — let's go | Snapshot (commitment_level) |
| Q29 | Is there anything else you'd like us to know about you, your goals, or your challenges? | Free text | Optional | Snapshot |

### 2.3 Dual-Mode Detection

The system supports two intake paths. Detection is automatic based on 3 structural signals:

| Signal | App Intake | Core Foundation Intake |
|--------|-----------|----------------------|
| Q7-Q14 present as integers (1-5) | Yes | No (free-text answers or missing) |
| Q15 present as multi-select from 8 options | Yes | No (different question format) |
| Q16 present as multi-select from 5 options | Yes | No (different question format) |

**Rule:** If all 3 signals present → `input_source = "app"`. Otherwise → `input_source = "core_foundation"`. Ambiguous defaults to Core Foundation.

### 2.4 Multi-System Routing Summary

Each question feeds one or more downstream systems:

| System | Input Questions |
|--------|----------------|
| **Athlete Snapshot** (narrative) | All except Q24 (28 of 29 questions) |
| **PPD Scoring** (deterministic) | Q15, Q16, Q18, Q9, Q13, Q23 |
| **ABI Scoring** (deterministic) | Q7-Q14 |
| **Ecosystem Profile** | Q22-Q25 |
| **Longitudinal Baselines** | Q6, Q9, Q19, Q27 |

---

## 3. PPD Scoring (Backend Computation)

The Primary Problem Detector (PPD) identifies an athlete's top 3 mental performance friction areas from 8 possible buckets. **Layers 1, 2, and 4 are fully deterministic — the backend computes these.** Layer 3 requires AI agent classification of free-text input.

### 3.1 The 8 PPD Buckets

| # | Bucket Name | Key: `ppd_all_scores` | Description |
|---|-------------|----------------------|-------------|
| 1 | Overthinking Loop | `overthinking_loop` | Rumination cycles before/during performance |
| 2 | Confidence Volatility | `confidence_volatility` | Confidence swings based on outcomes |
| 3 | Mistake Recovery Lag | `mistake_recovery_lag` | Slow reset after errors |
| 4 | Focus Drift / Distraction | `focus_drift` | Losing focus on controllables |
| 5 | Pressure Reactivity | `pressure_reactivity` | Performance disruption under pressure |
| 6 | Discipline Gap | `discipline_gap` | Motivation/consistency erosion |
| 7 | Structure Gap | `structure_gap` | Lack of routine or organization |
| 8 | Ecosystem Friction | `ecosystem_friction` | External pressure from coaches/parents |

### 3.2 Layer 1: Selection Weight [BACKEND]

Each Q15 friction selection adds **+3** to the matching bucket.

| Q15 Option | Target Bucket | Points |
|------------|--------------|--------|
| Overthinking | Overthinking Loop | +3 |
| Confidence going up and down | Confidence Volatility | +3 |
| Hard time letting go of mistakes | Mistake Recovery Lag | +3 |
| Losing focus or getting distracted | Focus Drift / Distraction | +3 |
| Pressure in big moments | Pressure Reactivity | +3 |
| Staying motivated or disciplined | Discipline Gap | +3 |
| Lack of routine or structure | Structure Gap | +3 |
| Pressure from coaches or parents | Ecosystem Friction | +3 |

Athlete selects 1-3 options. Only selected buckets receive +3. Unselected buckets start at 0.

### 3.3 Layer 2: Amplifiers [BACKEND]

Four questions act as amplifiers, adding points to specific buckets.

#### 2A. Reset Speed Amplifier (Q9 → Mistake Recovery Lag)

| Q9 Value | Points Added to MRL |
|----------|-------------------|
| 5 (reset almost immediately) | +0 |
| 4 | +1 |
| 3 | +1 |
| 2 | +2 |
| 1 (cannot reset) | +3 |

#### 2B. Routine Amplifier (Q13 → Structure Gap)

| Q13 Value | Points Added to SG |
|-----------|-------------------|
| 5 (strong routine) | +0 |
| 4 | +0 |
| 3 | +1 |
| 2 | +2 |
| 1 (no routine) | +3 |

#### 2C. Trigger Amplifier (Q16 → Multiple Buckets)

Each Q16 selection adds a **primary** (+2) and **secondary** (+1) amplifier:

| Q16 Option | Primary (+2) | Secondary (+1) |
|------------|-------------|----------------|
| Big competitions or high-stakes moments | Pressure Reactivity | Overthinking Loop |
| After making a mistake | Mistake Recovery Lag | Confidence Volatility |
| When being evaluated (coach, scouts, recruiters) | Overthinking Loop | Confidence Volatility |
| During busy or stressful life weeks | Discipline Gap | Focus Drift / Distraction |
| When expectations from others are high | Pressure Reactivity | Confidence Volatility |

Athlete selects 0-2 options. If 0 selected, no amplification occurs. Both primary and secondary apply per selection.

#### 2D. Ecosystem Amplifier (Q23 → Ecosystem Friction)

| Q23 Option | Points Added to EF |
|------------|-------------------|
| Mostly supportive | +0 |
| A lot of analysis or advice | +2 |
| Pressure to perform | +3 |
| We don't discuss performance much | +1 |

### 3.4 Layer 3: Tie-Breaker Classification [AI PIPELINE]

The AI agent classifies Q18 (pressure thought free-text) into one of 4 categories. **The backend stores the result but does not compute it.** This classification is returned as part of the Athlete Snapshot.

| Classification | Pattern | Adjustment |
|---------------|---------|------------|
| Avoidance | "Don't mess up," withdrawal language | +1 Overthinking Loop, +1 Pressure Reactivity |
| Proving | "Show them," validation-seeking | +1 Confidence Volatility |
| Obligation | "Can't let them down," duty language | +1 Pressure Reactivity, +1 Ecosystem Friction |
| Approach | "Execute my plan," process-focused | No adjustment (positive indicator) |

**Dual classification rules:**
- Max 2 categories per pressure thought. If 3+ categories detected, classify the 2 most dominant framings only.
- Valid dual combinations: Avoidance+Proving, Avoidance+Obligation, Proving+Obligation
- **Approach combinations are invalid** — Approach framing is definitionally incompatible with Avoidance/Proving/Obligation. If text contains both approach and non-approach elements, classify the non-approach framing(s) only.
- When dual: all adjustments from both categories apply (e.g., Avoidance+Obligation = +1 OL, +1 PR, +1 PR, +1 EF = +1 OL, +2 PR, +1 EF)

### 3.5 Layer 4: Final Ranking [BACKEND]

1. Sum all points per bucket (Layer 1 + Layer 2 + Layer 3)
2. Sort 8 buckets descending by total score
3. Take top 3

**Tie-breaking priority** (when scores are equal, higher priority wins):

| Priority | Bucket |
|----------|--------|
| 1 (highest) | Overthinking Loop |
| 2 | Confidence Volatility |
| 3 | Mistake Recovery Lag |
| 4 | Focus Drift / Distraction |
| 5 | Pressure Reactivity |
| 6 | Discipline Gap |
| 7 | Structure Gap |
| 8 (lowest) | Ecosystem Friction |

### 3.6 Output Schema

```json
{
  "ppd_primary_problem": "string (bucket name of rank 1)",
  "ppd_tie_breaker_classification": "Avoidance | Proving | Obligation | Approach | Avoidance+Proving | Avoidance+Obligation | Proving+Obligation | Unclassified",
  "ppd_top_3": [
    {
      "rank": 1,
      "bucket": "string (bucket name)",
      "score": "integer (total after all 4 layers)",
      "trigger_context": "string | array | null",
      "coaching_implication": "string (static per bucket — see table below)"
    },
    { "rank": 2, "...": "..." },
    { "rank": 3, "...": "..." }
  ],
  "ppd_all_scores": {
    "overthinking_loop": "integer",
    "confidence_volatility": "integer",
    "mistake_recovery_lag": "integer",
    "focus_drift": "integer",
    "pressure_reactivity": "integer",
    "discipline_gap": "integer",
    "structure_gap": "integer",
    "ecosystem_friction": "integer"
  }
}
```

**Static coaching implications per bucket** (assigned by rank position, not computed):

| Bucket | coaching_implication |
|--------|---------------------|
| Overthinking Loop | Controllable-focus cues + single Bullseye target under pressure |
| Confidence Volatility | Preparation-based confidence anchoring + evidence collection |
| Mistake Recovery Lag | Reset reps + next-play language |
| Focus Drift / Distraction | Focus cue routines + distraction boundaries |
| Pressure Reactivity | Controllable-focus under pressure + approach-framed self-talk |
| Discipline Gap | Win the Day minimums + habit stacking |
| Structure Gap | Build pre-performance routine + daily rhythm anchors |
| Ecosystem Friction | Communication boundaries + support system clarification |

### 3.7 Theoretical Maximum Scores Per Bucket

| Bucket | Max Score | How |
|--------|----------|-----|
| Pressure Reactivity | 9 | Selection(3) + two trigger primaries(2+2) + dual tie-breaker(1+1) |
| Mistake Recovery Lag | 8 | Selection(3) + Q9=1(3) + trigger primary(2) |
| Overthinking Loop | 7 | Selection(3) + trigger primary(2) + trigger secondary(1) + tie-breaker(1) |
| Ecosystem Friction | 7 | Selection(3) + Q23 pressure(3) + tie-breaker(1) |
| Confidence Volatility | 6 | Selection(3) + trigger secondary(1+1) + tie-breaker(1) |
| Structure Gap | 6 | Selection(3) + Q13=1(3) |
| Discipline Gap | 5 | Selection(3) + trigger primary(2) |
| Focus Drift | 4 | Selection(3) + trigger secondary(1) |

### 3.8 Edge Cases

1. **Minimum 1 selection** for Q15 — app form validation enforces 1-3 constraint.
2. **Multi-way tie for Top 3** — when 4+ buckets tie for positions within the Top 3, the deterministic bucket priority order (1-8) resolves all ties. No ties are left unresolved.
3. **Contradictory answers** (e.g., Q9=5 "resets quickly" but selects "Hard time letting go of mistakes"): Score as-is. Snapshot Builder may note the contradiction narratively.
4. **Layer 3 unclassifiable** (pressure thought empty, illegible, or too vague): `ppd_tie_breaker_classification = "Unclassified"`, no Layer 3 adjustments applied.
5. **Zero trigger selections (Q16)** — Q16 allows "up to 2" selections. If 0 selected, Layer 2C produces no adjustments. Valid state.
6. **Approach-framed pressure thought** — If Q18 classified as Approach, no tie-breaker adjustments are made. Layer 3 is skipped. Ties resolved by bucket priority order only.
7. **Maximum scoring scenario** — PR can reach 9: Selection(3) + two trigger primaries(2+2) + dual tie-breaker(1+1).

### 3.9 Worked Example: Grace Kindel

**Inputs:**
- Q9 = 3 (moderate reset), Q13 = 3 (somewhat consistent routine)
- Q15 selections: "Confidence going up and down", "Hard time letting go of mistakes", "Pressure in big moments" (3 selections)
- Q16 selections: "After making a mistake", "Big competitions or high-stakes moments"
- Q18: "I need to make sure I succeed and if I don't I will let myself and the team down" → classified as **Obligation**
- Q23: "Mostly supportive"

**Layer 1 (Selection Weight):**
- Confidence Volatility: +3
- Mistake Recovery Lag: +3
- Pressure Reactivity: +3

**Layer 2 (Amplifiers):**
- Q9=3 → MRL +1
- Q13=3 → SG +1
- Q16 "After making a mistake" → MRL +2, CV +1
- Q16 "Big competitions or high-stakes moments" → PR +2, OL +1
- Q23 "Mostly supportive" → EF +0

**Layer 3 (Tie-breaker = Obligation):**
- PR +1, EF +1

**Final Scores:**

| Bucket | L1 | L2 | L3 | Total |
|--------|----|----|----|----- |
| Overthinking Loop | 0 | 1 | 0 | **1** |
| Confidence Volatility | 3 | 1 | 0 | **4** |
| Mistake Recovery Lag | 3 | 1+2=3 | 0 | **6** |
| Focus Drift / Distraction | 0 | 0 | 0 | **0** |
| Pressure Reactivity | 3 | 2 | 1 | **6** |
| Discipline Gap | 0 | 0 | 0 | **0** |
| Structure Gap | 0 | 1 | 0 | **1** |
| Ecosystem Friction | 0 | 0 | 1 | **1** |

**Top 3** (tie at 6 broken by bucket priority: MRL #3 > PR #5):

**Result:** ppd_top_3 = [MRL(6), PR(6), CV(4)], ppd_primary_problem = "Mistake Recovery Lag", ppd_tie_breaker_classification = "Obligation"

---

## 4. ABI Scoring (Backend Computation)

The Athlete Baseline Index (ABI) produces 4 pillar scores measuring self-assessed mental performance baseline. **Entirely deterministic — the backend computes everything.**

### 4.1 Pillar Definitions and Input Mapping

| Pillar | Measures | Q_a | Q_b |
|--------|----------|-----|-----|
| **Ownership** | Self-directed development, locus of control | Q7 | Q8 |
| **Composure** | Emotional regulation, pressure resilience | Q9 | Q10 |
| **Focus** | Sustained attention, distraction resistance | Q11 | Q12 |
| **Structure** | Routine consistency, training rhythm | Q13 | Q14 |

### 4.2 Formula

```
pillar_score = round((Q_a + Q_b) / 2 * 2)
```

Where Q_a and Q_b are each integers 1-5.

**Range:** 2-10 per pillar (never 0, never 1, never 11). **Total ABI:** 8-40.

### 4.3 All 25 Valid Input Combinations

Every (Q_a, Q_b) pair produces a clean integer:

| Q_a | Q_b | (Q_a+Q_b)/2 | × 2 | round() | Result |
|-----|-----|-------------|-----|---------|--------|
| 1 | 1 | 1.0 | 2.0 | 2.0 | **2** |
| 1 | 2 | 1.5 | 3.0 | 3.0 | **3** |
| 1 | 3 | 2.0 | 4.0 | 4.0 | **4** |
| 1 | 4 | 2.5 | 5.0 | 5.0 | **5** |
| 1 | 5 | 3.0 | 6.0 | 6.0 | **6** |
| 2 | 2 | 2.0 | 4.0 | 4.0 | **4** |
| 2 | 3 | 2.5 | 5.0 | 5.0 | **5** |
| 2 | 4 | 3.0 | 6.0 | 6.0 | **6** |
| 2 | 5 | 3.5 | 7.0 | 7.0 | **7** |
| 3 | 3 | 3.0 | 6.0 | 6.0 | **6** |
| 3 | 4 | 3.5 | 7.0 | 7.0 | **7** |
| 3 | 5 | 4.0 | 8.0 | 8.0 | **8** |
| 4 | 4 | 4.0 | 8.0 | 8.0 | **8** |
| 4 | 5 | 4.5 | 9.0 | 9.0 | **9** |
| 5 | 5 | 5.0 | 10.0 | 10.0 | **10** |

Note: The table shows unique pairs. (Q_a=2, Q_b=1) produces the same result as (Q_a=1, Q_b=2).

### 4.4 Band Thresholds

**Total ABI Bands:**

| Range | Band |
|-------|------|
| 8-16 | Needs Foundation |
| 17-28 | Developing |
| 29-36 | Consistent |
| 37-40 | Leadership |

**Individual Pillar Bands:**

| Range | Band |
|-------|------|
| 2-4 | Low |
| 5-7 | Moderate |
| 8-10 | High |

### 4.5 Primary Emphasis Determination

Identifies the 1-2 pillars that need the most coaching attention.

**Algorithm:**
1. Rank all 4 pillars by score ascending (lowest first)
2. Lowest pillar = Emphasis #1 (always)
3. If 2nd-lowest is within 2 points of lowest → Emphasis #2
4. Maximum 2 emphases (never 3 or 4)
5. If all 4 pillars are equal → `primary_emphasis = ["Balanced"]`
6. Ties broken by pillar priority: Ownership > Composure > Focus > Structure

**Examples:**
- Scores: Own=6, Com=5, Foc=8, Str=7 → Lowest=Com(5), 2nd=Own(6), gap=1 ≤ 2 → `["Composure", "Ownership"]`
- Scores: Own=4, Com=8, Foc=7, Str=9 → Lowest=Own(4), 2nd=Foc(7), gap=3 > 2 → `["Ownership"]`
- Scores: Own=6, Com=6, Foc=6, Str=6 → All equal → `["Balanced"]`

### 4.6 Output Schema

```json
{
  "abi_scores": {
    "ownership": "integer 2-10",
    "composure": "integer 2-10",
    "focus": "integer 2-10",
    "structure": "integer 2-10",
    "total": "integer 8-40",
    "band": "Needs Foundation | Developing | Consistent | Leadership",
    "primary_emphasis": ["array of 1-2 pillar names OR [\"Balanced\"]"],
    "pillar_bands": {
      "ownership": "Low | Moderate | High",
      "composure": "Low | Moderate | High",
      "focus": "Low | Moderate | High",
      "structure": "Low | Moderate | High"
    }
  },
  "abi_raw_inputs": {
    "ownership_q1": "integer 1-5 (Q7)",
    "ownership_q2": "integer 1-5 (Q8)",
    "composure_q1": "integer 1-5 (Q9)",
    "composure_q2": "integer 1-5 (Q10)",
    "focus_q1": "integer 1-5 (Q11)",
    "focus_q2": "integer 1-5 (Q12)",
    "structure_q1": "integer 1-5 (Q13)",
    "structure_q2": "integer 1-5 (Q14)"
  }
}
```

### 4.7 Worked Example: Grace Kindel

**Inputs:** Q7=3, Q8=3, Q9=3, Q10=2, Q11=4, Q12=4, Q13=3, Q14=4

| Pillar | Q_a | Q_b | Calculation | Score | Band |
|--------|-----|-----|-------------|-------|------|
| Ownership | 3 | 3 | round(3.0×2) | **6** | Moderate |
| Composure | 3 | 2 | round(2.5×2) | **5** | Moderate |
| Focus | 4 | 4 | round(4.0×2) | **8** | High |
| Structure | 3 | 4 | round(3.5×2) | **7** | Moderate |

**Total:** 6+5+8+7 = **26** → Band: **Developing**

**Primary Emphasis:** Lowest=Composure(5), 2nd=Ownership(6), gap=1 ≤ 2 → `["Composure", "Ownership"]`

---

## 5. Daily Data Collection & Mini-JSON

### 5.1 What the App Collects Daily

Each day, the athlete interacts with two components:

**Morning Tune-Up** (before training/school):
- Focus word (system-assigned daily mental filter, e.g., "Compete", "Clarity", "Stalwart")
- 3 Quick Win items (system-generated micro-agreements — all 3 must be acknowledged to complete)
- Mindset Challenge acceptance (checkbox — V1 is mandatory to complete Tune-Up)
- Mindset Challenge text (system-generated challenge presented to athlete)
- Timestamp

**Evening Review** (end of day):
- Win the Day: 5 yes/no questions (WTD)
- Journaling: 3 domain entries (school/work, sport, home life)
- Bullseye Method: 3 rings with item arrays (center, influence, outer)
- Mindset Challenge follow-through (did they execute the challenge?)
- Component sequence (order they completed the components)
- Timestamp

### 5.2 Morning Tune-Up Event Schema

```json
{
  "completed": "boolean",
  "completion_timestamp": "ISO-8601 datetime or null",
  "trigger_method": "self_initiated | reminder | null",
  "mindset_challenge_accepted": "boolean or null",
  "mindset_challenge_text": "string or null",
  "focus_word": "string or null",
  "quick_win_items": ["string array (3 items) or null"]
}
```

**V1 Rule:** The Mindset Challenge checkbox and all 3 Quick Wins are REQUIRED to complete the Tune-Up. Therefore:
- When `completed = true` → `mindset_challenge_accepted = true`
- When `completed = false` (Tune-Up skipped) → `mindset_challenge_accepted = null`
- `mindset_challenge_accepted` is retained for future-proofing when V2 makes acceptance optional

**Morning Timing:**
- **On-time:** completed before 12:00 PM (noon) local time
- **Late:** completed at or after 12:00 PM local time

### 5.3 Evening Review Event Schema

```json
{
  "submitted": "boolean",
  "completion_timestamp": "ISO-8601 datetime or null",
  "trigger_method": "self_initiated | reminder | null",
  "wtd": {
    "completed": "boolean",
    "q1_intention": "boolean or null",
    "q2_challenge": "boolean or null",
    "q3_adversity": "boolean or null",
    "q4_progress": "boolean or null",
    "q5_gratitude": "boolean or null"
  },
  "journaling": {
    "completed": "boolean",
    "school_work_entry": "string or null",
    "sport_entry": "string or null",
    "home_life_entry": "string or null"
  },
  "bullseye": {
    "completed": "boolean",
    "center_ring_items": ["string array or null"],
    "influence_ring_items": ["string array or null"],
    "outer_ring_items": ["string array or null"]
  },
  "mindset_challenge_completed": "boolean or null",
  "component_sequence": ["array of component names or null"]
}
```

**Bullseye items as arrays** (not comma-separated text) — required for deterministic counting in execution signal computation.

**Component sequence** records the order the athlete completed components: e.g., `["wtd", "journaling", "bullseye"]` (designed order) or `["bullseye", "wtd", "journaling"]` (athlete chose different order).

### 5.4 Evening Timing: 4-Category Model

| Category | Window | Behavioral Meaning |
|----------|--------|-------------------|
| **On-time** | Before 10:00 PM local | Evening routine engagement |
| **Late** | 10:00 PM to backfill boundary | Same-night, after intended window |
| **Backfill** | 2 hours before hard-out to hard-out | Next-morning retroactive catch-up |
| **Missed** | After hard-out | Locked out — genuine disengagement |

**Hard-out time:** Default 6:00 AM local time (configurable per program).
**Backfill boundary:** Hard-out minus 2 hours (fixed constant, not configurable).

**Default windows (6:00 AM hard-out):**
```
On-time:   before 10:00 PM
Late:      10:00 PM to 4:00 AM
Backfill:  4:00 AM to 6:00 AM
Missed:    after 6:00 AM (locked out — no submission accepted)
```

**Hard-out lockout rule:** After hard-out time, the evening review for that day is permanently locked. Backend must enforce this — no late submissions after hard-out. Partial data is preserved if the athlete started but did not submit before lockout (`submitted = false` but component data may be partially populated).

### 5.5 WTD Daily Categories

| Daily Score (sum of 5 yes/no) | Category | Label |
|-------------------------------|----------|-------|
| 4-5 | Win the Day | Aligned + intentional |
| 2-3 | Partial Win | Inconsistent but effort shown |
| 0-1 | Missed the Mark | Reactive / disconnected |

**Note:** "Partial Win" replaces the previous "Neutral" terminology. Use "Partial Win" in all contexts.

**Weekly Tiers** (sum of 7 daily scores, range 0-35):

| Weekly Score | Tier |
|-------------|------|
| 28-35 | Growth Week |
| 14-27 | Mixed Week |
| 0-13 | Reset Week |

### 5.6 Daily Mini-JSON Schema

The Daily Mini-JSON is a structured intermediate assembled by the backend from raw daily events. **This is what Stage 6 (Daily Coaching Engine) and Stage 7 (Daily Coach Signal) consume.** The backend produces this deterministically — no AI involved.

```json
{
  "meta": {
    "athlete_id": "string",
    "athlete_name": "string",
    "date": "YYYY-MM-DD",
    "day_of_week": "string",
    "program_day_number": "integer",
    "week_period": "YYYY-MM-DD to YYYY-MM-DD",
    "days_into_week": "integer 1-7"
  },
  "morning_tune_up": {
    "completed": "boolean",
    "focus_word": "string or null",
    "mindset_challenge_text": "string or null",
    "quick_win_items": ["string array (3 items) or null"]
  },
  "evening_review": {
    "status": "completed | partial | missed",
    "wtd": {
      "completed": "boolean",
      "daily_score": "integer 0-5 or null",
      "day_category": "Win the Day | Partial Win | Missed the Mark | null",
      "q1_intention": "boolean or null",
      "q2_challenge": "boolean or null",
      "q3_adversity": "boolean or null",
      "q4_progress": "boolean or null",
      "q5_gratitude": "boolean or null",
      "missed_questions": ["array of Q labels or empty array"]
    },
    "journaling": {
      "completed": "boolean",
      "domains_completed": ["array of domain names or empty array"],
      "domains_omitted": ["array of domain names or empty array"],
      "sport_entry": "string or null",
      "school_work_entry": "string or null",
      "home_life_entry": "string or null"
    },
    "bullseye": {
      "completed": "boolean",
      "center_ring_items": ["string array or null"],
      "influence_ring_items": ["string array or null"],
      "outer_ring_items": ["string array or null"],
      "center_count": "integer or null",
      "influence_count": "integer or null",
      "outer_count": "integer or null"
    },
    "mindset_challenge_completed": "boolean or null"
  },
  "running_week_summary": {
    "days_completed": "integer 0-7",
    "win_days": "integer",
    "partial_win_days": "integer",
    "missed_days": "integer",
    "current_win_streak": "integer",
    "morning_completions": "integer",
    "evening_completions": "integer",
    "challenge_follow_throughs": "integer"
  }
}
```

### 5.7 Mini-JSON Evening Review Status Rules

| Condition | Status |
|-----------|--------|
| `submitted = true` in raw daily event | `"completed"` |
| `submitted = false` AND at least one component has `completed = true` | `"partial"` |
| `submitted = false` AND no components have `completed = true` | `"missed"` |

### 5.8 Deliberately Excluded Fields (Compliance)

The following fields exist in the raw daily event record but are **NEVER included in the Mini-JSON** — they are execution signal metrics that must remain backend-only per the pipeline's compliance framework.

| Excluded Field | Why |
|---------------|-----|
| `completion_timestamp` (morning and evening) | Execution timing data is backend-only |
| `trigger_method` (self_initiated / reminder) | Whether the athlete opened the app proactively or via reminder is an execution behavior metric, not coaching content |
| `mindset_challenge_accepted` | In V1 acceptance is mandatory to complete the Tune-Up, so `completed = true` implies `accepted = true` — redundant for Stage 6. Retained in raw daily event for Stage 2 weekly processing |
| `component_sequence` | Component completion order is a sequence integrity metric for Stage 2 weekly processing — Stage 6 references what the athlete produced, not the order |
| Rates and percentages (completion_rate, yes_rate, follow_through_rate) | Rates are derived analytical metrics computed by Stage 2 from weekly aggregated data — the Mini-JSON provides raw counts via running_week_summary |

These fields are collected by the backend for composite score computation (Section 7) but stripped before the Mini-JSON is sent to the AI pipeline. By excluding these fields at the data layer, Stage 6 cannot accidentally leak execution signal data — compliance-by-construction.

### 5.9 Generation Timing

- **When:** After hard-out lockout for the day (default: after 6:00 AM)
- **Before:** Morning Tune-Up release for the next day
- **Sequence:** Hard-out → Mini-JSON assembly → Stage 7 computation → Stage 6 generation → Morning Tune-Up release with snippet

### 5.10 Tiered Operation

| Feature | Base Tier | Premium Tier |
|---------|-----------|-------------|
| Mini-JSON generation | 7/week (Mon-Sun) | 7/week (Mon-Sun) |
| Stage 6 snippets | 7/week (Mon-Sun) | 6/week (Tue-Sun) |
| Stage 7 signals | No | 7/week (Mon-Sun) |
| Weekly JSON available | No | Yes (from Stage 2) |

**Premium Monday skip:** On Mondays, Premium athletes receive the full Coaching Message + Deep Dive instead of a snippet.

**Base tier operates standalone:** Mini-JSON + athlete snapshot are the only inputs. No weekly pipeline.

---

## 6. Weekly Data Assembly

### 6.1 Weekly Input Object Schema

Assembled after all 7 daily events are finalized (Sunday hard-out). This is what Stage 2 (Interpretation Engine) consumes.

```json
{
  "input_source": "app",
  "athlete_id": "string",
  "athlete_name": "string",
  "week_period": "YYYY-MM-DD to YYYY-MM-DD",
  "daily_events": [
    {
      "date": "YYYY-MM-DD",
      "day_of_week": "Monday",
      "morning_tune_up": { "/* Section 5.2 schema */" },
      "evening_review": { "/* Section 5.3 schema */" }
    }
  ],
  "weekly_check_in": {
    "submitted": "boolean",
    "submission_timestamp": "ISO-8601 datetime | null",
    "motivation_inventory": {
      "q1_achievements": "string | null",
      "q2_favorite_challenge": "string | null",
      "q3_upcoming_goals": "string | null",
      "q4_additional_context": "string | null",
      "q5_competition_schedule": "string | null"
    },
    "self_ratings": {
      "confidence_level": "integer 1-10 | null",
      "habit_consistency_level": "integer 1-10 | null"
    },
    "season_context": {
      "current_season_phase": "Pre-Season | In-Season | Off-Season | Post-Season | Year-Round Training"
    },
    "forward_anchor": {
      "text": "string | null",
      "submitted": "boolean"
    }
  }
}
```

**7 daily event records** (Monday through Sunday) using the schemas from Sections 5.2 and 5.3.

### 6.2 Weekly Check-In Contents

| Block | Fields | Purpose |
|-------|--------|---------|
| **Motivation Inventory** | 5 free-text questions | Feeds athlete_voice and upcoming_context in Interpretation JSON |
| **Self-Ratings** | confidence_level (1-10), habit_consistency_level (1-10) | Perception-reality alignment (compared against composite scores) |
| **Season Context** | current_season_phase | Live season phase (asked every week — may change mid-program) |
| **Forward Anchor** | text (free text, optional) | "One thing you can control next week" — athlete-authored intention |

**Self-Ratings Perception-Reality Alignment** (computed by Stage 2):
- `confidence_level` compared against Ownership Index + Follow-Through Score → Aligned / Conflated / Undervalued
- `habit_consistency_level` compared against Rhythm Score + completion rates → Aligned / Conflated / Undervalued

### 6.3 Core Foundation Weekly Input

```json
{
  "input_source": "core_foundation",
  "athlete_id": "string",
  "athlete_name": "string",
  "week_period": "YYYY-MM-DD to YYYY-MM-DD",
  "weekly_recap_text": "string"
}
```

No daily events, no composite scores, no daily signals.

### 6.4 Assembly Timing

1. Sunday hard-out closes final daily event
2. Backend assembles Weekly Input Object
3. Send to Stage 2 → returns Interpretation JSON
4. Interpretation JSON → Stage 3 → Coaching Message + Deep Dive + optional Parent CM
5. Stage 3 outputs → Stage 5 → Audit (PASS / REJECT AND REGENERATE)
6. Interpretation JSON → Stage 4 → Coach Insight + optional Parent Insight + optional Team Snapshot
7. All outputs stored and delivered

---

## 7. Execution Signal Computation (Backend)

All execution signal computations are **deterministic and performed by the backend.** The AI pipeline never computes these — it receives the results in the Interpretation JSON.

### 7.1 Overview

The backend computes three categories of execution signals from raw daily event data:

1. **7 Composite Scores** — weighted multi-component formulas producing 0-100 integer scores with categorical bands
2. **15 Coach Flags** — threshold-based warning flags with 3 severity tiers
3. **Self-Ratings Alignment** — perception vs. reality comparison using weekly self-ratings

**Score Directionality:**
- Higher = better: Ownership Index, Follow-Through Score, Rhythm Score, Review Quality Score, Recovery Score
- Higher = worse: Drift Score, Reactivity Risk Score

### 7.2 Composite Score #1: Ownership Index

**Measures:** Self-initiation vs. reminder dependency

**Input fields:** `evening_review.self_initiated_count` (0-7), `evening_review.backfill_count` (0-7), `morning_tune_up.on_time_count` (0-7)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Evening Self-Initiation | 50% | `(self_initiated_count / 7) × 100` | 0-100 |
| C2: Morning Proactivity | 30% | `(morning_tune_up.on_time_count / 7) × 100` | 0-100 |
| C3: Backfill Absence | 20% | `((7 - backfill_count) / 7) × 100` | 0-100 |

All three components use **7 (days in week) as denominator.**

**Final Score:** `round(C1 × 0.50 + C2 × 0.30 + C3 × 0.20)`

**Bands:**

| Range | Band |
|-------|------|
| 70-100 | High |
| 40-69 | Moderate |
| 0-39 | Low |

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- All app metrics = 0: C1=0, C2=0, C3=100 → score=20, band=Low
- Perfect week: C1=100, C2=100, C3=100 → score=100, band=High

### 7.3 Composite Score #2: Drift Score

**Measures:** Presence of engagement erosion indicators this week (higher = worse). Single-week measurement — cross-week drift trajectory is determined by comparing Drift Scores across weeks.

**Input fields:** `evening_review.completion_rate` (0.00-1.00, full only), `evening_review.late_submission_count` (0-7), `morning_tune_up.completion_rate` (0.00-1.00), `journaling_behavior.depth_profile` (enum), `bullseye_behavior.completion_reliability` (enum)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Evening Completion Erosion | 25% | `(1 - evening_review.completion_rate) × 100` | 0-100 |
| C2: Morning Completion Erosion | 20% | `(1 - morning_tune_up.completion_rate) × 100` | 0-100 |
| C3: Late Submission Rate | 20% | `(late_submission_count / 7) × 100` | 0-100 |
| C4: Journaling Compression | 20% | Enum mapping: Thorough=0, Adequate=25, Compressed=65, Minimal=100, insufficient data=0 (neutral) | 0-100 |
| C5: Bullseye Disengagement | 15% | Enum mapping: Consistent=0, Partial=50, Inconsistent=100, insufficient data=0 (neutral) | 0-100 |

**Final Score:** `round(C1 × 0.25 + C2 × 0.20 + C3 × 0.20 + C4 × 0.20 + C5 × 0.15)`

**Bands (asymmetric — Early threshold at 21 for early detection):**

| Range | Band |
|-------|------|
| 0-20 | None |
| 21-45 | Early |
| 46-100 | Active |

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- All worst (0/7 completion, Minimal, Inconsistent): score=100, band=Active
- `insufficient data` on enum fields: treated as 0 (neutral). Absence of data is not evidence of drift.

### 7.4 Composite Score #3: Follow-Through Score

**Measures:** Mindset Challenge acceptance-to-execution rate

**Input fields:** `morning_tune_up.days_completed` (0-7), `morning_tune_up.mindset_challenge_accepted_count` (0-7), `morning_tune_up.mindset_challenge_completed_count` (0-7), `morning_tune_up.mindset_challenge_follow_through_rate` (0.00-1.00)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Follow-Through Rate | 70% | `follow_through_rate × 100` | 0-100 |
| C2: Challenge Acceptance Rate | 30% | `(accepted_count / max(days_completed, 1)) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.70 + C2 × 0.30)`

**Bands:**

| Range | Band |
|-------|------|
| 75-100 | Strong |
| 40-74 | Moderate |
| 0-39 | Weak |

**Note:** In V1, Tune-Up completion requires challenge acceptance, so C2 = 100 whenever morning is completed. C2 becomes meaningful in future V2 when acceptance is optional. No sample-size cap — the C2 weighting naturally penalizes low acceptance (e.g., 1 accepted out of 7 mornings gives C2 = 14.3).

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- `days_completed = 0` → insufficient data (no morning engagement)
- `accepted_count = 0, days_completed > 0`: C1=0, C2=0 → score=0, band=Weak
- Perfect week (7/7 accepted, 7/7 completed): score=100, band=Strong

### 7.5 Composite Score #4: Rhythm Score

**Measures:** Timing consistency and sequence integrity

**Input fields:** `morning_tune_up.on_time_count` (0-7), `morning_tune_up.days_completed` (0-7), `evening_review.on_time_count` (0-7), `evening_review.late_submission_count` (0-7), `evening_review.backfill_count` (0-7), `evening_review.sequence_integrity` (enum)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Morning Timing Rate | 25% | If `days_completed = 0`: 0. Else: `(on_time_count / days_completed) × 100` | 0-100 |
| C2: Evening Timing Rate | 25% | `total_submitted = on_time_count + late_submission_count + backfill_count`. If `total_submitted = 0`: 0. Else: `(on_time_count / total_submitted) × 100` | 0-100 |
| C3: Sequence Integrity | 30% | Enum mapping: Intact=100, Partial=50, Broken=0, insufficient data=50 (neutral) | 0-100 |
| C4: Non-Backfill Rate | 20% | `total_submitted = on_time_count + late_submission_count + backfill_count`. If `total_submitted = 0`: 0. Else: `((total_submitted - backfill_count) / total_submitted) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.25 + C2 × 0.25 + C3 × 0.30 + C4 × 0.20)`

**Important:** Rhythm Score uses **completed-sessions denominator** (not 7). This measures timing quality of actual engagement. Sparse engagement is penalized through C3 (sequence likely Partial/Broken) and C4 (if backfills were involved), not through C1/C2.

**Bands:**

| Range | Band |
|-------|------|
| 75-100 | Stable |
| 40-74 | Variable |
| 0-39 | Disrupted |

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- Zero engagement: C1=0, C2=0, C3=50, C4=0 → score=15, band=Disrupted
- Perfect week: C1=100, C2=100, C3=100, C4=100 → score=100, band=Stable

### 7.6 Composite Score #5: Review Quality Score

**Measures:** Behavioral execution quality of the evening review (completeness depth, component engagement breadth, component balance)

**Input fields:** `evening_review.full_completion_count` (0-7), `evening_review.partial_completion_count` (0-7), `evening_review.completion_rate` (0.00-1.00, full only), `evening_review.component_completion.wtd_completed_count` (0-7), `evening_review.component_completion.journaling_completed_count` (0-7), `evening_review.component_completion.bullseye_completed_count` (0-7)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Full Completion Rate | 40% | `completion_rate × 100` | 0-100 |
| C2: Component Engagement Rate | 35% | `(wtd_completed + journaling_completed + bullseye_completed) / 21 × 100` where 21 = 3 components × 7 days | 0-100 |
| C3: Component Balance | 25% | `min_comp = min(wtd, journaling, bullseye)`, `max_comp = max(wtd, journaling, bullseye)`. If `max_comp = 0`: 0. Else: `(min_comp / max_comp) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.40 + C2 × 0.35 + C3 × 0.25)`

**Bands:**

| Range | Band |
|-------|------|
| 70-100 | High |
| 40-69 | Moderate |
| 0-39 | Low |

**Cherry-picker detection example:** An athlete with 5/7 full completion but 7/0/7 components (skips journaling): C1=71.4, C2=66.7, C3=0 → score=52, band=Moderate. The zero balance score drops what would otherwise be High.

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- Zero engagement: C1=0, C2=0, C3=0 → score=0, band=Low
- All partial, no full (0 full, 5 partial, 7/7/7 components): C1=0, C2=100, C3=100 → score=60, band=Moderate

### 7.7 Composite Score #6: Recovery Score

**Measures:** Post-disruption execution recovery. **Event-triggered** — only computed when a WTD disruption (Missed day) occurs.

**Input fields:** `wtd_question_patterns.recovery_speed_days`, `wtd_question_patterns.cross_week_recovery.prior_week_unresolved_miss`, `wtd_question_patterns.cross_week_recovery.recovery_days`, `morning_tune_up.completion_rate` (0.00-1.00), `evening_review.completion_rate` (0.00-1.00), `evening_review.sequence_integrity` (enum)

**5 States:**

| State | When | Score | Band |
|-------|------|-------|------|
| Calculated | Disruption occurred and recovery measurable | 0-100 | Strong 70+ / Moderate 40-69 / Low 0-39 |
| No disruption | `recovery_speed_days = "not applicable"` AND `prior_week_unresolved_miss = "No"` | Fixed 85 | Strong |
| Pending Data | `recovery_speed_days = "Pending Data"` (disruption on last day of week, recovery unmeasurable this week) | "Pending Data" | "Pending Data" |
| Insufficient data | First week or no prior data | "insufficient data" | "insufficient data" |
| CF fallback | Core Foundation athlete | "insufficient data" | "insufficient data" |

**Calculated State Formula (State 1):**

**C1 input determination (priority order):**
- If BOTH `recovery_speed_days` (within-week) AND `cross_week_recovery.recovery_days` are valid integers → use the SLOWER of the two (higher number)
- If ONLY `recovery_speed_days` is a valid integer → use it
- If ONLY `cross_week_recovery.recovery_days` is a valid integer → use it
- If either value = "did not recover" → C1 = 0

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Recovery Speed | 60% | Lookup table: 1 day=100, 2 days=85, 3 days=70, 4 days=50, 5 days=35, 6 days=20, 7 days=10, did not recover=0 | 0-100 |
| C2: Engagement Maintenance | 25% | `((morning_completion_rate + evening_completion_rate) / 2) × 100` — average of full-week morning AND evening completion rates | 0-100 |
| C3: Sequence Preservation | 15% | Enum mapping from `sequence_integrity`: Intact=100, Partial=50, Broken=0, insufficient data=50 (neutral) | 0-100 |

**Final Score:** `round(C1 × 0.60 + C2 × 0.25 + C3 × 0.15)`

**Why fixed 85 for no-disruption:** Athlete was not tested. 85 places them in Strong without claiming perfect recovery evidence.

**Recovery Speed measurement:** Days from a Missed day (WTD 0-1) to next Win day (WTD 4-5). Uses fastest recovery instance when multiple Missed days occur.

**Cross-week recovery:** If a Missed day occurs on the last day of the week, `recovery_speed_days = "Pending Data"` and recovery is measured in the **next week's** early days via `cross_week_recovery.recovery_days`. The prior week's JSON is NEVER modified — forward-only flow.

### 7.8 Composite Score #7: Reactivity Risk Score

**Measures:** Volatile execution patterns (higher = worse). Distinct from Drift Score: Drift = gradual consistent erosion; Reactivity = volatile event-driven disruption.

**Input fields:** `wtd_question_patterns.intraweek_volatility` (enum), `evening_review.sequence_integrity` (enum), `bullseye_behavior.contradiction_detected` (enum), `evening_review.full_completion_count` (0-7), `evening_review.partial_completion_count` (0-7)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: WTD Intraweek Volatility | 30% | Enum mapping: Low=0, Moderate=50, High=100, insufficient data=0 (neutral) | 0-100 |
| C2: Sequence Disruption | 25% | Enum mapping from `sequence_integrity`: Intact=0, Partial=50, Broken=100, insufficient data=0 (neutral) | 0-100 |
| C3: Bullseye Contradiction | 20% | Enum mapping from `contradiction_detected`: No=0, Yes=100, insufficient data=0 (neutral) | 0-100 |
| C4: Engagement Incompletion Rate | 25% | `(partial_completion_count / max(full_completion_count + partial_completion_count, 1)) × 100` — ratio of partial-to-full captures "started but abandoned" reactivity | 0-100 |

**Final Score:** `round(C1 × 0.30 + C2 × 0.25 + C3 × 0.20 + C4 × 0.25)`

**Bands:**

| Range | Band |
|-------|------|
| 0-25 | Low |
| 26-50 | Moderate |
| 51-100 | Elevated |

**Edge Cases:**
- `input_source = "core_foundation"` → insufficient data
- All enum fields = "insufficient data" + 0 partial: score=0, band=Low. Absence of data is not evidence of reactivity.
- All reviews missed (full=0, partial=0): C4=0. Missing engagement = Drift's domain, not Reactivity.

### 7.9 Composite Score Summary Table

| # | Score | Key: JSON path | Bands | Direction |
|---|-------|----------------|-------|-----------|
| 1 | Ownership Index | `composite_scores.ownership_index` | High 70+ / Moderate 40-69 / Low 0-39 | Higher = better |
| 2 | Drift Score | `composite_scores.drift_score` | None 0-20 / Early 21-45 / Active 46+ | Lower = better |
| 3 | Follow-Through Score | `composite_scores.follow_through_score` | Strong 75+ / Moderate 40-74 / Weak 0-39 | Higher = better |
| 4 | Rhythm Score | `composite_scores.rhythm_score` | Stable 75+ / Variable 40-74 / Disrupted 0-39 | Higher = better |
| 5 | Review Quality Score | `composite_scores.review_quality_score` | High 70+ / Moderate 40-69 / Low 0-39 | Higher = better |
| 6 | Recovery Score | `composite_scores.recovery_score` | Strong 70+ / Moderate 40-69 / Low 0-39 | Higher = better |
| 7 | Reactivity Risk Score | `composite_scores.reactivity_risk_score` | Low 0-25 / Moderate 26-50 / Elevated 51+ | Lower = better |

### 7.10 Coach Flags

15 execution-behavior-derived warning flags evaluated by the backend. Each flag fires independently when its trigger condition is met.

**Flag Object Schema:**

```json
{
  "flag_id": "string (snake_case identifier)",
  "severity": "monitor | attention | action",
  "label": "string (human-readable label)",
  "trigger_source": ["array of contributing data points"],
  "description": "string (template with dynamic variables)"
}
```

**Severity Tiers:**

| Tier | Count | Downstream Effect |
|------|-------|------------------|
| **action** | 3 flags | Shifts coaching direction entirely |
| **attention** | 8 flags | Direct coaching address, micro-commitment targets flagged area |
| **monitor** | 4 flags | Subtle tone adjustment only |

#### Action Flags (3)

| flag_id | Trigger Condition |
|---------|-------------------|
| `compound_disengagement` | 3 or more of these 5 scores in their worst band: Ownership=Low, Drift=Active, Rhythm=Disrupted, Review Quality=Low, Follow-Through=Weak. (Excludes Recovery and Reactivity.) |
| `persistent_attention_pattern` | Any attention-level flag fires in BOTH current week AND prior week. Requires cross-week data. `trigger_source` populated with the persistent flag_ids. |
| `sustained_compound_disengagement` | `compound_disengagement` fires in BOTH current week AND prior week. Requires cross-week data. |

#### Attention Flags (8)

| flag_id | Trigger Condition |
|---------|-------------------|
| `drift_active` | `drift_score.band == "Active"` |
| `reactivity_elevated` | `reactivity_risk_score.band == "Elevated"` |
| `recovery_failure` | `recovery_score.band == "Low"` AND Recovery Score state is "Calculated" (not Pending/insufficient) |
| `ownership_low` | `ownership_index.band == "Low"` |
| `follow_through_weak` | `follow_through_score.band == "Weak"` |
| `rhythm_disrupted` | `rhythm_score.band == "Disrupted"` |
| `review_quality_low` | `review_quality_score.band == "Low"` |
| `sustained_drift` | `drift_score.band != "None"` in BOTH current AND prior week. Requires cross-week data. |

#### Monitor Flags (4)

| flag_id | Trigger Condition |
|---------|-------------------|
| `drift_early` | `drift_score.band == "Early"` |
| `surface_engagement` | Evening completion rate ≥ 0.71 AND 2 or more of: Review Quality = Low or Moderate, Journaling depth = Compressed or Minimal, Follow-Through = Weak or Moderate |
| `component_avoidance` | Any single component has 0 completions while another component has ≥ 3 completions |
| `morning_disengagement` | Morning completion rate ≤ 0.29 AND evening completion rate ≥ 0.57 |

**Ordering Rule:** Flags in the array are ordered by severity descending (action first, then attention, then monitor). Within the same severity tier, maintain catalog sequence (flag_id numeric order).

**Independence Rule:** Individual worst-band flags fire independently even when compound or cross-week flags also fire. For example, if `compound_disengagement` fires AND `ownership_low` fires, BOTH appear in the array.

**Cross-Week Data Requirements:** Flags 13-15 (`sustained_drift`, `persistent_attention_pattern`, `sustained_compound_disengagement`) require the prior week's Interpretation JSON. If no prior week exists, these flags cannot fire.

**Core Foundation Fallback:** `coach_flags = []` (empty array).

### 7.11 Self-Ratings Alignment Classification

Compares the athlete's weekly self-assessment (from weekly check-in) against computed execution data. Each dimension is classified independently.

**Self-Perception Tier Mapping (both dimensions):**

| Self-Rating (1-10) | Perception Tier |
|---------------------|-----------------|
| 8-10 | High |
| 4-7 | Moderate |
| 1-3 | Low |

**Dimension 1: Confidence Alignment**
- Input: `self_ratings.confidence_level` (1-10) vs. Ownership Index band + Follow-Through Score band (2 scores)
- Execution tier determination: count top-band scores (Ownership High = +1 top, Follow-Through Strong = +1 top) and bottom-band scores (Ownership Low = +1 bottom, Follow-Through Weak = +1 bottom). High: top count = 2. Low: bottom count = 2. Moderate: all other combinations.
- **Aligned:** confidence perception tier == confidence execution tier
- **Conflated:** confidence perception tier > confidence execution tier (athlete self-rates higher than execution supports)
- **Undervalued:** confidence perception tier < confidence execution tier (execution exceeds self-assessment)
- If `confidence_level = null` → "insufficient data"
- If either composite score band = "insufficient data" → "insufficient data"

**Dimension 2: Habit Consistency Alignment**
- Input: `self_ratings.habit_consistency_level` (1-10) vs. Rhythm Score band (1 score)
- Execution tier mapping: Stable → High, Variable → Moderate, Disrupted → Low
- **Aligned:** habit perception tier == habit execution tier
- **Conflated:** habit perception tier > habit execution tier
- **Undervalued:** habit perception tier < habit execution tier
- If `habit_consistency_level = null` → "insufficient data"
- If `rhythm_score.band = "insufficient data"` → "insufficient data"

**Output:**

```json
"self_ratings_alignment": {
  "confidence_alignment": "Aligned | Conflated | Undervalued | insufficient data",
  "habit_consistency_alignment": "Aligned | Conflated | Undervalued | insufficient data"
}
```

### 7.12 Core Foundation Fallback

When `input_source = "core_foundation"`:
- All composite scores: `{ "score": "insufficient data", "band": "insufficient data" }`
- Coach flags: `[]` (empty array)
- Self-ratings alignment: `{ "confidence_alignment": "insufficient data", "habit_consistency_alignment": "insufficient data" }`
- Execution pattern summary: `"Core Foundation input — execution behavior signals not available"`

---

## 8. Daily Coach Signal — Stage 7 (Backend)

Stage 7 is **entirely deterministic** — the backend implements this with zero AI involvement and zero AI cost. It produces a daily traffic-light signal for each athlete, consumed by the coach dashboard.

### 8.1 Input

- **Required:** Daily Mini-JSON (Section 5.6)
- **Optional:** Weekly calibration cache (per-athlete, from most recent Interpretation JSON)

### 8.2 Output Schema

```json
{
  "athlete_id": "string",
  "signal_date": "YYYY-MM-DD",
  "program_day_number": "integer",
  "days_into_week": "integer 1-7",
  "traffic_light": "GREEN | YELLOW | ORANGE | GRAY",
  "day_outcome": "Aligned | Building | Reset Day | null",
  "focus_alignment": "Centered | Mixed | Drifting | null",
  "follow_through": "Demonstrated | Gap | null",
  "weekly_trajectory": "Building Week | Steady Week | Cooling Week | null",
  "has_data": "boolean",
  "_internal": {
    "point_score": "integer -4 to +6 | null",
    "calibration_applied": "emotional_intensity | growth_phase | none",
    "calibration_source": "High | Emerging | Regressing | Consistent | Leadership | none",
    "threshold_shift": "integer -1, 0, or +1",
    "green_min": "integer",
    "orange_max": "integer"
  }
}
```

**`_internal` fields are backend-only** — NEVER exposed to coaches, parents, or athletes.

**Field notes:**
- `weekly_trajectory`: null when `days_into_week <= 2` OR `days_completed < 2` (too early for meaningful trajectory).
- `has_data`: false when `traffic_light = "GRAY"` (entire Evening Review missed). true otherwise.
- `_internal.point_score`: null when GRAY (points not computed).

### 8.3 Step 1: Gray State Check

**Execute first, before any scoring.**

If `evening_review.status == "missed"` → Set `traffic_light = "GRAY"`, all contributing signals = `null`, `has_data = false`, `_internal.point_score = null`, `_internal.calibration_applied = "none"`, `_internal.threshold_shift = 0`. Weekly Trajectory MAY still be populated (uses running week summary, not today's evening review). **Skip all remaining steps.**

### 8.4 Step 2: Contributing Signal Determination

#### Day Outcome (from WTD category)

| WTD Category | Day Outcome |
|-------------|-------------|
| Win the Day (4-5) | Aligned |
| Partial Win (2-3) | Building |
| Missed the Mark (0-1) | Reset Day |
| null (no WTD data) | null |

#### Focus Alignment (from Bullseye rings)

| Condition | Focus Alignment |
|-----------|----------------|
| center_ring item count > outer_ring item count | Centered |
| outer_ring item count > center_ring item count | Drifting |
| center == outer, OR influence_ring dominant | Mixed |
| No Bullseye data | null |

#### Follow-Through (from Mindset Challenge)

| Condition | Follow-Through |
|-----------|---------------|
| Tune-Up completed + challenge accepted + challenge completed | Demonstrated |
| Tune-Up completed + challenge accepted + challenge NOT completed | Gap |
| No Tune-Up OR challenge not accepted | null |

#### Weekly Trajectory (from running week summary, computes from Day 3+)

| Condition | Weekly Trajectory |
|-----------|------------------|
| `win_rate >= 0.50` AND `miss_rate <= 0.25` | Building Week |
| `miss_rate >= 0.50` OR (`misses > wins` AND `partials <= 1`) | Cooling Week |
| Everything else | Steady Week |
| `days_into_week <= 2` OR `days_completed < 2` | null |

Where:
- `win_rate = win_days / days_completed`
- `miss_rate = missed_days / days_completed`

### 8.5 Step 3: Hidden Input Determination

These two inputs contribute to the point score but are **NEVER displayed to anyone**.

#### Reflection Breadth (from journaling)

| Condition | Value |
|-----------|-------|
| `domains_completed` = 3 (exactly 3 domains) | Broad |
| `domains_completed` = 1 or 2 | Narrow |
| No journaling or evening review missed | None |

#### Morning Engagement

| Condition | Value |
|-----------|-------|
| Morning Tune-Up completed = true | Yes |
| Morning Tune-Up completed = false | No |

### 8.6 Step 4: Point Scoring

| Signal | Value | Points |
|--------|-------|--------|
| Day Outcome | Aligned | +2 |
| Day Outcome | Building | +1 |
| Day Outcome | Reset Day | -1 |
| Day Outcome | null | 0 |
| Focus Alignment | Centered | +1 |
| Focus Alignment | Mixed | 0 |
| Focus Alignment | Drifting | -1 |
| Focus Alignment | null | 0 |
| Follow-Through | Demonstrated | +1 |
| Follow-Through | Gap | -1 |
| Follow-Through | null | 0 |
| Reflection Breadth (hidden) | Broad | +1 |
| Reflection Breadth (hidden) | Narrow | 0 |
| Reflection Breadth (hidden) | None | -1 |
| Morning Engagement (hidden) | Yes | +1 |
| Morning Engagement (hidden) | No | 0 |

**Point range:** -4 to +6

### 8.7 Step 5: Traffic Light Assignment

#### Standard Thresholds (default)

| Point Range | Traffic Light |
|------------|---------------|
| +4 to +6 | GREEN |
| +1 to +3 | YELLOW |
| 0 to -4 | ORANGE |

#### Weekly Calibration Modifiers

Applied in priority order — **first match wins, no stacking:**

| Priority | Condition | Modified Thresholds |
|----------|-----------|-------------------|
| 1 | `emotional_intensity == "High"` AND within first 3 days of the week | GREEN: +3 to +6, YELLOW: 0 to +2, ORANGE: -4 to -1 |
| 2 | `growth_phase` is "Emerging" or movement is "Regressing" | GREEN: +3 to +6, YELLOW: 0 to +2, ORANGE: -4 to -1 |
| 3 | `growth_phase` is "Consistent" or "Leadership" | GREEN: +5 to +6, YELLOW: +2 to +4, ORANGE: -4 to +1 |
| 4 | Default (Developing + not Regressing + not High EI) | Standard thresholds |

**Calibration source:** The `emotional_intensity` and `growth_phase` values come from the most recent weekly Interpretation JSON, stored in a per-athlete calibration cache.

**High EI expiration:** The +1 shift applies only to the first 3 days of the new week (Monday-Wednesday by default). On Day 4+, High EI modifier no longer applies even if the cached value is still "High."

### 8.8 Calibration Cache Management

- **Storage:** Per-athlete key-value store with fields: `emotional_intensity`, `growth_phase`, `growth_phase_movement`, `cache_updated` (timestamp)
- **Update trigger:** When a new Interpretation JSON arrives from Stage 2
- **Read timing:** When computing each day's traffic light
- **First week (no cache):** Use standard thresholds (Priority 4)
- **Cache lifetime:** Cached values persist until the next Interpretation JSON is produced. The cache is never manually expired. The `emotional_intensity` modifier self-expires via its application rule (`days_into_week <= 3`), not via cache expiration.

### 8.9 Team & Position Group Aggregation

**4-Tier Model** (computed from individual athlete signals):

| Tier | Label | Condition |
|------|-------|-----------|
| 1 | Strong Alignment | `green_pct >= 0.75` AND `orange_pct == 0` |
| 2 | Positive Trend | `green_pct >= 0.50` AND `orange_pct <= 0.15` |
| 3 | Mixed Signals | `green_pct` between 0.25-0.49 OR `orange_pct` between 0.15-0.30 |
| 4 | Needs Attention | Default (everything else) |

**Evaluation order:** Check Tier 1 first, then Tier 2, then Tier 3. If none match → Tier 4.

Where:
- `green_pct = count(GREEN) / count(non-GRAY)`
- `orange_pct = count(ORANGE) / count(non-GRAY)`
- **GRAY signals are excluded from all calculations**

**Minimum group sizes:**
- Position groups: 3 athletes minimum
- Teams: 5 athletes minimum
- Below minimum → do not generate aggregation

### 8.10 Twelve Edge Cases

| # | Edge Case | Handling |
|---|-----------|---------|
| 1 | Partial evening review (some components, not all) | Status = "partial". Score using available data. Missing components contribute null (0 points). |
| 2 | Day 1 (first day ever) | Weekly Trajectory = null. All other signals determined normally. Standard thresholds (no cache). |
| 3 | First week (no prior Interpretation JSON) | Standard thresholds. No calibration modifiers. |
| 4 | WTD only (no journaling, no Bullseye) | Day Outcome determined. Focus Alignment = null. Reflection Breadth = None. |
| 5 | Morning only (Tune-Up completed, evening missed) | Gray (evening missed triggers Gray). Morning data unused for this day's signal. |
| 6 | All signals negative | Score can reach -4. Traffic light = ORANGE. System works as designed. |
| 7 | All signals positive | Score can reach +6. Traffic light = GREEN. System works as designed. |
| 8 | Below minimum group size | Do not generate team/position aggregation. Return null for group tier. |
| 9 | Zero non-Gray data in group | All athletes missed → no aggregation possible. Return null. |
| 10 | Partial week trajectory | Weekly Trajectory computed from completed days only. Days 1-2 = null. Day 3+ uses running_week_summary rates from `days_completed`. |
| 11 | All Bullseye rings zero items | Focus Alignment = null (no data to determine ring balance). |
| 12 | Influence ring ties (center == outer, influence has most) | Focus Alignment = Mixed. |

### 8.11 Parent Signal Label Mapping

Parents see simplified labels. **Contributing signals are HIDDEN from parents.**

| Traffic Light | Parent Label |
|--------------|-------------|
| GREEN | Good Day |
| YELLOW | Building Day |
| ORANGE | Reset Day |
| GRAY | No Update Today |

**Parents do NOT see:** Day Outcome, Focus Alignment, Follow-Through, Weekly Trajectory, team aggregation, or any _internal data.

### 8.12 Timing

- **Trigger:** After Mini-JSON generation (Section 5.9)
- **Before:** Stage 6 (snippet generation) and Morning Tune-Up release
- **Computation time:** Milliseconds per athlete (deterministic rules, no AI)
- **Daily sequence:** Mini-JSON generation (starts 2 hours before hard-out) → Stage 7 → Stage 6 → hard-out → Tune-Up release with snippet

---

## 9. AI Pipeline Interface

This section defines the API boundary between the backend and the AI pipeline. The backend does NOT need to understand pipeline internals — it sends structured input and receives structured output.

### 9.1 Inputs to AI Pipeline (Backend Sends)

| Input | Destination | Cadence | Schema Reference |
|-------|------------|---------|-----------------|
| Intake form responses + computed PPD/ABI | Stage 1 (Athlete Snapshot) | One-time (at onboarding) | Sections 2-4 |
| Weekly Input Object | Stage 2 (Interpretation Engine) | Weekly (after Sunday hard-out) | Section 6.1 |
| Daily Mini-JSON | Stage 6 (Daily Coaching Engine) | Daily | Section 5.6 |
| Athlete Snapshot (reference) | Stage 6 (baseline context) | Provided with each daily call | Stage 1 output |
| Previous day's snippet (text) | Stage 6 (repetition avoidance) | Daily | Previous Stage 6 output |
| Most recent Interpretation JSON (reference) | Stage 6 Premium tier only | Weekly context for Tue-Sun snippets | Stage 2 output |

**Stage 7 is NOT an AI pipeline call** — the backend computes it directly (Section 8).

### 9.2 Outputs from AI Pipeline (Backend Receives and Stores)

| Output | Source | Cadence | Format | Approx Size | Audience |
|--------|--------|---------|--------|-------------|----------|
| **Athlete Snapshot** | Stage 1 | One-time | Structured text (header + data block + narrative) | 1,500-2,500 words | Internal (pipeline reference) |
| **Interpretation JSON** | Stage 2 | Weekly/athlete | Structured JSON text | 2,000-4,000 tokens (~1,100 lines) | Internal (feeds Stages 3-6, calibration cache) |
| **Coaching Message** | Stage 3 | Weekly/athlete | Plain text with header, separator bars, labeled sections | 250-450 words | **Athlete-facing** |
| **Deep Dive** | Stage 3 | Weekly/athlete | Plain text with 5 sections, dash separators | 850-1,200 words | **Athlete-facing** |
| **Parent Coaching Message** | Stage 3 | Weekly/athlete (conditional) | Plain text, 4 labeled sections + signature | 150-250 words | **Parent-facing** (D2C Premium only, when `parent_inclusion = true`) |
| **Daily Coaching Snippet** | Stage 6 | Daily/athlete | Plain text, 2-3 sentences + signature | 30-60 words | **Athlete-facing** |
| **Weekly Performance Insight** | Stage 4 | Weekly/athlete | Structured text, 10 numbered sections with indicators + narrative | ~500 words | **Coach-facing** (Institutional only) |
| **Parent Weekly Insight** | Stage 4 | Weekly/athlete (conditional) | Structured text, 9 sections scan-first format (indicator + blurb) | ~270 words | **Parent-facing** (D2C Premium only) |
| **Weekly Team Snapshot** | Stage 4 | Weekly/team | Structured text, 7 sections (T1-T7) with distributions + narrative | ~370 words | **Coach-facing** (Institutional only, requires 5+ athletes) |
| **Audit Summary** | Stage 5 | Weekly/athlete | Structured text | ~200 words | **Internal only** (QA, never displayed) |

### 9.3 Output File Naming Convention

All outputs use this locked format:

```
{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_{OutputType}.txt
```

| Output Type | Suffix |
|-------------|--------|
| Interpretation JSON | `_VF_Interpretation.txt` |
| Coaching Message | `_VF_CoachingMessage.txt` |
| Deep Dive | `_VF_DeepDive.txt` |
| Parent Coaching Message | `_VF_ParentMessage.txt` |
| Weekly Performance Insight | `_VF_WeeklyInsight.txt` |
| Parent Weekly Insight | `_VF_ParentInsight.txt` |
| Audit Summary | `_VF_AuditSummary.txt` |

Team Snapshot: `{TeamName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_WeeklyTeamSnapshot.txt`

Daily Snippet: stored by date, not week period.

### 9.4 Scheduling

**Daily Cycle:**
```
1. [hard-out - 2h] Backend generates Mini-JSON for each athlete
2. Backend computes Stage 7 signal for each athlete (milliseconds)
3. Backend sends Mini-JSON + context to Stage 6 (AI generates snippet)
4. Stage 6 returns snippet (seconds per athlete with batching)
5. [hard-out] Morning Tune-Up released to athlete with snippet attached
```

**Weekly Cycle:**
```
1. Sunday hard-out closes final daily event
2. Backend assembles Weekly Input Object
3. Stage 2 processes → returns Interpretation JSON (~30-60 seconds)
4. Backend updates calibration cache from Interpretation JSON
5. Stage 3 processes Interpretation JSON → returns CM + DD + optional Parent CM (~30-60 seconds)
6. Stage 5 audits Stage 3 output → PASS or REJECT AND REGENERATE
   - If REJECT: Stage 3 regenerates with audit instructions, Stage 5 re-audits (max 2 cycles)
7. Stage 4 processes Interpretation JSON → returns Coach Insight + optional Parent Insight (~30 seconds)
8. Stage 4 processes team aggregation → returns Team Snapshot if 5+ athletes (~30 seconds)
9. All outputs stored and delivered to respective audiences (Monday morning)
```

**Stage 3 generates 2 or 3 outputs per run:**
- Always: Coaching Message + Deep Dive
- Conditional: Parent Coaching Message (only when `parent_inclusion = true` AND tier is D2C Premium + Parent)

**Stage 4 generates 1-3 outputs per run (tier-dependent):**
- Conditional: Weekly Performance Insight (Institutional tier only)
- Conditional: Parent Weekly Insight (D2C Premium + Parent tier, when `parent_inclusion = true`)
- Conditional: Weekly Team Snapshot (Institutional tier, when 5+ athletes on a team)

**Note:** Stage 4 runs for both Institutional and D2C Premium + Parent tiers, producing different outputs for each. Institutional gets Coach Insight + Team Snapshot. Premium + Parent gets Parent Insight.

### 9.5 Interpretation JSON Key Fields

The Interpretation JSON is the central data object in the pipeline. Key fields the backend should understand for calibration cache and downstream rendering:

```json
{
  "athlete_name": "string",
  "week_period": "YYYY-MM-DD to YYYY-MM-DD",
  "input_source": "app | core_foundation",
  "win_the_day": {
    "weekly_tier": "Growth | Mixed | Reset",
    "win_days": "integer",
    "total_score": "integer 0-35"
  },
  "emotional_intensity": "Low | Moderate | High | insufficient data",
  "growth_phase": "Emerging | Developing | Consistent | Leadership",
  "growth_phase_movement": "Advancing | Stable | Regressing",
  "consistency_signal": "Stable | Improving | Variable | Declining",
  "confidence_momentum": "Building | Stable | Variable",
  "stress_load": "Low | Moderate | Elevated",
  "reflection_quality_score": "integer 1-4",
  "recommitment_signal": "Strong | Moderate | Low | Not Applicable | insufficient data",
  "composite_readiness_signal": "Positive (Green) | Steady (Yellow) | Attention (Orange)",
  "baseline_intake_profile": {
    "competitive_level": "string",
    "ppd_primary_problem": "string",
    "abi_primary_emphasis": ["array"],
    "adversity_response_pattern": "string"
  },
  "current_season_phase": "Pre-Season | In-Season | Off-Season | Post-Season | Year-Round Training | not available",
  "execution_behavior_signals": {
    "input_source": "app | core_foundation",
    "composite_scores": { "/* Section 7.9 schema */" },
    "coach_flags": ["/* Section 7.10 schema */"],
    "self_ratings_alignment": { "/* Section 7.11 schema */" },
    "execution_pattern_summary": "string"
  }
}
```

---

## 10. Dashboard Rendering

Dashboards are **presentation layers only** — they render data from pipeline output and Stage 7 signals. No new computations.

### 10.1 Coach Dashboard Metric Definitions (Institutional Tier Only)

6 compliance-safe metrics for coaching staff dashboard display. All metrics are trend-based, non-punitive, and informational. The dashboard is a presentation layer — it renders data from Stage 4 weekly output + Stage 7 daily output.

#### 10.1.1 Pattern Stability Indicator

- **Source:** 4+ weeks of `weekly_tier` + `consistency_signal` from Interpretation JSON
- **Display:** Text label + color band

| Label | Condition | Color |
|-------|-----------|-------|
| Predictable | 4+ consecutive same-tier weeks with Stable or Improving consistency signal | Green |
| Transitional | Mix of 2 tiers, 0-1 Reset weeks in window | Yellow |
| Fluctuating | 3+ tier changes in 4 weeks OR 2+ Reset weeks | Orange |

- **Update:** Weekly, rolling 4-week window
- **Minimum data:** 4 weeks of Interpretation JSONs
- **Early weeks (< 4 weeks):** Gray, "Building Pattern" placeholder
- **Compliance:** Frame as "Pattern Stability," never "Volatility Index"

#### 10.1.2 Response Recovery Indicator

- **Source:** 3+ weeks of tier transition history from Interpretation JSONs
- **Display:** Text label + color band

| Label | Condition | Color |
|-------|-----------|-------|
| Rapid | Non-Growth week → Growth next week | Green |
| Moderate | Non-Growth → Mixed → Growth (2-week recovery) | Yellow |
| Extended | Non-Growth → 2+ consecutive non-Growth before recovery | Orange |
| No Recovery Data | All Growth weeks (athlete untested — this is positive) | Gray |

- **Update:** Weekly, using all available history
- **Minimum data:** 3 weeks with at least one non-Growth week followed by subsequent weeks
- **Early weeks (< 3 weeks or all-Growth):** Gray, "No Recovery Data" (neutral/positive indicator)
- **Compliance:** Measures behavioral pattern, NOT resilience or mental toughness

#### 10.1.3 Multi-Week Trend Visualization

- **Source:** 4-8 weeks of 8 metrics from Interpretation JSONs
- **Display:** Sparkline dots per metric, color-coded, most recent week on right

**8 Tracked Metrics:**

| Metric | Source Field | Values |
|--------|-------------|--------|
| Weekly Tier | `win_the_day.weekly_tier` | Growth / Mixed / Reset |
| Consistency Signal | `consistency_signal` | Stable / Improving / Variable (see note in 10.1.4 regarding "Declining") |
| Stress Load | `stress_load` | Low / Moderate / Elevated |
| Confidence Momentum | `confidence_momentum` | Building / Stable / Variable |
| Focus Distribution | `focus_distribution` | Center-Dominant / Mixed / Outer-Ring Drift |
| Recommitment Strength | `recommitment_signal` | Strong / Moderate / Low |
| Growth Phase | `growth_phase` | Emerging / Developing / Consistent / Leadership |
| Composite Readiness | `composite_readiness_signal` | Positive / Steady / Attention |

- **Display rules:**
  - Most recent week on right side
  - Color-coded data points (Green / Yellow / Orange per metric — see color table below)
  - No raw numbers displayed — classification labels only
  - Gray dot for insufficient data weeks
  - Hovering shows: week date + classification label
  - Minimum 4 weeks to render; maximum 8 weeks shown
- **Update:** Weekly (Monday)

#### 10.1.4 Color Coding System (Complete Mapping)

| Metric | Green | Yellow | Orange | Gray |
|--------|-------|--------|--------|------|
| Weekly Tier | Growth | Mixed | Reset | — |
| Consistency | Stable / Improving | Variable (no other negatives) | Variable (with negatives) | insufficient data |
| Stress Load | Low | Moderate | Elevated | — |
| Confidence | Building | Stable | Variable | insufficient data |
| Focus Distribution | Center-Dominant | Mixed | Outer-Ring Drift | insufficient data |
| Recommitment | Strong | Moderate | Low | Not Applicable |
| Composite Readiness | Positive | Steady | Attention | — |
| Pattern Stability | Predictable | Transitional | Fluctuating | < 4 weeks |
| Response Recovery | Rapid | Moderate | Extended | No Recovery Data |

**Note on "Declining" consistency signal:** The Interpretation JSON uses `consistency_signal` values including "Declining" (per JSON Rules), but the Dashboard Metrics Reference source does not explicitly map "Declining" to a color band. The source handles the Consistency row via "Variable" with contextual modifiers (Yellow when no other negatives, Orange when co-occurring with other negative signals). If the backend encounters a "Declining" value, treat it as Orange. This mapping is an implementation inference — confirm with specification owner if precise color mapping for "Declining" is needed.

**Critical:** Orange ≠ "at-risk." No red color anywhere in the system. No evaluation implication. Orange means "coaching staff might want context" — nothing more.

#### 10.1.5 Season Phase Overlay

- **Source:** Administrator-configured calendar dates (NOT event-based, NOT athlete-reported)
- **Display:** Timeline bar beneath or above trend visualizations with phase dividers
- **Configuration:** Administrator sets phase start/end dates at season start for the team/program

| Phase | Typical Period |
|-------|---------------|
| Pre-Season | Before competitive season begins |
| Early Season | First 2-4 weeks of competition |
| Mid-Season | Core competitive schedule |
| Conference / Championship | Championship / postseason period |
| Post-Season | After competitive season ends |

- **Purpose:** Contextual layer only — provides temporal context for reading trends. No performance expectations tied to schedule phase.
- **Update:** Static per season (admin configures once, updates as needed)

#### 10.1.6 Team Trend Over Time

- **Source:** 4+ weeks of team-aggregate data, minimum 5 athletes per team
- **Display:** Stacked area/bar charts showing percentages over time

**Team-Level Metrics:**

| Metric | Display Format |
|--------|---------------|
| Performance Distribution | % Growth / % Mixed / % Reset per week |
| Team Consistency Trend | % Stable / % Variable / % Declining per week |
| Team Focus Distribution | % Center-Dominant / % Mixed / % Outer-Ring per week |
| Team Recommitment Trend | % Strong / % Moderate / % Low per week |
| Team Stress Load Distribution | % Low / % Moderate / % Elevated per week |
| Team Developmental Distribution | % by Growth Phase per week |

- **Display rules:**
  - All values as percentages (never raw athlete counts)
  - 4-8 week window
  - Minimum 5 athletes to generate
  - **No individual athlete identification** at any point — aggregate only
  - No athlete-to-athlete comparison views
- **Update:** Weekly (Monday)
- **Compliance:** Same rules as Weekly Team Snapshot output from Stage 4

#### 10.1.7 Coach Dashboard — Excluded Metrics

The following are **explicitly excluded** from the coach dashboard and must NEVER be generated or displayed:

| Excluded Category | Examples |
|-------------------|---------|
| Engagement/Activity | Login timestamps, time in app, completion counts, streak counts |
| Athlete Comparison | Rankings, side-by-side individual comparisons by name |
| Predictive Signals | Any forward-looking risk assessment (crosses into clinical territory) |
| Coach Action Tracking | Whether coaches viewed reports, acted on signals |
| Raw Reflection Quality | RQS 1-4 score surfaced directly (consumed indirectly through Growth Phase) |
| Effort-Based Metrics | Compliance ratings, adherence scores, participation rankings |

#### 10.1.8 Coach Dashboard — Layout Principles

- **Individual Athlete View:** Pattern Stability + Response Recovery as hero indicators, Multi-Week Trend sparklines below, Season Phase Overlay as contextual bar
- **Team View:** Team Trend charts as primary display, team-level aggregate signals
- **Daily Signal** (from Stage 7): Traffic light + 4 contributing signals displayed per athlete. Coach scans traffic lights across roster, drills into contributing signals for Yellow/Orange athletes.
- **All views** include mandatory disclaimer: "These indicators are informational only and may not be used as a basis for participation, selection, or disciplinary decisions."

#### 10.1.9 Coach Dashboard — Data Refresh Timing

| Metric | Cadence | When |
|--------|---------|------|
| Pattern Stability | Weekly | Monday (after pipeline) |
| Response Recovery | Weekly | Monday |
| Multi-Week Trends | Weekly | Monday |
| Season Phase Overlay | Static | Admin-configured |
| Team Trend | Weekly | Monday |
| Daily Signal (Stage 7) | Daily | Before morning Tune-Up |

Weekly metrics remain unchanged until next pipeline run. Daily Signal is the only metric refreshing daily for coaches.

### 10.2 Parent Dashboard (D2C Premium + Parent Tier Only)

**5 Metrics — all categorical, NO raw numbers shown to parents:**

| Metric | Source | Display | Labels |
|--------|--------|---------|--------|
| **Overall Signal** | Stage 4 Composite Readiness | Large color circle + label | Green = "Looking Strong", Yellow = "Steady", Orange = "Needs Extra Support" |
| **Growth Phase** | Interpretation JSON growth_phase | Text label + 4-step progress bar | "Getting Started" (Emerging), "Building Skills" (Developing), "Showing Consistency" (Consistent), "Leading the Way" (Leadership) |
| **Weekly Theme** | Stage 4 Key Performance Signal | Short phrase (5-10 words) | Agent-generated behavioral summary |
| **Confidence Direction** | Stage 4 Confidence Momentum | Directional label | "Confidence Building", "Confidence Steady", "Confidence Adjusting" |
| **Daily Signal** | Stage 7 traffic light | Color circle + label | GREEN = "Good Day", YELLOW = "Building Day", ORANGE = "Reset Day", GRAY = "No Update Today" |

**Layout Principles:**
- Overall Signal = hero metric (largest, most prominent — what parent sees first)
- Daily Signal = secondary prominence (updates daily, keeps app alive between weekly updates)
- Growth Phase, Weekly Theme, Confidence Direction = supporting context
- Parent Coaching Message linked/embedded from dashboard
- Each metric tappable → expands to corresponding Parent Insight section
- NO negative visual design for Orange (warm tones, no red, no alert icons)
- GRAY is always neutral (no "check in" prompts, no visual suggesting bad)

**Growth Phase display rules:**
- 4-step position bar (shows progress without naming phases)
- Advancing = subtle upward arrow / "Growing" badge
- Stable = no indicator
- Regressing = no visual flag (context handled in Parent Insight narrative)

**Confidence Direction:** "Adjusting" replaces "Variable" for parent-friendlier language.

### 10.3 Warm Placeholders (Parent Dashboard — Early Weeks)

Parents must NEVER see a blank screen.

| Timing | Overall Signal | Growth Phase | Weekly Theme | Confidence Direction | Daily Signal |
|--------|---------------|-------------|-------------|---------------------|-------------|
| **First App Open (pre-program or Day 1)** | Gray, "Building Baseline" + "First update after full week" | "Getting Started" (position 1 of 4) | "First week in progress" | "Building Picture" | If Day 1 data → render normally; else Gray, "Getting Started" |
| **Week 1** | Populated normally | Populated normally | Populated normally | Populated if determinable; else "Still building picture" | Populated normally |
| **Weeks 2-3** | Most metrics populated | Populated | Populated | Populated | Populated |
| **Week 4+** | Fully populated | Fully populated | Fully populated | Fully populated | Fully populated |

### 10.4 Data Refresh Timing

| Metric | Cadence | When |
|--------|---------|------|
| Overall Signal | Weekly | Monday (after pipeline completes) |
| Growth Phase | Weekly | Monday |
| Weekly Theme | Weekly | Monday |
| Confidence Direction | Weekly | Monday |
| Daily Signal | Daily | Before morning Tune-Up release |

Weekly metrics remain unchanged until next week's pipeline runs. Daily Signal is the only metric refreshing daily.

### 10.5 Mandatory Disclaimer (Coach Dashboard)

All coach-facing reports and signals must include:

> "These indicators are informational only and may not be used as a basis for participation, selection, or disciplinary decisions."

---

## 11. Data Storage & Retention

### 11.1 Persistent Storage Requirements

| Data | Mutability | Retention |
|------|-----------|-----------|
| Athlete intake form responses | Immutable after submission | Permanent |
| PPD scores and ABI scores | Computed once at intake, immutable | Permanent |
| Daily event data (raw app interactions) | Immutable per day after hard-out | Program duration + retention period |
| Daily Mini-JSONs | Assembled daily, immutable | Program duration + retention period |
| Weekly Input Objects | Assembled weekly, immutable | Program duration + retention period |
| Interpretation JSONs (Stage 2 output) | Weekly, immutable | Permanent (required for longitudinal analysis) |
| Coaching Messages, Deep Dives, Snippets | Generated outputs, immutable | Permanent |
| Coach Insights, Parent outputs, Team Snapshots | Generated outputs, immutable | Permanent |
| Audit Summaries | Internal QA, immutable | Permanent |
| Stage 7 calibration cache | Per-athlete, updated weekly | Rolling (current + prior week minimum) |
| Athlete Snapshot | One-time, immutable | Permanent |

### 11.2 Cross-Week Data Dependencies

Several computations require data from prior weeks:

| Computation | Data Needed | Minimum History |
|-------------|-------------|----------------|
| Coach flags 13-15 (cross-week escalation) | Prior week's Interpretation JSON | 1 prior week |
| Recovery Score cross-week recovery | Prior week's `recovery_speed_days` | 1 prior week |
| Morning Tune-Up streaks (`current_streak`, `longest_streak`) | ALL prior week Interpretation JSONs | Full program history |
| Cross-week recovery (`cross_week_recovery.recovery_days`) | Prior week's Sunday Missed status | 1 prior week |
| Trend analysis fields | 2+ prior weeks | 2 prior weeks |
| Narrative arc | 2+ prior weeks | 2 prior weeks |
| Pattern Stability Indicator | 4+ weeks | 4 weeks rolling |
| Response Recovery Indicator | 3+ weeks | 3 weeks rolling |
| Multi-Week Trend sparklines | 4-8 weeks | 4 weeks minimum |

### 11.3 Streak Computation

`morning_tune_up.current_streak` and `morning_tune_up.longest_streak` are longitudinal metrics requiring access to ALL prior week data. The backend must either:
- Store streak values cumulatively (update each week), OR
- Read all prior Interpretation JSONs to recompute

---

## 12. Compliance Requirements for Backend

### 12.1 Execution Timing Data — Backend Only

**The single most important compliance rule:**

Execution timing data is computed and used by the backend internally but is **NEVER exposed to coaches, parents, or athletes in any form.** This includes:

| Prohibited from Display | Examples |
|------------------------|---------|
| Completion rates | "80% evening completion rate" |
| Timestamps | "Submitted at 11:43 PM" |
| Login frequency | "Logged in 5 times this week" |
| Session duration | "Spent 12 minutes in app" |
| Reminder dependency | "Needed 3 reminders" |
| Streak counts | "5-day streak" |
| Backfill counts | "Backfilled 2 evenings" |
| Late submission counts | "3 late submissions" |

Only the derived categorical signals (composite score bands, traffic lights, coach flags) reach end users — and only through the AI pipeline's compliance-safe translations.

### 12.2 Journal Privacy

Raw journal text (school/work, sport, home life entries) is athlete-private. Coaches and parents see compliance-safe summaries produced by the AI pipeline only. The backend must never expose raw journal entries in any coach or parent view.

### 12.3 Hard-Out Enforcement

The backend must enforce the hard-out lockout. After the configured hard-out time (default 6:00 AM), no evening review submissions are accepted for the previous day. This is a data integrity requirement — the entire timing model depends on it.

### 12.4 Parent Data Boundary

Parents see the **same data as coaches**, reframed in parent-friendly language by the AI pipeline. The backend does not compute separate parent signals except:
- Parent label mapping in Stage 7 (GREEN → "Good Day", etc.)
- Parent dashboard renders categorical data from Stage 4 + Stage 7 output
- Contributing signals (Day Outcome, Focus Alignment, Follow-Through, Weekly Trajectory) are HIDDEN from parents

### 12.5 Prohibited Metrics (Never Generated or Displayed)

| Category | Examples |
|----------|---------|
| Engagement metrics | Time spent, login counts, screen time, session duration |
| Participation tracking | Streak counts, completion counts, daily completion rates |
| Comparison data | Athlete-to-athlete rankings, team member comparisons by name |
| Surveillance framing | "At-risk" labels, compliance/adherence ratings, effort-based metrics |
| Clinical language | Anxiety, depression, mental health diagnoses, therapeutic terminology |

### 12.6 Approved Language Standards

**Use:** indicator, signal, trend, directional, informational, context, pattern, stability, developmental phase

**Avoid:** compliance, adherence, monitoring, tracking behavior, accountability enforcement, at-risk, discipline, required, evaluation metric

---

## 13. Core Foundation Compatibility

### 13.1 What Core Foundation Is

Core Foundation (CF) is the legacy intake path using PDF weekly recaps instead of daily app interactions. CF is **transitional** — it will phase out as athletes migrate to the App.

### 13.2 Detection

The backend detects input mode via `input_source` field:
- `"app"` → Full app pipeline (daily data + weekly + all execution signals)
- `"core_foundation"` → PDF recap pipeline (weekly only, no execution data)

### 13.3 What CF Athletes Do NOT Receive

| Feature | Available? |
|---------|-----------|
| Daily Mini-JSON | No |
| Composite scores (Section 7) | No — all return "insufficient data" |
| Coach flags | No — empty array |
| Self-ratings alignment | No — "insufficient data" |
| Daily Coaching Snippets (Stage 6) | No |
| Daily Coach Signal (Stage 7) | No |
| Parent Dashboard daily signal | No |
| Execution-enriched coaching output | No — identical to pre-upgrade output |

### 13.4 What CF Athletes DO Receive

| Feature | Available? |
|---------|-----------|
| Interpretation JSON (Stage 2) | Yes — from PDF recap analysis |
| Coaching Message (Stage 3) | Yes — content-derived only |
| Deep Dive (Stage 3) | Yes — content-derived only |
| Parent Coaching Message (Stage 3) | Yes (if parent_inclusion = true) |
| Weekly Performance Insight (Stage 4) | Yes |
| Parent Weekly Insight (Stage 4) | Yes (if applicable) |
| Editorial Audit (Stage 5) | Yes |

### 13.5 CF Fallback Values

When `input_source = "core_foundation"`, the backend populates:

```json
"execution_behavior_signals": {
  "input_source": "core_foundation",
  "morning_tune_up": "/* all fields: 'not available — weekly recap input only' */",
  "evening_review": "/* all fields: 'not available — weekly recap input only' */",
  "composite_scores": {
    "ownership_index": { "score": "insufficient data", "band": "insufficient data" },
    "drift_score": { "score": "insufficient data", "band": "insufficient data" },
    "follow_through_score": { "score": "insufficient data", "band": "insufficient data" },
    "rhythm_score": { "score": "insufficient data", "band": "insufficient data" },
    "review_quality_score": { "score": "insufficient data", "band": "insufficient data" },
    "recovery_score": { "score": "insufficient data", "band": "insufficient data" },
    "reactivity_risk_score": { "score": "insufficient data", "band": "insufficient data" }
  },
  "coach_flags": [],
  "self_ratings_alignment": {
    "confidence_alignment": "insufficient data",
    "habit_consistency_alignment": "insufficient data"
  },
  "execution_pattern_summary": "Core Foundation input — execution behavior signals not available"
}
```

---

## 14. Product Tier Activation Matrix

| Component | D2C Base | D2C Premium | D2C Premium + Parent | Institutional |
|-----------|----------|-------------|---------------------|---------------|
| **Intake Form** | Yes | Yes | Yes | Yes |
| **PPD/ABI Scoring** | Yes | Yes | Yes | Yes |
| **Athlete Snapshot (Stage 1)** | Yes | Yes | Yes | Yes |
| **Daily Mini-JSON Assembly** | Yes | Yes | Yes | Yes |
| **Stage 7 Daily Signal** | No | Yes | Yes | Yes |
| **Stage 6 Daily Snippet** | Yes (7/wk Mon-Sun) | Yes (6/wk Tue-Sun) | Yes (6/wk Tue-Sun) | Yes (6/wk Tue-Sun) |
| **Stage 2 Interpretation** | No | Yes | Yes | Yes |
| **Stage 3 Coaching Message + Deep Dive** | No | Yes | Yes | Yes |
| **Stage 3 Parent Coaching Message** | No | No | Yes | No |
| **Stage 4 Weekly Performance Insight** | No | No | No | Yes |
| **Stage 4 Parent Weekly Insight** | No | No | Yes | No |
| **Stage 4 Weekly Team Snapshot** | No | No | No | Yes (5+ athletes) |
| **Stage 5 Editorial Audit** | No | Yes | Yes | Yes |
| **Coach Dashboard** | No | No | No | Yes |
| **Parent Dashboard** | No | No | Yes | No |
| **Composite Scores (Section 7)** | No | Yes | Yes | Yes |
| **Coach Flags (Section 7)** | No | Yes | Yes | Yes |

**Key conditional logic notes:**

- **Base tier operates standalone** — Mini-JSON + Athlete Snapshot are the only inputs to Stage 6. No weekly pipeline runs. Athletes receive 7 daily snippets per week and nothing else from the AI pipeline.
- **Monday skip (Premium and Institutional)** — Stage 6 does not generate a Monday snippet for Premium or Institutional athletes because they receive the full Coaching Message + Deep Dive on Monday instead. Both tiers produce 6 snippets per week (Tue-Sun). Only Base tier produces 7 snippets per week (Mon-Sun) since Base has no weekly pipeline.
- **Parent outputs gated by `parent_inclusion`** — even in the Premium + Parent tier, Parent CM and Parent Insight are only generated when the athlete's `parent_inclusion` flag is true (Q24 = Yes).
- **Team Snapshot requires 5+ athletes** — if a team or program has fewer than 5 athletes, no Team Snapshot is generated.
- **Stage 5 Audit is internal** — the audit result (PASS / REJECT) is never shown to any end user. It triggers Stage 3 regeneration if the output fails quality checks.

---

## Appendix A: Glossary of Key Terms

| Term | Definition |
|------|-----------|
| **WTD** | Win the Day — 5 yes/no questions scored 0-5 daily |
| **Bullseye Method** | 3-ring focus framework: Center (control), Influence (can affect), Outer (cannot control) |
| **PPD** | Primary Problem Detector — 8-bucket friction identification from intake |
| **ABI** | Athlete Baseline Index — 4-pillar self-assessment (Ownership, Composure, Focus, Structure) |
| **Mini-JSON** | Daily structured data intermediate assembled by backend for AI pipeline consumption |
| **Hard-out** | Lockout time after which evening review submissions are rejected (default 6:00 AM) |
| **Growth Phase** | Developmental stage: Emerging → Developing → Consistent → Leadership |
| **Composite Readiness Signal** | Overall weekly indicator: Positive (Green) / Steady (Yellow) / Attention (Orange) |
| **Traffic Light** | Daily indicator: GREEN / YELLOW / ORANGE / GRAY |
| **Coach Flags** | 15 execution-behavior-derived warnings (monitor / attention / action severity) |
| **Forward Anchor** | Athlete-authored weekly intention: "One thing you can control next week" |
| **RQS** | Reflection Quality Score -- 1-4 scale measuring journaling content depth (1=Surface, 2=Emerging, 3=Clear, 4=Advanced Self-Leadership). Consumed indirectly through Growth Phase progression; never surfaced directly on dashboards. |
| **EI** | Emotional Intensity -- language-based tone classification: Low / Moderate / High / insufficient data. Determines coaching tone calibration and Stage 7 calibration modifiers. |
| **KPS** | Key Performance Signal -- the single most important coaching observation for the week, determined by Stage 4. Appears as Section 8 of Coach Insight and drives Weekly Theme on parent dashboard. |
| **Calibration Cache** | Per-athlete key-value store holding emotional_intensity, growth_phase, growth_phase_movement, last_updated_week from most recent Interpretation JSON. Read by Stage 7 for daily traffic light calibration. Stale after 2 weeks. |
| **Backfill** | Evening review submitted between 2 hours before hard-out and hard-out time (e.g., 4:00-6:00 AM). Next-morning retroactive catch-up. Counted for composite scores but never surfaced to coaches or parents. |
| **Self-Ratings Alignment** | Perception-reality comparison of athlete weekly self-assessment against execution data. Produces Aligned / Conflated / Undervalued per dimension. |
| **Partial Win** | WTD daily score of 2-3 (replaces legacy "Neutral" terminology) |
| **Weekly Input Object** | Weekly structured data package assembled by backend after Sunday hard-out — contains 7 daily event records + 1 weekly check-in. Input to Stage 2 (Interpretation Engine). |
| **CF** | Core Foundation — legacy PDF-based intake/weekly recap system |

---

*Document generated 2026-03-18. Source specifications: VirtusFocus AI Coaching Pipeline v9.7 / v2.0 / v1.7 / v1.4.*
