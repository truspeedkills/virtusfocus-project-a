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
| Q1 | What sport do you play? | Free text | Required, 1-50 chars | Snapshot |
| Q2 | What position do you play? | Free text | Required, 1-50 chars | Snapshot |
| Q3 | What team or program are you part of? | Free text | Required, 1-100 chars | Snapshot |
| Q4 | What level do you compete at? | Single select | Middle School, High School, Club/Travel, College, Professional/Semi-Pro, Other | Snapshot, Pipeline (competitive_level calibration) |
| Q5 | How many years have you been competing in your sport? | Single select | Less than 1, 1-2, 3-5, 6-8, 9+ | Snapshot |
| Q6 | What phase of your season are you in right now? | Single select | Off-Season, Pre-Season, In-Season, Post-Season | Snapshot (baseline_season_phase) |

#### Section 2: Self-Assessment Scales (Q7-Q14) — ABI Input

All questions use a 1-5 scale: 1 = Not at all, 5 = Very much.

| # | Question | Pillar | ABI Role |
|---|----------|--------|----------|
| Q7 | I take responsibility for my own development — I don't wait to be told what to work on. | Ownership | Q_a |
| Q8 | When things aren't going well, I look at what I can control rather than blaming others. | Ownership | Q_b |
| Q9 | After a mistake in competition, I can reset and refocus quickly. | Composure | Q_a (also PPD amplifier for Mistake Recovery Lag) |
| Q10 | I stay composed when I feel pressure from coaches, teammates, or the situation. | Composure | Q_b |
| Q11 | I can maintain focus on what matters most, even when there are distractions. | Focus | Q_a |
| Q12 | During competition, I stay locked in on my performance rather than thinking about results. | Focus | Q_b |
| Q13 | I follow a consistent daily routine that supports my performance. | Structure | Q_a (also PPD amplifier for Structure Gap) |
| Q14 | I organize my time well enough that school, sport, and personal life don't constantly conflict. | Structure | Q_b |

#### Section 3: Performance Friction (Q15-Q16) — PPD Input

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q15 | Which of these do you deal with most? Pick 1-3. | Multi-select (1-3) | Overthinking, Confidence going up and down, Hard time letting go of mistakes, Losing focus or getting distracted, Pressure in big moments, Staying motivated or disciplined, Lack of routine or structure, Pressure from coaches or parents | PPD (selection weight +3 per bucket) |
| Q16 | When do these show up the most? Pick 1-2. | Multi-select (1-2) | Big competitions, After a mistake, Being evaluated or watched, Busy or stressful weeks, When expectations are high | PPD (trigger amplifier) |

**Q15 Validation:** Minimum 1, maximum 3 selections. No "Other" option (breaks deterministic PPD scoring).

**Q16 Validation:** Minimum 1, maximum 2 selections.

#### Section 4: Identity & Pressure (Q17-Q19)

| # | Question | Format | Validation | Routes To |
|---|----------|--------|------------|-----------|
| Q17 | Complete this sentence: "The athlete I want to become is someone who..." | Free text | Required, 10-300 chars | Snapshot (identity claim anchor), PPD |
| Q18 | Right before a big moment, what thought usually goes through your head? | Free text | Required, 10-300 chars | PPD (tie-breaker classification), Snapshot |
| Q19 | Name one athlete you admire. What is it about them you want for yourself? | Free text | Required, 10-300 chars | Snapshot (competitor aspiration), Longitudinal |

#### Section 5: Behavioral Patterns (Q20-Q21)

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q20 | When things go wrong in your sport, what's your first reaction? | Single select | Blame the situation, Get frustrated, Try to adjust right away, Reset and refocus | Snapshot (adversity_response_pattern), Pipeline |
| Q21 | How would you describe yourself under adversity? | Single select | I get frustrated but keep going, I shut down for a while, I talk myself through it, I look to others for support | Snapshot (adversity_self_description) |

#### Section 6: Ecosystem (Q22-Q25)

