# VirtusFocus — Project A: AI Coaching Pipeline
**Root Directory:** `D:\OneDrive\Documents\(TEST) Project A\`
**Last Updated:** 2026-03-08
**Session Notes:** Execution Signal Schema Design — Tasks 1-11 complete. Task 11 (Coach Insights Project Instructions v1.2) created new versioned file with execution signal integration guidance for Stage 4 (729 → 1709 lines). Team Snapshot design decision resolved: Option B (execution enrichment in T1, T2, T7 for all-App teams). Core Foundation confirmed as transitional (<20 athletes, phasing out). All execution routing consistent with JSON_logic_reference.txt (Task 10).

---

## What This Project Is

VirtusFocus is a non-clinical athlete mental performance coaching company. This project is building a **5-stage stacked AI pipeline** to replace the current manual "Core Foundation" system, which does not scale to app deployment.

**The pipeline is NOT a chatbot.** It is a structured data pipeline. Each stage reads structured input, applies deterministic rules, and writes structured output. Claude operates as a specialized agent at each stage.

---

## The 5-Stage Pipeline

| Stage | Agent | Status |
|---|---|---|
| 1 | Athlete Snapshot Generator | Built |
| 2 | Interpretation Engine | Built — Active schema: **v9.4** |
| 3 | Coaching Output Engine | Built — Active schema: **v1.5 / V3** |
| 4 | Coach Insights Engine | **Specification upgraded — v1.2** |
| 5 | Editorial Audit | **Specification complete — v1.0** |

---

## CRITICAL OPERATING RULES

### As the Interpretation Engine (Stage 2):
- Read the athlete's baseline snapshot from disk
- Read ALL prior week JSONs from disk (do not ask the user to re-paste)
- Apply all v9.4 schema fields including all 5 new fields and execution_behavior_signals block (see Schema section)
- Write output to: `Athlete Data\[Athlete]\Weekly JSONS\`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_Interpretation.txt`
- Do NOT reinterpret or override JSON classifications downstream

### As the Coaching Output Engine (Stage 3):
- Input: Interpretation JSON only
- Do NOT reinterpret raw recap data
- Do NOT recalculate Win the Day
- Do NOT use clinical language
- Follow all 5 new field usage rules (see below)
- Persona: Coach Arron, head mindset coach of VirtusFocus
- Write Coaching Message to: `Coaching and Deep Dive\Coaching Message\`
- Write Deep Dive to: `Coaching and Deep Dive\Deep Dive\`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_CoachingMessage.txt`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_DeepDive.txt`

### As the Coach Insights Engine (Stage 4):
- Input: Interpretation JSON only (v9.4 schema)
- You are NOT a coach. You do NOT generate athlete-facing content.
- Produce up to TWO compliance-safe outputs per run:
  - **Weekly Performance Insight** — individual athlete dashboard (Sections 1-10), compliance-safe, mandatory disclaimer
  - **Weekly Team Snapshot** — team aggregate dashboard (Sections T1-T7), requires 5+ athletes, positional group variants available
- ALL content must be safe for coaching staff at every organizational level (position coach → coordinator → head coach)
- coach_insights subfields INFORM the output but raw content is NEVER surfaced
- risk_flags, narrative_arc, upcoming_context, longitudinal_metrics stay internal to the pipeline — not surfaced in institutional output
- Clinical language prohibition applies
- Write individual reports to: `Athlete Data\[Athlete]\Coach Insights\`
- Write team snapshots to: `Team Reports\Coach Insights\`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_WeeklyInsight.txt`
- Naming: `{TeamName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_WeeklyTeamSnapshot.txt`

### As the Editorial Audit Agent (Stage 5):
- Input: Interpretation JSON + Coaching Message + Deep Dive (all three required)
- You are NOT a coach. You do NOT generate coaching content. You are a quality gate.
- Run all 12 audit criteria in order. Do not skip any.
- Three possible results: PASS / AUTO-CORRECTED PASS / REJECT AND REGENERATE
- Tier 1 failures always reject. Tier 2 failures auto-correct if possible, else reject. Tier 3 failures auto-correct silently.
- Never add new coaching content — only audit, correct, or reject
- The JSON is truth. If output contradicts JSON, the JSON wins.
- Write Audit Summary to: `Coaching and Deep Dive\Audit Summaries\`
- Write Regeneration Instructions to: `Coaching and Deep Dive\Audit Summaries\`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_AuditSummary.txt`
- Naming: `{FirstName_LastName}_{YYYY-MM-DD}to{YYYY-MM-DD}_VF_RegenerationInstruction.txt`
- Corrected outputs overwrite original files

---

## Active Schema — Interpretation Engine v9.4

### 5 New Fields Added (Pipeline Schema Upgrade — implemented this session)

**1. `prior_commitment_result`**
Tracks execution of previous week's micro_commitment.
- execution_status: Completed / Partial / Not Attempted / Unknown / No Prior Week
- execution_notes: Evidence-based explanation
- carry_forward: Yes / No

**2. `athlete_voice`**
Verbatim athlete language preserved.
- weekly_goal_stated, achievement_statement, key_phrase, mindset_resonance

**3. `narrative_arc`**
Longitudinal developmental story. Requires 2+ prior weeks to populate.
- arc_summary, milestone_this_week, open_thread
- Use "insufficient data" until 2 prior weeks are available

**4. `upcoming_context`**
Forward-looking competition and stressor context.
- scheduled_competition, anticipated_stressor, athlete_stated_next_goal

**5. `emotional_intensity`**
Language-based tone calibration: Low / Moderate / High / insufficient data
- High = explicit breakdown language, homesickness, identity-level crisis statements
- Moderate = friction named but managed
- Low = task-oriented, composed language

### Longitudinal Metrics Thresholds
- narrative_arc: requires 2+ prior weeks
- trend_analysis fields: requires 2+ prior weeks
- longitudinal_metrics full computation: requires 2+ prior weeks
- All fields use "insufficient data" until threshold is met

---

## Key File Locations

### Interpretation Engine
- Master Prompt: `Agents - Generators\Interpretation\SOP - Weekly Interp Prompt v7.3.txt`
- Project Instructions: `Agents - Generators\Interpretation\SOP_Interpretation_Engine_Project_Instructions_v9.4.txt`
- JSON Rules: `Agents - Generators\Interpretation\Source Files\VF_Interpretation_JSON_Rules.txt`
- Composite Score Rules: `Agents - Generators\Interpretation\Source Files\VF_Execution_Signal_Composite_Score_Rules.txt`
- Coach Flags Specification: `Agents - Generators\Interpretation\Source Files\VF_Coach_Flags_Specification.txt`
- App Input Format Specification: `Agents - Generators\Interpretation\Source Files\VF_App_Input_Format_Specification.txt`

