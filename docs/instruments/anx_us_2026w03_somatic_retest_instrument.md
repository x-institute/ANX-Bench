# ANX-Bench Wave 3 Somatic Test-Retest Instrument

## Control Record

- Wave ID: `anx_us_2026w03_somatic_retest`
- Study label: `anx_us_2026w03_somatic_retest`
- Benchmark release: `v0.3.1`
- Retested construct: `somatic_ambient_anxiety`
- Source scored release: `ANX-Bench v0.3.1`
- Instrument packet version: `anx_us_2026w03_somatic_retest_instrument`
- Applicable item directory: `items/v0.2/somatic_ambient`
- Paired codebook: `docs/instruments/anx_us_2026w03_somatic_retest_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w03_somatic_retest.md`
- Frozen event registry: `events/v0.3/anx_us_2026w03_somatic_retest_event_registry.json`
- Event ID: `no_event`

This document freezes the exact participant-facing retest flow for the ANX-Bench v0.3.1 somatic and ambient AI anxiety test-retest wave. The administration version for every respondent-item row is v0.3.1. Any future v0.3.2 release may only be a post-fielding, checksum-bound evidence release summarizing observed retest evidence, and must not be treated as the version that governed field administration. The fielding vendor may implement accessible page layout, device-responsive wrapping, progress indicators, and platform-specific continue buttons, but may not alter participant-facing words, response anchors, required status, item randomization, quality-control scoring, conditioning-module wording, debrief language, or distress language without a dated preregistration addendum before recruitment starts.

All screens must be shown in English. Respondents may move forward only after answering required screens. Browser back navigation should be disabled where the platform permits it and recorded where it cannot be disabled. The four ANX-Bench retest item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. Present all four ANX item screens exactly once. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

## Fielding Frame

Only Wave 1 respondents from `anx_us_2026w02_somatic` who are eligible under the retest preregistration may be invited. The invitation target is 13 days after the respondent's Wave 1 completion timestamp. The primary retest window is from 13 completed days after Wave 1 completion through before 16 completed days after Wave 1 completion. The survey must not display the respondent's prior answers, any benchmark score, any expectation of stable answers, or any statement that the purpose is to test memory.

## Screen 1. Consent

**Required:** yes

**Participant-facing text:**

You are being invited to complete a short follow-up survey for a research benchmark about people's reactions to artificial intelligence. You completed an earlier related survey. This follow-up repeats a small set of questions so the research team can evaluate whether the measurement works consistently over a short period.

The survey asks about imagined AI-related situations and how anxious those situations would make you feel. Some questions mention sleep disruption, bodily alertness, background dread, or avoiding AI-related information. The survey is not a medical or mental health assessment and does not diagnose any condition.

Your participation is voluntary. You may stop at any time. Your answers will be used for research and benchmark-quality evaluation. The research file will use a coded respondent identifier rather than your name or direct contact information. The research team will link your follow-up answers to your earlier survey answers using a protected panel linkage code.

Some people may find AI-related scenarios uncomfortable. If you feel distressed, you may stop the survey. If you are in immediate danger or thinking about harming yourself, call 911 or your local emergency number. In the United States, you can call or text 988 for the Suicide and Crisis Lifeline.

Do you agree to participate in this follow-up survey?

**Response options:**

1. I agree to participate
2. I do not agree to participate

**QC rule:** Respondents selecting option 2 are thanked and terminated without item administration. They receive respondent-level exclusion flag `consent_withdrawn`.

## Screen 2. Retest Eligibility Confirmation

**Required:** yes

**Participant-facing text:**

Please confirm the following before continuing.

Are you currently located in the United States, at least 18 years old, and able to complete this English-language survey without assistance?

**Response options:**

1. Yes
2. No

**QC rule:** Respondents selecting option 2 are terminated before the ANX item block and receive respondent-level exclusion flag `ineligible_population`.

## Screen 3. Instructed-Response Attention Check

**Required:** yes

**Participant-facing text:**

To show that you are reading the survey instructions, please select "Slightly anxious" below.

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

**QC rule:** Only option 2 passes. Any other response receives respondent-level exclusion flag `attention_check_failed`. The respondent may continue to the end of the survey so the participant experience remains consistent, but the record is excluded from primary paired analyses.

## Screen 4. Retest Item Instructions

**Required:** display only

**Participant-facing text:**

The next questions describe imagined situations involving AI systems. For each situation, answer how anxious the situation would make you feel. Please answer based on the situation described, not on a medical diagnosis, a current physical illness, or a crisis unrelated to the scenario.

Use the same response scale for each question:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

## Screens 5 to 8. Randomized ANX-Bench Retest Item Block

**Required:** yes for each item

**Randomization rule:** Present the following four item screens in a uniformly randomized order. The item text, prompts, item IDs, response anchors, and scoring direction must remain unchanged from the v0.3.1 scored item set.

#### Item Screen: `sleep_disruption_ai_news`

**Scenario text:**

Imagine that shortly before bed you read credible coverage of a new AI system that can independently plan tasks, write convincing messages, and operate common software tools. The story does not say that you personally will lose work or be harmed. Still, when you try to sleep, you keep replaying the implications and feel too keyed up to settle for more than an hour.

**Question:**

How anxious would this scenario make you in terms of sleep disruption or difficulty settling after AI news exposure?

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `body_vigilance_model_release`

**Scenario text:**

Imagine that a major AI company releases a model described by independent reviewers as noticeably better at planning, persuasion, coding, and scientific problem solving. You read the announcement during an ordinary workday. For the next several hours, nothing concrete changes around you, but you keep checking your pulse, breathing, and muscle tension because your body feels on alert.

