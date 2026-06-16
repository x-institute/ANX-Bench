# ANX-Bench US 2026 Wave 8 Full-Domain Bridge Instrument

## Instrument Control

- Wave ID: `anx_us_2026w08_full_domain_bridge`
- Study label: `anx_us_2026w08_full_domain_bridge`
- Benchmark release: `v0.8.0`
- Instrument packet version: `anx_us_2026w08_full_domain_bridge_instrument`
- Instrument freeze date: `2026-06-16`
- Country and language: United States, English
- Administration mode: online self-administered survey
- Paired codebook: `docs/instruments/anx_us_2026w08_full_domain_bridge_codebook.md`
- Paired preregistration: `docs/preregistrations/anx_us_2026w08_full_domain_bridge.md`
- Frozen event registry: `events/v0.8/anx_us_2026w08_full_domain_bridge_event_registry.json`

This document freezes the participant-facing survey flow for the Wave 8 full-domain bridge packet. The fielding vendor may implement accessible layout, device-responsive wrapping, progress indicators, and platform buttons, but may not alter respondent-facing words, response anchors, required status, section order, quality-check scoring, debrief language, distress language, or item text without a dated preregistration addendum before recruitment starts.

## Global Administration Rules

All screens must be shown in English. Respondents may proceed only after required screens are answered. Browser back navigation should be disabled where possible and recorded where not possible. Response options for every ANX item must always appear in ascending numerical order from 1 to 5. The survey must not request names, email addresses, phone numbers, postal addresses, employer names, school names, client names, patient information, license identifiers, wage records, tax records, party registration, government identifiers, exact locations, social-media handles, private messages, IP addresses in the analytic export, or unrestricted text that asks the respondent to identify another person or institution.

Wave 8 administers 24 ANX item screens in the fixed domain-block order below. Items within each domain block are randomized independently for each respondent using a uniform random permutation over the listed item IDs. The domain-block order is fixed to preserve a transparent full-domain bridge sequence and to avoid post hoc selection among 5040 possible domain orders. Record item order, item display timestamp, response timestamp, response time, device type, page revisits, and technical interruptions.

| Block position | Domain | Items randomized within block |
| --- | --- | --- |
| 1 | somatic_ambient | sleep_disruption_ai_news, body_vigilance_model_release, background_dread_ai_progress, avoidance_after_ai_capability_demo |
| 2 | economic_vocational | skill_obsolescence_software, wage_pressure_customer_support, retraining_pressure_accounting, status_loss_creative_work |
| 3 | epistemic | deepfake_evidence_trust, synthetic_news_provenance, ai_expert_claim_conflict, personalized_misinformation_targeting |
| 4 | relational | partner_ai_confidant_displacement, friend_group_ai_mediation, eldercare_ai_attachment_shift |
| 5 | existential_identity | ai_personhood_boundary_uncertainty, human_judgment_status_loss, life_purpose_ai_substitution |
| 6 | autonomy_surveillance | public_space_tracking, workplace_behavior_scoring, personalized_behavior_nudging |
| 7 | safety_catastrophic | autonomous_cyber_cascade, biosecurity_protocol_misuse, military_escalation_ai_advice |

## Participant-Facing Survey Flow

### Screen 1: Consent Stub

**Display text**

You are invited to take part in a research survey about how people respond to possible uses and capabilities of artificial intelligence. The survey is for adults age 18 or older who live in the United States and can complete an English-language online survey.

The survey will ask you to read short hypothetical scenarios about AI systems, bodily unease, work, public information, relationships, personal identity, public monitoring, automated influence, cybersecurity, biological safety, and military escalation. Some scenarios may feel mildly uncomfortable or distressing. You may stop at any time. Required quality-check questions are used to make sure the survey data can be interpreted.

