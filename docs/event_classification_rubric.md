# ANX-Bench Prospective AI Capability Event Adjudication Rubric

Rubric version: `v0.1.0`

This rubric defines how ANX-Bench classifies AI capability events before outcome data are inspected. Its purpose is to prevent post hoc event selection, standardize event-study exposure definitions, and make confirmatory claims auditable across benchmark releases.

The rubric governs event records in `schema/event_registry.schema.json`. A registry may contain `event_id: no_event` for calibration, bridge, or reliability waves. Any other event record must include completed `event_adjudication` metadata locked before ANX-Bench response outcomes are inspected.

## Qualifying AI Events

A qualifying AI event is a discrete, externally timestamped public occurrence that plausibly changes what affected respondents know, believe, or experience about AI capabilities. The event must satisfy all criteria below:

1. It concerns AI capability, capability access, capability deployment, capability misuse, or authoritative societal response to capability.
2. It has an independently verifiable timestamp from an official release note, archived public report, regulatory filing, court or policy document, archived news wire, academic or dataset record, or comparable archived source.
3. It is public enough to plausibly reach the study population during the exposure window.
4. It can be mapped prospectively to at least one ANX-Bench domain using evidence available before outcome inspection.
5. It can be separated from routine background AI news by novelty, scale, concrete deployment, or documented public attention.

Qualifying categories include frontier model releases, capability demonstrations, AI safety incidents, labor-market announcements, policy or regulatory actions, misinformation or deepfake incidents, infrastructure or access changes, and other events explicitly prespecified in a locked registry.

## Exclusion Rules

Exclude an event from confirmatory event-study use if any condition below applies:

- The event was selected, retimed, or reclassified after inspecting ANX-Bench outcomes.
- The timestamp cannot be independently verified or is based only on informal social media discussion without archival support.
- The event is merely routine product maintenance, pricing noise, minor user-interface revision, marketing repetition, or speculative commentary without a new capability, deployment, incident, or authoritative action.
- The event primarily concerns a non-AI technology unless the AI mechanism is central to the public claim.
- The expected affected domains are defined from observed ANX-Bench response movement rather than prospective rationale.
- The event is too diffuse to define a credible exposure timestamp, baseline window, and follow-up windows.
- A larger contemporaneous event is likely to dominate interpretation and cannot be handled through competing-event documentation or sensitivity analysis.

Excluded events may be described in exploratory notes, but they cannot support confirmatory event-study claims.

## Severity Tiers

Severity is assigned from external evidence available before outcome inspection. It measures the expected psychological salience of the AI capability event for the target population, not the observed ANX-Bench effect size.

| Tier | Label | Definition | Confirmatory use |
| --- | --- | --- | --- |
| `tier_1_minor` | Minor | Narrow, incremental, or specialist-facing AI event with limited likely public reach or limited implication for ordinary respondents. | Exploratory by default unless a preregistration justifies a domain-specific confirmatory claim. |
| `tier_2_moderate` | Moderate | Public AI event with clear new capability, access, deployment, incident, or policy implication and plausible relevance to at least one ANX-Bench domain. | Minimum default tier for confirmatory event-study claims. |
| `tier_3_major` | Major | Broadly visible AI event with substantial capability, deployment, misuse, labor, safety, policy, or public-trust implications across one or more domains. | Eligible for confirmatory overall and domain claims when other preregistration requirements are met. |
| `tier_4_systemic` | Systemic | Exceptional AI event with sustained public reach, cross-domain implications, and credible potential to shift broad psychological response to AI capabilities. | Eligible for confirmatory overall, domain, and prespecified subgroup claims when other requirements are met. |

Preregistrations may set a stricter minimum tier. They may not lower the minimum tier for confirmatory claims after outcome inspection.

## Public Reach Tiers

Public reach is coded separately from severity because a technically important event may have low public exposure.

| Tier | Definition |
| --- | --- |
| `reach_1_specialist` | Primarily visible to AI specialists, developers, investors, researchers, or directly affected organizations. |
| `reach_2_sectoral` | Visible within a major sector, occupation, user community, or policy community relevant to a named ANX-Bench domain. |
| `reach_3_general_public` | Reported or disseminated through channels plausibly reaching a broad adult population in the study geography. |
| `reach_4_sustained_mass` | Sustained, high-volume public attention across multiple mainstream or official channels. |

