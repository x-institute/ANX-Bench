# ANX-Bench US 2026 Wave 6 Epistemic Trust Calibration Instrument

## Instrument Control

- Wave ID: `anx_us_2026w06_epistemic`
- Study label: `anx_us_2026w06_epistemic_calibration`
- Benchmark release: `v0.6.0`
- Instrument packet version: `anx_us_2026w06_epistemic_instrument`
- Instrument freeze date: `2026-06-16`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items/v0.1/epistemic`
- Paired codebook: `docs/instruments/anx_us_2026w06_epistemic_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w06_epistemic_calibration.md`
- Frozen event registry: `events/v0.6/anx_us_2026w06_epistemic_event_registry.json`

This document freezes the participant-facing survey flow for the Wave 6 `epistemic_trust_anxiety` calibration packet. The fielding vendor may implement accessible layout, device-responsive wrapping, progress indicators, and platform buttons, but may not alter respondent-facing words, response anchors, required status, randomization, quality-check scoring, debrief language, distress language, or non-randomized section order without a dated preregistration addendum before recruitment starts.

## Global Administration Rules

All screens must be shown in English. Respondents may proceed only after required screens are answered. Browser back navigation should be disabled where possible and recorded where not possible. The four ANX-Bench epistemic trust item screens are randomized at the respondent level using a uniform random permutation over the four item IDs. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, client names, patient information, license identifiers, government identifiers, exact locations, social-media handles, party registration records, real case names, real news-source accusations, private messages, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted operations files and must be excluded from public analytic data.

This instrument is not a clinical, legal, political, media-literacy, or fact-checking instrument. It asks about hypothetical anxiety responses to standardized AI capability and epistemic trust scenarios.

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI systems and public information. Some scenarios mention digital evidence, synthetic news media, conflicting expert reports, personalized misinformation, elections, or public decisions. These scenarios may feel mildly uncomfortable. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, real case names, social-media handles, party registration records, employer name, school name, client name, or other direct identifiers. Survey responses may be combined with demographic, sampling, media exposure, AI exposure, institutional trust, baseline general anxiety, and information-environment variables for analysis.

This survey does not provide legal advice, political advice, clinical advice, media-literacy training, fact-checking guidance, or predictions about any real court case, election, news story, public agency, household, or future event. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read four short hypothetical scenarios about AI capabilities and public information. Please answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally, your community, a real news event, a real legal matter, or a real election. They are not asking whether the scenario is likely, whether you approve of it, whether a claim is true, or whether you have personally experienced it. We are interested in your anxiety response to the described situation.

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

### Screen 3: Randomized Epistemic Trust ANX Item Block

**Randomization rule:** Present all four ANX item screens exactly once. Randomize item screen order independently for each respondent using a uniform random permutation over the four item IDs. Record the presented order as restricted paradata and derive item-level response timestamp, item response time, and block position variables. Do not randomize response option order.

**Required status:** Each ANX item response is requested, but the platform may allow a respondent to proceed without an item response only if the vendor platform cannot enforce soft-required item screens. Any skipped item must be coded as `missingness_code: skipped_by_respondent` in respondent-item rows.

**Response options for every ANX item**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

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

1. They were hypothetical research scenarios about possible AI capabilities, information, and how a person might feel in response.
2. They were instructions telling me which news, evidence, expert, or election claim to believe.
3. They were predictions about a real court case, election, public health risk, news event, or person.
4. They were questions asking me to provide identifiable political, legal, medical, or media-use information.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities, information, and how a person might feel in response.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 6: Required Epistemic Trust Attribution Check

**Display text**

When answering the four scenarios, what were you mainly asked to rate?

**Response options**

1. How anxious the AI information scenario would make me feel about trusting evidence, media, or expert claims.
2. Whether the scenario is certain to happen to me personally.
3. Which source, expert, platform, party, or institution I should believe.
4. Whether I have personally experienced the exact event described.

**Required:** Yes.

**Correct response:** 1. How anxious the AI information scenario would make me feel about trusting evidence, media, or expert claims.

**QC rule:** Respondents who select any response other than 1 fail the epistemic trust attribution check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `epistemic_attribution_failed`.

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

### Screen 8: Perceived AI Information Exposure Covariate

**Display text**

Thinking about the information you see in daily life, including news, social media, videos, images, search results, official statements, and expert commentary, how exposed is that information environment to current or near-future AI tools?

**Response options**

1. Not at all exposed
2. Slightly exposed
3. Moderately exposed
4. Very exposed
5. Extremely exposed
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `perceived_ai_information_exposure`.

### Screen 9: Information-Environment Role Covariate

**Display text**

Which option best describes the role in which you most often evaluate public information?

**Response options**

1. I mainly evaluate information as a private citizen or community member
2. I study, teach, report, analyze, moderate, or professionally communicate information
3. I work in law, public administration, health, science, education, journalism, or technology
4. I often help family, clients, students, patients, or coworkers interpret information
5. None of these fits well
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `information_environment_role`.

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

How likely is it that AI-generated or AI-contested information will make it harder for people in the United States to know what evidence to trust during the next 6 months?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_information_uncertainty_worry_6m`.

