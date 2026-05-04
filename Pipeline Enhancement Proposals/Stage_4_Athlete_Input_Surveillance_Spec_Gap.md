# Stage 4 Coach Insights / Stage 5 Editorial Audit — Athlete Input Surveillance Spec Gap

**Discovered:** 2026-05-03 (during Focus Group artifact preparation)
**Status:** Documented for post-event resolution
**Target session:** First post-event work session after May 9, 2026
**Severity:** HIGH — affects core privacy/non-surveillance commitment of the product

---

## The Gap in One Paragraph

Stage 4 Coach Insights v1.9 has detailed prohibition rules for **pipeline metadata leaks** (composite score names, coach flag IDs, raw execution metrics, etc.) and Stage 5 Editorial Audit v1.6 Criterion 13 (Pipeline Data Leakage Compliance) catches those metadata leaks via Categories A-G. But neither spec has explicit rules against surfacing **athlete reflective input** — direct verbatim quotes from journal/Bullseye/recap text, references to input mechanisms by name ("Wednesday recap entry", "Competition section recap"), paraphrases of athlete-content that surface what the athlete shared, references to coach-criticism content the athlete wrote, or athlete medical/health information the athlete may not have communicated to staff. The actual pipeline output for Athlete A Wk12 (Grace Kindel) Coach Insight contained all of these violation classes despite passing the existing audit criteria. The gap was caught visually during focus group artifact preparation, not by the audit pipeline.

---

## Concrete Violations Found in Live Pipeline Output

Source file: `Athlete Data/Grace Kindel/Coach Insights/Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.txt` (untouched, preserved as evidence)

**Tier 1 — Direct Verbatim Quotes from Athlete Reflective Input:**
- Section 3: `("the work that I decide each day to put in")` — verbatim Bullseye entry
- Section 3: `("the effort and attitude I portray to how others might [perceive me]")` — verbatim Bullseye entry
- Section 5 (in original/pre-cleanup): verbatim recap quote `('if i get the chance I will perform')`
- Section 6 (in original): full recap entry quoted verbatim including emotional content
- Section 6 (in original): verbatim quote `('idk at this point give me something')`
- Section 8 (in original): verbatim recap quote `('fast asf today tbh, got all my mf bunts down')`

**Tier 2 — Input-Mechanism References:**
- "Wednesday recap entry"
- "the recap entry"
- "Competition section recap"
- "Wednesday entry richest recap content"

**Tier 3 — Athlete-Content Paraphrases:**
- "the athlete maintained composed forward-facing framing across both event days" (no-play game context)
- "A brief frustration response was named within the Wednesday practice context"
- "the athlete is choosing to sustain forward direction regardless"
- "request for external direction (first occurrence in the reporting history)"
- "Coach-athlete friction has re-escalated with practice-specific frustration about positional practice access" (Wk7)
- "outer-ring engagement re-intensified with elevated emotional charge directed at coaching decisions" (Wk7)

**Tier 4 — Reflection-Depth Surveillance:**
- "Reflection depth indicators held at the reduced level for a third consecutive reporting period"
- "Phase advancement indicators not met (reflection depth benchmark not achieved)"
- "Goal-setting specificity remained at the program low for two consecutive weeks" (Wk7)
- "Wednesday entry richest recap content recorded since Week 9"
- "reflection quality at the qualifying tier" (Angelo Wk10)

**Tier 5 — Health/Medical Information Without Communication Context:**
- "A new minor physical-recovery thread (foot rehabilitation) appeared this period with one-period self-managed response"
- (Athlete may not have communicated foot issue to coaching staff yet)

**Tier 6 — Coach-Criticism Content Surfaced TO the Coach:**
- "Coach-athlete friction has re-escalated around positional practice access" (Wk7) — surfaces athlete's reflective content critical of coach's playing-time decisions, surfaced TO that coach
- "playing-time articulation" / "playing-time pattern" descriptions (Wk12)

---

## Why the Existing Audit Doesn't Catch These