| # | Question | Format | Options | Routes To |
|---|----------|--------|---------|-----------|
| Q22 | How involved are your parents or guardians in your sport? | Single select | Very involved, Supportive and involved, Aware but hands-off, Not involved | Snapshot (Ecosystem), Parent Output calibration |
| Q23 | When you talk about performance at home, what does it usually sound like? | Single select | Mostly supportive listening, A lot of analysis or advice after games, Pressure to perform or meet expectations, We don't discuss sports performance much | PPD (ecosystem amplifier), Snapshot (Ecosystem), Parent CM calibration |
| Q24 | Would you like a parent or guardian to receive weekly updates about your progress? | Yes/No + conditional email | If Yes: email field (validated email format) | Parent Output (gating), Snapshot (parent_inclusion) |
| Q25 | Who do you go to first when something is bothering you about your sport? | Single select | Parents, Coaches, Teammates, Friends outside sport, I handle things on my own | Snapshot (Ecosystem), Parent CM calibration |

#### Section 7: Goals & Commitment (Q26-Q29)

| # | Question | Format | Validation | Routes To |
|---|----------|--------|------------|-----------|
| Q26 | What does success look like for you 6 months from now? | Free text | Required, 10-300 chars | Snapshot |
| Q27 | On a scale of 1-10, how strong is your mental game right now? | Scale 1-10 | Required, integer | Snapshot (mental_game_self_rating), Longitudinal |
| Q28 | How committed are you to working on your mindset? | Single select | All in, Willing to try, Curious but unsure, Someone suggested I do this | Snapshot (commitment_level) |
| Q29 | Anything else you want us to know? | Free text | Optional, 0-500 chars | Snapshot |

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
| **Athlete Snapshot** (narrative) | Q1-Q6, Q17-Q22, Q25-Q29 |
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
| 5 (resets quickly) | +0 |
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
| Big competitions | Pressure Reactivity | Overthinking Loop |
| After a mistake | Mistake Recovery Lag | Confidence Volatility |
| Being evaluated or watched | Overthinking Loop | Confidence Volatility |
| Busy or stressful weeks | Discipline Gap | Focus Drift |
| When expectations are high | Pressure Reactivity | Confidence Volatility |

Athlete selects 1-2 options. Both primary and secondary apply per selection.

#### 2D. Ecosystem Amplifier (Q23 → Ecosystem Friction)

| Q23 Option | Points Added to EF |
|------------|-------------------|
| Mostly supportive listening | +0 |
| A lot of analysis or advice after games | +2 |
| Pressure to perform or meet expectations | +3 |
| We don't discuss sports performance much | +1 |

### 3.4 Layer 3: Tie-Breaker Classification [AI PIPELINE]

The AI agent classifies Q18 (pressure thought free-text) into one of 4 categories. **The backend stores the result but does not compute it.** This classification is returned as part of the Athlete Snapshot.

| Classification | Pattern | Adjustment |
|---------------|---------|------------|
| Avoidance | "Don't mess up," withdrawal language | +1 Overthinking Loop, +1 Pressure Reactivity |
| Proving | "Show them," validation-seeking | +1 Confidence Volatility |
| Obligation | "Can't let them down," duty language | +1 Pressure Reactivity, +1 Ecosystem Friction |
| Approach | "Execute my plan," process-focused | No adjustment (positive indicator) |

**Dual classification allowed** (max 2 categories):
- Avoidance+Obligation, Avoidance+Proving, Proving+Obligation
- When dual: both adjustments apply (e.g., Avoidance+Obligation = +1 OL, +1 PR, +1 PR, +1 EF = +1 OL, +2 PR, +1 EF)

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
| Overthinking Loop | Focus on present-moment anchoring and pre-performance routines |
| Confidence Volatility | Build process-based confidence independent of outcomes |
| Mistake Recovery Lag | Develop in-competition reset sequences and hinge habits |
| Focus Drift / Distraction | Strengthen controllable-focus habits and Bullseye clarity |
| Pressure Reactivity | Build approach-framed pre-performance activation |
| Discipline Gap | Establish minimum daily structure and accountability rhythms |
| Structure Gap | Design and reinforce consistent daily routines |
| Ecosystem Friction | Navigate external pressure while maintaining internal locus of control |

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

- **Minimum 1 selection** for Q15 (form validation enforces this)
- **All buckets score 0** except selected ones after Layer 1 (non-selected buckets can still accumulate via Layers 2-3)
- **Contradictory answers** (e.g., Q9=5 "resets quickly" but selects "Hard time letting go of mistakes"): Score as-is. Snapshot Builder adds narrative note.
- **Layer 3 unclassifiable** (pressure thought too vague): `ppd_tie_breaker_classification = "Unclassified"`, no Layer 3 adjustments applied.

