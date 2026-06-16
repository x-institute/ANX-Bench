# ANX-Bench Wave 4 Somatic Event-Study Instrument

## Control Record

- Wave ID: `anx_us_2026w04_somatic_event_study`
- Candidate release: `v0.4.0`
- Source scored release: `v0.3.1`
- Construct: `somatic_ambient_anxiety`
- Primary outcome: `somatic_ambient_anxiety_mean`
- Applicable item directory: `items/v0.2/somatic_ambient`
- Paired preregistration: `docs/preregistrations/anx_us_2026w04_somatic_event_study.md`
- Event registry template: `events/v0.4/anx_us_2026w04_somatic_event_registry.template.json`
- Analysis plan: `analysis/v0.4/somatic_event_study/wave4_event_study_analysis_plan.json`

This document freezes the participant-facing Wave 4 event-study flow for the v0.3.1 somatic and ambient AI anxiety item set. The four scored ANX-Bench items below must reuse the exact v0.3.1 scenario wording, questions, response anchors, item IDs, scoring direction, and item versions. The only Wave 4 additions are event-wave instructions, exposure timing variables, quality-control items, consent and debrief language, and response-row mapping fields needed for the preregistered event-study design.

All screens must be shown in English. Respondents may continue only after answering required screens. The four ANX-Bench item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

## Screen 1. Consent

**Required:** yes

**Participant-facing text:**

You are being invited to complete a short research survey about people's reactions to artificial intelligence. The survey asks about imagined AI-related situations and how anxious those situations would make you feel. Some questions mention sleep disruption, bodily alertness, background dread, or avoiding AI-related information. The survey is not a medical or mental health assessment and does not diagnose any condition.

Your participation is voluntary. You may stop at any time. Your answers will be used for research and benchmark-quality evaluation. The research file will use a coded respondent identifier rather than your name or direct contact information.

Some people may find AI-related scenarios uncomfortable. If you feel distressed, you may stop the survey. If you are in immediate danger or thinking about harming yourself, call 911 or your local emergency number. In the United States, you can call or text 988 for the Suicide and Crisis Lifeline.

Do you agree to participate in this survey?

**Response options:**

1. I agree to participate
2. I do not agree to participate

**QC rule:** Respondents selecting option 2 are thanked and terminated without item administration. They receive respondent-level exclusion flag `consent_withdrawn`.

## Screen 2. Eligibility Confirmation

**Required:** yes

**Participant-facing text:**

Please confirm the following before continuing.

Are you currently located in the United States, at least 18 years old, and able to complete this English-language survey without assistance?

**Response options:**

1. Yes
2. No

**QC rule:** Respondents selecting option 2 are terminated before the ANX item block and receive respondent-level exclusion flag `ineligible_population`.

## Screen 3. Event-Wave Instructions

**Required:** display only

**Participant-facing text:**

The next questions describe imagined situations involving AI systems. For each situation, answer how anxious the situation would make you feel. Please answer based on the situation described, not on a medical diagnosis, a current physical illness, or a crisis unrelated to the scenario.

Use the same response scale for each question:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

## Screen 4. Instructed-Response Attention Check

**Required:** yes

**Participant-facing text:**

To show that you are reading the survey instructions, please select "Slightly anxious" below.

**Response options:**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

**QC rule:** Only option 2 passes. Any other response receives respondent-level exclusion flag `attention_check_failed`. The respondent may continue to the end of the survey so the participant experience remains consistent, but the record is excluded from primary analyses.

## Screens 5 to 8. Randomized ANX-Bench Event Item Block

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

**QC rule:** Only option 1 passes. Any other response receives respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `event_scenario_comprehension_failed`.

## Screen 10. Somatic-Attribution Check

**Required:** yes

**Participant-facing text:**

When answering the questions about sleep, bodily alertness, dread, or avoidance, what were you mainly rating?

**Response options:**

1. Anxiety linked to the AI situations described in the questions
2. A current medical condition unrelated to the AI situations
3. A medication, substance, or sleep problem unrelated to the AI situations
4. I was not sure what I was rating

**QC rule:** Only option 1 passes. Any other response receives respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `event_somatic_attribution_failed`.

## Screen 11. Exposure Timing Module

**Required:** yes for each question

These questions are not ANX-Bench scored items. They must appear only after all four scored item responses and QC checks have been submitted so they cannot prime the primary outcome.

### Screen 11a. Event Awareness

**Participant-facing text:**

Before starting this survey, had you heard, read, or watched anything about the AI release described in the study invitation or recent public coverage?

**Response options:**

1. No
2. I am not sure
3. Yes

**Variable:** `event_awareness_before_survey`

### Screen 11b. First Exposure Timing

**Participant-facing text:**

When did you first hear, read, or watch anything about that AI release?

**Response options:**

