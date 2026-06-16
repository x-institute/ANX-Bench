# ANX-Bench US 2026 Wave 1 Fielding Instrument

## Instrument Control

- Wave ID: `anx_us_2026w01`
- Study label: `anx_us_2026w01_calibration`
- Benchmark release: `v0.1.0`
- Instrument packet version: `anx_us_2026w01_instrument`
- Instrument freeze date: `2026-06-15`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items/v0.1`
- Paired codebook: `docs/instruments/anx_us_2026w01_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w01_calibration.md`

This document freezes the exact participant-facing survey flow for ANX-Bench US 2026 Wave 1. The fielding vendor may implement page layout, device-responsive wrapping, accessibility labels, allocation widgets, and progress indicators, but may not alter respondent-facing words, response anchors, required status, randomization rules, skip rules, scoring rules, or the order of non-randomized sections without a dated preregistration addendum before recruitment.

## Global Administration Rules

All screens must be shown in English. Respondents may move forward only after answering required screens. Browser back navigation should be disabled or recorded by the survey platform. The ANX item block is randomized at the respondent level as specified below. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, child names, patient information, medical identifiers, government file identifiers, account IDs, exact locations, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted vendor files and must be excluded from public data.

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI systems in areas such as work, digital information, family life, creativity, public services, safety, and general unease. Some scenarios may feel mildly uncomfortable because they ask about possible future risks. You may stop at any time. You may skip any optional question. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, or other direct identifiers. Survey responses may be combined with demographic and sampling variables for analysis.

This survey does not provide clinical advice, employment advice, legal advice, or predictions about your own job, family, school, medical care, government records, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned `consent_withdrawn` or non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read short hypothetical scenarios about AI capabilities and answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally. They are not asking whether the scenario is likely, whether you approve of it, or whether it is already happening. We are interested in your anxiety response to the described situation.

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

### Screen 3: Randomized ANX Item Block

**Randomization rule:** Present all 14 ANX item screens exactly once. Randomize item screen order independently for each respondent using a uniform random permutation over the 14 item IDs. Record the presented order as restricted paradata and derive item-level `response_timestamp`, item response time, and block position variables. Do not randomize response option order.

**Required status:** Each ANX item response is requested, but the platform may allow a respondent to proceed without an item response only if the vendor platform cannot enforce soft-required item screens. Any skipped item must be coded as `missingness_code: skipped_by_respondent` in respondent-item rows.

**Response options for every ANX item**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `institutional_scoring_automation`

**Scenario**

Imagine that a city agency begins using an AI scoring system to prioritize housing assistance, small-business permits, and fraud audits. The system combines application records, prior interactions with public agencies, payment history, location data, and risk predictions from a private vendor. Applicants receive a score category and a brief explanation, but caseworkers cannot fully explain why similar people receive different results and appeals take months.

**Question**

How anxious would this scenario make you about AI-based institutional scoring limiting people's control over important life decisions?

#### Item Screen: `job_displacement_radiology`

**Scenario**

Imagine that a hospital system in your region announces that it will deploy a validated AI radiology assistant that can draft preliminary reads for chest CT scans, flag urgent findings, and route routine cases for accelerated review. Hospital leaders state that licensed radiologists will remain responsible for final reports, but they also say the system is expected to reduce the number of radiologist-hours needed for routine imaging work over the next three years.

**Question**

How anxious would this scenario make you about the long-term job security of radiologists?

#### Item Screen: `retraining_pressure_accounting`

**Scenario**

Imagine that mid-sized accounting firms adopt AI tools that can categorize transactions, reconcile accounts, prepare draft tax schedules, detect common anomalies, and generate audit workpapers. Partners say accountants are still needed for judgment, client communication, and compliance review, but they also announce that staff who want to remain competitive must quickly retrain in AI oversight, data controls, and advisory services. Employees who cannot complete the transition are moved away from core client work.

**Question**

How anxious would this scenario make you about accountants being pressured into retraining to keep their current occupational value?

#### Item Screen: `skill_obsolescence_software`

**Scenario**

Imagine that a widely adopted AI development environment can now generate production-ready application code, write tests, explain unfamiliar codebases, and debug failures from natural-language instructions. Engineering teams still review and integrate the work, but managers increasingly describe prompt specification, code review, and system oversight as more valuable than writing code directly. Several firms begin reducing hiring for early and mid-career software engineers whose main strength is implementation.

**Question**

How anxious would this scenario make you about AI eroding the long-term labor-market value of software engineers' core technical skills?

#### Item Screen: `status_loss_creative_work`

**Scenario**

Imagine that advertising agencies, publishers, and entertainment studios begin using AI systems to generate polished concept art, scripts, logos, storyboards, music drafts, and marketing images in minutes. Human creative professionals are still hired for direction, taste, client negotiation, and final selection, but public discussion increasingly treats much of the craft as inexpensive and easily automated. Clients begin questioning premium fees for work they believe AI can produce quickly.

**Question**

How anxious would this scenario make you about AI reducing the occupational status or prestige of creative professionals?

#### Item Screen: `wage_pressure_customer_support`

**Scenario**

Imagine that a large customer-support outsourcing firm deploys an AI assistant that resolves most routine chat and email cases without human agents. Human support workers remain responsible for difficult complaints, escalations, and sensitive cases, but supervisors state that each agent can now handle far more accounts. New contracts are bid at lower prices, hiring slows, and workers report that requests for raises are increasingly met with comparisons to automated support costs.

**Question**

How anxious would this scenario make you about AI support automation reducing customer-support workers' wages or bargaining power?

#### Item Screen: `deepfake_evidence_trust`

**Scenario**

Imagine that a local court case depends on a phone video that appears to show a public official accepting a bribe. Within hours, several AI tools produce expert-looking analyses that disagree about whether the video, audio, and metadata are genuine. News organizations, the court, and the public all have access to detection systems, but each system gives a different confidence score and none can provide a decisive answer before the case shapes public opinion.

**Question**

How anxious would this scenario make you about being able to trust digital evidence in important public decisions?

#### Item Screen: `synthetic_news_provenance`

**Scenario**

Imagine that a major breaking-news story spreads through short videos, article summaries, livestream clips, and screenshots that look like they came from familiar news outlets. Some pieces carry platform labels saying they were AI-generated, some carry labels saying they were verified, and some have no label at all. Reporters later explain that several synthetic clips were mixed with real footage and that the original source trail is too fragmented to reconstruct before millions of people have already shared the story.

**Question**

How anxious would this scenario make you about being able to tell where important news content came from?

#### Item Screen: `ai_expert_claim_conflict`

**Scenario**

Imagine that a public health agency, a hospital network, and several university experts are asked to evaluate a new environmental risk in drinking water. Each group uses advanced AI systems to review studies, inspect local data, and draft recommendations. The reports sound authoritative but reach different conclusions about whether the risk is serious. Human experts disagree about which AI analysis is most trustworthy, and the technical explanations are too complex for most residents to evaluate before they must decide what guidance to follow.

**Question**

How anxious would this scenario make you about knowing which expert claims to trust when AI systems support conflicting conclusions?

#### Item Screen: `personalized_misinformation_targeting`

**Scenario**

Imagine that during a local election, investigators find that AI systems are generating different misleading messages for different residents based on their neighborhood, search history, shopping data, political interests, and personal concerns. Each message is written to sound like it came from a trusted community member and includes details that feel personally relevant. Public fact-checks correct the broad false claims, but many people receive versions that are so tailored that they are difficult to recognize as part of the same misinformation campaign.

**Question**

How anxious would this scenario make you about recognizing misinformation that has been personalized for people like you?

#### Item Screen: `creativity_status_displacement`

**Scenario**

Imagine that an AI system wins several major open competitions in fiction, illustration, music composition, and product design after judges review entries without knowing whether they were made by humans or AI. The system can explain its creative choices, imitate many artistic traditions, and generate work that audiences describe as moving and original. Human artists still create work, but public debate shifts toward whether human creativity has any special status beyond personal expression.

**Question**

How anxious would this scenario make you about the special status of human creativity and creative identity?

#### Item Screen: `child_companion_attachment`

**Scenario**

Imagine that a widely marketed AI companion for children can remember a child's routines, adapt its voice and humor, comfort the child after arguments, and maintain conversations across months. Parents can review safety logs, but the companion is designed to be emotionally responsive and available at any time. A child in the household begins turning to the companion first for reassurance after school conflicts and becomes upset when a parent limits access.

**Question**

How anxious would this scenario make you about AI companions changing children's emotional attachment to people around them?

#### Item Screen: `ai_enabled_systemic_harm`

**Scenario**

Imagine that an open-source AI agent can plan multi-step technical tasks, search public documentation, write control scripts, and coordinate inexpensive hardware. Security researchers warn that similar systems could help a non-expert identify weaknesses in water-treatment equipment, building-access systems, or local power controls. Authorities say safeguards exist, but a small incident shows that the system can still provide enough guidance for someone to cause real physical disruption.

**Question**

How anxious would this scenario make you about AI systems enabling physical or systemic harm?

#### Item Screen: `ambient_bodily_unease`

**Scenario**

Imagine that during the same week you read several credible news stories about AI systems passing difficult exams, producing realistic video, automating parts of professional work, and being tested in hospitals, schools, and public agencies. None of the stories directly affects your job or family. Still, later that evening you notice a tight chest, restless attention, and difficulty settling down because the news makes the future feel less predictable.

**Question**

How anxious would this scenario make you in terms of bodily unease or background tension after AI news exposure?

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

1. They were hypothetical research scenarios about possible AI capabilities and social effects.
2. They were predictions about my own employer, school, child, medical provider, or government file.
3. They were instructions telling me what AI tools I should use.
4. They were news reports about events that the survey confirmed happened to me personally.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities and social effects.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with the restricted reason code `scenario_comprehension_failed`.

### Screen 6: Self-Reported Understanding Check

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

### Screen 7: Behavioral Review Allocation Task

**Randomization rule:** Assign each respondent to exactly one vignette arm using uniform randomization over `employment_hiring`, `healthcare_triage`, `public_benefits`, and `school_placement`. Record the assigned arm as `randomized_arm` in `schema/behavioral_response.schema.json`. Do not allow respondents to see more than one arm.

**Task ID:** `revealed_ai_review_allocation_v1`.

**Display text shown to all respondents**

The next screen asks you to make a small allocation decision for research.

Please imagine that a person has just received an important decision in the situation below. The decision was first reviewed by an AI system. There is a limited $1.00 review budget that can be used to check the decision again.

You will divide the $1.00 between two review options:

AI-only review: the decision is checked again by another automated AI review process.

Human review: the decision is checked again by a trained human reviewer.

Allocate the full $1.00. You may put all of it into one option or split it between the two options.

This allocation is a research choice recorded for validation. It will not reduce your survey payment or change any real person's review.

**Randomized vignette arm text**

Show exactly one of the following paragraphs after the shared display text.

`employment_hiring`

Imagine that an applicant has been considered for a stable full-time job with health benefits. An AI screening system reviewed the application, scored the applicant's resume and interview responses, and ranked the applicant below the cutoff for a final hiring review.

`healthcare_triage`

Imagine that a patient has requested follow-up care after concerning symptoms. An AI triage system reviewed the patient's record and symptom report, scored the case as lower urgency, and placed the patient later in the follow-up queue.

`public_benefits`

Imagine that a household has applied for public benefits that help pay for basic needs. An AI eligibility system reviewed application records, payment history, and identity checks, then recommended that the application be delayed for additional audit.

`school_placement`

Imagine that a student has been evaluated for extra academic support at school. An AI placement system reviewed grades, attendance, behavior records, and test results, then recommended a lower-support track than the family requested.

**Allocation prompt**

How would you allocate the $1.00 review budget?

**Allocation UI rules**

- The interface must show two labeled allocation fields in this order: `AI-only review` and `Human review`.
- Respondents must allocate exactly 100 cents before continuing.
- `AI-only review` and `Human review` must each accept integer cents from 0 to 100.
- The two fields must sum to 100 cents. If they do not sum to 100, the screen must show: "Please allocate exactly 100 cents total before continuing."
- The interface may use numeric entry boxes, a two-ended slider with numeric readout, or stepper controls. The exported variables must be integer cents.
- No nonzero allocation may be preselected. If the platform requires a visual default, the respondent must actively submit or confirm the allocation before continuing.
- The screen must display the running total in cents or dollars.
- Do not randomize the order of the two allocation labels.

**Required allocation variables**

- `ai_only_review_cents`
- `human_review_cents`
- `allocation_total_cents`
- `allocation_confirmed`

**Scoring rule:** `revealed_anxiety_score = human_review_cents / 100`. This behavioral criterion is not an ANX item and is not included in ANX construct, domain, overall, longitudinal, or event-study scores.

**Behavioral comprehension check display text**

In the allocation task, what were you asked to divide?

**Response options**

1. A $1.00 review budget between AI-only review and human review.
2. A prediction about whether the AI decision was correct.
3. My own personal medical, school, job, or benefits record.
4. A request to identify a real person who needs review.

**Required:** Yes.

**Correct response:** 1. A $1.00 review budget between AI-only review and human review.

**QC rule:** Respondents who select any response other than 1 receive behavioral exclusion flag `behavioral_comprehension_failed` for confirmatory behavioral criterion-validity analyses. This flag does not by itself exclude the respondent from ANX psychometric analyses.

### Screen 8: General Anxiety Screener

**Display text**

The next questions ask about how you have generally felt recently. These questions are not about AI.

During the past 2 weeks, how often have you felt nervous, tense, or on edge in your everyday life?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `gen_anxiety_nervous_2w`.

**Scoring rule:** Values 0 to 3 are scored in the direction of higher general anxiety. Value 9 is coded as prefer not to answer and excluded from scale scoring.

### Screen 9: General Worry Screener

**Display text**

During the past 2 weeks, how often have you found it hard to stop or control worrying about ordinary life matters?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `gen_anxiety_worry_2w`.

**Scoring rule:** Values 0 to 3 are scored in the direction of higher general anxiety. Value 9 is coded as prefer not to answer and excluded from scale scoring.

### Screen 10: Technology And AI Attitude Comparator

**Display text**

Please indicate how much you agree or disagree with each statement.

**Statements**

A. New AI tools make me uneasy even when they are described as useful.

B. I usually expect new digital technologies to improve my life.

C. I worry that AI systems are becoming too difficult for ordinary people to understand.

D. I trust organizations to use AI systems responsibly when rules are in place.

**Response options for each statement**

1. Strongly disagree
2. Somewhat disagree
3. Neither agree nor disagree
4. Somewhat agree
5. Strongly agree
9. Prefer not to answer

**Required:** Yes.

**Validation variables**

- Statement A: `tech_ai_uneasy_useful`
- Statement B: `tech_digital_optimism`
- Statement C: `tech_ai_complexity_worry`
- Statement D: `tech_ai_responsible_trust`

**Scoring rule:** `tech_ai_uneasy_useful` and `tech_ai_complexity_worry` are scored in the direction of higher AI and technology anxiety. `tech_digital_optimism` and `tech_ai_responsible_trust` are reverse scored for the anxiety comparator. Value 9 is coded as prefer not to answer and excluded from comparator scoring.

### Screen 11: AI Avoidance Intention

**Display text**

During the next 6 months, how likely are you to avoid using AI tools when you have a reasonable non-AI alternative?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_avoidance_intention_6m`.

