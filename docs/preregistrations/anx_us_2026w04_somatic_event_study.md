# ANX-Bench US 2026 Wave 4 Somatic Event-Study Preregistration

## Registration Metadata

- Preregistration file: `docs/preregistrations/anx_us_2026w04_somatic_event_study.md`
- Study label: `anx_us_2026w04_somatic_event_study`
- Candidate benchmark version: `ANX-Bench v0.4.0`
- Source scored release: `ANX-Bench v0.3.1`
- Source scored item set: `items/v0.2/somatic_ambient`
- Primary outcome: `somatic_ambient_anxiety_mean`
- Event registry template: `events/v0.4/anx_us_2026w04_somatic_event_registry.template.json`
- Fielding instrument: `docs/instruments/anx_us_2026w04_somatic_event_instrument.md`
- Analysis plan: `analysis/v0.4/somatic_event_study/wave4_event_study_analysis_plan.json`
- Target country and language: United States, English
- Administration mode: online self-administered survey
- Registration status: trigger-based preregistration for the next qualifying major AI capability release

This preregistration freezes the confirmatory design for the next qualifying major AI capability release that occurs after this packet is locked and before any Wave 4 outcome inspection. It converts the already validated v0.3.1 somatic and ambient AI anxiety construct into an event-study outcome without changing item wording, anchors, scoring direction, or construct definition. The packet is a candidate infrastructure release only. It does not create a new citable scored release, does not authorize an overall ANX-Bench score, and does not authorize an event-study claim until the event registry is completed, locked before outcome inspection, fielding is completed, and the observed evidence passes the thresholds specified here and in the machine-readable analysis plan.

## Event Eligibility Rules

A qualifying event is a public AI capability release or deployment that satisfies all inclusion criteria and none of the exclusion criteria below. The event must be about a generally available or clearly documented AI system, model, agent, or AI product capability rather than a rumor, benchmark leak, policy speech, fundraising announcement, or speculative media cycle.

Inclusion criteria:

- The release is publicly announced by the developer, distributor, or a primary documentation source with a timestamped source URL.
- At least two independent sources classify the release as a major capability advance within 48 hours of the public announcement. Independent sources may include benchmark evaluators, technical review outlets, academic labs, safety evaluation organizations, or major technology reporters with direct access to release materials. Developer marketing pages alone do not count as independent classification.
- The released system shows at least one material capability improvement in agentic task execution, coding, scientific problem solving, multimodal generation, persuasion-relevant communication, autonomous tool use, or broad real-world task completion.
- The system is available to a nontrivial external user base, developer base, enterprise customer base, or documented evaluation partner during the exposure window.
- The event has a single first-public timestamp that can anchor an event time. If announcements are staggered, the event timestamp is the earliest public timestamp at which the capability was described with enough specificity for independent classification.
- The event is not already known during the baseline measurement window.

Exclusionary event confounds:

- A major non-AI national crisis, natural disaster, war escalation, terrorist attack, market crash, federal election disruption, or pandemic emergency overlaps the primary exposure or follow-up window and plausibly changes general anxiety independent of AI.
- A separate major AI incident or model release occurs within the primary follow-up window and cannot be separated by timing or exposure measurement.
- The primary source retracts or materially corrects the release announcement before follow-up fielding closes.
- The release is accessible only to a small private test group and has no public documentation suitable for exposure measurement.
- The registry cannot be locked before any outcome data from the follow-up wave are inspected.

If more than one qualifying AI capability release occurs within the same 14-day trigger period, the event adjudication team selects the first event by public timestamp unless the first event fails independent classification by the freeze deadline. Later releases during the same period are recorded as competing AI events and handled as confounds or sensitivity exclusions, not as alternate primary events.

## Registry Lock And Freeze Deadline

The event registry must be completed from `events/v0.4/anx_us_2026w04_somatic_event_registry.template.json` and locked before any follow-up outcome inspection. The registry lock must occur no later than 72 hours after the event timestamp and before the first interim or final tabulation of `somatic_ambient_anxiety_mean`, item means, subgroup means, missingness by outcome value, or treatment-control contrasts.

The locked registry must include:

- Event timestamp in UTC and source-local time when available.
- Primary source URLs and archived URLs.
- Independent classification source URLs and reviewer decisions.
- Exposure window start and end.
- Baseline and follow-up fielding windows.
- Exclusionary confounds reviewed before lock.
- Event adjudicator names or coded reviewer IDs.
- A literal boolean field `event_locked_before_outcome_inspection: true`.

If the registry is not locked by the freeze deadline, the wave may still be reported descriptively as non-preregistered monitoring, but all confirmatory event-study claims are blocked.

## Baseline And Follow-Up Windows

The preferred design is a repeated cross-sectional event study with panel recontact when available. Baseline and follow-up samples must be drawn from the same target population, vendor frame, survey mode, language, eligibility rules, and item wording.

Primary baseline window:

- Opens 14 completed days before the event timestamp.
- Closes 24 hours before the event timestamp.
- Excludes interviews started after the release became public or after credible embargo leakage is documented.