Stage 5 v1.6 Criterion 13 detects pipeline metadata vocabulary (Categories A-G):
- A: clinical language
- B: surveillance framing patterns
- C: pipeline classification labels (Composite Readiness Signal, Drift Score, etc.)
- D: numeric score values
- E: execution timing data
- F: intake profile terminology (PPD bucket names, ABI emphasis labels, etc.)
- G: forward anchor terminology

These categories were designed to prevent leakage of the SYSTEM'S internal vocabulary into output. They were not designed to prevent surfacing of the ATHLETE'S OWN INPUT into output. That is a different leak vector entirely.

The "no surveillance framing" check in Category B catches surveillance-style sentences like "the athlete logged 6 of 7 days" but does not catch "the athlete's Wednesday recap contained X" because the latter does not pattern-match as surveillance framing — it pattern-matches as institutional reporting.

---

## Proposed Resolution

### Stage 4 Coach Insights Spec Update (v1.10 or v2.0)

Add to the Prohibited Content section explicit rules:

1. **No verbatim quotes from athlete reflective input.** The Coach Insight body shall not contain any text in quotation marks that originates from athlete-supplied journal text, Bullseye text, recap free-text fields, or weekly check-in free-text fields. Required compliance disclaimer is the only quoted text permitted.

2. **No references to input mechanisms by name.** Phrases such as "recap entry", "journal entry", "Bullseye text", "Competition section recap", "Wednesday entry", "Sunday entry", "his recap", "her journal" are prohibited in the Coach Insight body. The system reads these inputs internally; the coach does not need to know which input mechanism produced a given signal.

3. **No paraphrased athlete reflective content that surfaces what the athlete wrote.** If a system observation cannot be stated as a pattern classification or system-derived signal without referencing what the athlete wrote, it does not belong in the Coach Insight. The boundary: "the system observed pattern X" is acceptable; "the athlete wrote X / felt X / reflected X" is not.

4. **No references to athlete reflection depth, journal length, recap word count, or reflection quality benchmarks.** Surveilling the depth or quantity of athlete reflective input is a privacy violation by itself. The Reflection Quality Score may exist as an internal pipeline signal; the Coach Insight may not surface it as a coaching observation.

5. **No coach-criticism content surfaced to coaching staff.** If athlete reflective content includes criticism of, frustration with, or negative observations about the coaching staff (including playing-time decisions, practice access, communication patterns, etc.), this content shall not be surfaced to the same coaching staff in any form (verbatim, paraphrased, or pattern-summarized). The athlete's reflective space about coaching dynamics is private from the coaches who are the subject of those reflections.

6. **No athlete medical or health information without communicated-to-staff context.** Health observations from athlete reflective input (injury mentions, recovery threads, illness, physical complaints) shall not be surfaced in the Coach Insight unless the system has explicit signal that the athlete has communicated this information to coaching staff via a non-program channel (e.g., medical staff report, athlete-disclosed-to-coach flag). Default: do not surface.

7. **Day-of-week references permitted only for public/scheduled events.** "The Saturday meet" is acceptable when the meet was scheduled and observable. "Wednesday's reflection" is not acceptable. "Sunday banquet" is acceptable when the banquet is a public event. "Sunday journal entry" is not.

### Stage 5 Editorial Audit Spec Update (v1.7)

Add new Criterion 15: Athlete Input Surveillance.

**Tier 1 — MUST PASS, never auto-corrected (matches Criterion 13 severity).**

Detection logic: 8 sub-categories under new Category H.

