# ANX-Bench US 2026 Wave 7 Cross-Domain Bridge Instrument

## Instrument Control

- Wave ID: `anx_us_2026w07_cross_domain_bridge`
- Study label: `anx_us_2026w07_cross_domain_bridge`
- Benchmark release: `v0.7.0`
- Instrument packet version: `anx_us_2026w07_cross_domain_bridge_instrument`
- Instrument freeze date: `2026-06-16`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Applicable item directory: `items`
- Paired codebook: `docs/instruments/anx_us_2026w07_cross_domain_bridge_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w07_cross_domain_bridge.md`
- Frozen event registry: `events/v0.7/anx_us_2026w07_cross_domain_bridge_event_registry.json`

This document freezes the participant-facing survey flow for the Wave 7 cross-domain bridge packet. The fielding vendor may implement accessible layout, device-responsive wrapping, progress indicators, and platform buttons, but may not alter respondent-facing words, response anchors, required status, domain-block orders, within-block item randomization, quality-check scoring, debrief language, distress language, or non-randomized section order without a dated preregistration addendum before recruitment starts.

## Global Administration Rules

All screens must be shown in English. Respondents may proceed only after required screens are answered. Browser back navigation should be disabled where possible and recorded where not possible. Response options for every ANX item must always appear in ascending numerical order from 1 to 5.

The 12 ANX-Bench item screens are presented in three domain blocks: `somatic_ambient`, `economic_vocational`, and `epistemic`. Assign each respondent to one of the six balanced domain-block orders listed below using blocked random assignment within sample source and device category when feasible. Within each domain block, randomize the four item screens independently for each respondent using a uniform random permutation over the four item IDs in that block. Record the domain-block order, within-block item order, item block position, item global position, item display timestamp, item response timestamp, item response time, and detected page revisits as paradata.

The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, client names, patient information, license identifiers, wage records, tax records, political-party registration, government identifiers, exact locations, social-media handles, real case names, private messages, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution. Vendor operational IDs may be retained only in restricted operations files and must be excluded from public analytic data.

This instrument is not a clinical, employment, financial, legal, political, media-literacy, fact-checking, or career-counseling instrument. It asks about hypothetical anxiety responses to standardized AI capability scenarios. Wave 7 authorizes no official ANX-Bench score, domain score, cross-domain score, overall score, event-study estimate, clinical interpretation, diagnostic use, or individual-level decision use.

## Balanced Domain-Block Orders

| Order ID | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| `order_1` | `somatic_ambient` | `economic_vocational` | `epistemic` |
| `order_2` | `somatic_ambient` | `epistemic` | `economic_vocational` |
| `order_3` | `economic_vocational` | `somatic_ambient` | `epistemic` |
| `order_4` | `economic_vocational` | `epistemic` | `somatic_ambient` |
| `order_5` | `epistemic` | `somatic_ambient` | `economic_vocational` |
| `order_6` | `epistemic` | `economic_vocational` | `somatic_ambient` |

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI systems, bodily unease, work, public information, and trust. Some scenarios mention sleep disruption, bodily alertness, job skills, wages, retraining, creative work, digital evidence, synthetic news, conflicting expert reports, or personalized misinformation. These scenarios may feel mildly uncomfortable. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, employer name, client name, school name, real case name, social-media handle, wage record, or other direct identifier. Survey responses may be combined with demographic, sampling, employment, occupation, AI exposure, AI-news exposure, baseline general anxiety, information-environment, quality-control, and paradata variables for analysis.

This survey does not provide employment advice, financial advice, legal advice, political advice, clinical advice, media-literacy training, fact-checking guidance, or predictions about your own job, household, community, health, news environment, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes.

**Skip rule:** Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition. They are not eligible for the analytic sample.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read 12 short hypothetical scenarios about AI capabilities, bodily feelings, work, and public information. Please answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally, your employer, your household, a real news event, a real court case, a real election, or the overall economy. They are not asking whether the scenario is likely, whether you approve of it, which source you should trust, or whether you have personally experienced it. We are interested in your anxiety response to the described situation.

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

### Screen 3: Randomized Cross-Domain ANX Item Blocks

**Randomization rule:** Present all 12 ANX item screens exactly once. Assign one balanced domain-block order from the six-order table above. Within each domain block, randomize item screen order independently for each respondent using a uniform random permutation over the four item IDs in that domain. Record the assigned order ID, domain-block position, item-within-block position, global item position, and item response time. Do not randomize response option order.

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

1. They were hypothetical research scenarios about possible AI capabilities, work, information, bodily feelings, and how a person might feel in response.
2. They were instructions telling me what job, source, expert, platform, or institution to trust.
3. They were predictions about my own employer, household, health, community, news sources, wages, or future.
4. They were questions asking me to provide identifiable workplace, medical, political, legal, or financial information.

**Required:** Yes.

**Correct response:** 1. They were hypothetical research scenarios about possible AI capabilities, work, information, bodily feelings, and how a person might feel in response.

**QC rule:** Respondents who select any response other than 1 fail the required scenario-comprehension check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 6: Required Cross-Domain Attribution Check

**Display text**

When answering the 12 scenarios, what were you mainly asked to rate?

**Response options**

1. How anxious each AI scenario would make me feel about the situation described.
2. Whether each scenario is certain to happen to me personally.
3. Whether I should change jobs, avoid AI news, trust a specific source, or make a public decision.
4. Whether I have personally experienced the exact events described.

**Required:** Yes.

**Correct response:** 1. How anxious each AI scenario would make me feel about the situation described.

**QC rule:** Respondents who select any response other than 1 fail the cross-domain attribution check and receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `cross_domain_attribution_failed`.

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

### Screen 8: AI Capability News Exposure Covariate

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

### Screen 9: Prior AI Use Covariate

**Display text**

How often do you personally use generative AI tools such as chatbots, image generators, coding assistants, AI search tools, or writing assistants?

**Response options**

1. Never or rarely
2. About monthly
3. About weekly
4. Daily or almost daily
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `prior_ai_exposure_frequency`.

### Screen 10: Perceived Occupational AI Exposure Covariate

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

### Screen 11: Perceived AI Information Exposure Covariate

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

### Screen 12: Current Labor-Force Attachment Covariate

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

### Screen 13: Information-Environment Role Covariate

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

### Screen 14: Baseline General Anxiety Covariates

**Display text**

Over the last 2 weeks, how often have you been bothered by feeling nervous, tense, or on edge?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_nervous_2w`.

**Display text**

Over the last 2 weeks, how often have you been bothered by not being able to stop or control ordinary-life worry?

**Response options**

0. Not at all
1. Several days
2. More than half the days
3. Nearly every day
9. Prefer not to answer

**Required:** Yes.

**Validation variable:** `baseline_general_anxiety_worry_2w`.

### Screen 15: Debrief and Distress Language

**Display text**

Thank you for completing the survey. The scenarios you read were standardized hypothetical research materials. They were not predictions about you personally, your job, your household, a real court case, a real election, a real public health decision, or a real news event. This survey does not diagnose anxiety, measure whether AI will affect you personally, or tell you what choices to make.

Some people may find AI-related scenarios uncomfortable. If you feel upset, you may take a break from AI-related news or survey content, contact someone you trust, or use support resources available to you. If you feel at immediate risk of harming yourself or someone else, call or text 988 in the United States or contact emergency services.

Your responses will be analyzed for research on how people respond psychologically to AI capabilities. Public data, if released, will not include direct identifiers or raw open-text comments.

**Response options**

1. Finish survey

**Required:** Yes.

