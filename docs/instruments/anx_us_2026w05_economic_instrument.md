# ANX-Bench US 2026 Wave 5 Economic and Vocational Calibration Instrument

## Instrument Control

- Wave ID: `anx_us_2026w05_economic`
- Study label: `anx_us_2026w05_economic_calibration`
- Benchmark release: `v0.5.0`
- Instrument packet version: `anx_us_2026w05_economic_instrument`
- Instrument freeze date: `2026-06-16`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items/v0.1/economic_vocational`
- Paired codebook: `docs/instruments/anx_us_2026w05_economic_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w05_economic_calibration.md`
- Frozen event registry: `events/v0.5/anx_us_2026w05_economic_event_registry.json`

This document freezes the participant-facing survey flow for the Wave 5 `economic_vocational_anxiety` calibration packet. The fielding vendor may implement accessible layout, device-responsive wrapping, progress indicators, and platform buttons, but may not alter respondent-facing words, response anchors, required status, randomization, quality-check scoring, debrief language, distress language, or non-randomized section order without a dated preregistration addendum before recruitment starts.

## Global Administration Rules

All screens must be shown in English. Respondents may proceed only after required screens are answered. Browser back navigation should be disabled where possible and recorded where not possible. The four ANX-Bench economic and vocational item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, client names, patient information, license identifiers, wage records, tax records, performance reviews, union membership details, government identifiers, exact locations, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted operations files and must be excluded from public analytic data.

This instrument is not a clinical, employment, financial, legal, or career-counseling instrument. It asks about hypothetical anxiety responses to standardized AI capability and labor-market scenarios.

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI systems and work. Some scenarios mention job skills, wages, retraining, hiring, bargaining power, or the occupational status of workers. These scenarios may feel mildly uncomfortable. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, employer name, client name, wage record, or other direct identifiers. Survey responses may be combined with demographic, sampling, employment, occupation, AI exposure, perceived occupational AI exposure, and general anxiety variables for analysis.

This survey does not provide employment advice, financial advice, legal advice, clinical advice, or predictions about your own job, employer, occupation, wages, school, household, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read four short hypothetical scenarios about AI capabilities and work. Please answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally, your employer, your occupation, or the overall economy. They are not asking whether the scenario is likely, whether you approve of it, or whether you have personally experienced it. We are interested in your anxiety response to the described situation.

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

### Screen 3: Randomized Economic and Vocational ANX Item Block

**Randomization rule:** Present all four ANX item screens exactly once. Randomize item screen order independently for each respondent using a uniform random permutation over the four item IDs. Record the presented order as restricted paradata and derive item-level response timestamp, item response time, and block position variables. Do not randomize response option order.

**Required status:** Each ANX item response is requested, but the platform may allow a respondent to proceed without an item response only if the vendor platform cannot enforce soft-required item screens. Any skipped item must be coded as `missingness_code: skipped_by_respondent` in respondent-item rows.

**Response options for every ANX item**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `skill_obsolescence_software`

**Scenario**

Imagine that a widely adopted AI development environment can now generate production-ready application code, write tests, explain unfamiliar codebases, and debug failures from natural-language instructions. Engineering teams still review and integrate the work, but managers increasingly describe prompt specification, code review, and system oversight as more valuable than writing code directly. Several firms begin reducing hiring for early and mid-career software engineers whose main strength is implementation.

**Question**

How anxious would this scenario make you about AI eroding the long-term labor-market value of software engineers' core technical skills?

#### Item Screen: `wage_pressure_customer_support`

**Scenario**

Imagine that a large customer-support outsourcing firm deploys an AI assistant that resolves most routine chat and email cases without human agents. Human support workers remain responsible for difficult complaints, escalations, and sensitive cases, but supervisors state that each agent can now handle far more accounts. New contracts are bid at lower prices, hiring slows, and workers report that requests for raises are increasingly met with comparisons to automated support costs.

**Question**

How anxious would this scenario make you about AI support automation reducing customer-support workers' wages or bargaining power?

#### Item Screen: `retraining_pressure_accounting`

**Scenario**

Imagine that mid-sized accounting firms adopt AI tools that can categorize transactions, reconcile accounts, prepare draft tax schedules, detect common anomalies, and generate audit workpapers. Partners say accountants are still needed for judgment, client communication, and compliance review, but they also announce that staff who want to remain competitive must quickly retrain in AI oversight, data controls, and advisory services. Employees who cannot complete the transition are moved away from core client work.

**Question**

How anxious would this scenario make you about accountants being pressured into retraining to keep their current occupational value?

#### Item Screen: `status_loss_creative_work`

**Scenario**

Imagine that advertising agencies, publishers, and entertainment studios begin using AI systems to generate polished concept art, scripts, logos, storyboards, music drafts, and marketing images in minutes. Human creative professionals are still hired for direction, taste, client negotiation, and final selection, but public discussion increasingly treats much of the craft as inexpensive and easily automated. Clients begin questioning premium fees for work they believe AI can produce quickly.

**Question**

How anxious would this scenario make you about AI reducing the occupational status or prestige of creative professionals?

### Screen 4: Required Attention Check

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

### Screen 5: Required Scenario-Comprehension Check

**Display text**

Which statement best describes the AI scenarios you just read?

**Response options**

1. They were hypothetical research scenarios about possible AI capabilities, work, and how a person might feel in response.
2. They were instructions telling me whether to quit a job, retrain, ask for a raise, or choose a career.
3. They were predictions about my own employer, occupation, wages, school, household, or future.
4. They were questions asking me to provide identifiable workplace or financial information.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities, work, and how a person might feel in response.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 6: Required Economic-Vocational Attribution Check

**Display text**

When answering the four scenarios, what were you mainly asked to rate?

**Response options**

1. How anxious the AI work scenario would make me feel about economic or vocational changes.
2. Whether the scenario is certain to happen to me personally.
3. Whether I should change jobs, retrain, negotiate wages, or avoid a profession.
4. Whether I have personally experienced the exact workplace described.

**Required:** Yes.

**Correct response:** 1. How anxious the AI work scenario would make me feel about economic or vocational changes.

**QC rule:** Respondents who select any response other than 1 fail the economic-vocational attribution check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `economic_vocational_attribution_failed`.

### Screen 7: Self-Reported Understanding Check

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

### Screen 8: Perceived Occupational AI Exposure Covariate

**Display text**

Thinking about the kind of work you do now, did most recently, or are preparing to do, how exposed is that work to current or near-future AI tools?

**Response options**

1. Not at all exposed
2. Slightly exposed
3. Moderately exposed
4. Very exposed
5. Extremely exposed
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `perceived_occupational_ai_exposure`.

### Screen 9: Current Labor-Force Attachment Covariate

**Display text**

Which option best describes your current connection to paid work?

**Response options**

1. Working full time
2. Working part time
3. Self-employed or freelance
4. Unemployed and looking for work
5. Student or training for work
6. Retired
7. Not in the labor force for another reason
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `labor_force_attachment`.

### Screen 10: AI-News Exposure Covariate

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

### Screen 11: Prior AI Use Covariate

**Display text**

How often do you personally use generative AI tools such as chatbots, image generators, coding assistants, or AI search tools?

**Response options**

1. Never or rarely
2. About monthly
3. About weekly
4. Daily or almost daily
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `prior_ai_exposure_frequency`.

### Screen 12: Baseline General Anxiety Covariates

**Display text**

The next two questions ask about ordinary feelings during the past 2 weeks. They are not ANX-Bench scored items.

During the past 2 weeks, how often have you felt nervous, tense, or on edge?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_nervous_2w`.