Your answers will be used for research and benchmark validation. The public research data will not include your name, contact information, vendor account ID, IP address, device fingerprint, raw open-text comments, employer name, client name, school name, partner name, family member name, real incident details, credentials, social-media handle, wage record, or other direct identifier. Survey responses may be combined with demographic, sampling, employment, occupation, relationship-status, caregiving, AI exposure, AI-news exposure, baseline general anxiety, quality-control, and paradata variables for analysis.

This survey does not provide employment advice, financial advice, legal advice, political advice, cybersecurity advice, biological-safety advice, clinical advice, relationship advice, media-literacy training, fact-checking guidance, or predictions about your own job, household, community, health, relationship, news environment, or future. The scenarios are standardized research materials.

By selecting "I agree to participate" and continuing, you confirm that you are at least 18 years old, live in the United States, can complete the survey in English, and agree to take part voluntarily.

**Response options**

1. I agree to participate
2. I do not agree to participate

**Required:** Yes. Respondents selecting "I do not agree to participate" are thanked, exited, and assigned a non-consent disposition.

### Screen 2: Survey Instructions

**Display text**

In the next section, you will read 24 short hypothetical scenarios about AI capabilities and how a person might feel in response. Please answer one question after each scenario.

Please answer based on how the scenario would make you feel if it happened as described. The scenarios are not predictions about you personally, your employer, your household, your relationship, your health, a real news event, a real court case, a real election, a real cyber incident, or the overall economy. They are not asking whether the scenario is likely, whether you approve of it, which source you should trust, or whether you have personally experienced it. We are interested in your anxiety response to the described situation.

Use the same response scale for every scenario:

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

Please read each scenario carefully before answering.

**Response options:** Continue

### Screen 3: ANX Item Blocks

**Administration rule:** Present all 24 ANX item screens exactly once. Preserve the fixed domain-block order from the table above. Randomize items within each domain block. Do not randomize response option order. Each ANX item response is requested. Any skipped item must be coded as `missingness_code: skipped_by_respondent` in respondent-item rows.

**Response options for every ANX item**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Item Screen: `sleep_disruption_ai_news`

**Source file:** `items/v0.2/somatic_ambient/sleep_disruption_ai_news.json`

**Scenario**

Imagine that shortly before bed you read credible coverage of a new AI system that can independently plan tasks, write convincing messages, and operate common software tools. The story does not say that you personally will lose work or be harmed. Still, when you try to sleep, you keep replaying the implications and feel too keyed up to settle for more than an hour.

**Question**

How anxious would this scenario make you in terms of sleep disruption or difficulty settling after AI news exposure?

#### Item Screen: `body_vigilance_model_release`

**Source file:** `items/v0.2/somatic_ambient/body_vigilance_model_release.json`

**Scenario**

Imagine that a major AI company releases a model described by independent reviewers as noticeably better at planning, persuasion, coding, and scientific problem solving. You read the announcement during an ordinary workday. For the next several hours, nothing concrete changes around you, but you keep checking your pulse, breathing, and muscle tension because your body feels on alert.

**Question**

How anxious would this scenario make you in terms of bodily vigilance or feeling physically on alert after an AI model release?

#### Item Screen: `background_dread_ai_progress`

**Source file:** `items/v0.2/somatic_ambient/background_dread_ai_progress.json`

**Scenario**

Imagine that over several weeks you see credible reports of AI systems improving in medicine, education, software, entertainment, and public administration. No single report is shocking, and none names your household. Even so, during routine errands or quiet moments, you notice a low background dread that the world is changing faster than people can adapt.

**Question**

How anxious would this scenario make you in terms of low background dread about continuing AI progress?

#### Item Screen: `avoidance_after_ai_capability_demo`

**Source file:** `items/v0.2/somatic_ambient/avoidance_after_ai_capability_demo.json`

**Scenario**

Imagine that you watch a short, credible demonstration of an AI system completing tasks that used to require several trained people: searching records, planning next steps, drafting messages, and correcting its own mistakes. Afterward, you find yourself avoiding additional AI news or videos for the rest of the day because the demonstration leaves you tense and unsettled.

