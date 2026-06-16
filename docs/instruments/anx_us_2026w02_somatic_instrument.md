# ANX-Bench US 2026 Wave 2 Somatic Calibration Instrument

## Instrument Control

- Wave ID: `anx_us_2026w02_somatic`
- Study label: `anx_us_2026w02_somatic_calibration`
- Benchmark release: `v0.2.1`
- Instrument packet version: `anx_us_2026w02_somatic_instrument`
- Instrument freeze date: `2026-06-15`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items/v0.2/somatic_ambient`
- Paired codebook: `docs/instruments/anx_us_2026w02_somatic_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w02_somatic_calibration.md`

This document freezes the exact participant-facing survey flow for the ANX-Bench v0.2 somatic and ambient calibration packet. The fielding vendor may implement accessible page layout, device-responsive wrapping, progress indicators, and platform-specific buttons, but may not alter respondent-facing words, response anchors, required status, item randomization, check scoring, debrief language, distress language, or the order of non-randomized sections without a dated preregistration addendum before recruitment starts.

## Global Administration Rules

All screens must be shown in English. Respondents may move forward only after answering required screens. Browser back navigation should be disabled where the platform permits it and recorded where it cannot be disabled. The four ANX-Bench somatic and ambient item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, child names, patient information, clinical diagnoses, medication details, government file identifiers, account IDs, exact locations, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted operations files and must be excluded from public analytic data.

This instrument is not a clinical screening instrument. It asks about hypothetical anxiety responses to standardized AI capability scenarios. It must not be presented as diagnosing insomnia, panic, illness anxiety, generalized anxiety disorder, phobia, or any mental health condition.

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI capability news, AI model releases, continuing AI progress, and AI capability demonstrations. Some scenarios mention bodily unease, difficulty settling, feeling physically on alert, background dread, or avoiding more AI information. These scenarios may feel mildly uncomfortable. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, or other direct identifiers. Survey responses may be combined with demographic, sampling, AI exposure, sleep sensitivity, health anxiety sensitivity, and general anxiety variables for analysis.

This survey does not provide clinical advice, medical advice, employment advice, legal advice, or predictions about your own job, health, family, school, medical care, public records, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read four short hypothetical scenarios about AI capabilities and answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally. They are not asking whether the scenario is likely, whether you approve of it, whether you have a health condition, or whether the situation is already happening. We are interested in your anxiety response to the described situation.

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

### Screen 3: Randomized Somatic and Ambient ANX Item Block

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

1. They were hypothetical research scenarios about possible AI capabilities and how a person might feel in response.
2. They were medical questions asking whether I have a sleep disorder, panic attack, or health condition.
3. They were predictions about my own employer, school, family, medical care, or government file.
4. They were instructions telling me what AI tools I should use or avoid.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities and how a person might feel in response.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 6: Required Somatic-Attribution Check

**Display text**

When answering the four scenarios, what were you mainly asked to rate?

**Response options**

1. How anxious the AI scenario would make me feel, including any bodily unease described in the scenario.
2. Whether I currently have a medical condition that explains sleep, breathing, pulse, or muscle tension.
3. Whether the AI scenario is certain to happen to me personally.
4. Whether I think all AI news should be avoided.

**Required:** Yes.

**Correct response:** 1. How anxious the AI scenario would make me feel, including any bodily unease described in the scenario.

**QC rule:** Respondents who select any response other than 1 fail the somatic-attribution check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `somatic_attribution_failed`. This check protects against interpreting the ANX item responses as medical symptom reports rather than scenario-linked anxiety responses.

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

### Screen 8: Sleep Sensitivity Covariate

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

### Screen 9: Health Anxiety Sensitivity Covariate

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

### Screen 11: Baseline General Anxiety Screener

**Display text**

During the past 2 weeks, how often have you felt nervous, tense, or on edge in your everyday life?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_nervous_2w`.

### Screen 12: Baseline General Worry Screener

**Display text**

During the past 2 weeks, how often have you found it hard to stop or control worrying about ordinary life matters?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_worry_2w`.

### Screen 13: AI Avoidance Criterion

**Display text**

During the next 6 months, how likely are you to avoid AI-related news, videos, or demonstrations when you have a reasonable choice not to engage with them?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_information_avoidance_intention_6m`.

### Screen 14: AI Information Checking Criterion

**Display text**

During the next 6 months, how likely are you to seek reliable information about AI capabilities even when the topic feels uncomfortable?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_information_checking_intention_6m`.

### Screen 15: Optional Debrief Comment

**Display text**

Optional: If you want, you may briefly tell us whether anything about the scenarios was confusing, upsetting, unrealistic, or difficult to answer. Do not include your name, contact information, employer name, school name, child name, medical information, health diagnosis, medication details, government case details, or other identifying information.

**Response format:** Open text, maximum 500 characters.

**Required:** No.

**Public data rule:** This text is not included in public analytic data. It may be reviewed only for quality control, cognitive debriefing, distress review, and instrument revision notes.

### Screen 16: Debrief And Distress Language

**Display text**

Thank you for completing the survey.

The AI scenarios in this survey were standardized hypothetical research scenarios. They were not personalized predictions about you, your job, your family, your health, your medical care, your school, your public records, or your future. The study measures psychological responses to AI capability scenarios so that researchers can validate ANX-Bench, a benchmark for tracking human responses to AI capabilities over time.

This wave is a calibration study for four somatic and ambient anxiety items. No official aggregate ANX score is being assigned to you, to your demographic group, or to the United States from this survey alone. The questions are not a medical or mental health assessment.

Some people may find questions about AI progress, sleep disruption, bodily alertness, background dread, avoidance, or future uncertainty uncomfortable. If the survey left you feeling distressed, you may pause, step away from AI-related news, talk with someone you trust, or contact a qualified mental health professional. If you are in immediate danger or may harm yourself or someone else, call 911 or your local emergency number. In the United States, you can call or text 988 to reach the Suicide and Crisis Lifeline.

If you have questions about this research, use the study contact information provided by the survey vendor or research team.

**Response options**

1. Finish survey

**Required:** Yes.

## Non-ANX Background Variable Placement

Demographics, quota variables, device type, vendor profile variables, and standard AI exposure variables may be collected before Screen 2, after Screen 14, or appended from vendor profile records if the wording and coding satisfy `docs/instruments/anx_us_2026w02_somatic_codebook.md`. Their placement must not interrupt the randomized four-item ANX block.

## Fielding Deviations

Any deviation from this instrument after recruitment starts must be documented as a dated fielding deviation. Deviations affecting participant-facing wording, response anchors, required status, item randomization, attention-check scoring, comprehension-check scoring, somatic-attribution scoring, debrief language, or distress language invalidate use of the affected completes for confirmatory Wave 2 somatic calibration unless an approved addendum states otherwise before outcome inspection.