- **H1 — Direct Verbatim Quote:** any text in quotation marks in the Coach Insight body that is not the required compliance disclaimer
- **H2 — Input Mechanism Reference:** literal string match against prohibited list (recap entry, journal entry, Bullseye text, Competition section recap, his/her/their recap, his/her/their journal, etc.)
- **H3 — Day-Plus-Content Pattern:** day-of-week token (Monday-Sunday) within sentence containing reflective-content vocabulary (entry, articulation, recognition, reflection, naming, frustration, etc.) that is not anchored to a public/scheduled event token (meet, game, competition, championship, banquet, ceremony)
- **H4 — Reflection Surveillance:** literal string match against prohibited list (reflection depth, reflection quality, recap content, journal content, articulation depth, reflection benchmark, goal-setting specificity)
- **H5 — Coach Criticism Surfacing:** sentence containing coach/staff/coaching reference within sentence containing critical/negative vocabulary (friction, frustration, dissatisfaction, criticism, conflict, decision-quality, playing-time)
- **H6 — Health/Medical Reference:** literal string match against prohibited list (rehab, rehabilitation, injury, recovery, sickness, illness, soreness, pain, physical thread, physical-recovery, body-recovery) without paired explicit-disclosure flag
- **H7 — First-Person Athlete-Voice Bleed:** first-person pronouns (I, my, me, mine) appearing inside quoted text in the Coach Insight body
- **H8 — Stated Goal Verbatim Surfacing:** athlete's stated weekly goal text appearing verbatim in the Coach Insight body (must be paraphrased)

**Auto-correction:** None. All Category H violations require regeneration. The auto-correction risk is too high for this category — paraphrasing while preserving meaning requires generative judgment that should not be applied silently after the fact.

### Validation Approach Post-Spec-Update

After v1.10/v2.0 Stage 4 + v1.7 Stage 5 land:
1. Regenerate the 3 Coach Insights flagged in this document
2. Compare regenerated output to the manually-cleaned focus group versions in `Focus Group Materials/Athlete Materials/`
3. Confirm new pipeline output passes the new Criterion 15 audit
4. If new pipeline output materially differs from manual cleanup (i.e., still contains violations), iterate on the prompt rules

---

## Reference Files for the Post-Event Session

- This document: `Pipeline Enhancement Proposals/Stage_4_Athlete_Input_Surveillance_Spec_Gap.md`
- Source pipeline output (preserved, contains violations): `Athlete Data/Grace Kindel/Coach Insights/Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.txt`
- Manually-cleaned focus group version: `Focus Group Materials/Athlete Materials/Grace Kindel/Grace_Kindel_2026-04-20to2026-04-26_VF_WeeklyInsight.txt`
- Stage 4 current spec: `Agents - Generators/Coach Insights Engine/SOP_Coach_Insights_Project_Instructions_v1.9.txt`
- Stage 5 current spec: `Agents - Generators/Editorial Audit/SOP_Editorial_Audit_Project_Instructions_v1.6.txt`
- Stage 5 current Master Prompt: `Agents - Generators/Editorial Audit/SOP_Editorial_Audit_Master_Prompt_v1.6.txt`

---

## Out of Scope for This Spec Update

- Parent-facing output (Stage 3 Parent CM and Stage 4 Parent Insight) uses different rules. Parent output IS allowed to surface positive athlete content, public events, and coaching guidance. This spec gap is specifically about COACH-FACING output.
- Athlete-facing output (Stage 3 CM and Deep Dive) is direct-address to the athlete. Surfacing the athlete's own input back to them is the entire point of the message. Not affected by this gap.
- Daily Coaching Snippet (Stage 6) is athlete-facing. Same logic.
- Daily Coach Signal (Stage 7) is deterministic categorical output with no narrative body. Not affected.

---

## Honest Note on the Original Coach Insight Generation

The pre-cleanup violation pattern in the live pipeline output reflects how the v1.9 Stage 4 spec was written: it asked for institutional-voice analytical reports that explained WHY signals were what they were. The model interpreted "explain the signals" as "reference the input that produced the signals" because that produces a more grounded-feeling report. The model was not wrong relative to the spec — the spec was incomplete. The generation system did its job. The audit system caught what it was told to catch. Neither system was instructed to enforce the boundary between "system-observed pattern" and "athlete-reported content."

This spec gap discovery is exactly the kind of thing focus group artifact prep is supposed to catch. The cost of catching it now (one cleanup session, one spec-fix session post-event) is much lower than catching it in production with real coaches reading real reports about real athletes.