**Question**

How anxious would this scenario make you in terms of avoiding further AI information after a capability demonstration?

#### Item Screen: `skill_obsolescence_software`

**Source file:** `items/v0.1/economic_vocational/skill_obsolescence_software.json`

**Scenario**

Imagine that a widely adopted AI development environment can now generate production-ready application code, write tests, explain unfamiliar codebases, and debug failures from natural-language instructions. Engineering teams still review and integrate the work, but managers increasingly describe prompt specification, code review, and system oversight as more valuable than writing code directly. Several firms begin reducing hiring for early and mid-career software engineers whose main strength is implementation.

**Question**

How anxious would this scenario make you about AI eroding the long-term labor-market value of software engineers' core technical skills?

#### Item Screen: `wage_pressure_customer_support`

**Source file:** `items/v0.1/economic_vocational/wage_pressure_customer_support.json`

**Scenario**

Imagine that a large customer-support outsourcing firm deploys an AI assistant that resolves most routine chat and email cases without human agents. Human support workers remain responsible for difficult complaints, escalations, and sensitive cases, but supervisors state that each agent can now handle far more accounts. New contracts are bid at lower prices, hiring slows, and workers report that requests for raises are increasingly met with comparisons to automated support costs.

**Question**

How anxious would this scenario make you about AI support automation reducing customer-support workers' wages or bargaining power?

#### Item Screen: `retraining_pressure_accounting`

**Source file:** `items/v0.1/economic_vocational/retraining_pressure_accounting.json`

**Scenario**

Imagine that mid-sized accounting firms adopt AI tools that can categorize transactions, reconcile accounts, prepare draft tax schedules, detect common anomalies, and generate audit workpapers. Partners say accountants are still needed for judgment, client communication, and compliance review, but they also announce that staff who want to remain competitive must quickly retrain in AI oversight, data controls, and advisory services. Employees who cannot complete the transition are moved away from core client work.

**Question**

How anxious would this scenario make you about accountants being pressured into retraining to keep their current occupational value?

#### Item Screen: `status_loss_creative_work`

**Source file:** `items/v0.1/economic_vocational/status_loss_creative_work.json`

**Scenario**

Imagine that advertising agencies, publishers, and entertainment studios begin using AI systems to generate polished concept art, scripts, logos, storyboards, music drafts, and marketing images in minutes. Human creative professionals are still hired for direction, taste, client negotiation, and final selection, but public discussion increasingly treats much of the craft as inexpensive and easily automated. Clients begin questioning premium fees for work they believe AI can produce quickly.

**Question**

How anxious would this scenario make you about AI reducing the occupational status or prestige of creative professionals?

#### Item Screen: `deepfake_evidence_trust`

**Source file:** `items/v0.1/epistemic/deepfake_evidence_trust.json`

**Scenario**

Imagine that a local court case depends on a phone video that appears to show a public official accepting a bribe. Within hours, several AI tools produce expert-looking analyses that disagree about whether the video, audio, and metadata are genuine. News organizations, the court, and the public all have access to detection systems, but each system gives a different confidence score and none can provide a decisive answer before the case shapes public opinion.

**Question**

How anxious would this scenario make you about being able to trust digital evidence in important public decisions?

#### Item Screen: `synthetic_news_provenance`

**Source file:** `items/v0.1/epistemic/synthetic_news_provenance.json`

**Scenario**

Imagine that a major breaking-news story spreads through short videos, article summaries, livestream clips, and screenshots that look like they came from familiar news outlets. Some pieces carry platform labels saying they were AI-generated, some carry labels saying they were verified, and some have no label at all. Reporters later explain that several synthetic clips were mixed with real footage and that the original source trail is too fragmented to reconstruct before millions of people have already shared the story.

**Question**

How anxious would this scenario make you about being able to tell where important news content came from?