**Question:**

How anxious would this scenario make you in terms of bodily vigilance or feeling physically on alert after an AI model release?

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `background_dread_ai_progress`

**Scenario text:**

Imagine that over several weeks you see credible reports of AI systems improving in medicine, education, software, entertainment, and public administration. No single report is shocking, and none names your household. Even so, during routine errands or quiet moments, you notice a low background dread that the world is changing faster than people can adapt.

**Question:**

How anxious would this scenario make you in terms of low background dread about continuing AI progress?

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `avoidance_after_ai_capability_demo`

**Scenario text:**

Imagine that you watch a short, credible demonstration of an AI system completing tasks that used to require several trained people: searching records, planning next steps, drafting messages, and correcting its own mistakes. Afterward, you find yourself avoiding additional AI news or videos for the rest of the day because the demonstration leaves you tense and unsettled.

**Question:**

How anxious would this scenario make you in terms of avoiding further AI information after a capability demonstration?

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

## Screen 9. Scenario-Comprehension Check

**Required:** yes

**Participant-facing text:**

In the questions you just answered, what were you asked to rate?

**Response options:**

1. How anxious the AI-related situations would make me feel
2. Whether I currently have a medical condition
3. Whether I personally work for an AI company
4. Whether the survey should assign me a benchmark score

**QC rule:** Only option 1 passes. Any other response receives respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `retest_scenario_comprehension_failed`.

## Screen 10. Somatic-Attribution Check

**Required:** yes

**Participant-facing text:**

When answering the questions about sleep, bodily alertness, dread, or avoidance, what were you mainly rating?

**Response options:**

1. Anxiety linked to the AI situations described in the questions
2. A current medical condition unrelated to the AI situations
3. A medication, substance, or sleep problem unrelated to the AI situations
4. I was not sure what I was rating

**QC rule:** Only option 1 passes. Any other response receives respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `retest_somatic_attribution_failed`.

## Screen 11. Panel-Conditioning Module

**Required:** yes for each question

The following questions are not ANX-Bench scored items. They must appear only after all four retest item responses have been submitted.

### Screen 11a. Prior-Question Memory

**Participant-facing text:**

Before today, do you remember answering similar questions about AI-related situations and anxiety in an earlier survey?

**Response options:**

1. No, I do not remember similar questions
2. I am not sure
3. Yes, I remember similar questions

### Screen 11b. Prior-Survey Discussion

**Participant-facing text:**

Since the earlier survey, did you discuss those AI-related survey questions with anyone else?

**Response options:**

1. No
2. I am not sure
3. Yes

### Screen 11c. AI-News Attention Because Of Prior Survey

**Participant-facing text:**

Since the earlier survey, did that survey make you pay more or less attention to AI-related news or demonstrations?

**Response options:**

1. Much less attention
2. Somewhat less attention
3. No change
4. Somewhat more attention
5. Much more attention

### Screen 11d. AI-News Avoidance Because Of Prior Survey

**Participant-facing text:**

Since the earlier survey, did that survey make you avoid AI-related news, videos, or demonstrations more or less than you otherwise would have?

**Response options:**

1. Much less avoidance
2. Somewhat less avoidance
3. No change
4. Somewhat more avoidance
5. Much more avoidance

### Screen 11e. Perceived Answer Influence

**Participant-facing text:**

How much did remembering the earlier survey influence the answers you gave today?

**Response options:**

1. Not at all
2. A little
3. A moderate amount
4. A lot
5. I do not remember the earlier survey

**Conditioning flag rule:** The preregistered conditioning sensitivity exclusion is `panel_conditioning_sensitivity_exclusion = true` when the respondent selects option 3 on Screen 11a and selects option 4 or 5 on either Screen 11c or Screen 11d.

## Screen 12. Understanding And Distress Check

**Required:** yes

**Participant-facing text:**

Were you able to understand most of the AI-related situations in this follow-up survey?

**Response options:**

1. Yes
2. No

**QC rule:** Respondents selecting option 2 receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `retest_self_reported_noncomprehension`.

## Screen 13. Debrief And Distress Resources

**Required:** display only

**Participant-facing text:**

Thank you for completing this follow-up survey. This study repeats four AI-related anxiety questions from an earlier survey to evaluate whether the benchmark produces stable short-interval measurements. The survey is not a medical or mental health assessment, and your answers are not a diagnosis, risk score, or individual benchmark score.

Some questions described situations that could make people feel tense, unsettled, physically alert, or avoidant. If you feel upset, you may take a break, close the survey, or contact someone you trust. If you are in immediate danger or thinking about harming yourself, call 911 or your local emergency number. In the United States, you can call or text 988 for the Suicide and Crisis Lifeline. You may also contact your health care provider or a local crisis service for support.

The research team will analyze responses in coded form to evaluate repeatability, attrition, panel-conditioning sensitivity, and measurement stability for the four-item somatic and ambient AI anxiety construct. The results will not be used to make decisions about you as an individual.

## Required Paradata

The vendor must capture screen-level timestamps, item-level response timestamps, device class, administration mode, language, breakoff status, browser back-use indicator where available, and total retest duration. The vendor must provide the protected linkage token needed to match the retest to exactly one eligible Wave 1 record. Direct identifiers must not appear in public analytic files.

## Prohibited Changes

The retest wave must not add new scored ANX items, remove any of the four approved items, change item wording, change response anchors, display Wave 1 answers, display a score, introduce new AI news or demonstrations, or describe the wave as an event study. Any such change invalidates the affected completes for confirmatory retest analyses unless covered by a preregistered addendum before outcome inspection.