Primary follow-up window:

- Opens 24 hours after the event timestamp.
- Closes 7 completed days after the event timestamp.
- Excludes interviews started before the respondent could plausibly have been exposed to post-event public information.

Secondary event-time bins:

- `pre_minus_14_to_minus_8`
- `pre_minus_7_to_minus_2`
- `event_minus_24h_to_plus_24h`, excluded from the primary contrast
- `post_plus_24h_to_plus_3d`
- `post_plus_4d_to_plus_7d`
- `post_plus_8d_to_plus_14d`, collected only if budget and fielding continuity permit

The primary confirmatory contrast compares eligible baseline respondents from day -14 through day -2 with eligible follow-up respondents from +24 hours through +7 days. The event-day buffer is excluded from the primary contrast because exposure timing is ambiguous.

## Outcome And Scoring

The primary outcome is `somatic_ambient_anxiety_mean`, defined exactly as in ANX-Bench v0.3.1: the arithmetic mean of valid responses to the four approved scored somatic and ambient items:

- `sleep_disruption_ai_news`
- `body_vigilance_model_release`
- `background_dread_ai_progress`
- `avoidance_after_ai_capability_demo`

Each item is scored 1 to 5 with higher scores indicating stronger self-reported somatic and ambient AI anxiety in the scenario. The Wave 4 event instrument must reuse the exact v0.3.1 scenario wording, questions, and response anchors. No item response is reverse coded. Respondents missing any of the four item responses are excluded from the primary construct mean. No item-level or construct-level imputation is permitted for the primary analysis.

Secondary outcomes are the four item scores. They are used for diagnostic interpretation and robustness only. No secondary item result can support a standalone confirmatory event claim unless the primary construct threshold passes and the item result survives the multiple-testing rule in the analysis plan.

## Eligibility, Exclusions, And Quality Control

Eligible respondents must be adults aged 18 or older, located in the United States at administration, able to complete an English-language online survey without assistance, and willing to provide informed consent. The analytic file must not contain direct names, phone numbers, street addresses, email addresses, IP addresses, or raw device fingerprints.

Primary-analysis exclusions are fixed before outcome inspection:

- No informed consent.
- Under age 18, not located in the United States, or unable to complete the English instrument without assistance.
- Duplicate respondent or ambiguous panel linkage, retaining only the earliest complete eligible record when a duplicate can be resolved.
- Failed instructed-response attention check.
- Failed AI-scenario comprehension check.
- Failed somatic-attribution check.
- Any missing, refused, non-substantive, or out-of-range response for the four scored items.
- Completion time below one-third of the median among non-breakoff completes within the same baseline or follow-up period.
- Vendor or platform evidence of fraudulent, bot-assisted, non-human, or inattentive responding.
- Respondent reports that a current medical condition, medication, substance use, acute illness, or unrelated personal crisis was the main basis for their answers rather than the AI scenarios.
- Respondent was interviewed in the event-day buffer from 24 hours before through 24 hours after the event timestamp.
- Respondent was exposed to a documented exclusionary confound before completing the follow-up survey, when the confound is listed as release-blocking in the locked registry.

Exclusion counts must be reported in a CONSORT-style flow table separately for baseline and follow-up. Exclusion rules may not be changed after outcome inspection except as explicitly labeled exploratory.

## Weighting

Primary estimates use survey weights designed to make baseline and follow-up analytic samples comparable to the US adult online target population and to each other. The starting weight is the vendor or panel post-stratification weight for age group, gender, race and ethnicity, education, Census region, and, when available, urbanicity. A balancing adjustment then calibrates baseline and follow-up samples to a common covariate distribution using pre-outcome variables only.

Required balancing variables:

- Age group.
- Gender.
- Race and ethnicity.
- Education.
- Census region.
- Employment status.
- Household income band.
- Political ideology or party identification when collected before outcome items.
- Baseline general anxiety screener or brief distress covariate when collected before outcome items.
- Prior AI use.
- AI-news attention in the 30 days before the survey.
- Occupational proximity to AI systems.
- Device type.

Weights are trimmed to the interval 0.25 to 4.00 and rescaled to the analytic sample size within baseline and follow-up periods. Unweighted estimates, weight-trim sensitivity estimates, and overlap diagnostics are required. If effective sample size falls below 65 percent of nominal sample size in either period, the event evidence must be labeled weighting-sensitive.

## Estimand And Confirmatory Model

The primary estimand is the average event-associated change in `somatic_ambient_anxiety_mean` among US English online adult respondents in the post-event window relative to the pre-event baseline window, adjusted for secular response differences using a control outcome or comparison exposure where available.

The confirmatory model is a weighted difference-in-differences or event-study regression:

`somatic_ambient_anxiety_mean_i = alpha + beta_1 post_event_i + beta_2 exposed_i + beta_3 post_event_i * exposed_i + gamma'X_i + epsilon_i`