1. I had not heard about it before this survey
2. Earlier today
3. Yesterday
4. 2 to 3 days ago
5. 4 to 7 days ago
6. More than 7 days ago
7. I am not sure

**Variable:** `event_first_exposure_timing`

### Screen 11c. Source Of Exposure

**Participant-facing text:**

Where did you first encounter information about that AI release?

**Response options:**

1. I had not heard about it before this survey
2. AI company or product announcement
3. News article or broadcast
4. Social media or online discussion
5. Workplace, school, or professional setting
6. Friend, family member, or personal contact
7. Other source
8. I am not sure

**Variable:** `event_source_seen`

### Screen 11d. Attention Amount

**Participant-facing text:**

Before starting this survey, about how much time had you spent reading, watching, listening to, or discussing information about that AI release?

**Response options:**

1. None
2. Less than 5 minutes
3. 5 to 15 minutes
4. 16 to 60 minutes
5. More than 60 minutes
6. I am not sure

**Variable:** `event_attention_minutes_category`

### Screen 11e. Perceived Capability Jump

**Participant-facing text:**

Based on what you had seen before this survey, how large did the AI release seem as a change in AI capability?

**Response options:**

1. I had not seen information about it
2. Not a meaningful change
3. A small change
4. A moderate change
5. A large change
6. I am not sure

**Variable:** `event_perceived_capability_jump`

## Screen 12. Unrelated Distress And Confound Check

**Required:** yes for each question

These variables are used only for preregistered exclusion or sensitivity analysis. They are not ANX-Bench scored items.

### Screen 12a. Unrelated Personal Crisis

**Participant-facing text:**

During the past 7 days, did a major personal crisis unrelated to AI strongly affect how anxious or physically unsettled you felt?

**Response options:**

1. No
2. I am not sure
3. Yes
4. Prefer not to answer

**Variable:** `unrelated_personal_crisis_7d`

### Screen 12b. Current Medical Attribution

**Participant-facing text:**

Were your answers to the AI scenario questions mainly based on a current medical condition, medication, substance use, acute illness, or sleep problem unrelated to AI?

**Response options:**

1. No
2. I am not sure
3. Yes
4. Prefer not to answer

**QC rule:** Option 3 receives respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `current_non_ai_somatic_attribution`.

**Variable:** `current_non_ai_somatic_attribution`

## Screen 13. Debrief

**Required:** display only

**Participant-facing text:**

Thank you for completing the survey. This study measures how people respond to AI-related scenarios over time and around public AI capability releases. The questions are research measures only. They are not a medical or mental health assessment, and they do not diagnose anxiety, sleep problems, or any other condition.

Some people may find AI-related topics uncomfortable. If this survey raised concerns for you, you may take a break from AI-related news or talk with someone you trust. If you are in immediate danger or thinking about harming yourself, call 911 or your local emergency number. In the United States, you can call or text 988 for the Suicide and Crisis Lifeline.

## Response-Row Mapping

Each scored item creates one respondent-item row compatible with `schema/wave_response.schema.json`. Non-scored exposure and QC variables are stored at the respondent-wave level and may be joined by `respondent_id` or the protected panel linkage token.

Required row-level mappings for all four scored item rows:

| Field | Required value or source |
| --- | --- |
| `study_label` | `anx_us_2026w04_somatic_event_study` |
| `benchmark_version` | `v0.3.1` for scored item rows because item scoring is inherited from the citable v0.3.1 release |
| `candidate_release` | `v0.4.0` in wave metadata, not as the scored release |
| `item_id` | One of the four approved item IDs |
| `item_version` | `v0.2.0` |
| `domain` | `somatic_ambient` |
| `construct_id` | `somatic_ambient_anxiety` |
| `response_value` | Integer 1 to 5 from the selected anchor |
| `score` | Same integer 1 to 5 |
| `event_id` | Locked event ID from the completed v0.4 event registry |
| `baseline_or_followup` | `baseline`, `followup`, or `event_buffer_excluded` based on interview timestamp and locked windows |
| `event_time_hours` | Interview start timestamp minus locked event timestamp, in hours |
| `exclusion_flags` | Fixed preregistered flags from consent, eligibility, QC, timing, duplicate, missingness, and attribution checks |

Required respondent-wave variables:

- `survey_start_timestamp_utc`
- `survey_end_timestamp_utc`
- `event_awareness_before_survey`
- `event_first_exposure_timing`
- `event_source_seen`
- `event_attention_minutes_category`
- `event_perceived_capability_jump`
- `unrelated_personal_crisis_7d`
- `current_non_ai_somatic_attribution`
- `attention_check_passed`
- `scenario_comprehension_passed`
- `somatic_attribution_passed`
- `poststratified_balanced_event_weight`
- `sample_source`
- `device_type`