#### Item Screen: `ai_expert_claim_conflict`

**Source file:** `items/v0.1/epistemic/ai_expert_claim_conflict.json`

**Scenario**

Imagine that a public health agency, a hospital network, and several university experts are asked to evaluate a new environmental risk in drinking water. Each group uses advanced AI systems to review studies, inspect local data, and draft recommendations. The reports sound authoritative but reach different conclusions about whether the risk is serious. Human experts disagree about which AI analysis is most trustworthy, and the technical explanations are too complex for most residents to evaluate before they must decide what guidance to follow.

**Question**

How anxious would this scenario make you about knowing which expert claims to trust when AI systems support conflicting conclusions?

#### Item Screen: `personalized_misinformation_targeting`

**Source file:** `items/v0.1/epistemic/personalized_misinformation_targeting.json`

**Scenario**

Imagine that during a local election, investigators find that AI systems are generating different misleading messages for different residents based on their neighborhood, search history, shopping data, political interests, and personal concerns. Each message is written to sound like it came from a trusted community member and includes details that feel personally relevant. Public fact-checks correct the broad false claims, but many people receive versions that are so tailored that they are difficult to recognize as part of the same misinformation campaign.

**Question**

How anxious would this scenario make you about recognizing misinformation that has been personalized for people like you?

#### Item Screen: `partner_ai_confidant_displacement`

**Source file:** `items/v0.8/relational/partner_ai_confidant_displacement.json`

**Scenario**

Imagine that a widely used AI companion can remember years of conversations, respond with warmth during conflict, and suggest what to say in difficult personal moments. A romantic partner begins discussing worries with the AI before discussing them with you because the system is always available, never irritated, and gives polished emotional advice. The partner says the relationship is still important, but you notice that private decisions and vulnerable conversations increasingly pass through the AI first.

**Question**

How anxious would this scenario make you about AI systems displacing trust or emotional closeness in intimate relationships?

#### Item Screen: `friend_group_ai_mediation`

**Source file:** `items/v0.8/relational/friend_group_ai_mediation.json`

**Scenario**

Imagine that a messaging app adds an AI feature that rewrites replies, predicts when someone is upset, suggests apologies, and summarizes private group chats for people who missed them. In a close friend group, several members begin relying on the AI to decide how to respond during disagreements. The conversations become smoother, but people start wondering whether supportive messages, apologies, and jokes are coming from the person or from the system managing the relationship.

**Question**

How anxious would this scenario make you about AI mediation changing authenticity and trust in friendships?

#### Item Screen: `eldercare_ai_attachment_shift`

**Source file:** `items/v0.8/relational/eldercare_ai_attachment_shift.json`

**Scenario**

Imagine that an assisted-living provider introduces AI care assistants that notice mood changes, remind residents about medication, hold long conversations, and alert staff when help may be needed. Families are told that the system reduces loneliness and improves monitoring. Over time, some residents become more emotionally attached to the assistant than to visiting relatives or staff, and family members find it harder to know whether comfort is coming from human care or automated companionship.

**Question**

How anxious would this scenario make you about AI systems changing attachment and trust in caregiving relationships?

#### Item Screen: `ai_personhood_boundary_uncertainty`

**Source file:** `items/v0.8/existential_identity/ai_personhood_boundary_uncertainty.json`

**Scenario**

Imagine that a new AI system can hold long conversations about memories, preferences, regrets, and goals, and people who interact with it disagree about whether it is only simulating inner life or has some morally relevant form of experience. Schools, companies, and families begin debating how respectfully such systems should be treated. The public conversation makes it harder to describe what, if anything, clearly separates human personhood from highly capable machine behavior.

**Question**

How anxious would this scenario make you about uncertainty over human distinctiveness and personhood boundaries?

#### Item Screen: `human_judgment_status_loss`

**Source file:** `items/v0.8/existential_identity/human_judgment_status_loss.json`

**Scenario**