**Display text**

During the past 2 weeks, how often have you had difficulty stopping or controlling ordinary-life worry?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_worry_2w`.

### Screen 13: External-Validity Criteria

**Display text**

How likely is it that AI will create serious labor-market uncertainty for workers in the United States during the next 6 months?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_labor_market_worry_6m`.

**Display text**

How likely is it that many workers will feel pressure to retrain quickly because of AI tools during the next 6 months?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_retraining_pressure_expectation_6m`.

**Display text**

How likely is it that you would avoid reading more AI work-related news for a while if it made you feel tense about jobs, wages, or skills?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_work_news_avoidance_intention_6m`.

### Screen 14: Optional Debrief Comment

**Display text**

If there is anything important about your responses that the research team should understand, you may write it here. Do not include your name, employer name, client name, school name, contact information, wage records, tax records, or information that identifies another person or institution.

**Response format:** Open text.

**Required:** No.

**QC and ethics use:** Restricted review only for confusion, protest responding, implementation defects, and distress monitoring. Raw text is excluded from public analytic files.

### Screen 15: Debrief and Distress Information

**Display text**

Thank you for completing the survey. The scenarios you read were standardized research materials for validating ANX-Bench, a benchmark that studies psychological responses to AI capabilities. They were hypothetical scenarios, not predictions about your own job, employer, occupation, wages, school, household, or future.

This survey does not assign an official ANX-Bench score to you or to any group. It does not provide employment, financial, legal, clinical, or career advice. The questions are used to evaluate whether a set of research items can be interpreted consistently.

If any scenario felt upsetting, you may pause from AI-related news or work-related discussions, take a break, and talk with someone you trust. If you are in the United States and feel in immediate danger, call 911. If you are experiencing a mental health crisis or thoughts of self-harm, call or text 988 for the Suicide and Crisis Lifeline. For employment, financial, legal, or career decisions, consider consulting a qualified professional rather than relying on survey scenarios.

**Response options**

1. Finish survey

**Required:** Yes.