The primary coefficient is `beta_3` when a valid comparison group or exposure gradient exists. If all respondents are population-exposed and no defensible comparison group is available, the primary coefficient is `beta_1` from the interrupted repeated-cross-section model with the same covariates, and the claim label must be "event-associated change" rather than "difference-in-differences effect."

Acceptable comparison definitions are fixed in priority order:

1. Respondent-level verified awareness of the event before outcome response, compared with respondents who had not heard of the event, using only awareness questions administered after the four scored items.
2. High versus low pre-event AI-news attention, measured before outcome items, if awareness is not available or is post-treatment-contaminated.
3. A negative-control construct or non-AI anxiety item collected with stable wording across baseline and follow-up, if included in the same fielding packet.

Covariates are age group, gender, race and ethnicity, education, Census region, employment status, household income band, political ideology or party identification, prior AI use, AI-news attention, occupational AI exposure, brief general anxiety or distress covariate, device type, day-of-week fixed effects, and survey vendor or sample-source fixed effects if more than one source is used. Robust standard errors must be used. If the same respondents appear in baseline and follow-up, respondent-clustered standard errors are required.

## Heterogeneity Limits

Confirmatory heterogeneity is limited to four pre-specified moderators:

- Prior AI use: none or rare versus monthly or more.
- AI-news attention before the event: low versus high.
- Occupational AI exposure: low versus high.
- Baseline general anxiety or distress: lower half versus upper half of the analytic sample.

Heterogeneity tests use interaction terms with the primary event coefficient and Holm adjustment across the four moderators. Demographic subgroup tables may be reported descriptively for transparency, but age, gender, race and ethnicity, education, income, region, and political subgroups are not confirmatory heterogeneity claims in this packet unless a later preregistered addendum is locked before fielding.

## Multiple Testing And Robustness

The primary construct test is evaluated at two-sided alpha 0.05. Secondary item tests are interpreted only after the primary construct threshold passes and use Holm adjustment across four item outcomes. Heterogeneity tests use a separate Holm family across the four moderators and cannot rescue a failed primary construct test.

Required robustness checks:

- Unweighted model.
- Alternative weight trimming at 0.20 to 5.00.
- Excluding respondents who report no awareness of the event before the survey.
- Excluding respondents who report a major unrelated personal crisis during the prior week.
- Excluding respondents with very high general distress measured before the item block.
- Narrow follow-up window of +24 hours through +3 days.
- Placebo pre-trend contrast comparing day -14 through day -8 with day -7 through day -2.
- Event-day buffer sensitivity that includes, then excludes, interviews from -24 hours through +24 hours.
- Negative-control outcome or comparison outcome when collected.

Robustness checks are supportive diagnostics. The confirmatory claim requires the primary specification to pass.

## Pass, Fail, And Blocked Claims

The packet supports a confirmatory event-associated somatic anxiety claim only if all conditions hold:

- Locked registry has `event_locked_before_outcome_inspection: true`.
- Event satisfies eligibility rules and has no release-blocking confound.
- Primary baseline analytic N is at least 750 and primary follow-up analytic N is at least 750.
- Effective weighted N is at least 500 in each period.
- Primary coefficient is positive, two-sided p < 0.05, and at least 0.15 points on the 1 to 5 construct scale.
- The 95 percent confidence interval lower bound for the primary coefficient is above 0.03 points.
- Placebo pre-trend absolute coefficient is below 0.10 points and not statistically significant at p < 0.05.
- The result is not reversed or reduced below 0.10 points in the unweighted, narrow-window, and weight-trim robustness checks.

The packet supports a stronger difference-in-differences claim only if a valid comparison definition is available before outcome inspection and the primary interaction coefficient passes the same threshold. Without a valid comparison definition, reports must use "event-associated change" language.

Blocked claims:

- No claim that the event caused clinical anxiety, illness, panic, insomnia, or population mental-health harm.
- No overall ANX-Bench score, cross-domain score, or general AI anxiety index.
- No claim about countries, languages, offline populations, adolescents, clinical populations, organizations, or occupational groups outside the sampled frame.
- No claim that the event changed long-term anxiety beyond the preregistered follow-up window.
- No mechanistic claim that model capability itself, media framing, stock-market reaction, policy discourse, or personal job threat caused the outcome unless a future design directly identifies that mechanism.
- No item-level headline claim if the construct-level result fails.
- No exploratory subgroup, alternate window, alternate exposure definition, or post hoc exclusion result may be described as confirmatory.

## Reproducibility Archive

The completed evidence packet must archive the locked event registry, frozen instrument, sampling frame definition, invitation and completion timestamps, exact baseline and follow-up windows, fielding vendor documentation, exclusion flow, weight construction code, analysis code, model outputs, robustness tables, event-source archive, independent classification records, and a deviation log. Any release, benchmark card, manuscript, or public report must cite this preregistration, the locked event registry, and the analysis plan. Deviations after outcome inspection must be labeled exploratory and cannot support v0.4.0 candidate promotion to a citable event-study release.