### 3.9 Worked Example: Grace Kindel

**Inputs:**
- Q9 = 3 (moderate reset), Q13 = 4 (decent routine)
- Q15 selections: "Confidence going up and down", "Hard time letting go of mistakes" (2 selections)
- Q16 selections: "Big competitions", "After a mistake"
- Q18 tie-breaker: classified as "Avoidance"
- Q23: "Mostly supportive listening"

**Layer 1 (Selection Weight):**
- Confidence Volatility: +3
- Mistake Recovery Lag: +3

**Layer 2 (Amplifiers):**
- Q9=3 → MRL +1
- Q13=4 → SG +0
- Q16 "Big competitions" → PR +2, OL +1
- Q16 "After a mistake" → MRL +2, CV +1
- Q23 "Mostly supportive" → EF +0

**Layer 3 (Tie-breaker = Avoidance):**
- OL +1, PR +1

**Final Scores:**

| Bucket | L1 | L2 | L3 | Total |
|--------|----|----|----|----- |
| Mistake Recovery Lag | 3 | 1+2=3 | 0 | **6** |
| Pressure Reactivity | 0 | 2 | 1 | 3 |→ not top 3 in this case |
| Confidence Volatility | 3 | 1 | 0 | **4** |
| Overthinking Loop | 0 | 1 | 1 | **2** |→ enters top 3 via tie-break priority |

**Result:** ppd_top_3 = [MRL(6), CV(4), OL(2)], ppd_primary_problem = "Mistake Recovery Lag"

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

**Inputs:** Q7=4, Q8=3, Q9=3, Q10=3, Q11=5, Q12=4, Q13=4, Q14=4

| Pillar | Q_a | Q_b | Calculation | Score | Band |
|--------|-----|-----|-------------|-------|------|
| Ownership | 4 | 3 | round(3.5×2) | **7** | Moderate |
| Composure | 3 | 3 | round(3.0×2) | **6** | Moderate |
| Focus | 5 | 4 | round(4.5×2) | **9** | High |
| Structure | 4 | 4 | round(4.0×2) | **8** | High |

**Total:** 7+6+9+8 = **30** → Band: **Consistent**

**Primary Emphasis:** Lowest=Composure(6), 2nd=Ownership(7), gap=1 ≤ 2 → `["Composure", "Ownership"]`

---

## 5. Daily Data Collection & Mini-JSON

### 5.1 What the App Collects Daily

Each day, the athlete interacts with two components:

**Morning Tune-Up** (before training/school):
- Focus word for the day (free text)
- 3 Quick Win items (short free-text entries)
- Mindset Challenge acceptance (checkbox — V1 is mandatory to complete Tune-Up)
- Mindset Challenge text (displayed by backend, not athlete-authored)
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
  "completion_timestamp": "ISO-8601 datetime | null",
  "trigger_method": "self_initiated | reminder | null",
  "mindset_challenge_accepted": "boolean | null",
  "mindset_challenge_text": "string | null",
  "focus_word": "string | null",
  "quick_win_items": ["string array (3 items) | null"]
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
  "completion_timestamp": "ISO-8601 datetime | null",
  "trigger_method": "self_initiated | reminder | null",
  "wtd": {
    "completed": "boolean",
    "q1_intention": "boolean | null",
    "q2_challenge": "boolean | null",
    "q3_adversity": "boolean | null",
    "q4_progress": "boolean | null",
    "q5_gratitude": "boolean | null"
  },
  "journaling": {
    "completed": "boolean",
    "school_work_entry": "string | null",
    "sport_entry": "string | null",
    "home_life_entry": "string | null"
  },
  "bullseye": {
    "completed": "boolean",
    "center_ring_items": ["string array | null"],
    "influence_ring_items": ["string array | null"],
    "outer_ring_items": ["string array | null"]
  },
  "mindset_challenge_completed": "boolean | null",
  "component_sequence": ["array of component names | null"]
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
    "day_of_week": "Monday | Tuesday | ... | Sunday",
    "program_day_number": "integer (days since athlete started)",
    "week_period": "YYYY-MM-DD to YYYY-MM-DD",
    "days_into_week": "integer 1-7",
    "input_source": "app",
    "tier": "base | premium"
  },
  "morning_tune_up": {
    "completed": "boolean",
    "focus_word": "string | null",
    "quick_win_items": ["string array | null"],
    "mindset_challenge_text": "string | null",
    "mindset_challenge_accepted": "boolean | null"
  },
  "evening_review": {
    "status": "complete | partial | missed",
    "wtd": {
      "completed": "boolean",
      "daily_score": "integer 0-5 | null",
      "category": "Win the Day | Partial Win | Missed the Mark | null",
      "questions": {
        "q1_intention": "boolean | null",
        "q2_challenge": "boolean | null",
        "q3_adversity": "boolean | null",
        "q4_progress": "boolean | null",
        "q5_gratitude": "boolean | null"
      }
    },
    "journaling": {
      "completed": "boolean",
      "school_work_entry": "string | null",
      "sport_entry": "string | null",
      "home_life_entry": "string | null"
    },
    "bullseye": {
      "completed": "boolean",
      "center_ring_items": ["string array | null"],
      "influence_ring_items": ["string array | null"],
      "outer_ring_items": ["string array | null"]
    },
    "mindset_challenge_completed": "boolean | null"
  },
  "running_week_summary": {
    "days_completed": "integer 0-7",
    "win_days": "integer",
    "partial_win_days": "integer",
    "miss_days": "integer",
    "no_data_days": "integer",
    "current_win_streak": "integer",
    "running_weekly_score": "integer"
  }
}
```

### 5.7 Mini-JSON Evening Review Status Rules

| Condition | Status |
|-----------|--------|
| `submitted = true` AND all 3 components completed | `"complete"` |
| `submitted = true` AND 1-2 components completed | `"partial"` |
| `submitted = false` (hard-out lockout or didn't start) | `"missed"` |

### 5.8 Deliberately Excluded Fields (Compliance)

The following fields are **NEVER included in the Mini-JSON** even though the backend collects them:

| Excluded Field | Why |
|---------------|-----|
| `trigger_method` (self_initiated / reminder) | Surfacing would reveal engagement monitoring |
| `completion_timestamp` (exact times) | Timing data is backend-only computation input |
| `reminder_timestamps` | Notification data is private |
| `session_duration` | Time-in-app is prohibited metric |
| `login_count` | Usage frequency is prohibited metric |
| `screen_time` | Engagement measurement is prohibited |
| `evening_timing_category` (on-time/late/backfill) | Backend uses for composite scores, never surfaces |

These fields are collected by the backend for composite score computation (Section 7) but stripped before the Mini-JSON is sent to the AI pipeline.

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
- `confidence_level` compared against Ownership + Follow-Through + Recovery → Aligned / Conflated / Undervalued
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

### 7.2 Composite Score #1: Ownership Index

**Measures:** Self-initiation vs. reminder dependency

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Evening Self-Initiation Rate | 50% | `(self_initiated_count / max(full_completion_count + partial_completion_count, 1)) × 100` | 0-100 |
| C2: Morning Proactivity Rate | 30% | `(morning_on_time_count / max(morning_completed_count, 1)) × 100` | 0-100 |
| C3: Backfill Absence Rate | 20% | `((7 - backfill_count) / 7) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.50 + C2 × 0.30 + C3 × 0.20)`

**Bands:**

| Range | Band |
|-------|------|
| 70-100 | High |
| 40-69 | Moderate |
| 0-39 | Low |

### 7.3 Composite Score #2: Drift Score

**Measures:** Engagement erosion over the week (higher = worse)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Evening Completion Erosion | 25% | Compare first-half vs. second-half evening completion rates. If second-half < first-half: `((first_half_rate - second_half_rate) / max(first_half_rate, 0.01)) × 100`. If equal or improving: 0 | 0-100 |
| C2: Morning Completion Erosion | 20% | Same pattern as C1 but for morning tune-up | 0-100 |
| C3: Late Submission Increase | 20% | `(late_submission_count / max(full_completion_count + partial_completion_count, 1)) × 100` | 0-100 |
| C4: Journaling Compression | 20% | If depth_profile = Compressed or Minimal: proportional score. Thorough/Adequate = 0 | 0-100 |
| C5: Bullseye Disengagement | 15% | `((7 - bullseye_completed_count) / 7) × 100` if bullseye completed < 4; else 0 | 0-100 |

**Final Score:** `round(C1 × 0.25 + C2 × 0.20 + C3 × 0.20 + C4 × 0.20 + C5 × 0.15)`

**Bands (asymmetric — Early threshold at 21 for early detection):**

| Range | Band |
|-------|------|
| 0-20 | None |
| 21-45 | Early |
| 46-100 | Active |

### 7.4 Composite Score #3: Follow-Through Score

**Measures:** Mindset Challenge acceptance-to-execution rate

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Follow-Through Rate | 70% | `(mindset_challenge_completed_count / max(mindset_challenge_accepted_count, 1)) × 100` | 0-100 |
| C2: Acceptance Rate | 30% | `(mindset_challenge_accepted_count / max(morning_completed_count, 1)) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.70 + C2 × 0.30)`

**Bands:**

| Range | Band |
|-------|------|
| 75-100 | Strong |
| 40-74 | Moderate |
| 0-39 | Weak |

**Note:** In V1, Tune-Up completion requires challenge acceptance, so C2 = 100 whenever morning is completed. C2 becomes meaningful in future V2 when acceptance is optional.

### 7.5 Composite Score #4: Rhythm Score

**Measures:** Timing consistency and sequence integrity

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Morning Timing Consistency | 25% | `(morning_on_time_count / max(morning_completed_count, 1)) × 100` | 0-100 |
| C2: Evening Timing Consistency | 25% | `(evening_on_time_count / max(evening_submitted_count, 1)) × 100` | 0-100 |
| C3: Sequence Integrity | 30% | Intact=100, Partial=50, Broken=0, insufficient data=50 | 0-100 |
| C4: Non-Backfill Rate | 20% | `((evening_submitted_count - backfill_count) / max(evening_submitted_count, 1)) × 100` | 0-100 |

**Final Score:** `round(C1 × 0.25 + C2 × 0.25 + C3 × 0.30 + C4 × 0.20)`

**Important:** Rhythm Score uses **completed-sessions denominator** (not 7). This measures timing quality of actual engagement, not penalizing non-engagement (which Ownership and Drift already capture).

**Bands:**

| Range | Band |
|-------|------|
| 75-100 | Stable |
| 40-74 | Variable |
| 0-39 | Disrupted |

### 7.6 Composite Score #5: Review Quality Score

**Measures:** Behavioral execution quality of the evening review

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Full Completion Rate | 40% | `(full_completion_count / 7) × 100` | 0-100 |
| C2: Component Engagement Depth | 35% | Average of (wtd_completed_count + journaling_completed_count + bullseye_completed_count) / 3, as percentage of submitted evenings | 0-100 |
| C3: Component Balance | 25% | `(min_component_count / max(max_component_count, 1)) × 100`. Catches cherry-picking (e.g., always WTD, never journaling) | 0-100 |

**Final Score:** `round(C1 × 0.40 + C2 × 0.35 + C3 × 0.25)`

**Bands:**

| Range | Band |
|-------|------|
| 70-100 | High |
| 40-69 | Moderate |
| 0-39 | Low |

### 7.7 Composite Score #6: Recovery Score

**Measures:** Post-disruption execution recovery. **Event-triggered** — only computed when a disruption occurs.

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: Recovery Speed | 60% | Based on `recovery_speed_days`: 1 day=100, 2 days=80, 3 days=60, 4 days=40, 5 days=20, 6-7 days or "did not recover"=0 | 0-100 |
| C2: Engagement Maintenance | 25% | Evening completion rate in the 3 days following disruption | 0-100 |
| C3: Sequence Preservation | 15% | Whether designed component order was maintained post-disruption | 0-100 |

**Final Score:** `round(C1 × 0.60 + C2 × 0.25 + C3 × 0.15)`

**5 States:**

| State | When | Score | Band |
|-------|------|-------|------|
| Calculated | Disruption occurred and recovery measurable | 0-100 | Strong 70+ / Moderate 40-69 / Low 0-39 |
| No disruption | No Missed or low-WTD day this week | Fixed 85 | Strong |
| Pending Data | Disruption on Sunday (recovery unmeasurable this week) | "Pending Data" | "Pending Data" |
| Insufficient data | First week or no prior data | "insufficient data" | "insufficient data" |
| CF fallback | Core Foundation athlete | "insufficient data" | "insufficient data" |

**Recovery Speed measurement:** Days from a Missed day (WTD 0-1) to next Win day (WTD 4-5). Uses fastest recovery instance when multiple Missed days occur.

**Cross-week recovery:** If a Missed day occurs on Sunday, recovery is measured in the **next week's** early days via `cross_week_recovery.recovery_days` in the weekly Interpretation JSON.

### 7.8 Composite Score #7: Reactivity Risk Score

**Measures:** Volatile execution patterns (higher = worse)

| Component | Weight | Formula | Range |
|-----------|--------|---------|-------|
| C1: WTD Intraweek Volatility | 30% | Standard deviation of daily WTD scores, normalized to 0-100 | 0-100 |
| C2: Sequence Disruption Frequency | 25% | Days where component_sequence deviates from designed order, as % of submitted days | 0-100 |
| C3: Bullseye Contradiction Rate | 20% | Days where outer-ring items > center-ring items, as % of Bullseye-completed days | 0-100 |
| C4: Engagement Incompletion Rate | 25% | `(partial_completion_count / max(full_completion_count + partial_completion_count, 1)) × 100` — ratio of partial to full completions as reactivity signal | 0-100 |

**Final Score:** `round(C1 × 0.30 + C2 × 0.25 + C3 × 0.20 + C4 × 0.25)`

**Bands:**

| Range | Band |
|-------|------|
| 0-25 | Low |
| 26-50 | Moderate |
| 51-100 | Elevated |

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

Compares the athlete's weekly self-assessment (from weekly check-in) against computed execution data.

**Dimension 1: Confidence Alignment**
- Input: `self_ratings.confidence_level` (1-10) vs. average of Ownership Index band + Follow-Through Score band + Recovery Score band
- Mapping: If self-rating suggests high confidence (7-10) but execution bands are Low/Weak/Low → **Conflated**
- If self-rating suggests low confidence (1-4) but execution bands are High/Strong/Strong → **Undervalued**
- Otherwise → **Aligned**

**Dimension 2: Habit Consistency Alignment**
- Input: `self_ratings.habit_consistency_level` (1-10) vs. Rhythm Score band + completion rates
- Same Conflated / Undervalued / Aligned logic

**Output:** Each dimension classified independently.

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
  "date": "YYYY-MM-DD",
  "traffic_light": "GREEN | YELLOW | ORANGE | GRAY",
  "day_outcome": "Aligned | Building | Reset Day | null",
  "focus_alignment": "Centered | Mixed | Drifting | null",
  "follow_through": "Demonstrated | Gap | null",
  "weekly_trajectory": "Building Week | Steady Week | Cooling Week | null",
  "has_data": "boolean",
  "_internal": {
    "point_score": "integer",
    "calibration_applied": "string | null",
    "thresholds": { "green_min": "integer", "yellow_min": "integer" }
  }
}
```

