# ANX-Bench Behavioral Validation Protocol

## Purpose

This protocol defines a standardized revealed-preference criterion-validity task for ANX-Bench. The task measures whether self-reported AI anxiety predicts a consequential allocation choice when respondents are asked to divide a real or bonus-stated `$1.00` between an AI-only review process and a human review process after reading a high-impact AI decision scenario.

The behavioral measure is not an ANX-Bench item and must not be included in item, construct, domain, overall, longitudinal, or event-study ANX scores. It is a criterion variable used to evaluate whether candidate ANX scores predict behavior beyond self-report comparators.

## Standard Task Definition

Task ID: `revealed_ai_review_allocation_v1`

Task label: revealed AI anxiety bonus-allocation task

Administration placement: after the randomized ANX item block and survey-level comprehension or understanding checks, before demographics whenever demographics are collected inside the survey. If vendor demographics are appended from panel records, the task still appears after the ANX item block and before post-task validation comparators unless a wave preregistration fixes a different order.

Incentive status: the task may be implemented with either real bonus allocation or bonus-stated allocation. The implementation mode must be preregistered and recorded in the behavioral response file. Real bonus allocation is preferred when vendor and IRB constraints permit it. Bonus-stated allocation may be used only when it is clearly described to respondents as a research choice that may not change their compensation.

## Randomized Scenario Arms

Each respondent is assigned exactly one high-impact AI decision scenario arm using equal-probability randomization unless a wave preregistration specifies blocked randomization. The assigned arm is recorded as `randomized_arm`.

| Randomized arm | Domain | High-impact decision context | Core decision described |
| --- | --- | --- | --- |
| `employment_hiring` | economic_vocational | Hiring for a stable full-time job | An AI system screens applications and ranks finalists for hiring review. |
| `healthcare_triage` | safety_catastrophic | Health care priority review | An AI system sorts patients by urgency for follow-up review. |
| `public_benefits` | autonomy_surveillance | Public benefits eligibility | An AI system reviews application records and recommends approval, delay, or audit. |
| `school_placement` | relational | School support placement | An AI system reviews a student record and recommends placement into a higher-support or lower-support track. |

The arms deliberately span high-impact domains while preserving a common decision structure: an AI system has made or prioritized an important recommendation, and the respondent can allocate review resources between AI-only review and human review.

## Participant-Facing Core Wording

Each wave instrument must include exact participant wording. The following text is the canonical source for the task prompt, with only the bracketed randomized scenario paragraph replaced by the assigned arm text:

> The next screen asks you to make a small allocation decision for research.
>
> Please imagine that a person has just received an important decision in the situation below. The decision was first reviewed by an AI system. There is a limited `$1.00` review budget that can be used to check the decision again.
>
> You will divide the `$1.00` between two review options:
>
> AI-only review: the decision is checked again by another automated AI review process.
>
> Human review: the decision is checked again by a trained human reviewer.
>
> Allocate the full `$1.00`. You may put all of it into one option or split it between the two options.

The instrument must state whether the allocation is real bonus allocation or bonus-stated allocation. If real, it must state the implementation rule for converting respondent allocations into payments or review donations. If bonus-stated, it must state that the choice is recorded for research and may not change compensation.

## Allocation UI Rules

The allocation interface must satisfy all rules below:

- Respondents allocate exactly 100 cents.
- `ai_only_review_cents` and `human_review_cents` are integer values from 0 to 100.
- The two allocation fields must sum to 100 before the respondent can continue.
- The interface may use two numeric entry boxes, a two-ended slider with numeric readout, or plus and minus stepper controls. Whatever interface is used, the exported values must be integer cents.
- The interface must not preselect a nonzero allocation. If the platform requires a default visual position, the respondent must still actively confirm or change the allocation before continuing, and the implementation must record an active confirmation flag.
- Response labels must keep the order `AI-only review` then `Human review`.
- The screen must display a live total or validation message so respondents can see whether the full `$1.00` has been allocated.
- The respondent must not be told that human review is the desired answer.

## Comprehension Check

Immediately after the allocation screen, the task must include a required comprehension check:

Question: In the allocation task, what were you asked to divide?

Response options:

1. A `$1.00` review budget between AI-only review and human review.
2. A prediction about whether the AI decision was correct.
3. My own personal medical, school, job, or benefits record.
4. A request to identify a real person who needs review.

Correct response: option 1.

Respondents who fail this check receive behavioral exclusion flag `behavioral_comprehension_failed`. They remain eligible for ANX psychometric analyses if they otherwise pass the preregistered survey-level rules, but they are excluded from confirmatory behavioral criterion-validity models.

## Scoring

The primary behavioral criterion is `revealed_anxiety_score`.

`revealed_anxiety_score = human_review_cents / 100`

The score ranges from 0.00 to 1.00. Higher values indicate greater revealed preference for human review over AI-only review in a high-impact AI decision context. A score of 0.00 means all review cents were allocated to AI-only review. A score of 1.00 means all review cents were allocated to human review.

This score is interpreted as revealed AI anxiety only at the criterion-validity level. It is not a clinical anxiety measure, not a moral judgment about the respondent, and not an official ANX-Bench score.

## Data Contract

One row is exported per respondent for this task. Rows must validate against `schema/behavioral_response.schema.json`. The required fields include:

- `wave_id`
- `respondent_id`
- `task_id`
- `benchmark_version`
- `randomized_arm`
- `allocation_mode`
- `ai_only_review_cents`
- `human_review_cents`
- `allocation_total_cents`
- `allocation_confirmed`
- `behavioral_comprehension_response`
- `behavioral_comprehension_passed`
- `exclusion_flags`
- `missingness_code`
- `revealed_anxiety_score`

Direct identifiers, raw vendor IDs, IP addresses, device fingerprints, and unrestricted open text are prohibited in the behavioral response file. The respondent identifier must be the same study-scoped pseudonymous identifier used for analytic linkage in the wave.

## Missingness And Exclusions

The behavioral criterion is observed only when the respondent was shown the task, submitted a valid allocation totaling 100 cents, actively confirmed the allocation when required by the interface, passed the behavioral comprehension check, and was not removed by preregistered survey-level quality control.

Confirmatory behavioral validity analyses exclude rows with any of the following flags:

- `behavioral_task_not_presented`
- `behavioral_allocation_invalid`
- `behavioral_comprehension_failed`
- `attention_check_failed`
- `speeding`
- `straightlining`
- `duplicate_respondent`
- `ineligible_population`
- `consent_withdrawn`
- `quality_review_failed`
- `technical_failure`
- `other_preregistered_exclusion`

Rows may be retained in restricted or public analytic files for reproducibility with `revealed_anxiety_score` set to null when scoring is not valid.

## Criterion-Validity Use

Each wave using this task must preregister the primary model linking candidate ANX scores to `revealed_anxiety_score`. At minimum, the preregistration must specify:

- The candidate ANX score or scores tested.
- Whether the primary model pools randomized arms with arm fixed effects or tests arm-specific score matches.
- Covariates, including demographics, AI exposure, and general anxiety where collected.
- Exclusion rules for behavioral rows and survey-level quality control.
- A pass threshold for practical and statistical evidence.

For `approved_scored` consideration, a candidate ANX score should predict higher `revealed_anxiety_score` in the preregistered direction after covariate adjustment, with a practically interpretable effect and uncertainty interval excluding zero under the primary model. Behavioral evidence may complement other criterion variables, but self-report comparators alone are insufficient for a full revealed-preference claim.