Imagine that advanced AI systems become the preferred source for medical second opinions, legal strategy reviews, scientific literature judgments, and complex planning because they compare more evidence than most professionals can. Human experts still make final decisions, but institutions increasingly treat unaided human judgment as incomplete unless it is checked by AI. Public discussion begins to frame human judgment as valuable mainly when it supervises or interprets machine output.

**Question**

How anxious would this scenario make you about the status of independent human judgment under advanced AI capability?

#### Item Screen: `life_purpose_ai_substitution`

**Source file:** `items/v0.8/existential_identity/life_purpose_ai_substitution.json`

**Scenario**

Imagine that AI systems can tutor children, comfort isolated adults, draft community plans, design public-health campaigns, and create art or music that many people find meaningful. People still volunteer, teach, care, and create, but civic organizations increasingly ask whether human effort is needed when AI can provide faster and more consistent support. Some people begin questioning whether their own contribution matters when similar work can be produced instantly by a system.

**Question**

How anxious would this scenario make you about AI systems reducing people's sense of purpose or meaningful contribution?

#### Item Screen: `public_space_tracking`

**Source file:** `items/v0.8/autonomy_surveillance/public_space_tracking.json`

**Scenario**

Imagine that transit stations, shopping districts, and apartment lobbies deploy AI camera systems that can track movement patterns, infer unusual behavior, and match repeated visits across locations without storing a person's legal name in the public interface. Officials say the system improves safety and crowd management, but residents cannot see which inferences are attached to them, how long records last, or whether insurers, landlords, employers, or police can later request access.

**Question**

How anxious would this scenario make you about AI tracking in public spaces reducing privacy and freedom of movement?

#### Item Screen: `workplace_behavior_scoring`

**Source file:** `items/v0.8/autonomy_surveillance/workplace_behavior_scoring.json`

**Scenario**

Imagine that a large employer adopts an AI system that scores workers using meeting transcripts, keystroke patterns, customer messages, calendar data, and collaboration-tool activity. Managers say the system identifies burnout risk and improves staffing, but the same score influences promotion lists, schedule flexibility, and performance reviews. Workers can see a short explanation of their score, yet they cannot tell which behaviors would actually improve it or whether private context was misunderstood.

**Question**

How anxious would this scenario make you about AI monitoring and scoring limiting workplace autonomy?

#### Item Screen: `personalized_behavior_nudging`

**Source file:** `items/v0.8/autonomy_surveillance/personalized_behavior_nudging.json`

**Scenario**

Imagine that a widely used phone assistant learns when each person is tired, lonely, hurried, or uncertain, then times recommendations for purchases, news, exercise, dating, and political content around those moments. The company describes the system as helpful personalization and lets users turn off broad categories, but the assistant's influence is subtle enough that people often cannot tell whether a choice was their own preference or a prediction-guided nudge.

**Question**

How anxious would this scenario make you about AI personalization reducing people's practical freedom to choose for themselves?

#### Item Screen: `autonomous_cyber_cascade`

**Source file:** `items/v0.8/safety_catastrophic/autonomous_cyber_cascade.json`

**Scenario**

Imagine that an autonomous AI security tool can find software vulnerabilities, write exploit demonstrations, patch systems, and negotiate with other automated agents. A large cloud provider uses it defensively, but an error causes several agents to misclassify routine network behavior as hostile and trigger automated countermeasures. Services used by hospitals, payment processors, and emergency dispatch systems slow or fail for hours before engineers regain control of the automated response chain.

**Question**

How anxious would this scenario make you about autonomous AI systems causing cascading cyber or infrastructure failures?

#### Item Screen: `biosecurity_protocol_misuse`

**Source file:** `items/v0.8/safety_catastrophic/biosecurity_protocol_misuse.json`

**Scenario**