**Display text**

How likely is it that people will feel burdened by needing extra verification steps before trusting AI-mediated images, videos, news summaries, or expert claims during the next 6 months?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_authenticity_verification_burden_6m`.

**Display text**

How likely is it that you would avoid reading, watching, or sharing AI-related news for a while if it made you feel tense about whether information can be trusted?

**Response options**

1. Very unlikely
2. Somewhat unlikely
3. Neither likely nor unlikely
4. Somewhat likely
5. Very likely
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `ai_news_verification_avoidance_intention_6m`.

### Screen 14: Behavioral Criterion Task

**Display text**

The next task is not an ANX-Bench item. It asks how you would allocate a small verification budget in a hypothetical information-review setting.

Imagine that you are helping decide how to review four pieces of public information before they are shared in a community briefing. Each piece has already been checked once by an automated AI system. You have 10 review credits. Each credit assigned to "additional human review" means a trained person spends more time checking source provenance, authenticity, and context. Each credit assigned to "AI-only review is enough" means no additional human review is requested.

Please allocate exactly 10 credits across the two options.

**Response fields**

- `behavioral_human_review_credits`: integer from 0 to 10.
- `behavioral_ai_only_review_credits`: integer from 0 to 10.

**Validation rule:** The two fields must sum to 10. The task must record `behavioral_task_started_timestamp`, `behavioral_task_submitted_timestamp`, `behavioral_task_response_time_seconds`, and whether the platform required correction before submission.

**Required:** Yes.

**Criterion variable:** `revealed_human_verification_allocation_v1`.

**Scoring rule:** This task is a non-scored behavioral criterion. It must not create respondent-item rows and must not be interpreted as an official ANX-Bench score.

### Screen 15: Optional Debrief Comment

**Display text**

If there is anything important about your responses that the research team should understand, you may write it here. Do not include your name, contact information, employer name, school name, social-media handle, party registration information, case names, private messages, or information that identifies another person or institution.

**Response format:** Open text.

**Required:** No.

**QC and ethics use:** Restricted review only for confusion, protest responding, implementation defects, and distress monitoring. Raw text is excluded from public analytic files.

### Screen 16: Debrief and Distress Information

**Display text**

Thank you for completing the survey. The scenarios you read were standardized research materials for validating ANX-Bench, a benchmark that studies psychological responses to AI capabilities. They were hypothetical scenarios, not predictions about any real court case, election, public health issue, news story, person, household, or future event.

This survey does not assign an official ANX-Bench score to you or to any group. It does not provide legal, political, clinical, fact-checking, or media-literacy advice. The questions are used to evaluate whether a set of research items can be interpreted consistently.

If any scenario felt upsetting, you may pause from AI-related news or public-information discussions, take a break, and talk with someone you trust. If you are in the United States and feel in immediate danger, call 911. If you are experiencing a mental health crisis or thoughts of self-harm, call or text 988 for the Suicide and Crisis Lifeline. For legal, political, medical, safety, or public-information decisions, consider consulting qualified sources rather than relying on survey scenarios.

**Response options**

1. Finish survey

**Required:** Yes.