**`_internal` fields are backend-only** — NEVER exposed to coaches, parents, or athletes.

### 8.3 Step 1: Gray State Check

**Execute first, before any scoring.**

If `evening_review.status == "missed"` → Set `traffic_light = "GRAY"`, all contributing signals = `null`, `has_data = false`. **Skip all remaining steps.**

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

#### Weekly Trajectory (from running week summary, after Day 2)

| Condition | Weekly Trajectory |
|-----------|------------------|
| `win_rate >= 0.50` AND `miss_rate <= 0.25` | Building Week |
| `miss_rate >= 0.50` OR (`misses > wins` AND `partials <= 1`) | Cooling Week |
| Everything else | Steady Week |
| Day 1 (insufficient data) | null |

Where:
- `win_rate = win_days / days_completed`
- `miss_rate = (miss_days + no_data_days) / days_completed`

### 8.5 Step 3: Hidden Input Determination

These two inputs contribute to the point score but are **NEVER displayed to anyone**.

#### Reflection Breadth (from journaling)

| Condition | Value |
|-----------|-------|
| Journaling completed with entries in 2+ domains | Broad |
| Journaling completed with entry in exactly 1 domain | Narrow |
| No journaling or all domains empty | None |

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

- **Storage:** Per-athlete key-value store with fields: `emotional_intensity`, `growth_phase`, `growth_phase_movement`, `last_updated_week`
- **Update trigger:** When a new Interpretation JSON arrives from Stage 2
- **Read timing:** When computing each day's traffic light
- **First week (no cache):** Use standard thresholds (Priority 4)
- **Stale cache:** If `last_updated_week` is more than 2 weeks old, fall back to standard thresholds

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
| 10 | Partial week trajectory | Weekly Trajectory computed from available days. Day 1 = null. Day 2+ uses running_week_summary. |
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
- **Daily sequence:** Hard-out → Mini-JSON → Stage 7 → Stage 6 → Tune-Up release with snippet

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
1. Hard-out lockout (default 6:00 AM)
2. Backend assembles Mini-JSON for each athlete
3. Backend computes Stage 7 signal for each athlete (milliseconds)
4. Backend sends Mini-JSON + context to Stage 6 (AI generates snippet)
5. Stage 6 returns snippet (seconds per athlete with batching)
6. Morning Tune-Up released to athlete with snippet attached
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