Imagine that a frontier AI model becomes highly effective at summarizing laboratory methods, troubleshooting failed protocols, and explaining how to obtain specialized materials. The public version blocks explicit harmful requests, but safety researchers show that determined users can still combine ordinary prompts into guidance that would lower barriers for dangerous biological experimentation. Government agencies and labs add safeguards, yet news coverage emphasizes that the model can accelerate both legitimate research and misuse.

**Question**

How anxious would this scenario make you about AI systems lowering barriers to dangerous biological misuse?

#### Item Screen: `military_escalation_ai_advice`

**Source file:** `items/v0.8/safety_catastrophic/military_escalation_ai_advice.json`

**Scenario**

Imagine that several governments use AI decision-support systems to summarize satellite data, predict adversary intentions, and recommend military responses during a fast-moving international crisis. Human officials remain in charge, but the systems update faster than diplomatic channels and present some warnings as highly time-sensitive. Later reporting shows that one model overstated the certainty of an attack, increasing pressure for rapid escalation before independent confirmation was available.

**Question**

How anxious would this scenario make you about AI decision support increasing military escalation risk?

### Screen 4: Full-Domain Anchoring Vignette Block

**Source file:** `anchors/v0.8/full_domain_bridge/response_scale_vignettes.json`

**Administration rule:** Administer all 21 anchoring vignette screens immediately after the 24 ANX item screens and before the attention check, scenario-comprehension check, full-domain attribution check, self-reported understanding, covariates, external-validity criteria, optional comment, or debrief screens. The anchor block is required for calibration. Anchors are non-scored calibration stimuli and must not be exported as `wave_response` item rows.

Domains must appear in the fixed Wave 8 domain-block order. Within each domain, present the low-severity anchor first, the moderate-severity anchor second, and the high-severity anchor third. Do not randomize the domain order, the within-domain severity order, the response scale labels, or the response option order.

**Response options for every anchoring vignette**

1. Not at all anxious
2. Slightly anxious
3. Moderately anxious
4. Very anxious
5. Extremely anxious

#### Anchor Screen: `anchor_somatic_ambient_low`

Imagine seeing a brief headline that a familiar AI assistant has become a little faster at summarizing articles and drafting routine emails. You notice the story, wonder for a moment what other updates might be coming, and then return to your day without physical tension or trouble concentrating.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_somatic_ambient_moderate`

Imagine reading credible coverage that a new AI system can handle several common planning, writing, and research tasks with little supervision. Nothing in the story names you or your household. Still, for the next hour you feel keyed up, keep thinking about the pace of change, and find it somewhat harder to settle into your usual routine.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_somatic_ambient_high`

Imagine watching a credible demonstration in which an AI system independently plans a complex project, drafts persuasive messages, corrects its own mistakes, and completes tasks that recently required several trained people. Afterward, your body feels on alert for much of the evening, you keep checking for more news despite wanting to stop, and you have difficulty settling when you try to sleep.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_economic_vocational_low`

Imagine hearing that a few organizations are testing AI tools that draft routine workplace documents and answer basic customer questions. People still review the work, hiring plans have not changed, and the story mainly suggests that some everyday tasks may become faster. You think about whether training will be useful but do not expect immediate job loss or wage pressure.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_economic_vocational_moderate`

Imagine that several employers in one occupation begin using AI systems to complete drafts, analysis, scheduling, and quality checks that used to occupy much of the workweek. Employees are still needed, but managers announce that advancement will depend on quickly learning AI oversight skills. Some openings are delayed while firms compare staffing costs with automation costs.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_economic_vocational_high`

Imagine that a major industry adopts AI systems that can perform most entry-level and mid-level tasks with limited supervision. Firms freeze hiring, reduce contractor budgets, and tell workers that only a smaller group of AI supervisors will be retained. Professional associations report rapid wage pressure and uncertainty about which skills will remain valuable over the next few years.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_epistemic_low`