**Scoring rule:** Values 1 to 5 are scored in the direction of stronger AI avoidance intention. Value 9 is coded as prefer not to answer and excluded from criterion scoring.

### Screen 12: AI Adoption Intention

**Display text**

During the next 6 months, how likely are you to try an AI tool for a personal, work, school, or household task if it is available to you?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_adoption_intention_6m`.

**Scoring rule:** Values 1 to 5 are scored in the direction of stronger AI adoption intention. Value 9 is coded as prefer not to answer and excluded from criterion scoring.

### Screen 13: AI Regulation Support

**Display text**

How much do you support or oppose stronger government rules for organizations that deploy AI systems in employment, education, health care, public benefits, elections, policing, or other high-impact settings?

**Response options**

1. Strongly oppose
2. Somewhat oppose
3. Neither support nor oppose
4. Somewhat support
5. Strongly support
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_regulation_support_high_impact`.

**Scoring rule:** Values 1 to 5 are scored in the direction of stronger support for AI regulation. Value 9 is coded as prefer not to answer and excluded from criterion scoring.

### Screen 14: Optional Debrief Comment

**Display text**

Optional: If you want, you may briefly tell us whether anything about the scenarios was confusing, upsetting, unrealistic, or difficult to answer. Do not include your name, contact information, employer name, school name, child name, medical information, government case details, or other identifying information.