**Stage 4 generates 1-3 outputs per run:**
- Always (Institutional): Weekly Performance Insight
- Conditional: Parent Weekly Insight (D2C Premium + Parent)
- Conditional: Weekly Team Snapshot (when 5+ athletes on a team)

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

### 10.1 Coach Dashboard (Institutional Tier Only)

**6 Metrics:**

| Metric | Source | Display | Color Coding |
|--------|--------|---------|-------------|
| **Pattern Stability Indicator** | 4+ weeks of weekly_tier + consistency_signal | Predictable / Transitional / Fluctuating | Green / Yellow / Orange |
| **Response Recovery Indicator** | 3+ weeks of tier transitions | Rapid / Moderate / Extended / No Recovery Data | Green / Yellow / Orange / Gray |
| **Multi-Week Trend Visualization** | 4-8 weeks of 8 metrics | Sparkline dots, color-coded, most recent on right | Per-metric color bands |
| **Color Coding System** | All metrics | Green (positive) / Yellow (steady) / Orange (attention) | See table below |
| **Season Phase Overlay** | Administrator-configured dates | Timeline bar with phase dividers | Neutral (informational only) |
| **Team Trend Over Time** | 4+ weeks of team aggregates, 5+ athletes | Stacked area/bar charts, percentages only | Green / Yellow / Orange |

