# ANX-Bench US 2026 Wave 2 Somatic Calibration Instrument v0.2.3

## Instrument Control

- Wave ID: `anx_us_2026w02_somatic`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release: `v0.2.3`
- Instrument packet version: `anx_us_2026w02_somatic_instrument_v0.2.3`
- Instrument freeze date: `2026-06-16`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items/v0.2/somatic_ambient`
- Anchoring vignette set: `anchors/v0.2/somatic_ambient/response_scale_vignettes.json`
- Paired codebook: `releases/v0.2.3/anx_us_2026w02_somatic_codebook.md`
- Paired preregistration: `releases/v0.2.3/anx_us_2026w02_somatic_calibration_preregistration.md`

This v0.2.3 packet freezes the v0.2 somatic and ambient calibration survey with three non-scored response-scale anchoring vignettes and the standardized revealed-preference AI review allocation task. The ANX item block is unchanged from v0.2.1. The participant-flow changes relative to v0.2.2 are insertion of `revealed_ai_review_allocation_v1` after the ANX item block and required QC checks, before covariates and demographics, and mapping the task to `schema/behavioral_response.schema.json`.

## Global Administration Rules

All screens must be shown in English. Respondents may move forward only after answering required screens. Browser back navigation should be disabled where the platform permits it and recorded where it cannot be disabled. The four ANX-Bench somatic and ambient item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. The three anchoring vignettes are not randomized and must be presented in fixed order from low to moderate to high severity. Response options for every ANX item and every anchoring vignette must appear in ascending numerical order from 1 to 5. The behavioral allocation task is not an ANX item, is not included in item scoring, and must be administered after the ANX item block and required QC checks but before covariates and demographics.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, child names, patient information, clinical diagnoses, medication details, government file identifiers, account IDs, exact locations, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted operations files and must be excluded from public analytic data.

This instrument is not a clinical screening instrument. It asks about hypothetical anxiety responses to standardized AI capability scenarios. It must not be presented as diagnosing insomnia, panic, illness anxiety, generalized anxiety disorder, phobia, or any mental health condition. The anchoring vignettes are calibration materials only and are never ANX scored items.

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI capability news, AI model releases, continuing AI progress, and AI capability demonstrations. Some scenarios mention bodily unease, difficulty settling, feeling physically on alert, background dread, or avoiding more AI information. These scenarios may feel mildly uncomfortable. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, or other direct identifiers. Survey responses may be combined with demographic, sampling, AI exposure, sleep sensitivity, health anxiety sensitivity, general anxiety, and response-scale calibration variables for analysis.

This survey does not provide clinical advice, medical advice, employment advice, legal advice, or predictions about your own job, health, family, school, medical care, public records, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read four short hypothetical scenarios about AI capabilities and answer one question after each scenario. After those scenarios, you will read three additional short calibration scenarios that use the same response scale. The calibration scenarios help researchers understand how people use the response options. They are not scored ANX-Bench items.

Please answer based on how each scenario would make you feel if it happened as described. The scenarios are not predictions about you personally. They are not asking whether the scenario is likely, whether you approve of it, whether you have a health condition, or whether the situation is already happening. We are interested in your anxiety response to the described situation.

Use the same response scale for every scenario:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

Please read each scenario carefully before answering.

**Response options**

1. Continue

**Required:** Yes.

### Screen 3: Randomized Somatic And Ambient ANX Item Block

**Randomization rule:** Present all four ANX item screens exactly once. Randomize item screen order independently for each respondent using a uniform random permutation over the four item IDs. Record the presented order as restricted paradata and derive item-level response timestamp, item response time, and block position variables. Do not randomize response option order.

**Required status:** Each ANX item response is requested, but the platform may allow a respondent to proceed without an item response only if the vendor platform cannot enforce soft-required item screens. Any skipped item must be coded as `missingness_code: skipped_by_respondent` in respondent-item rows.

**Response options for every ANX item**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `sleep_disruption_ai_news`

**Scenario**

Imagine that shortly before bed you read credible coverage of a new AI system that can independently plan tasks, write convincing messages, and operate common software tools. The story does not say that you personally will lose work or be harmed. Still, when you try to sleep, you keep replaying the implications and feel too keyed up to settle for more than an hour.

**Question**

How anxious would this scenario make you in terms of sleep disruption or difficulty settling after AI news exposure?

#### Item Screen: `body_vigilance_model_release`

**Scenario**

Imagine that a major AI company releases a model described by independent reviewers as noticeably better at planning, persuasion, coding, and scientific problem solving. You read the announcement during an ordinary workday. For the next several hours, nothing concrete changes around you, but you keep checking your pulse, breathing, and muscle tension because your body feels on alert.

**Question**

How anxious would this scenario make you in terms of bodily vigilance or feeling physically on alert after an AI model release?

#### Item Screen: `background_dread_ai_progress`

**Scenario**

Imagine that over several weeks you see credible reports of AI systems improving in medicine, education, software, entertainment, and public administration. No single report is shocking, and none names your household. Even so, during routine errands or quiet moments, you notice a low background dread that the world is changing faster than people can adapt.

**Question**

How anxious would this scenario make you in terms of low background dread about continuing AI progress?

#### Item Screen: `avoidance_after_ai_capability_demo`

**Scenario**

Imagine that you watch a short, credible demonstration of an AI system completing tasks that used to require several trained people: searching records, planning next steps, drafting messages, and correcting its own mistakes. Afterward, you find yourself avoiding additional AI news or videos for the rest of the day because the demonstration leaves you tense and unsettled.

**Question**

How anxious would this scenario make you in terms of avoiding further AI information after a capability demonstration?

### Screen 4: Fixed Response-Scale Anchoring Vignettes

**Administration rule:** Present all three anchoring vignette screens exactly once in the fixed order below. Do not randomize vignette order. Do not mix anchoring vignettes into the randomized ANX item block. The vignettes are response-scale calibration materials only and are never ANX scored items.

**Required status:** Each anchoring vignette response is required unless the vendor platform cannot enforce required screens. Missing responses are coded in respondent-level anchor variables and must not create ANX respondent-item rows.

**Response options for every anchoring vignette**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Anchoring Vignette: `anchor_somatic_ambient_low`

**Scenario**

Imagine seeing a brief headline that a familiar AI assistant has become a little faster at summarizing articles and drafting routine emails. You notice the story, wonder for a moment what other updates might be coming, and then return to your day without physical tension or trouble concentrating.

**Question**

How anxious would this scenario make you feel?

#### Anchoring Vignette: `anchor_somatic_ambient_moderate`

**Scenario**

Imagine reading credible coverage that a new AI system can handle several common planning, writing, and research tasks with little supervision. Nothing in the story names you or your household. Still, for the next hour you feel keyed up, keep thinking about the pace of change, and find it somewhat harder to settle into your usual routine.

**Question**

How anxious would this scenario make you feel?

#### Anchoring Vignette: `anchor_somatic_ambient_high`

**Scenario**

Imagine watching a credible demonstration in which an AI system independently plans a complex project, drafts persuasive messages, corrects its own mistakes, and completes tasks that recently required several trained people. Afterward, your body feels on alert for much of the evening, you keep checking for more news despite wanting to stop, and you have difficulty settling when you try to sleep.

**Question**

How anxious would this scenario make you feel?

### Screen 5: Required Attention Check

**Display text**

To show that you are reading the survey instructions, please select "Moderately anxious" for this question.

**Response options**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

**Required:** Yes.

**Correct response:** 3. Moderately anxious.

**QC rule:** Respondents who select any response other than 3 fail the required attention check and receive respondent-level exclusion flag `attention_check_failed` for confirmatory analyses.

### Screen 6: Required Scenario-Comprehension Check

**Display text**

Which statement best describes the AI scenarios you just read?

**Response options**

1. They were hypothetical research scenarios about possible AI capabilities and how a person might feel in response.
2. They were medical questions asking whether I have a sleep disorder, panic attack, or health condition.
3. They were predictions about my own employer, school, family, medical care, or government file.
4. They were instructions telling me what AI tools I should use or avoid.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities and how a person might feel in response.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 7: Required Somatic-Attribution Check

**Display text**

When answering the scenarios, what were you mainly asked to rate?

**Response options**

1. How anxious the AI scenario would make me feel, including any bodily unease described in the scenario.
2. Whether I currently have a medical condition that explains sleep, breathing, pulse, or muscle tension.
3. Whether the AI scenario is certain to happen to me personally.
4. Whether I think all AI news should be avoided.

**Required:** Yes.

**Correct response:** 1. How anxious the AI scenario would make me feel, including any bodily unease described in the scenario.

**QC rule:** Respondents who select any response other than 1 fail the somatic-attribution check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `somatic_attribution_failed`.

### Screen 8: Self-Reported Understanding Check

**Display text**

Overall, how well were you able to understand the scenarios in this survey?

**Response options**

1. I understood all or almost all of the scenarios.
2. I understood most of the scenarios.
3. I understood about half of the scenarios.
4. I understood only a few of the scenarios.
5. I did not understand the scenarios.

**Required:** Yes.

**QC rule:** Respondents selecting option 4 or 5 receive respondent-level exclusion flag `quality_review_failed` for the preregistered rule "self-reported inability to understand most scenarios."

### Screen 9: Revealed AI Review Allocation Task

**Task ID:** `revealed_ai_review_allocation_v1`.

**Administration rule:** Assign each respondent exactly one randomized scenario arm using equal-probability randomization across `employment_hiring`, `healthcare_triage`, `public_benefits`, and `school_placement`. Record the assigned arm as `randomized_arm`. Do not display more than one arm to a respondent. This task is a behavioral criterion-validity task only and must not be included in ANX item scoring, anchoring vignette scoring, construct scoring, domain scoring, overall scoring, longitudinal scoring, or event-study outcomes.

**Allocation mode:** `bonus_stated` unless a dated preregistration addendum before recruitment changes the implementation to `real_bonus` and describes the payment or donation rule.

**Display text before randomized arm**

The next screen asks you to make a small allocation decision for research.

Please imagine that a person has just received an important decision in the situation below. The decision was first reviewed by an AI system. There is a limited `$1.00` review budget that can be used to check the decision again.

You will divide the `$1.00` between two review options:

AI-only review: the decision is checked again by another automated AI review process.

Human review: the decision is checked again by a trained human reviewer.

Allocate the full `$1.00`. You may put all of it into one option or split it between the two options.

For this survey, your choice is recorded for research and may not change your compensation.

**Randomized arm text**

Show exactly one of the following paragraphs after the common display text.

| Randomized arm | Participant-facing scenario paragraph |
| --- | --- |
| `employment_hiring` | Imagine that a person applied for a stable full-time job. An AI system screened the applications, ranked the finalists, and recommended how the hiring review should proceed. |
| `healthcare_triage` | Imagine that a person requested follow-up review for a health care concern. An AI system sorted patient records by urgency and recommended how quickly the person should receive review. |
| `public_benefits` | Imagine that a person applied for public benefits. An AI system reviewed application records and recommended approval, delay, or audit for the case. |
| `school_placement` | Imagine that a student was reviewed for school support placement. An AI system reviewed the student record and recommended placement into a higher-support or lower-support track. |

**Allocation question**

How many cents of the `$1.00` review budget do you allocate to each option?

**Response interface requirements**

- AI-only review cents: integer from 0 to 100.
- Human review cents: integer from 0 to 100.
- The two values must sum to exactly 100 before the respondent can continue.
- The screen must display a live total or validation message showing whether the full `$1.00` has been allocated.
- The interface must not preselect a nonzero allocation. If the platform requires a default visual position, the respondent must actively confirm or change the allocation before continuing, and `allocation_confirmed` must be recorded as `true` only after that active submit or confirmation action.
- Response labels must appear in this order: AI-only review, then Human review.
- The respondent must not be told that human review is the desired answer.

**Required:** Yes.

**Exported fields:** `task_id`, `randomized_arm`, `allocation_mode`, `ai_only_review_cents`, `human_review_cents`, `allocation_total_cents`, `allocation_confirmed`, and `revealed_anxiety_score` in the one-row-per-respondent behavioral response file.

**Scoring rule:** `revealed_anxiety_score = human_review_cents / 100`. The score ranges from 0.00 to 1.00. Higher values indicate greater revealed preference for human review over AI-only review in the high-impact AI decision context. This score is a criterion variable only and is never an official ANX-Bench score.

### Screen 10: Behavioral Task Comprehension Check

**Display text**

In the allocation task, what were you asked to divide?

**Response options**

1. A `$1.00` review budget between AI-only review and human review.
2. A prediction about whether the AI decision was correct.
3. My own personal medical, school, job, or benefits record.
4. A request to identify a real person who needs review.

**Required:** Yes.

**Correct response:** 1. A `$1.00` review budget between AI-only review and human review.

**QC rule:** Respondents who select any response other than 1 receive behavioral exclusion flag `behavioral_comprehension_failed` for confirmatory behavioral criterion-validity analyses. They remain eligible for ANX psychometric analyses if they otherwise pass the preregistered survey-level quality-control rules.

### Screen 11: Sleep Sensitivity Covariate

**Display text**

The next questions ask about general background factors that may affect how people answer the scenarios. These questions are not ANX-Bench scored items.

In general, how easily is your sleep disrupted by stressful news or worries?

**Response options**

1. Not at all easily
2. Slightly easily
3. Moderately easily
4. Very easily
5. Extremely easily
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `sleep_sensitivity_stress_news`.

### Screen 12: Health Anxiety Sensitivity Covariate

**Display text**

In general, how often do ordinary body sensations make you worry that something may be wrong with your health?

**Response options**

1. Never or almost never
2. Rarely
3. Sometimes
4. Often
5. Very often
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `health_anxiety_body_sensation_worry`.

### Screen 13: AI-News Exposure Covariate

**Display text**

During the past 30 days, how often have you seen, read, watched, or listened to news or commentary about AI capabilities?

**Response options**

1. Not at all
2. Less than once a week
3. About once a week
4. Several times a week
5. Daily or almost daily
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_news_exposure_30d`.

### Screen 14: Debrief

**Display text**

Thank you for completing the survey. The scenarios you read were hypothetical research materials used to study how people respond to possible AI capabilities. The anchoring scenarios helped researchers understand how people use the response scale. The allocation task was a research task about how people divide a review budget between AI-only review and human review. None of the questions were intended to diagnose a health condition, predict what will happen to you personally, or produce an official ANX-Bench score for you or any group.

If any scenario felt uncomfortable, you may pause, step away from AI-related news, or talk with someone you trust. If you feel in immediate danger or may harm yourself or someone else, call 911 in the United States. If you are in emotional crisis in the United States, call or text 988 for crisis support.

**Response options**

1. Finish survey

**Required:** Yes.