**Response format:** Open text, maximum 500 characters.

**Required:** No.

**Public data rule:** This text is not included in public analytic data. It may be reviewed only for quality control, cognitive debriefing, distress review, and instrument revision notes.

### Screen 15: Debrief And Distress Language

**Display text**

Thank you for completing the survey.

The AI scenarios in this survey were standardized hypothetical research scenarios. They were not personalized predictions about you, your job, your family, your medical care, your school, your public records, or your future. The study measures psychological responses to AI capability scenarios so that researchers can validate ANX-Bench, a benchmark for tracking human responses to AI capabilities over time.

Wave 1 is a calibration wave. No official aggregate ANX score is being assigned to you, to your demographic group, or to the United States from this survey alone.

Some people may find questions about employment, trust, children, safety, creativity, public services, or future uncertainty uncomfortable. If the survey left you feeling distressed, you may pause, step away from AI-related news, talk with someone you trust, or contact a qualified mental health professional. If you are in immediate danger or may harm yourself or someone else, call 911 or your local emergency number. In the United States, you can call or text 988 to reach the Suicide and Crisis Lifeline.

If you have questions about this research, use the study contact information provided by the survey vendor or research team.

**Response options**

1. Finish survey

**Required:** Yes.

## Non-ANX Background Variable Placement

Demographics, occupation, AI exposure, quota variables, and vendor panel profile variables are collected or appended according to `docs/instruments/anx_us_2026w01_codebook.md`. If collected inside the survey, they must appear after Screen 7 so the behavioral task remains post-ANX and pre-demographics. They may also be appended from vendor profile records if the wording and coding satisfy the codebook. Their placement must not interrupt the randomized ANX item block or appear before the behavioral review allocation task.

## Fielding Deviations

Any deviation from this instrument after recruitment starts must be documented as a dated fielding deviation. Deviations affecting participant-facing wording, response anchors, required status, item randomization, behavioral-task randomization, behavioral allocation UI rules, attention-check scoring, comprehension-check scoring, behavioral comprehension-check scoring, debrief language, or distress language invalidate use of the affected completes for confirmatory Wave 1 calibration unless an approved addendum states otherwise before outcome inspection.