**Pattern Stability Computation:**
- 4+ consecutive same-tier weeks → **Predictable**
- Mix of 2 tiers, 0-1 Reset weeks → **Transitional**
- 3+ tier changes in 4 weeks OR 2+ Reset weeks → **Fluctuating**

**Response Recovery Computation:**
- Non-Growth → Growth next week → **Rapid**
- Non-Growth → Mixed → Growth → **Moderate**
- Non-Growth → 2+ consecutive non-Growth → **Extended**
- All Growth weeks (untested) → **No Recovery Data** (Gray, positive indicator)

**Color Coding (complete mapping):**

| Metric | Green | Yellow | Orange |
|--------|-------|--------|--------|
| Weekly Tier | Growth | Mixed | Reset |
| Consistency | Stable / Improving | Variable (no other negatives) | Variable (with negatives) |
| Stress Load | Low | Moderate | Elevated |
| Confidence | Building | Stable | Variable |
| Focus Distribution | Center-Dominant | Mixed | Outer-Ring Drift |
| Recommitment | Strong | Moderate | Low |
| Composite Readiness | Positive | Steady | Attention |
| Pattern Stability | Predictable | Transitional | Fluctuating |
| Response Recovery | Rapid | Moderate | Extended |

**Important:** Orange ≠ "at-risk." No red color anywhere. No evaluation implication.

**Season Phase Overlay:**
- Administrator sets phase dates at season start (calendar-based, not event-based)
- 5 phases: Pre-Season, Early Season, Mid-Season, Conference, Post-Season
- Displayed as timeline bar beneath trend visualizations

**Team Trend:** Minimum 5 athletes. All percentages, no individual athlete identification.

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
| **Stage 6 Daily Snippet** | Yes (7/wk Mon-Sun) | Yes (6/wk Tue-Sun) | Yes (6/wk Tue-Sun) | Yes (7/wk Mon-Sun) |
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
- **Premium Monday skip** — Stage 6 does not generate a Monday snippet for Premium athletes because they receive the full Coaching Message + Deep Dive on Monday instead.
- **Institutional snippets are 7/week** — no Monday skip because coaches (not just athletes) are the audience, and institutional athletes receive snippets alongside (not instead of) the weekly output.
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
| **Partial Win** | WTD daily score of 2-3 (replaces legacy "Neutral" terminology) |
| **CF** | Core Foundation — legacy PDF-based intake/weekly recap system |

---

*Document generated 2026-03-18. Source specifications: VirtusFocus AI Coaching Pipeline v9.6 / v1.9 / v1.6 / v1.3.*