### Coaching Output Engine
- Master Prompt: `Agents - Generators\Coaching Output\SOP_Coaching_Output_Master_Prompt_V3.txt`
- Project Instructions: `Agents - Generators\Coaching Output\SOP_Coaching_Output_Instructions_v1.5.txt`
- Message Map: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Output_JSON_to_Message_Map.txt`
- Brand Voice: `Agents - Generators\Coaching Output\Source FIles\brand_voice.txt`
- Brand Themes: `Agents - Generators\Coaching Output\Source FIles\brand_themes.txt`
- Style Guide: `Agents - Generators\Coaching Output\Source FIles\content_style_guide.txt`
- System Identity: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Output_System_Identity.txt`
- Coaching Message Framework: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Message_Framework.txt`
- Deep Dive Framework: `Agents - Generators\Coaching Output\Source FIles\VF_Deep_Dive_Coaching_Analysis_Framework.txt`
- Reflection/Growth Model: `Agents - Generators\Coaching Output\Source FIles\VF_Reflection_Quality_Growth_Phase_Model.txt`

### Coach Insights Engine (Stage 4)
- Master Prompt: `Agents - Generators\Coach Insights Engine\SOP_Coach_Insights_Master_Prompt_v1.1.txt`
- Project Instructions: `Agents - Generators\Coach Insights Engine\SOP_Coach_Insights_Project_Instructions_v1.2.txt`
- JSON Logic Reference: `Agents - Generators\Coach Insights Engine\Source Files\JSON_logic_reference.txt`
- Compliance Framework: `Agents - Generators\Coach Insights Engine\Source Files\VF_Coach_Insights_Compliance_Framework.txt`
- Dashboard Metrics Reference: `Agents - Generators\Coach Insights Engine\Source Files\VF_Coach_Insights_Dashboard_Metrics_Reference.txt`
- Tracking Metrics Reference: `Agents - Generators\Coach Insights Engine\Source Files\VF_Tracking_Reporting_Metrics_Reference.txt`
- Output Structure Master: `Agents - Generators\Coach Insights Engine\Source Files\COACH INSIGHTS OUTPUT STRUCTURE MASTER.txt`
- Monthly Summary Prompt: `Agents - Generators\Coach Insights Engine\(MASTER) Monthly_Institutional_Summary_Master_Prompt.txt`
- Pre-pipeline versions (historical): `v1.0`, `(MASTER) Coach_Insights_Project_Instructions_v2.txt`, `v3.txt`, `Weekly_Coach_Insights_Master_Prompt.txt`
- Model: Opus (recommended for accurate field routing and compliance judgment)
- Outputs: Weekly Performance Insight (individual, 10 sections) + Weekly Team Snapshot (aggregate, 7 sections, 5+ athletes)

### Editorial Audit Agent (Stage 5)
- Master Prompt: `Agents - Generators\Editorial Audit\SOP_Editorial_Audit_Master_Prompt_v1.0.txt`
- Project Instructions: `Agents - Generators\Editorial Audit\SOP_Editorial_Audit_Project_Instructions_v1.0.txt`
- Reference Files: Uses the same 9 source files as the Coaching Output Engine (brand_voice, brand_themes, content_style_guide, System Identity, Message Framework, Deep Dive Framework, Reflection/Growth Model, JSON-to-Message Map, JSON Rules)
- Model: Opus (recommended for judgment-intensive audit criteria)
- Mode: Fully autonomous — PASS / AUTO-CORRECTED PASS / REJECT AND REGENERATE (no human in the loop)

### Execution Signal Strategy Documents (External — Google Shared Drive)
- Strategy: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\VirtusFocus_Execution_Signal_Strategy.md`
- Pillar Signals: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Pillar Based Coaching Signals.md`
- WTD Signal Improvement: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Win The Day App Signal Improvement.md`
- Source Material — WTD: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Source Material - Win the Day System in the Mindset Operating System.md`
- Source Material — Bullseye: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Source Material - Bullseye Method in the Mindset Operating System.md`
- Source Material — Journaling: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Source Material - Daily Journaling in the Mindset Operating System.md`
- Source Material — Motivation Inventory: `G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\Source Material - Weekly Motivation Inventory in the Mindset Operating System.md`

### Versioning Rules (established this session)
- Prompts + Instructions = new versioned files (never edit in place)
- Source reference files (JSON Rules, Message Map) = edit in place
- Previous versions kept on disk for audit trail

---

## Athlete Data Status

### Grace Kindel
**Baseline Snapshot:** `Athlete Data\Grace Kindel\grace_kindel_athlete_snapshot V2.txt`
- baseline_identity_claim: Wants to stay confident in her ability during competition
- baseline_hinge_habit: Immediate reset and refocus after mistakes
- baseline_primary_derailer: Loss of confidence following errors or perceived failure
- baseline_growth_phase: Developing

**Interpretation JSONs — All 5 Weeks Complete:**

| Week | Period | File | Tier | Emotional Intensity | Notes |
|---|---|---|---|---|---|
| 1 | Jan 12–18 | `Grace_Kindel_2026-01-12to2026-01-18_VF_Interpretation.txt` | Growth | Low | No prior week. narrative_arc = insufficient data |
| 2 | Jan 19–25 | `Grace_Kindel_2026-01-19to2026-01-25_VF_Interpretation.txt` | Growth | Low | Prior = Unknown. narrative_arc = insufficient data |
| 3 | Feb 9–15 | `Grace_Kindel_2026-02-09to2026-02-15_VF_Interpretation.txt` | Growth | **High** | Derailer activated. Partially Aligned. narrative_arc activates |
| 4 | Feb 16–22 | `Grace_Kindel_2026-02-16to2026-02-22_VF_Interpretation.txt` | Growth | Moderate | RQS=4 first time. Breakthrough SC at-bat |
| 5 | Feb 23–Mar 1 | `Grace_Kindel_2026-02-23to2026-03-01_VF_Interpretation.txt` | Growth | Low | **Growth phase: Consistent (Advancing).** Max longitudinal (4wk). Full arc embedded. "If I'm given a chance, use it well" |

**Three-System Comparative Analysis — Complete:**
- Analysis file: `Output Comparison\THREE-SYSTEM COMPARATIVE ANALYSIS 3-5-26.txt`
- Compared: Core Foundation (System A) vs Old Project A (System B) vs v1.2/V3 (System C)
- All 30 coaching outputs evaluated across 10 quality dimensions
- 12 Editorial Audit criteria identified and tiered (Tier 1: must-pass, Tier 2: should-pass, Tier 3: quality checks)

**Coaching Output — All 5 Weeks Complete (regenerated under v1.3 rules):**

| Week | Period | Coaching Message | Deep Dive |
|---|---|---|---|
| 1 | Jan 12–18 | `Grace_Kindel_2026-01-12to2026-01-18_VF_CoachingMessage.txt` | `Grace_Kindel_2026-01-12to2026-01-18_VF_DeepDive.txt` |
| 2 | Jan 19–25 | `Grace_Kindel_2026-01-19to2026-01-25_VF_CoachingMessage.txt` | `Grace_Kindel_2026-01-19to2026-01-25_VF_DeepDive.txt` |
| 3 | Feb 9–15 | `Grace_Kindel_2026-02-09to2026-02-15_VF_CoachingMessage.txt` | `Grace_Kindel_2026-02-09to2026-02-15_VF_DeepDive.txt` |
| 4 | Feb 16–22 | `Grace_Kindel_2026-02-16to2026-02-22_VF_CoachingMessage.txt` | `Grace_Kindel_2026-02-16to2026-02-22_VF_DeepDive.txt` |
| 5 | Feb 23–Mar 1 | `Grace_Kindel_2026-02-23to2026-03-01_VF_CoachingMessage.txt` | `Grace_Kindel_2026-02-23to2026-03-01_VF_DeepDive.txt` |

**Historical outputs (pre-schema-upgrade) also on disk:**
- Core Foundation (System A): `VF Core Program Output\` — 10 files (5 messages + 5 deep dives)
- Old Project A (System B): `Coaching and Deep Dive\` — 10 files (prefixed "Old Proejct A")

**Grace Kindel 5-Week Arc:**
Outcome-reactive (baseline) → Preparation-energized (Wks 1–2) → Structure-sustained under pressure (Wk 3: "doing it for me") → Action-proven (Wk 4: "the one chance I got, I did something with") → Identity-embedded (Wk 5: "If I'm given a chance, use it well"). 35/35 Win days.

**Open Thread Heading Into Week 6:**
NC trip begins March 2 (same location as Week 3 emotional strain episode). Florida follows immediately after. Same coach conditions unchanged. Whether Week 4–5 composure holds across back-to-back trips in previously destabilizing environments is the defining arc test.

---

### Tucker Lloyd
**Baseline Snapshot:** `Athlete Data\Tucker Lloyd\tucker_lloyd_snapshot.txt`
- baseline_identity_claim: Developing into a better person and coach within the football environment
- baseline_hinge_habit: Consistent gym attendance and personal discipline routines
- baseline_primary_derailer: Pre-performance focus on what could go wrong
- baseline_growth_phase: Developing

**Interpretation JSONs — All 3 Weeks Complete:**

| Week | Period | File | Tier | Emotional Intensity | Notes |
|---|---|---|---|---|---|
| 1 | Feb 9–15 | `Tucker_Lloyd_2026-02-09to2026-02-15_VF_Interpretation.txt` | Mixed | Low | No prior week. narrative_arc = insufficient data |
| 2 | Feb 16–22 | `Tucker_Lloyd_2026-02-16to2026-02-22_VF_Interpretation.txt` | Mixed | Low | First Missed day (Sunday). Recommitment = insufficient data |
| 3 | Feb 23–Mar 1 | `Tucker_Lloyd_2026-02-23to2026-03-01_VF_Interpretation.txt` | Mixed | Low | 2nd consecutive Missed Sunday. narrative_arc activates. Stagnant consistency trend |

**Coaching Output — All 3 Weeks Complete under v1.4 rules:**

| Week | Period | Coaching Message | Deep Dive |
|---|---|---|---|
| 1 | Feb 9–15 | `Tucker_Lloyd_2026-02-09to2026-02-15_VF_CoachingMessage.txt` | `Tucker_Lloyd_2026-02-09to2026-02-15_VF_DeepDive.txt` |
| 2 | Feb 16–22 | `Tucker_Lloyd_2026-02-16to2026-02-22_VF_CoachingMessage.txt` | `Tucker_Lloyd_2026-02-16to2026-02-22_VF_DeepDive.txt` |
| 3 | Feb 23–Mar 1 | `Tucker_Lloyd_2026-02-23to2026-03-01_VF_CoachingMessage.txt` | `Tucker_Lloyd_2026-02-23to2026-03-01_VF_DeepDive.txt` |

**Coach Insights — All 3 Weeks Complete:**

| Week | Period | Stress | Composite Readiness | Key Signal |
|---|---|---|---|---|
| 1 | Feb 9–15 | Low | → Steady (Yellow) | Self-Directed Structure Consistency |
| 2 | Feb 16–22 | Low | → Steady (Yellow) | Unstructured Day Engagement |
| 3 | Feb 23–Mar 1 | Low | → Steady (Yellow) | Sunday Engagement Structure |

**Tucker Lloyd 3-Week Arc:**
Structure-dependent execution (baseline) → Weekday-strong with emerging Sunday gap (Wk 1) → First Missed day, Sunday disengagement confirmed (Wk 2) → Pattern crystallized — consistent Mixed tier, stagnant consistency trend, gym recovery but Sunday gap repeating (Wk 3). 11/21 Win days. Micro-commitment modality shifted from Written to Behavioral after 2 consecutive non-executions.

**Editorial Audit:** Week 3 audited — PASS on all 12 criteria. Micro-commitment modality adaptation correctly applied (Written → Behavioral). No clinical language violations. No JSON fidelity issues.

---

### Mergim Bushati
**Baseline Snapshot:** `Athlete Data\Mergim Bushati\mergim_bushati_snapshot.txt`
- baseline_identity_claim: Wants to become a national champion by learning to believe in himself and get out of his own head
- baseline_hinge_habit: Consistent training and preparation routines maintained regardless of competitive outcomes or confidence state
- baseline_primary_derailer: Overthinking and self-doubt before and during competitive moments, anchored in avoidance-framed pre-performance thinking
- baseline_growth_phase: Developing

**Interpretation JSONs — All 19 Weeks Complete:**

| Week | Period | File | Tier | Emotional Intensity | Notes |
|---|---|---|---|---|---|
| 1 | Sep 8–14 | `Mergim_Bushati_2025-09-08to2025-09-14_VF_Interpretation.txt` | Mixed | Low | No prior week. narrative_arc = insufficient data |
| 2 | Sep 15–21 | `Mergim_Bushati_2025-09-15to2025-09-21_VF_Interpretation.txt` | Mixed | Low | narrative_arc = insufficient data |
| 3 | Sep 22–28 | `Mergim_Bushati_2025-09-22to2025-09-28_VF_Interpretation.txt` | Growth | Low | First Growth week. Derailer override in practice |
| 4 | Sep 29–Oct 5 | `Mergim_Bushati_2025-09-29to2025-10-05_VF_Interpretation.txt` | Growth | Low | Peak discipline begins |
| 5 | Oct 6–12 | `Mergim_Bushati_2025-10-06to2025-10-12_VF_Interpretation.txt` | Mixed | Low | Wrestle-off disruption, first dip |
| 6 | Oct 13–19 | `Mergim_Bushati_2025-10-13to2025-10-19_VF_Interpretation.txt` | Growth | Low | Recovery bounce, training specificity |
| 7 | Oct 20–26 | `Mergim_Bushati_2025-10-20to2025-10-26_VF_Interpretation.txt` | Growth | Low | First 7/7 Win week |
| 8 | Oct 27–Nov 2 | `Mergim_Bushati_2025-10-27to2025-11-02_VF_Interpretation.txt` | Mixed | Low | Second dip — oscillation pattern confirmed |
| 9 | Nov 3–9 | `Mergim_Bushati_2025-11-03to2025-11-09_VF_Interpretation.txt` | Mixed | Low | Stagnant consistency, self-directed gap |
| 10 | Nov 10–16 | `Mergim_Bushati_2025-11-10to2025-11-16_VF_Interpretation.txt` | Growth | Low | Recovery, self-directed training initiative |
| 11 | Nov 17–23 | `Mergim_Bushati_2025-11-17to2025-11-23_VF_Interpretation.txt` | Growth | Moderate | Competition clearance, competitive preparation |
| 12 | Nov 24–30 | `Mergim_Bushati_2025-11-24to2025-11-30_VF_Interpretation.txt` | Growth | Moderate | Approach-framed execution, Lock Haven cancellation |
| 13 | Dec 1–7 | `Mergim_Bushati_2025-12-01to2025-12-07_VF_Interpretation.txt` | Growth | Low | Peak win rate (0.86). Self-directed Thanksgiving break |
| 14 | Dec 8–14 | `Mergim_Bushati_2025-12-08to2025-12-14_VF_Interpretation.txt` | Mixed | **High** | HAMSTRING INJURY. Peak to worst outcome |
| 15 | Dec 15–21 | `Mergim_Bushati_2025-12-15to2025-12-21_VF_Interpretation.txt` | Mixed | Low | Doctor diagnosis, film study, multi-domain discipline |
| 16 | Dec 22–28 | `Mergim_Bushati_2025-12-22to2025-12-28_VF_Interpretation.txt` | Mixed | Low | Unexpected wrestling return, Sunday self-regulation |
| 17 | Dec 29–Jan 4 | `Mergim_Bushati_2025-12-29to2026-01-04_VF_Interpretation.txt` | Growth | Moderate | BREAKTHROUGH: D1 qualifier takedowns. RQS=4. "I leveled up" |
| 18 | Jan 5–11 | `Mergim_Bushati_2026-01-05to2026-01-11_VF_Interpretation.txt` | Growth | **High** | FIRST COMPETITION: match 1 derailer, match 2 recovery, shoulder re-injury |
| 19 | Jan 12–18 | `Mergim_Bushati_2026-01-12to2026-01-18_VF_Interpretation.txt` | Mixed | Low | Season-ending decision. 19-week arc complete |

**Coaching Output — All 19 Weeks Complete under v1.4 rules:**

| Week | Period | Coaching Message | Deep Dive |
|---|---|---|---|
| 1–19 | Sep 8–Jan 18 | `Mergim_Bushati_*_VF_CoachingMessage.txt` | `Mergim_Bushati_*_VF_DeepDive.txt` |

All 19 Coaching Messages and 19 Deep Dives on disk in `Athlete Data\Mergim Bushati\Coaching and Deep Dive\`.

**Coach Insights — All 19 Weeks Complete:**

| Week | Period | Stress | Composite Readiness | Key Signal |
|---|---|---|---|---|
| 1 | Sep 8–14 | Low | → Steady (Yellow) | Daily Structure Consistency |
| 2 | Sep 15–21 | Low | → Steady (Yellow) | Conditioning Execution Persistence |
| 3 | Sep 22–28 | Low | ↑ Positive (Green) | Pre-Performance Preparation Quality |
| 4 | Sep 29–Oct 5 | Low | ↑ Positive (Green) | Training Goal Execution |
| 5 | Oct 6–12 | Low | → Steady (Yellow) | Self-Directed Structure Consistency |
| 6 | Oct 13–19 | Low | ↑ Positive (Green) | Training Specificity Development |
| 7 | Oct 20–26 | Low | ↑ Positive (Green) | Competition Readiness Execution |
| 8 | Oct 27–Nov 2 | Low | → Steady (Yellow) | Self-Directed Structure Consistency |
| 9 | Nov 3–9 | Low | → Steady (Yellow) | Self-Directed Structure Consistency |
| 10 | Nov 10–16 | Low | ↑ Positive (Green) | Self-Directed Training Initiative |
| 11 | Nov 17–23 | Moderate | ↑ Positive (Green) | Competitive Preparation Readiness |
| 12 | Nov 24–30 | Moderate | ↑ Positive (Green) | Approach-Framed Execution Consistency |
| 13 | Dec 1–7 | Low | ↑ Positive (Green) | Self-Directed Preparation Structure |
| 14 | Dec 8–14 | Elevated | ↓ Attention (Orange) | Adaptive Engagement Under Adversity |
| 15 | Dec 15–21 | Low | → Steady (Yellow) | Multi-Domain Preparation Consistency |
| 16 | Dec 22–28 | Low | → Steady (Yellow) | Recovery Balance Discipline |
| 17 | Dec 29–Jan 4 | Moderate | ↑ Positive (Green) | Competition Mindset Preparation |
| 18 | Jan 5–11 | Elevated | → Steady (Yellow) | Competition Experience Processing |
| 19 | Jan 12–18 | Low | → Steady (Yellow) | Offseason Rehabilitation Commitment |

**Editorial Audit:** Week 18 audited — PASS on all 12 criteria. Highest-complexity case: High EI, Partially Aligned, first competition, derailer activation, shoulder re-injury, Partial prior commitment. No corrections needed. Style note: prefer "mental reframe" over "cognitive reframe" in future outputs.

**Mergim Bushati 19-Week Arc:**
Recovery entry (Wk1-2, shoulder surgery recovery) → Derailer override in practice (Wk3) → Peak discipline cycle with Growth/Mixed oscillation (Wk4-13, 86% peak win rate) → Hamstring injury (Wk14, only ↓ Attention week) → Adaptive recovery (Wk15-16) → Breakthrough return with D1 qualifier takedowns (Wk17, "I leveled up") → First competition: derailer activation match 1, within-tournament recovery match 2, shoulder re-injury (Wk18) → Season-ending decision with forward-looking reframe (Wk19, "figured out a plan for the future"). Zero Missed days across 133 program days.

**Open Thread — Offseason:**
Three developmental threads: (1) Practice-to-competition transfer gap — derailer overridden in practice but activated in tournament match 1; match 2 showed mid-tournament recovery is possible. (2) Shoulder rehabilitation — must be fully resolved before next competitive season. (3) Reflection quality regression (RQS dropped 4→2 in Week 19) — monitor whether depth returns.

---

### Other Athletes (not yet processed under v9.4 schema)
- **John Tastinger** — data exists, no v9.4 JSONs generated

---

## Version Control (Git)

This project is tracked with Git. All meaningful changes must be committed before the session ends.

### When to Commit
- After any schema file change (prompts, instructions, source files)
- After any new athlete output written to disk (interpretation JSONs, coaching messages, deep dives)
- After any prompt or instruction version update
- After any CLAUDE.md update
- After any new agent/generator file is created
- **Always commit before closing a session** so the next session starts from a known state

### Commit Message Format
One sentence describing the *what*. One sentence describing the *why*.
Example: `"Generated Grace Kindel Week 5 Coaching Message and Deep Dive. First full v1.2/V3 coaching output run."`

### What is NOT Tracked (protected by .gitignore)
- `Weekly Reviews/` — Raw athlete recap PDFs (contain personal journal entries and identifiable data)
- Athlete intake PDFs (original intake forms with personal information)
- `.claude/` — Local Claude Code session settings
- Word temp files (`~$*.docx`), OS files, backup files

### How to Ask for a Commit
Say: "Commit what we've done" or "commit this work." Claude will stage the relevant files, write a commit message, and save the snapshot. You don't need to know Git commands.

---

## What's Been Done This Project (Session History)

1. Assessed full project directory and understood pipeline architecture
2. Learned Core Foundation system (current manual GPT-based workflow)
3. Ran Lossy Compression Audit analysis and read Pipeline Schema Upgrade Specification (.docx)
4. Implemented Schema Upgrade — 5 new fields — across 6 files (4 new versioned, 2 in-place)
5. Ran full Interpretation Engine (v9.3) on Grace Kindel Weeks 1–5
6. Ran full Coaching Output Engine (v1.2/V3) on Grace Kindel Week 5
7. Established this CLAUDE.md
8. Ran full Coaching Output Engine (v1.2/V3) on Grace Kindel Weeks 1–4 (all 5 weeks now complete)
9. Completed three-system comparative analysis (30 files, 10 dimensions, 12 audit criteria identified)
10. Initialized Git version control — .gitignore protecting raw athlete data, first commit capturing full project state
11. Built Editorial Audit Agent (Stage 5) specification — Master Prompt v1.0 + Project Instructions v1.0 with 12 tiered audit criteria, clinical language exclusion list, decision tree, auto-correction rules, and regeneration instruction format
12. Ran live validation audits against Grace Kindel Weeks 3 and 5 — both REJECTED on Criterion 2 (clinical language in non-framework Deep Dive sections). Identical systemic pattern confirmed: Stage 3 producing coach-facing sections with clinical terms ("anxiety," "clinical") in the athlete-readable Deep Dive. Coaching Messages passed all 12 criteria in both weeks.
13. Patched Coaching Output Instructions v1.2 → v1.3 — added Deep Dive section boundary rule (5 mandatory sections only), JSON field routing rule (coach_insights/risk_flags to Stage 4), clinical language prohibition with specific terms and replacements, coaching message length target (250-450 words), prior commitment bridge length rule (1-3 sentences). Also refined Audit Agent Criterion 4 sentence limit from 2 to 3.
14. Regenerated all 5 Grace Kindel Deep Dives under v1.3 rules — removed coach-facing sections (Coach Reinforcement, Coach Avoidance, Risk and Compliance Note), fixed coach-directive language in mandatory sections to athlete-facing second person, eliminated clinical terms ("anxiety," "clinical"). Re-audited Weeks 3 and 5 — both PASS all 12 criteria.
15. Addressed remaining comparative analysis gaps — added Growth Phase Progression Thresholds (Section 4C) to VF_Interpretation_JSON_Rules.txt with deterministic criteria for Developing→Consistent and Consistent→Leadership advancement, regression rules, and 2-week minimum dwell time. Added Micro-Commitment Modality Adaptation Rule (Section 10) and Growth Phase Advancement Surfacing Rule (Section 11) to Coaching Output Instructions v1.4. Updated Reflection/Growth Phase Model with progression criteria summary. Promoted Audit Criterion 10 (Micro-Commitment Realism) from Tier 3 to Tier 2 with modality adaptation check logic.
16. Applied growth phase progression thresholds to Grace Kindel Weeks 1-5. Week 5 advances to Consistent (Weeks 1-4 remain Developing — Week 3's Partially Aligned status blocks earlier advancement). Updated Week 5 JSON (growth_phase, growth_phase_movement), Coaching Message (identity thread names phase change), and Deep Dive (Mindset Summary leads with advancement criteria, Trendline shows Advancing). Also cleaned residual "trigger/triggered" clinical language from Weeks 2 and 5 Deep Dives.
17. Built Coach Insights Engine (Stage 4) pipeline-aligned specification v1.0. Upgraded from pre-pipeline v3 to pipeline-aligned architecture. Initial design used two outputs (institutional dashboard + coach strategic brief), but compliance review confirmed all coach-visible content must be institutional-safe across full staff hierarchy (position coach → coordinator → head coach). Revised to single compliance-safe output: Weekly Performance Insight (9 sections). coach_insights subfields inform the output indirectly (Sections 1, 8, 9) but raw content never surfaced. risk_flags, narrative_arc, upcoming_context, longitudinal_metrics stay internal to pipeline. Updated JSON_logic_reference.txt with v9.3 field routing and inform-only rules.
18. Expanded Coach Insights Engine to v1.1 with full dashboard metrics catalog. Added: Composite Readiness Signal (Section 10 — synthesizes Sections 1-6 into single ↑ Positive / → Steady / ↓ Attention indicator with Green/Yellow/Orange color band), Weekly Team Snapshot aggregate output (Sections T1-T7, 5+ athlete minimum, positional group variants), and Dashboard Metrics Reference document defining 6 app-layer metrics: Pattern Stability Indicator (cross-week predictability), Response Recovery Indicator (return-to-Growth speed), Multi-Week Trend Visualization (4-8 week sparklines), Color Coding System (Green/Yellow/Orange), Season Phase Overlay (competitive calendar context), Team Trend Over Time (multi-week aggregate movement). Updated VF_Tracking_Reporting_Metrics_Reference.txt with full v1.1 approved metric taxonomy. All metrics compliance-safe per VF_Coach_Insights_Compliance_Framework.txt.
19. Validated Coach Insights Engine v1.1 against Grace Kindel Weeks 5 and 3. Week 5 exposed Composite Readiness "Not Applicable" recommitment bug — perfect execution (7/7 Wins, no adverse events) produced Yellow instead of Green because "Not Applicable" ≠ "Strong" under literal rules. Patched determination rules in JSON_logic_reference.txt and SOP_Coach_Insights_Project_Instructions_v1.1.txt to treat "Not Applicable" as equivalent to "Strong." Week 3 (HIGH emotional intensity) validated compliance boundaries — zero leakage of coach frustration, personal details, or risk flags. Generated all 5 Weekly Performance Insights for Grace Kindel (Weeks 1-5). First complete Stage 4 run.
20. Processed Tucker Lloyd through full 5-stage pipeline (Stages 2-5). First cross-athlete validation. Generated 3 v9.3 Interpretation JSONs, 3 Coaching Messages (v1.4), 3 Deep Dives (v1.4), and 3 Weekly Performance Insights (v1.1). Tucker is a fundamentally different athlete profile from Grace Kindel: Mixed tier (not Growth), structure-dependent execution (weekday Win / weekend Neutral-Missed), 2 consecutive Missed Sundays, declining goal specificity, stagnant consistency trend. Pipeline handled all differences correctly: Mixed tier → Steady (Yellow) Composite Readiness, Variable consistency signal, micro-commitment modality shift from Written to Behavioral after 2 non-executions. Editorial Audit PASS on all 12 criteria (Week 3 validated).
21. Processed Mergim Bushati through full 5-stage pipeline (Stages 2-5). Longest dataset in pipeline: 19 weeks. Generated 19 v9.3 Interpretation JSONs, 19 Coaching Messages (v1.4), 19 Deep Dives (v1.4), and 19 Weekly Performance Insights (v1.1). Mergim is the third athlete profile validated: Wrestling, 184 lbs, Seton Hill, Developing phase throughout, Growth/Mixed oscillation pattern, two injury events (hamstring Wk14, shoulder re-injury Wk18), first competition with full derailer activation + within-tournament recovery, season-ending decision. Pipeline handled all 19-week complexity correctly including: 2 High EI weeks (Wk14 hamstring, Wk18 competition), only ↓ Attention (Orange) readiness signal in entire pipeline (Wk14), Elevated stress modifier shifting Green→Yellow (Wk18), micro-commitment modality adaptation (ORAL→WRITTEN after Partial execution). Editorial Audit PASS on all 12 criteria (Week 18 validated — highest-complexity case).
22. Execution Signal Strategy review and assessment. Reviewed 7 strategy and source material documents covering the transition from Core Foundation (weekly recap only) to App ecosystem (daily granular data + weekly recap). Assessed integration with current v9.3 Interpretation schema, v1.4 Coaching Output rules, v1.1 Coach Insights specification. Identified 8 risks, resolved all with confirmed design constraints: dual-mode operation mandatory, execution signal is additive enrichment (not replacing), Morning Tune-Up is new input stream, all signals at app launch, 5 overlap resolutions decided (keep/rename/complementary), execution timing data is backend-only (never surfaced to coaches), Core Foundation athletes protected from degradation. Captured all decisions in CLAUDE.md Execution Signal Strategy section. No schema files changed — design-phase only.
23. Execution Signal Schema Design — Task 1 complete: Defined and approved the `execution_behavior_signals` JSON block structure. 6 sub-blocks (morning_tune_up, evening_review, wtd_question_patterns, journaling_behavior, bullseye_behavior, composite_scores) plus coach_flags array and execution_pattern_summary. 50+ fields total. Key decisions: composite scores use numeric 0-100 with categorical bands (not enum-only) for precision in Stage 3 tone calibration and longitudinal sensitivity; streaks included at JSON level for quantitative coaching output; journaling depth_profile added as behavioral execution quality metric (distinct from RQS content quality); bullseye ring_balance expanded with granular center/outer dominant rates and asymmetric thresholds; recovery_speed_days kept at weekly JSON level. Core Foundation fallback rules fully defined. Task 3 (fallback rules) also completed within Task 1 documentation.
24. Execution Signal Schema Design — Task 4 complete: Designed and approved deterministic calculation rules for all 7 composite scores. Batched in three rounds: (1) Ownership Index + Drift Score + Follow-Through Score, (2) Rhythm Score + Review Quality Score, (3) Recovery Score + Reactivity Risk Score. All formulas are weighted multi-component with custom band thresholds per score. Key design decisions: Ownership uses 7-day denominator for all components; Drift uses asymmetric thresholds (Early at 21, not 33) for early detection; Follow-Through renamed "set" to "accept" (athlete accepts presented challenges, field rename mindset_challenge_set_count → mindset_challenge_accepted_count pending for Tasks 6-7); Rhythm uses completed-sessions denominator (not 7) to measure timing quality of actual engagement; Review Quality includes component balance (min/max ratio) to catch cherry-picking; Recovery is event-triggered with 4 states (calculated/no disruption=85/Pending Data/insufficient data); Reactivity uses partial-to-full completion ratio as unique reactivity signal. Cross-week recovery extension approved: new `cross_week_recovery` sub-object in `wtd_question_patterns` resolves Sunday Missed blind spot. New `"Pending Data"` enum value added to `recovery_speed_days` (distinct from "insufficient data" — deferred measurement, not absent data). Rules document saved to `VF_Execution_Signal_Composite_Score_Rules.txt`.
25. Execution Signal Schema Design — Task 5 designed and approved (pending save to disk): Designed the `coach_flags` array — 15 execution-behavior-derived warning flags across 4 batches. Flag object structure: 5 fields (flag_id, severity, label, trigger_source, description). Three severity tiers: monitor (4 flags), attention (8 flags), action (3 flags). Four flag categories: score-band threshold (8 flags: drift_early, drift_active, reactivity_elevated, recovery_failure, ownership_low, follow_through_weak, rhythm_disrupted, review_quality_low), cross-score convergence (2 flags: compound_disengagement, surface_engagement), raw metric pattern (2 flags: component_avoidance, morning_disengagement), cross-week escalation (3 flags: sustained_drift, persistent_attention_pattern, sustained_compound_disengagement). All triggers deterministic. Core Foundation fallback = empty array. coach_flags (execution-behavior-derived) complementary to risk_flags (content-derived), never duplicative. Specification document pending save to `VF_Coach_Flags_Specification.txt`.
26. Execution Signal Schema Design — Task 5 saved to disk: Wrote `VF_Coach_Flags_Specification.txt` to `Agents - Generators\Interpretation\Source Files\`. Complete specification document modeled after `VF_Execution_Signal_Composite_Score_Rules.txt` style — includes flag object structure definition, severity tier definitions with downstream routing, all 15 flag specifications with deterministic trigger conditions and description templates, flag independence rule, cross-week data requirements, Core Foundation fallback, compliance boundary statement (coach_flags vs risk_flags), and downstream routing summary (Stage 3 tone calibration, Stage 4 inform-only, Stage 5 audit verification). Updated CLAUDE.md coach_flags JSON reference and all Task 5 completion markers.
27. Execution Signal Schema Design — Task 2 complete: Defined and approved the app daily input format — the API contract between the app backend and Stage 2 (Interpretation Engine). Weekly Input Object contains 7 daily event records + 1 weekly check-in record. Daily events capture Morning Tune-Up (7 fields including mindset_challenge_accepted, focus_word, quick_win_items) and Evening Review (WTD 5 questions, Journaling 3 domain fields, Bullseye 3 ring arrays, Mindset Challenge follow-through, component sequence). Weekly check-in captures Motivation Inventory (5 questions) and self_ratings (confidence_level and habit_consistency_level, both 1-10 scale — enables perception-reality alignment analysis: conflated/undervalued/aligned self-view vs. execution data). Key design decisions: WTD daily category terminology updated ("Partial Win" replaces "Neutral" for 2-3 range, aligns with positive self-speak model); 4-category evening timing model with hard-out rule (on-time before 10 PM / late 10 PM to backfill boundary / backfill 2 hours before hard-out / missed after hard-out lockout); hard-out time = Morning Tune-Up release (default 6 AM, configurable per program); backfill window = fixed 2-hour constant before hard-out (not configurable); Morning Tune-Up V1 acceptance is mandatory (required to complete — mindset_challenge_accepted retained for future-proofing, null when Tune-Up skipped); Bullseye items as arrays (not free text) for deterministic counting; app tags trigger_method at point of entry; partial data preserved on hard-out lockout (submitted=false but component data available). Core Foundation input format confirmed (recap text only). Specification saved to `VF_App_Input_Format_Specification.txt`. 5 downstream implications flagged for Tasks 6-7.
28. Execution Signal Schema Design — Task 6 complete: First IMPLEMENTATION task. Updated `VF_Interpretation_JSON_Rules.txt` with 10 new classification sections (Sections 6-15) covering all execution_behavior_signals subfields. File expanded from 417 to 1449 lines. New sections: Input Source Classification (dual-mode + Core Foundation fallback), Morning Tune-Up (timeliness_profile thresholds, V1 mandatory acceptance derivation, longitudinal streaks), Evening Review (4-category timing model with hard-out parameter, submitted-only rule for component counts, partial data from hard-out lockout), WTD Question Patterns (yes rates, weakest/strongest question, intraweek volatility, recovery speed days, cross-week recovery), Journaling Behavior (depth_profile word count thresholds, compression detection, domain omission), Bullseye Behavior (completion reliability, ring dominance rates, asymmetric ring balance thresholds, contradiction detection), Self-Ratings Perception-Reality Alignment (tier-based comparison: confidence vs Ownership+Follow-Through, habit consistency vs Rhythm Score — Aligned/Conflated/Undervalued), Composite Score summary table with band thresholds, Coach Flags summary table with structural rules, Execution Pattern Summary generation rules. All 5 downstream implications from Task 2 incorporated: "Partial Win" note added to Section 1A, V1 mandatory acceptance documented, self-ratings classification defined, hard-out time parameter consumption documented, partial data counting rules specified. Old Section 6 (Global Guardrails) renumbered to 16 with execution timing backend-only guardrail added. Old Section 7 (Final Rule) renumbered to 17. self_ratings_alignment sub-block added to execution_behavior_signals (extends approved block per Task 2 deferral).
29. Execution Signal Schema Design — Task 7 complete: Second Stage 2 IMPLEMENTATION task. Created `SOP_Interpretation_Engine_Project_Instructions_v9.4.txt` — new versioned Project Instructions file with dual-input processing workflow. File expanded from 294 to 480 lines, cleanly renumbered to 17 sections + final rule. 5 new sections added: Input Source Detection (Section 3 — app vs core_foundation determination with ambiguous-defaults-to-CF rule), Core Foundation Fallback Rules (Section 6 — skip Steps 12-17, populate fallback values), Cross-Week Data Access (Section 7 — streaks, cross-week recovery, coach flags 13-15, compression detection), No Degradation Rule (Section 8 — Steps 1-11 identical regardless of input_source), Execution Timing Backend-Only Rule (Section 9 — compliance across all pipeline stages). Core Interpretation Process (Section 4) expanded with: Data Source Mapping for App athletes (motivation_inventory → athlete_voice/upcoming_context field routing, daily journaling/Bullseye → content analysis), data source notes at Steps 3/4/5 distinguishing content analysis (v9.3 fields) from metric extraction (execution signals), and new Steps 12-17 for execution behavior signal processing (raw metric extraction, subfield classification, composite score computation, coach flag evaluation, self-ratings alignment, execution pattern summary). Production Schema Validation (Section 11) expanded with 4 new checks for execution_behavior_signals (app-mode completeness, CF-mode fallback verification). Canonical Output Schema (Section 17) expanded with full execution_behavior_signals block including self_ratings_alignment. Authoritative Sources (Section 2) updated with 3 new source files in authority hierarchy. Export filename updated to match established naming convention (_VF_Interpretation.txt). v9.3 file preserved on disk per versioning rules.
30. Execution Signal Schema Design — Task 8 complete: First Stage 3 IMPLEMENTATION task. Updated `VF_Coaching_Output_JSON_to_Message_Map.txt` in place (source reference file, not versioned). File expanded from 131 to 233 lines. Added execution signal routing to all existing Coaching Message and Deep Dive sections. New content: (1) Composite score band routing — all 7 scores mapped to specific sections based on band value. Positive bands (High/Strong/Stable) route to Recognition + Strength Signals/Sections. Concern bands route to Drift Identification + Growth Sections. Recovery Score special handling for Pending Data (name open thread) and no-disruption fixed-85 (no routing). (2) Coach flag routing — global rules section with per-severity-tier section destinations. monitor→subtle tone in Drift/Growth, attention→direct address in Drift/Growth + micro_commitment targets flagged area, action→message leads with flagged pattern + coaching focus areas dominated by flag. compound_disengagement addressed as broad behavioral shift. (3) Self-ratings alignment routing — Conflated→Drift Identification (Coaching Message) + Mindset Summary (Deep Dive) with approved grounding language. Undervalued→Recognition + Identity Anchor (Coaching Message) + Mindset Summary (Deep Dive) with approved elevation language. Prohibited language noted. (4) Execution pattern summary routes to Deep Dive Weekly Overview only (not Coaching Message — summary tone doesn't match coaching voice). (5) Raw metric exclusion rule — explicit list of 7 metric categories that NEVER appear in coaching output. Only composite score bands, flag-driven patterns, self-ratings classifications, and execution_pattern_summary may inform output. (6) Core Foundation athlete rule — when input_source = "core_foundation", all execution routing skipped. (7) Moderate-band routing heuristic — weekly_tier-based: Growth→Strength, Mixed/Reset→Growth. (8) Parent Summary exclusion list expanded with "execution behavior data."
31. Execution Signal Schema Design — Task 10 complete: First Stage 4 IMPLEMENTATION task. Updated `JSON_logic_reference.txt` in place (source reference file, not versioned). File expanded from 246 to 449 lines. Added execution signal inform-only routing for all applicable sections. 4 design decisions resolved: (1) Composite Readiness Step 2.5 — execution signal modifier after Stress Load modifier: action-severity coach flags OR 3+ composite scores in concern bands shift one level toward Attention, not cumulative with each other, cumulative with Stress Load. (2) KPS priority prepend — action flags at priority 0 (highest), attention flags at priority 1.5 (between outer-ring and consistency checks), with compliance-safe signal label translations for all 11 possible flags (compound_disengagement→"Broad Engagement Shift", drift_active→"Engagement Pattern Drift", etc.). (3) Self-ratings confidence adjustment in Section 5 — Conflated shifts one level toward Variable, Undervalued shifts one level toward Building, applied after v9.3 base determination. (4) No Reactivity Risk integration in Stress Load — execution volatility is conceptually distinct from emotional weight, Reactivity Risk routes through KPS and Composite Readiness instead. New file sections: Dual-Mode Awareness (input source with App vs CF routing), per-section Execution Enrichment blocks (Sections 1, 2, 4, 5, 8, 9, 10 — Sections 3, 6, 7 explicitly noted as no execution routing), expanded Inform-Only Fields (composite_scores, coach_flags, self_ratings_alignment, execution_pattern_summary), Execution Signal Raw Metrics Not Consumed (morning_tune_up, evening_review, wtd_question_patterns, journaling_behavior, bullseye_behavior, numeric scores, raw flag content), Execution Signal Compliance Filter (12 prohibited categories including score names, numeric values, band labels, flag IDs, severity tier names, alignment labels), Core Foundation Handling section (7 skip rules). Team Snapshot execution routing deferred to Task 11 (Instructions).
32. Execution Signal Schema Design — Task 9 complete: Second Stage 3 IMPLEMENTATION task. Created `SOP_Coaching_Output_Instructions_v1.5.txt` — new versioned Instructions file with execution signal integration rules. File expanded from 414 to ~700 lines, 12 to 18 sections. 4 existing sections expanded: Section 2 (added Composite Score Rules + Coach Flags Spec to authority list), Section 3 (v9.4 dual-mode awareness — App vs Core Foundation), Section 4 (7 new execution signal field usage rules in NEW FIELD USAGE RULES block), Section 6 (execution fields added to 3 routing categories + new 4th category "FIELDS THAT DO NOT APPEAR IN ANY COACHING OUTPUT" for raw metrics). Section 10 expanded with Coach Flag Interaction Rule (flag directs micro-commitment topic, modality rule directs format, both apply simultaneously). 6 new sections: Section 12 Execution Signal Integration Rule (master rule — sharpens not expands, convergence/divergence handling, v9.3 fields remain foundation), Section 13 Composite Score Tone Calibration Rule (per-score behavioral translations with example phrases, score directionality, moderate-band heuristic, consolidation rule against score-by-score listing), Section 14 Coach Flag Integration Rule (monitor=subtle tone adjustment, attention=direct behavioral address + micro-commitment targeting, action=primary direction shift with compound_disengagement as broad shift, EI + action flag priority subsection — empathy leads and flag woven into empathetic frame), Section 15 Self-Ratings Alignment Integration Rule (Conflated=gentle grounding with approved/prohibited language, Undervalued=elevate with evidence, dual-dimension independent handling, insufficient data handling), Section 16 Core Foundation Execution Skip Rule (binary check — skip Sections 12-17, output identical to v1.4), Section 17 Raw Metric Exclusion Rule (compliance rule — 7 prohibited categories, WRONG vs CORRECT examples, same classification as Clinical Language Prohibition). v1.4 preserved on disk per versioning rules.

33. Execution Signal Schema Design — Task 11 complete (prior session): Second Stage 4 IMPLEMENTATION task. Created `SOP_Coach_Insights_Project_Instructions_v1.2.txt` — new versioned Project Instructions file with execution signal integration guidance. File expanded from 729 to 1709 lines, 15 to 18 sections. 4 existing sections expanded: Section 1 (v9.4 schema reference, execution_behavior_signals awareness), Section 3 (3 new authoritative sources: Composite Score Rules, Coach Flags Spec, App Input Format), Section 4 (v9.4 dual-mode awareness, expanded prohibited data list with 17 new execution-related items), Section 6 (per-section execution enrichment HOW-TO guidance for Sections 1, 2, 4, 5, 8, 9, 10 with WRONG/CORRECT examples — Sections 3, 6, 7 explicitly noted as no execution routing). Section 7 expanded with Team Snapshot execution enrichment (Option B): T1 executive summary may reference broad execution stability patterns, T2 enriched by rhythm_score.band distribution, T7 includes team-level Composite Readiness distribution (% Green/Yellow/Orange). Team Snapshot design decision resolved: all team athletes are App athletes (no mixed teams), Core Foundation is transitional (<20 athletes). Section 8 expanded with v9.4 field routing (inform-only execution entries, raw metrics not consumed). Section 12 expanded with execution signal prohibited items (composite score names/values/bands, coach flag IDs/labels/severity tiers, self-ratings labels/values, raw execution metrics). 3 new sections: Section 15 Execution Signal Integration Master Rule (sharpens not expands, convergence/divergence handling, v9.3 foundation), Section 16 Core Foundation Execution Skip Rule (binary check, identical v1.1 output, team snapshot impact note), Section 17 Raw Metric Exclusion Rule (12 prohibited categories with WRONG/CORRECT examples, compliance classification matching clinical language prohibition). Verified fully consistent with JSON_logic_reference.txt (Task 10) across all 7 verification points. v1.1 preserved on disk per versioning rules.

34. Post-Task 11 accuracy correction: Removed phantom prohibited category from v1.2 — "Self-ratings numeric values (1-10 scale)" was listed as prohibited category 13 in both Section 12 and Section 17 of SOP_Coach_Insights_Project_Instructions_v1.2.txt. This was inaccurate: self_ratings numeric values (confidence_level, habit_consistency_level) are raw app input consumed by Stage 2 to produce alignment classifications. The raw 1-10 values do not appear in the Interpretation JSON that Stage 4 reads — Stage 4 only sees the processed classifications (Aligned/Conflated/Undervalued), already prohibited under category 12. Prohibiting data Stage 4 cannot access violates the accuracy standard for a national launch pipeline. Removed from both v1.2 locations. Corrected all CLAUDE.md references from "13 prohibited categories" to "12 prohibited categories" (session history items 31 and 33, completed section Task 10 entry). Task 12 Handoff Prompt created for fresh-session handoff.

---

## Execution Signal Strategy — Design Decisions (Confirmed 2026-03-06)

### Context
VirtusFocus is transitioning from the Core Foundation Program (single weekly check-in via PDF recap) to an App ecosystem (multiple daily inputs, real-time data collection, plus the weekly check-in). The Execution Signal Strategy adds a third signal category — execution-behavior signal — alongside the existing score signal and text signal. This measures *how the athlete uses the system* (timing, completion, sequence, consistency) rather than just *what they scored or wrote*.

### Source Documents
All strategy and source material documents are located at:
`G:\Shared drives\Mindset Coaching\Mindset OS App\Future Docs\Interp to Coaching Signal Improvement\`

Files reviewed:
- `VirtusFocus_Execution_Signal_Strategy.md` — Formal strategy document
- `Pillar Based Coaching Signals.md` — Comprehensive signal design across all pillars
- `Win The Day App Signal Improvement.md` — WTD-specific signal enhancement
- `Source Material - Win the Day System in the Mindset Operating System.md`
- `Source Material - Bullseye Method in the Mindset Operating System.md`
- `Source Material - Daily Journaling in the Mindset Operating System.md`
- `Source Material - Weekly Motivation Inventory in the Mindset Operating System.md`

### Confirmed Design Constraints

**1. Dual-Mode Operation (MANDATORY)**
The pipeline must handle both Core Foundation athletes (weekly recap only) and App athletes (daily granular data + weekly recap) simultaneously. The `execution_behavior_signals` JSON block will include an `input_source` indicator (`"core_foundation"` vs `"app"`). When source is Core Foundation, all execution subfields populate with `"not available — weekly recap input only"` and all composite scores = `"insufficient data"`. Core Foundation athletes receive identical quality output to what they receive today — execution signal is additive enrichment, never a scoring dependency. No existing field calculation, growth phase threshold, consistency classification, or coaching output routing changes based on whether execution data is present.

**2. Execution Signal Is Additive, Not Replacing**
All existing v9.3 schema fields remain valid and unchanged. The `execution_behavior_signals` block sits alongside existing fields. The 5-stage pipeline architecture is unchanged. WTD scoring, Bullseye classification, RQS, growth phase progression, and all existing deterministic rules remain as-is.

**3. Morning Tune-Up Is a New Input Stream**
The Morning Mindset Tune-Up transitions from passive (email-only, non-interactive) in Core Foundation to interactive and trackable in the App. This requires: (a) a new input format definition, (b) new Interpretation Engine processing steps, (c) new JSON fields. The current pipeline has no Tune-Up data source.

**4. All Execution Signals Available at App Launch**
No phased rollout. No `"available": true/false` gating per signal. The full execution signal set ships with the app. (Earlier V1/V1.5/V2 phasing references in source docs are superseded.)

### Overlap Resolutions (All Five Decided)

| Existing Field | New Signal | Resolution |
|---|---|---|
| `reflection_quality_score` (RQS 1-4, content quality) | Review quality metric (behavioral execution quality) | **Keep both. Rename new one → `review_quality_score`.** RQS measures journaling content depth. `review_quality_score` measures behavioral execution quality (completeness, timing, Bullseye engagement). |
| `recommitment_signal` (Strong/Moderate/Low) | Recovery Score | **Complementary. Both exist. Used in tandem** for deeper recovery understanding. `recommitment_signal` measures within-week post-Missed-day rebound. Recovery Score measures broader execution recovery patterns. |
| `risk_flags` (content-derived warnings) | Coach Flags (execution-behavior-derived warnings) | **Clear boundary.** `risk_flags` = content-derived warnings from recap text. `coach_flags` = execution-behavior-derived warnings from app usage patterns. |
| `consistency_signal` + `trend_analysis` (declining pattern detection) | Drift Score | **Complementary scope.** Existing fields detect score-based declining patterns. Drift Score adds execution-behavior dimension (timing decay, completion drop-off, engagement compression) for more nuanced detection. |
| `emotional_intensity` + `noise_fixation_present` | Reactivity Risk Score | **Complementary scope.** Existing fields measure language-based and Bullseye-based reactivity. Reactivity Risk Score adds execution-behavior dimension (timing patterns, completion volatility). |

### Compliance Ruling — Execution Data Is Backend Only (CRITICAL)

**Execution timing data CANNOT be surfaced to coaching staff.** This is the single most important compliance decision.

The pipeline collects and processes execution behavior data internally to produce *better* compliance-safe output, but raw execution data (completion rates, timing, backfill counts, reminder dependence, late submission counts) NEVER reaches coaching staff in any form.

This follows the same "inform-only" routing pattern already established for `coach_insights` subfields in Stage 4. The `execution_behavior_signals` block will be classified as inform-only for Stage 4, identical to how `coach_insights.routine_execution_summary` currently informs Section 1 but is never reproduced.

This ruling aligns with `VF_Coach_Insights_Compliance_Framework.txt` which already prohibits:
- Time spent in app
- Daily completion counts
- Last login timestamps
- Engagement scores
- Compliance or adherence ratings
- Streak counts

### How Execution Signal Flows Through the Pipeline

**Stage 2 (Interpretation Engine):** Processes both weekly recap AND daily app data. Produces the existing v9.3 fields *plus* a new `execution_behavior_signals` block with composite scores and coach flags. Core Foundation athletes get neutral fallback values.

**Stage 3 (Coaching Output Engine):** Consumes `execution_behavior_signals` to *sharpen* existing coaching sections — same structure, same word targets (250-450 words), same 5 Deep Dive sections. Execution data makes recognition more behaviorally specific, drift identification more mechanistic, micro-commitments more targeted, and identity threads more behaviorally grounded. Execution signal does NOT expand the output — it sharpens it.

**Stage 4 (Coach Insights Engine):** `execution_behavior_signals` is an inform-only block. Raw execution data never surfaces. The engine uses it internally to produce better compliance-safe sections (sharper Key Performance Signal, more accurate Composite Readiness, better Coach Context Cue). Completion rates, timing data, and backfill counts never appear in any report.

**Stage 5 (Editorial Audit):** Gets new audit criteria to verify: (a) execution signal language doesn't leak raw metrics into Coaching Output, (b) execution data doesn't leak into Coach Insights, (c) no clinical or surveillance-style framing introduced.

### Approved: `execution_behavior_signals` JSON Block Structure (Task 1 — COMPLETE)

Approved 2026-03-06. Full JSON block with all subfield names, types, enum values, and nesting.

```json
"execution_behavior_signals": {
  "input_source": "app | core_foundation",

  "morning_tune_up": {
    "days_completed": "integer 0-7",
    "days_missed": "integer 0-7",
    "completion_rate": "decimal 0.00-1.00",
    "on_time_count": "integer 0-7",
    "late_count": "integer 0-7",
    "timeliness_profile": "Proactive | Delayed | Reactive | insufficient data",
    "mindset_challenge_accepted_count": "integer 0-7 (renamed from mindset_challenge_set_count)",
    "mindset_challenge_completed_count": "integer 0-7",
    "mindset_challenge_follow_through_rate": "decimal 0.00-1.00",
    "current_streak": "integer (longitudinal — computed from prior weeks)",
    "longest_streak": "integer (longitudinal — all-time program max)"
  },

  "evening_review": {
    "full_completion_count": "integer 0-7",
    "partial_completion_count": "integer 0-7",
    "missed_count": "integer 0-7",
    "completion_rate": "decimal 0.00-1.00 (full only)",
    "on_time_count": "integer 0-7",
    "late_submission_count": "integer 0-7",
    "backfill_count": "integer 0-7",
    "reminder_dependent_count": "integer 0-7",
    "self_initiated_count": "integer 0-7",
    "sequence_integrity": "Intact | Partial | Broken | insufficient data",
    "component_completion": {
      "wtd_completed_count": "integer 0-7",
      "journaling_completed_count": "integer 0-7",
      "bullseye_completed_count": "integer 0-7"
    }
  },

  "wtd_question_patterns": {
    "q1_intention_yes_rate": "decimal 0.00-1.00",
    "q2_challenge_yes_rate": "decimal 0.00-1.00",
    "q3_adversity_yes_rate": "decimal 0.00-1.00",
    "q4_progress_yes_rate": "decimal 0.00-1.00",
    "q5_gratitude_yes_rate": "decimal 0.00-1.00",
    "weakest_question": "Q1 | Q2 | Q3 | Q4 | Q5 | none | insufficient data",
    "strongest_question": "Q1 | Q2 | Q3 | Q4 | Q5 | none | insufficient data",
    "intraweek_volatility": "Low | Moderate | High | insufficient data",
    "recovery_speed_days": "integer 1-7 | not applicable | did not recover | Pending Data | insufficient data",
    "cross_week_recovery": {
      "prior_week_unresolved_miss": "Yes | No",
      "recovery_days": "integer 1-7 | did not recover | not applicable"
    }
  },

  "journaling_behavior": {
    "depth_profile": "Thorough | Adequate | Compressed | Minimal | insufficient data",
    "compression_detected": "Yes | No | insufficient data",
    "domain_omission_pattern": "none | school_work | sport | home_life | multiple | insufficient data"
  },

  "bullseye_behavior": {
    "completion_reliability": "Consistent | Partial | Inconsistent | insufficient data",
    "center_ring_dominant_rate": "decimal 0.00-1.00",
    "outer_ring_dominant_rate": "decimal 0.00-1.00",
    "ring_balance": "Center-Weighted | Balanced | Outer-Weighted | insufficient data",
    "contradiction_detected": "Yes | No | insufficient data"
  },

  "composite_scores": {
    "ownership_index": { "score": "integer 0-100", "band": "High | Moderate | Low | insufficient data" },
    "rhythm_score": { "score": "integer 0-100", "band": "Stable | Variable | Disrupted | insufficient data" },
    "follow_through_score": { "score": "integer 0-100", "band": "Strong | Moderate | Weak | insufficient data" },
    "review_quality_score": { "score": "integer 0-100", "band": "High | Moderate | Low | insufficient data" },
    "recovery_score": { "score": "integer 0-100", "band": "Strong | Moderate | Low | Pending Data | insufficient data" },
    "reactivity_risk_score": { "score": "integer 0-100", "band": "Low | Moderate | Elevated | insufficient data" },
    "drift_score": { "score": "integer 0-100", "band": "None | Early | Active | insufficient data" }
  },

  "coach_flags": "[] (array of flag objects — see VF_Coach_Flags_Specification.txt)",

  "execution_pattern_summary": "string (1-2 sentence behavioral execution summary)"
}
```

**Key Design Decisions in This Block:**

1. **Composite Score Format: Numeric (0-100) with Categorical Bands.** Each composite score is a nested object with `score` (integer 0-100) and `band` (categorical enum). Numeric gives resolution for Stage 3 tone calibration and longitudinal sensitivity. Bands give deterministic classification for Stage 4 compliance-safe routing. Band thresholds are custom per score (defined in Task 4).

2. **Streaks Included at JSON Level.** `current_streak` and `longest_streak` in morning_tune_up are longitudinal metrics computed from prior week JSONs (same pattern as rolling_win_rate_4wk). Used for quantitative coaching output, not gamification.

3. **Journaling depth_profile = Behavioral Execution Quality.** Distinct from RQS (content quality). Measures timing + length + specificity of engagement. An athlete can have RQS=3 + depth_profile=Compressed (insightful but rushed) or RQS=1 + depth_profile=Adequate (lengthy but surface).

4. **Bullseye ring_balance = Granular Version.** Three fields: `center_ring_dominant_rate`, `outer_ring_dominant_rate`, `ring_balance` enum. Asymmetric thresholds: Center-Weighted ≥ 0.60, Outer-Weighted ≥ 0.40 (outer-ring dominance at 0.40 is already a coaching signal).

5. **recovery_speed_days in Weekly JSON.** Integer 1-7 measuring days from Missed (0-1 WTD) to next Win (4-5 WTD). Uses fastest recovery instance when multiple Missed days occur (consistent with recommitment_signal logic).

**Core Foundation Fallback Values:**
- All raw metrics in morning_tune_up, evening_review, wtd_question_patterns, journaling_behavior, bullseye_behavior → `"not available — weekly recap input only"`
- All composite_scores → `{ "score": "insufficient data", "band": "insufficient data" }`
- coach_flags → `[]` (empty array)
- execution_pattern_summary → `"Core Foundation input — execution behavior signals not available"`

### Composite Scores — All 7 Calculation Rules APPROVED (Task 4 Complete)

Full deterministic calculation rules saved to: `Agents - Generators\Interpretation\Source Files\VF_Execution_Signal_Composite_Score_Rules.txt`

| # | Score | Measures | Formula | Bands |
|---|---|---|---|---|
| 1 | **Ownership Index** | Self-initiation vs. reminder dependency | 3-comp (50/30/20) | High 70+ / Mod 40-69 / Low 0-39 |
| 2 | **Drift Score** | Engagement erosion (higher=worse) | 5-comp (25/20/20/20/15) | None 0-20 / Early 21-45 / Active 46+ |
| 3 | **Follow-Through Score** | Mindset Challenge accept-to-execute | 2-comp (70/30) | Strong 75+ / Mod 40-74 / Weak 0-39 |
| 4 | **Rhythm Score** | Timing consistency + sequence | 4-comp (25/25/30/20) | Stable 75+ / Variable 40-74 / Disrupted 0-39 |
| 5 | **Review Quality Score** | Evening Review behavioral depth | 3-comp (40/35/25) | High 70+ / Mod 40-69 / Low 0-39 |
| 6 | **Recovery Score** | Post-disruption execution recovery | 3-comp (60/25/15), event-triggered | Strong 70+ / Mod 40-69 / Low 0-39 |
| 7 | **Reactivity Risk Score** | Volatile execution (higher=worse) | 4-comp (30/25/20/25) | Low 0-25 / Mod 26-50 / Elevated 51+ |

**Key Task 4 Decisions:**
- Follow-Through: "set" renamed to "accept" (athlete accepts presented Mindset Challenge). No sample-size cap.
- Drift: Asymmetric thresholds (Early at 21) for early detection.
- Recovery: Event-triggered with 4 states (calculated / no disruption=85 fixed / Pending Data / insufficient data).
- Cross-week recovery extension added to `wtd_question_patterns` — resolves Sunday Missed blind spot.
- `"Pending Data"` enum added to `recovery_speed_days` and Recovery Score (deferred measurement, not absent data).
- `recommitment_signal` retains "insufficient data" for same case — alignment flagged for future v9.4.

### Coach Flags — 15-Flag Catalog APPROVED (Task 5 Complete)

Full specification saved to: `Agents - Generators\Interpretation\Source Files\VF_Coach_Flags_Specification.txt`

Flag object structure: 5 fields per flag (flag_id, severity, label, trigger_source, description). Description templates contain dynamic variables populated by the Interpretation Engine at runtime.

| # | flag_id | Severity | Category | Trigger |
|---|---|---|---|---|
| 9 | **compound_disengagement** | action | Cross-score | 3+ of 5 scores in worst band |
| 14 | **persistent_attention_pattern** | action | Cross-week | Any attention flag fires in both current + prior week |
| 15 | **sustained_compound_disengagement** | action | Cross-week | compound_disengagement fires in both current + prior week |
| 2 | **drift_active** | attention | Score-band | drift_score.band == "Active" |
| 3 | **reactivity_elevated** | attention | Score-band | reactivity_risk_score.band == "Elevated" |
| 4 | **recovery_failure** | attention | Score-band | recovery_score.band == "Low" (calculated only) |
| 5 | **ownership_low** | attention | Score-band | ownership_index.band == "Low" |
| 6 | **follow_through_weak** | attention | Score-band | follow_through_score.band == "Weak" |
| 7 | **rhythm_disrupted** | attention | Score-band | rhythm_score.band == "Disrupted" |
| 8 | **review_quality_low** | attention | Score-band | review_quality_score.band == "Low" |
| 13 | **sustained_drift** | attention | Cross-week | drift_score.band != "None" in both current + prior week |
| 1 | **drift_early** | monitor | Score-band | drift_score.band == "Early" |
| 10 | **surface_engagement** | monitor | Cross-score | completion ≥ 0.71 + 2/3 quality signals degraded |
| 11 | **component_avoidance** | monitor | Raw metric | Any component at 0 while another ≥ 3 |
| 12 | **morning_disengagement** | monitor | Raw metric | morning ≤ 0.29 + evening ≥ 0.57 |

**Key Task 5 Decisions:**
- Flags ordered by severity descending (action → attention → monitor) in the array.
- Individual worst-band flags fire independently when compound/cross-week flags also fire — additive, not replacing.
- compound_disengagement uses 5 of 7 scores (excludes Recovery and Reactivity).
- persistent_attention_pattern is one generic flag covering all attention-level persistence — trigger_source dynamically populated with persistent flag_ids.
- Cross-week flags (13-15) require prior week JSON read — same pattern as trend_analysis and cross_week_recovery.
- coach_flags (execution-behavior-derived) complementary to risk_flags (content-derived), never duplicative. Neither surfaced to coaching staff.
- Core Foundation fallback: coach_flags = [] (empty array).
- Downstream: monitor → Stage 3 subtle tone. attention → Stage 3 direct address + Stage 4 KPS/CCCue. action → Stage 3 direction shift + Stage 4 dominant signal. Stage 5 → audit verification.

### Design Task Queue

1. ~~Define the `execution_behavior_signals` JSON block — all subfield names, types, enum values, and nesting structure~~ **COMPLETE — approved 2026-03-06**
~~Define the app input format — what daily data looks like when it arrives at Stage 2~~ **COMPLETE — approved 2026-03-07. Spec saved to VF_App_Input_Format_Specification.txt**
3. ~~Define Core Foundation fallback rules — exact neutral-state values for every subfield~~ **COMPLETE — documented in approved block above**
4. ~~Collaboratively design deterministic calculation rules for all 7 composite scores (numeric 0-100 + categorical bands)~~ **COMPLETE — approved 2026-03-06. Rules saved to VF_Execution_Signal_Composite_Score_Rules.txt**
5. ~~Define the `coach_flags` array — flag types, trigger conditions, severity levels~~ **COMPLETE — 15 flags, 3 severity tiers, 4 categories. Saved to VF_Coach_Flags_Specification.txt**
6. ~~Update `VF_Interpretation_JSON_Rules.txt` with new classification sections~~ **COMPLETE — 10 new sections (6-15), old 6→16 with execution timing guardrail, old 7→17. 417→1449 lines. All execution subfield classification rules, self_ratings_alignment sub-block added.**
7. ~~Update `SOP_Interpretation_Engine_Project_Instructions` to new version with dual-input processing~~ **COMPLETE — v9.4 created. 17 sections + final rule. Dual-input workflow (Steps 0-17), data source mapping for App athletes, 5 new sections (Input Source Detection, Core Foundation Fallback, Cross-Week Data Access, No Degradation Rule, Execution Timing Backend-Only Rule). 294→480 lines.**
8. ~~Update `VF_Coaching_Output_JSON_to_Message_Map.txt` with execution signal routing~~ **COMPLETE — 131→288 lines. Composite score band routing (7 scores × positive/concern bands), coach flag routing (3 severity tiers with section-specific destinations), self-ratings alignment routing (Conflated→Drift/Mindset, Undervalued→Recognition/Identity), execution_pattern_summary→Deep Dive Weekly Overview, raw metric exclusion rule, Core Foundation skip rule, moderate-band weekly_tier heuristic.**
9. ~~Update `SOP_Coaching_Output_Instructions` to new version with execution signal usage rules~~ **COMPLETE — v1.5 created. 414→~700 lines. 12→18 sections. 4 existing sections expanded (2, 3, 4, 6, 10), 6 new sections added (Execution Signal Integration Rule, Composite Score Tone Calibration, Coach Flag Integration, Self-Ratings Alignment Integration, Core Foundation Execution Skip, Raw Metric Exclusion). EI + action flag priority defined. Micro-commitment flag interaction rule added.**
10. ~~Update `JSON_logic_reference.txt` with inform-only routing for execution signals~~ **COMPLETE — 246→449 lines. Dual-mode awareness, per-section execution enrichment routing (Sections 1, 2, 4, 5, 8, 9, 10), Composite Readiness Step 2.5 execution modifier, KPS priorities 0/1.5 for coach flags, self-ratings confidence adjustment, inform-only fields expanded, raw metrics not-consumed list, execution signal compliance filter, Core Foundation handling section.**
11. ~~Update `SOP_Coach_Insights_Project_Instructions` to new version~~ **COMPLETE — v1.2 created. 729→1709 lines. 15→18 sections. Dual-mode awareness, per-section execution enrichment guidance (Sections 1, 2, 4, 5, 8, 9, 10 with WRONG/CORRECT examples), Team Snapshot execution enrichment (T1, T2, T7 — Option B), expanded prohibited content, 3 new sections (Execution Signal Integration Master Rule, Core Foundation Execution Skip Rule, Raw Metric Exclusion Rule).**
12. Define new Editorial Audit criteria for execution signal leakage
13. Validate against existing athlete data (Grace Kindel, Tucker Lloyd, Mergim Bushati) to confirm no degradation

---

## What's Next (Pending)

### Execution Signal Schema Design (ACTIVE)
- [x] Define `execution_behavior_signals` JSON block structure (subfields, types, enums) — **APPROVED 2026-03-06**
- [x] Define app input format (what daily data looks like arriving at Stage 2) — **APPROVED 2026-03-07. Spec in VF_App_Input_Format_Specification.txt**
- [x] Define Core Foundation fallback rules (neutral-state values) — **documented in approved block**
- [x] Collaboratively design deterministic calculation rules for all 7 composite scores — **APPROVED 2026-03-06. Rules in VF_Execution_Signal_Composite_Score_Rules.txt**
- [x] Define `coach_flags` array (flag types, trigger conditions, severity) — **COMPLETE. 15 flags saved to VF_Coach_Flags_Specification.txt**
- [x] Update Interpretation Engine JSON Rules — **COMPLETE (Task 6). VF_Interpretation_JSON_Rules.txt updated with 10 new sections.**
- [x] Update Interpretation Engine Project Instructions to new version — **COMPLETE (Task 7). SOP_Interpretation_Engine_Project_Instructions_v9.4.txt created.**
- [x] Update Coaching Output Message Map — **COMPLETE (Task 8). VF_Coaching_Output_JSON_to_Message_Map.txt updated with execution signal routing.**
- [x] Update Coaching Output Instructions to new version — **COMPLETE (Task 9). SOP_Coaching_Output_Instructions_v1.5.txt created.**
- [x] Update Coach Insights JSON Logic Reference — **COMPLETE (Task 10). JSON_logic_reference.txt updated with execution signal inform-only routing.**
- [x] Update Coach Insights Project Instructions to new version (Task 11) — **COMPLETE. SOP_Coach_Insights_Project_Instructions_v1.2.txt created. 729→1709 lines, 15→18 sections.**
- [ ] Define new Editorial Audit criteria for execution signal leakage
- [ ] Validate against existing athlete data to confirm no degradation

### Athlete Pipeline Work
- [ ] Grace Kindel Week 6 (when recap arrives post-Florida trip)
- [ ] John Tastinger — process through v9.4 Interpretation Engine

### Completed
- [x] Coaching Output (v1.2/V3) for Grace Kindel Weeks 1–5 — all on disk
- [x] Three-system comparative analysis — complete
- [x] Git version control — initialized
- [x] Editorial Audit Agent (Stage 5) — specification complete (Master Prompt v1.0 + Project Instructions v1.0)
- [x] Live validation audits — Weeks 3 and 5 audited, systemic issue identified and confirmed
- [x] Coaching Output Engine v1.3 patch — Deep Dive boundary, clinical compliance, length controls
- [x] Deep Dive regeneration — all 5 weeks updated under v1.3 rules, Weeks 3 and 5 re-audited PASS
- [x] Comparative analysis gaps addressed — micro-commitment modality adaptation + growth phase progression thresholds
- [x] Growth phase progression applied — Week 5 Developing → Consistent, outputs updated, clinical language cleaned
- [x] Coach Insights Engine (Stage 4) — specification upgraded to pipeline-aligned v1.0 (single compliance-safe output, all staff levels)
- [x] Coach Insights Engine v1.1 — Composite Readiness Signal, Weekly Team Snapshot, Dashboard Metrics Reference with 6 app-layer metrics
- [x] Coach Insights Engine v1.1 validation — Week 5 + Week 3 validated, Composite Readiness "Not Applicable" patch applied
- [x] Grace Kindel Coach Insights Weeks 1-5 — all 5 Weekly Performance Insights generated and on disk
- [x] Tucker Lloyd full pipeline (Stages 2-5) — 3 weeks processed, first cross-athlete validation, all 12 audit criteria PASS
- [x] Mergim Bushati full pipeline (Stages 2-5) — 19 weeks processed, longest dataset, all 12 audit criteria PASS (Week 18)
- [x] Execution Signal Strategy review and assessment — 7 documents reviewed, 8 risks identified and resolved, all design constraints confirmed, CLAUDE.md updated with decisions
- [x] Execution Signal Schema Design Task 1 — `execution_behavior_signals` JSON block structure approved (50+ fields, 6 sub-blocks, numeric 0-100 composite scores with categorical bands, Core Foundation fallback rules defined)
- [x] Execution Signal Schema Design Task 4 — All 7 composite score calculation rules approved (weighted formulas, custom band thresholds, edge cases). Cross-week recovery extension approved. "Pending Data" enum added. Field rename: set→accepted. Rules saved to VF_Execution_Signal_Composite_Score_Rules.txt.
- [x] Execution Signal Schema Design Task 5 — coach_flags array complete (15 flags, 3 severity tiers, 4 categories). Saved to VF_Coach_Flags_Specification.txt.
- [x] Execution Signal Schema Design Task 2 — App input format specification complete. Weekly Input Object (daily_events[7] + weekly_check_in), 4-category evening timing (on-time/late/backfill/missed with hard-out), "Partial Win" terminology, self-ratings (confidence + habit consistency 1-10), V1 Morning Tune-Up (3 active elements), mindset_challenge_accepted retained. Saved to VF_App_Input_Format_Specification.txt.
- [x] Execution Signal Schema Design Task 6 — VF_Interpretation_JSON_Rules.txt updated with 10 new sections (6-15). 417→1449 lines. All execution subfield classification rules defined. 5 downstream implications from Task 2 incorporated. self_ratings_alignment sub-block added. Old Sections 6-7 renumbered to 16-17.
- [x] Execution Signal Schema Design Task 7 — SOP_Interpretation_Engine_Project_Instructions_v9.4.txt created. 294→480 lines. 17 sections + final rule. Dual-input workflow (Steps 0-17), data source mapping for App athletes, 5 new sections (Input Source Detection, Core Foundation Fallback, Cross-Week Data Access, No Degradation Rule, Execution Timing Backend-Only Rule). Canonical schema expanded with full execution_behavior_signals block.
- [x] Execution Signal Schema Design Task 8 — VF_Coaching_Output_JSON_to_Message_Map.txt updated in place. 131→288 lines. Composite score band routing (7 scores to Coaching Message + Deep Dive sections), coach flag routing (3 severity tiers with section-specific destinations), self-ratings alignment routing (Conflated/Undervalued with approved language), execution_pattern_summary→Deep Dive Weekly Overview, raw metric exclusion rule (7 metric categories prohibited), Core Foundation skip rule, moderate-band weekly_tier heuristic, Parent Summary exclusion expanded.
- [x] Execution Signal Schema Design Task 9 — SOP_Coaching_Output_Instructions_v1.5.txt created. 414→~700 lines, 12→18 sections. 4 existing sections expanded (2, 3, 4, 6, 10), 6 new sections (Execution Signal Integration Rule, Composite Score Tone Calibration with per-score behavioral translations, Coach Flag Integration with per-severity-tier coaching approach + EI priority, Self-Ratings Alignment Integration with dual-dimension handling, Core Foundation Execution Skip, Raw Metric Exclusion compliance rule with WRONG/CORRECT examples). Micro-commitment flag interaction rule added to Section 10.
- [x] Execution Signal Schema Design Task 10 — JSON_logic_reference.txt updated in place. 246→449 lines. Dual-mode awareness (App vs Core Foundation), per-section execution enrichment routing (Sections 1, 2, 4, 5, 8, 9, 10), Composite Readiness Step 2.5 execution modifier (action flags or 3+ concern bands → shift toward Attention), KPS priorities 0/1.5 for coach flags with 11 compliance-safe signal label translations, self-ratings confidence adjustment (Conflated→Variable shift, Undervalued→Building shift), Stress Load unchanged (no Reactivity Risk integration). Inform-only fields expanded (composite_scores, coach_flags, self_ratings_alignment, execution_pattern_summary). Raw metrics not-consumed list. Execution signal compliance filter (12 prohibited categories). Core Foundation handling section. Team Snapshot deferred to Task 11.
- [x] Execution Signal Schema Design Task 11 — SOP_Coach_Insights_Project_Instructions_v1.2.txt created. 729→1709 lines, 15→18 sections. 4 existing sections expanded (1, 3, 4, 6, 7, 8, 12), 3 new sections added (Execution Signal Integration Master Rule, Core Foundation Execution Skip Rule, Raw Metric Exclusion Rule). Per-section execution enrichment HOW-TO guidance for Sections 1, 2, 4, 5, 8, 9, 10 with WRONG/CORRECT examples. Team Snapshot execution enrichment (Option B: T1, T2, T7 — all team athletes are App). Core Foundation confirmed transitional (<20 athletes, phasing out). Verified consistent with JSON_logic_reference.txt across all routing, determination rules, compliance filters, and inform-only fields.

**Grace Kindel Coach Insights — All 5 Weeks Complete:**

| Week | Period | Stress | Composite Readiness | Key Signal |
|---|---|---|---|---|
| 1 | Jan 12–18 | Low | ↑ Positive (Green) | Reset Response Consistency |
| 2 | Jan 19–25 | Low | ↑ Positive (Green) | Daily Structure Consistency |
| 3 | Feb 9–15 | Elevated | → Steady (Yellow) | Controllable Focus Alignment |
| 4 | Feb 16–22 | Moderate | ↑ Positive (Green) | Competition Readiness Execution |
| 5 | Feb 23–Mar 1 | Low | ↑ Positive (Green) | Pre-Competition Preparation Quality |

---

## The VirtusFocus Behavioral System (Reference)

**3 Loops:**
- Intra-day: Daily Mindset Tune-Up → Win the Day scoring → Bullseye Method
- Inter-day: Daily Journaling
- Weekly: Weekly Recap + Motivation Inventory

**Win the Day Scoring:**
- 5 yes/no questions, 0–5 pts/day
- Day: 4–5 = Win, 2–3 = Neutral, 0–1 = Missed
- Week: 28–35 = Growth, 14–27 = Mixed, 0–13 = Reset

**Bullseye Method:**
- Center Ring: Control (effort, preparation, response, routine)
- Middle Ring: Influence (teammates, team culture, body language)
- Outer Ring: Cannot Control (lineup decisions, scores, coach behavior)

**Growth Phases:** Emerging → Developing → Consistent → Leadership

**Reflection Quality Scale:** 1 (Surface) → 2 (Emerging) → 3 (Clear) → 4 (Advanced Self-Leadership)

---

## Compliance Rule (Non-Negotiable)
VirtusFocus is a non-clinical coaching service. All output must use performance and behavioral language only. No clinical, therapeutic, or mental health framing. No exceptions.