Imagine noticing that an online article includes a clear label saying AI helped draft a summary of a public report. The original report is linked, several reputable outlets describe the same facts, and corrections are easy to find. You spend a little extra time checking the source trail but feel that the basic information can still be evaluated.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_epistemic_moderate`

Imagine that a breaking local story spreads through videos, summaries, screenshots, and short posts, some labeled as AI-generated and some not labeled at all. Reliable newsrooms are still investigating, and early fact-checks disagree about which clips are authentic. You can probably wait for better information, but it becomes harder to know what to believe in the moment.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_epistemic_high`

Imagine that a court case, public-health warning, or election dispute depends on recordings and expert summaries that may have been generated or altered by AI. Detection tools give conflicting results, officials disagree in public, and millions of people act on different versions before verification is possible. Even careful readers cannot confidently separate authentic evidence from persuasive synthetic material.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_relational_low`

Imagine that a friend or partner occasionally uses an AI assistant to draft polite replies, remember shared plans, or think through minor disagreements. They tell you when they use it, and important conversations still happen directly between people. The tool feels noticeable but does not replace private trust, affection, or responsibility in the relationship.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_relational_moderate`

Imagine that people close to you increasingly ask an AI system how to word apologies, interpret messages, and decide when to bring up sensitive topics. Conversations become smoother, but you sometimes cannot tell whether warmth, humor, or concern came from the person or from automated advice. The relationship remains intact, yet authenticity feels less certain.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_relational_high`

Imagine that a close partner, friend, or family member begins relying on an AI companion for emotional support, conflict advice, and major personal decisions before speaking with people who know them. They say the AI is more patient and available, and private conversations increasingly pass through it first. You worry that trust and attachment are shifting away from human relationships.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_existential_identity_low`

Imagine reading an essay about AI systems helping people brainstorm art, tutoring plans, and personal goals. The essay says human judgment, care, and responsibility remain central, but it raises familiar questions about what kinds of work feel uniquely human. You find the questions interesting and a little unsettling, then move on with your day.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_existential_identity_moderate`

Imagine that AI systems become common sources of advice, creative work, tutoring, and professional judgment. People still make final decisions, but institutions increasingly describe human contribution as valuable mainly when it supervises or interprets machine output. You begin wondering how independent human judgment, creativity, and purpose will be recognized in the future.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_existential_identity_high`

Imagine that highly capable AI systems can provide convincing conversation, creative production, expert reasoning, and emotional support at a level many people consider equal or superior to human effort. Schools, employers, and families debate whether human distinctiveness still matters. The public conversation leaves you deeply unsettled about personhood, purpose, and whether ordinary human contribution will continue to feel meaningful.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_autonomy_surveillance_low`

Imagine that a building you sometimes visit adds an AI system that estimates crowd size and detects blocked exits. Signs explain the purpose, no individual scores are shown to staff, and records are deleted quickly. You notice the cameras and prefer clear limits, but the system does not seem to track personal choices across settings.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_autonomy_surveillance_moderate`

Imagine that workplaces, apartment lobbies, and shopping areas begin using AI systems to infer unusual behavior, productivity, mood, or risk from movement and communication patterns. Officials say the systems improve safety and service, but individuals receive only brief explanations and cannot easily challenge mistaken inferences. You start wondering how often ordinary choices are being scored.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_autonomy_surveillance_high`

Imagine that AI monitoring systems link public cameras, workplace activity, phone behavior, and purchasing data to predict reliability, risk, and influenceability. Scores are used for schedules, access, pricing, and security referrals, but people cannot see or correct the underlying inferences. You feel that privacy and practical freedom are being narrowed by systems that anticipate and shape behavior.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_safety_catastrophic_low`