## Novelty Tiers

Novelty captures whether the event changes the public capability reference point rather than restating known information.

| Tier | Definition |
| --- | --- |
| `novelty_1_incremental` | Small extension, routine deployment, or repeated public claim with little new capability evidence. |
| `novelty_2_distinct` | Clear new capability, access condition, incident, or institutional action relative to recent public knowledge. |
| `novelty_3_breakthrough` | Material capability or deployment change that would reasonably update public expectations in at least one domain. |
| `novelty_4_paradigm` | Exceptional event that plausibly changes the general public frame for AI capability, control, safety, labor, or social trust. |

## Affected-Domain Mapping

Coders must assign `capability_domain` and `affected_domains` prospectively. The mapping must be justified in `affected_domain_rationale` using only source evidence available before outcome inspection.

| ANX-Bench affected domain | Include when the external evidence implies |
| --- | --- |
| `economic_vocational` | Labor displacement, occupational automation, hiring, wages, professional identity, workplace surveillance, or employment security. |
| `epistemic` | Truth, expertise, misinformation, persuasion, deepfakes, model reliability, information verification, or public knowledge integrity. |
| `relational` | Human relationships, companionship, social replacement, intimacy, caregiving, education, or interpersonal dependence on AI systems. |
| `existential_identity` | Human distinctiveness, meaning, status, creativity, agency, self-concept, or long-run human role concerns. |
| `autonomy_surveillance` | Monitoring, behavioral control, profiling, targeting, coercive personalization, institutional deployment, or loss of privacy. |
| `safety_catastrophic` | Physical safety, biosecurity, cybersecurity, weapons, autonomous harm, loss of control, or catastrophic risk. |
| `somatic_ambient` | Sleep, bodily arousal, background dread, vigilance, avoidance, or diffuse physiological unease tied to AI capability news. |

If an event maps to multiple domains, coders must identify the primary `capability_domain` and list all expected ANX-Bench affected domains in the registry. A domain cannot be added after outcome inspection for confirmatory analysis.

## Coder Independence

Each candidate event must be reviewed by at least two coders before outcome inspection. Coders must:

- Work from the same source packet and rubric version.
- Record independent values for qualification status, severity tier, public reach tier, novelty tier, capability domain, affected domains, and exclusion-rule flags.
- Avoid viewing ANX-Bench response outcomes, score distributions, subgroup estimates, item summaries, or preliminary event-study models.
- Use stable `coder_ids` that identify the adjudication role without exposing unnecessary personal information in public artifacts.

The registry records the final coder identifiers in `coder_ids` and summarizes material disagreements in `coder_disagreements`.

## Reconciliation

Disagreements must be reconciled before registry lock. Reconciliation may use discussion, a third adjudicator, or a documented principal-investigator decision. The final `reconciliation_decision` must state:

- Which disputed fields changed during reconciliation.
- The evidence that determined the final classification.
- Whether any coder maintained a dissent.
- Whether the event remains eligible for confirmatory claims.

If coders disagree on qualification or severity and no documented reconciliation is completed before outcome inspection, the event is ineligible for confirmatory event-study claims.

## Lock Before Outcome Inspection

For confirmatory use, the event registry and completed preregistration must be locked before any ANX-Bench outcome inspection for the relevant wave. Outcome inspection includes viewing overall, domain, construct, item, subgroup, or respondent-level response summaries, even if no formal model has been run.

The locked registry must include:

- `event_adjudication.qualifies` set from prospective adjudication.
- Severity, public reach, novelty, and capability-domain tiers.
- Affected-domain rationale.
- Coder identifiers, disagreements, and reconciliation decision.
- `source_count` and source URLs sufficient to verify the timestamp and classification.
- Baseline, exposure, and follow-up windows.
- Registry and event lock dates.

Post-lock changes that alter event qualification, severity, affected domains, or timing make the affected confirmatory claim exploratory unless the change is a documented clerical correction that preserves the original prospective decision.
