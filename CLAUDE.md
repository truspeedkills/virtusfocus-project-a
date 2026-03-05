# VirtusFocus — Project A: AI Coaching Pipeline
**Root Directory:** `D:\OneDrive\Documents\(TEST) Project A\`
**Last Updated:** 2026-03-05
**Session Notes:** Addressed remaining comparative analysis gaps — micro-commitment modality adaptation rule and growth phase progression thresholds. Coaching Output Engine patched to v1.4. JSON Rules updated with deterministic phase advancement criteria. Audit Criterion 10 promoted from Tier 3 to Tier 2.

---

## What This Project Is

VirtusFocus is a non-clinical athlete mental performance coaching company. This project is building a **5-stage stacked AI pipeline** to replace the current manual "Core Foundation" system, which does not scale to app deployment.

**The pipeline is NOT a chatbot.** It is a structured data pipeline. Each stage reads structured input, applies deterministic rules, and writes structured output. Claude operates as a specialized agent at each stage.

---

## The 5-Stage Pipeline

| Stage | Agent | Status |
|---|---|---|
| 1 | Athlete Snapshot Generator | Built |
| 2 | Interpretation Engine | Built — Active schema: **v9.3** |
| 3 | Coaching Output Engine | Built — Active schema: **v1.4 / V3** |
| 4 | Coach Insights Engine | Built |
| 5 | Editorial Audit | **Specification complete — v1.0** |

---

## CRITICAL OPERATING RULES

### As the Interpretation Engine (Stage 2):
- Read the athlete's baseline snapshot from disk
- Read ALL prior week JSONs from disk (do not ask the user to re-paste)
- Apply all v9.3 schema fields including all 5 new fields (see Schema section)
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

## Active Schema — Interpretation Engine v9.3

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
- Project Instructions: `Agents - Generators\Interpretation\SOP_Interpretation_Engine_Project_Instructions_v9.3.txt`
- JSON Rules: `Agents - Generators\Interpretation\Source Files\VF_Interpretation_JSON_Rules.txt`

### Coaching Output Engine
- Master Prompt: `Agents - Generators\Coaching Output\SOP_Coaching_Output_Master_Prompt_V3.txt`
- Project Instructions: `Agents - Generators\Coaching Output\SOP_Coaching_Output_Instructions_v1.4.txt`
- Message Map: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Output_JSON_to_Message_Map.txt`
- Brand Voice: `Agents - Generators\Coaching Output\Source FIles\brand_voice.txt`
- Brand Themes: `Agents - Generators\Coaching Output\Source FIles\brand_themes.txt`
- Style Guide: `Agents - Generators\Coaching Output\Source FIles\content_style_guide.txt`
- System Identity: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Output_System_Identity.txt`
- Coaching Message Framework: `Agents - Generators\Coaching Output\Source FIles\VF_Coaching_Message_Framework.txt`
- Deep Dive Framework: `Agents - Generators\Coaching Output\Source FIles\VF_Deep_Dive_Coaching_Analysis_Framework.txt`
- Reflection/Growth Model: `Agents - Generators\Coaching Output\Source FIles\VF_Reflection_Quality_Growth_Phase_Model.txt`

### Editorial Audit Agent (Stage 5)
- Master Prompt: `Agents - Generators\Editorial Audit\SOP_Editorial_Audit_Master_Prompt_v1.0.txt`
- Project Instructions: `Agents - Generators\Editorial Audit\SOP_Editorial_Audit_Project_Instructions_v1.0.txt`
- Reference Files: Uses the same 9 source files as the Coaching Output Engine (brand_voice, brand_themes, content_style_guide, System Identity, Message Framework, Deep Dive Framework, Reflection/Growth Model, JSON-to-Message Map, JSON Rules)
- Model: Opus (recommended for judgment-intensive audit criteria)
- Mode: Fully autonomous — PASS / AUTO-CORRECTED PASS / REJECT AND REGENERATE (no human in the loop)

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
| 5 | Feb 23–Mar 1 | `Grace_Kindel_2026-02-23to2026-03-01_VF_Interpretation.txt` | Growth | Low | Max longitudinal (4wk). Full arc embedded. "If I'm given a chance, use it well" |

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

### Other Athletes (not yet processed under v9.3 schema)
- **Tucker Lloyd** — data exists, no v9.3 JSONs generated
- **John Tastinger** — data exists, no v9.3 JSONs generated

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

---

## What's Next (Pending)

### Immediate — Pipeline Refinement
- [ ] Re-run Interpretation Engine on Grace Kindel Weeks 3-5 with updated growth phase progression rules (Weeks 3-5 may now classify as Consistent instead of Developing)
- [ ] Regenerate coaching outputs for any weeks where growth_phase changes

### Athlete Pipeline Work
- [ ] Grace Kindel Week 6 (when recap arrives post-Florida trip)
- [ ] Tucker Lloyd — process through v9.3 Interpretation Engine
- [ ] John Tastinger — process through v9.3 Interpretation Engine

### Completed
- [x] Coaching Output (v1.2/V3) for Grace Kindel Weeks 1–5 — all on disk
- [x] Three-system comparative analysis — complete
- [x] Git version control — initialized
- [x] Editorial Audit Agent (Stage 5) — specification complete (Master Prompt v1.0 + Project Instructions v1.0)
- [x] Live validation audits — Weeks 3 and 5 audited, systemic issue identified and confirmed
- [x] Coaching Output Engine v1.3 patch — Deep Dive boundary, clinical compliance, length controls
- [x] Deep Dive regeneration — all 5 weeks updated under v1.3 rules, Weeks 3 and 5 re-audited PASS
- [x] Comparative analysis gaps addressed — micro-commitment modality adaptation + growth phase progression thresholds

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