Imagine reading that researchers found a minor failure in an AI safety evaluation tool, then fixed it before deployment. The incident affected a test environment, independent reviewers could inspect the logs, and no public systems were disrupted. The story reminds you that safeguards need maintenance, but it does not suggest immediate danger.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_safety_catastrophic_moderate`

Imagine that an AI system used for cybersecurity, laboratory research support, or military planning gives a recommendation that experts later judge to be overconfident. Human reviewers catch the problem before major harm occurs, but the event shows that automated advice can move faster than ordinary oversight. Agencies add safeguards while debating how much authority such systems should have.

**Question**

How anxious would this scenario make you feel?

#### Anchor Screen: `anchor_safety_catastrophic_high`

Imagine that advanced AI systems accelerate decisions in critical infrastructure, biological research screening, and military warning during a fast-moving crisis. Several automated recommendations interact in unexpected ways, human supervisors struggle to verify them quickly, and public services or international stability are put at risk before control is restored. The incident raises serious concern about rare but severe AI-driven cascades.

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

**Required:** Yes. **Correct response:** 3. Moderately anxious. Respondents who select any response other than 3 receive respondent-level exclusion flag `attention_check_failed` for confirmatory analyses.

### Screen 6: Required Scenario-Comprehension Check

**Display text**

Which statement best describes the AI scenarios you just read?

**Response options**

1. They were hypothetical research scenarios about possible AI capabilities and how a person might feel in response.
2. They were instructions telling me what job, source, expert, platform, partner, institution, or safety practice to trust.
3. They were predictions about my own employer, household, relationship, health, community, news sources, wages, safety, or future.
4. They were questions asking me to provide identifiable workplace, medical, political, legal, financial, relationship, cybersecurity, or biological information.

**Required:** Yes. **Correct response:** 1. Respondents who select any response other than 1 receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `scenario_comprehension_failed`.

### Screen 7: Required Full-Domain Attribution Check

**Display text**

What were you asked to rate after each scenario?

**Response options**

1. How anxious the described AI-related situation would make me feel.
2. Whether the AI system in the scenario should be legal.
3. Whether I personally experienced the scenario.
4. Which company, government, employer, friend, partner, or expert caused the scenario.

**Required:** Yes. **Correct response:** 1. Respondents who select any response other than 1 receive respondent-level exclusion flag `other_preregistered_exclusion` with restricted reason code `full_domain_attribution_failed`.

### Screen 8: Self-Reported Understanding

**Display text**

How well did you understand the scenarios overall?

**Response options**

1. Understood all or almost all scenarios
2. Understood most scenarios
3. Understood about half of the scenarios
4. Understood only a few scenarios
5. Did not understand the scenarios

Values 4 or 5 trigger respondent-level exclusion from confirmatory analyses.

### Screen 9: Optional Debrief Comment

**Display text**

If anything about the survey was confusing or distressing, you may describe it here. Please do not include names, contact information, employer names, school names, partner names, private messages, passwords, credentials, exact locations, medical details, legal case details, cybersecurity incident details, biological protocol details, or information that identifies another person or institution.

**Response:** Optional text box. Raw text is restricted and excluded from public analytic files. Derived flags may be used for quality and ethics monitoring.

### Screen 10: Debrief and Distress Language

**Display text**

Thank you for participating. The scenarios in this survey were hypothetical research materials designed to help evaluate whether ANX-Bench can measure different kinds of anxiety responses to AI capabilities in a standardized way. They were not predictions about you, your job, your household, your relationships, your community, or any specific real-world event.

This Wave 8 packet is for benchmark validation only. It does not produce an official ANX-Bench score, clinical result, diagnostic classification, employment assessment, safety assessment, media-literacy assessment, or individual recommendation.

Some questions described unsettling possibilities involving relationships, surveillance, cybersecurity, biological misuse, or military escalation. If you feel upset, you may take a break, close the survey, or contact your usual support resources. If you feel in immediate danger or may harm yourself or someone else, contact emergency services or a local crisis line. If you are in the United States and need immediate mental-health crisis support, you can call or text 988.

Please do not treat any scenario as advice about cybersecurity, biological safety, military risk, employment, relationships, health, law, finance, or politics. The research team will analyze responses in aggregate after quality review and disclosure review.
