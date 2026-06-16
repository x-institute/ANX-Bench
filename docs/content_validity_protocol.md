# ANX-Bench Content-Validity Blueprint Gate

This protocol defines the content-validity gate that every ANX-Bench item set must pass before it can move to `approved_scored`. Psychometric fit cannot rescue an item set that has not first demonstrated construct coverage, construct distinctiveness, reading accessibility, and ethical acceptability through independent expert review. The gate applies to original item pools, revised item pools, translated or culturally adapted item pools, bridge packets that propose scored promotion, and any item set proposed for construct, domain, overall, longitudinal, or event-study scoring.

The content-validity dossier is a frozen review artifact. It must be completed, versioned, checksum-bound, and signed before exploratory factor analysis, confirmatory factor analysis, reliability, IRT, DIF, invariance, or external-validity results can justify `approved_scored` status. Statistical evidence may diagnose remaining problems, but it cannot substitute for this blueprint review.

## Required Dossier

Each item set seeking scored promotion must have a machine-readable dossier that validates against `schema/content_validity_dossier.schema.json`. The dossier must identify the construct, all candidate item IDs and item versions, domain facets, reviewer eligibility, item-level ratings, item-level content-validity index values, scale-level content-validity index values, revision decisions, unresolved overlap flags, and signoff.

The dossier must be stored with the release or validation materials for the relevant item set. Item records and validation dossiers must reference it before an item set can be labeled `approved_scored`. A narrative memo, spreadsheet, or reviewer correspondence file may supplement the dossier, but none of those artifacts replaces the schema-valid dossier.

## Reviewer Panel

The panel must include at least three independent reviewers. Reviewers are independent only if they did not draft the candidate items, did not manage the fielding vendor for the item set, and do not have a direct release decision role for the same item set. At least two reviewers must have psychometric, survey-methods, clinical, social-science, risk-communication, labor, information-integrity, or adjacent domain expertise relevant to the construct. At least one reviewer must have ethics, participant-protection, human-subjects, or harm-assessment competence.

Before rating, reviewers receive the construct definition, intended score use, target population, administration mode, response scale, domain-facet blueprint, item wording, scoring direction, prior item status, and any planned bridge or longitudinal claim. Reviewers must rate independently before any consensus meeting. Consensus discussion may resolve interpretation issues and guide revision, but it must not overwrite the independent ratings used to calculate CVI.

## Facet Coverage

The item set must include a preregistered domain-facet blueprint. Facets are the substantive coverage claims that the item set is meant to represent, such as somatic sleep disruption, bodily vigilance, labor-market skill obsolescence, wage pressure, evidence provenance, or targeted misinformation. Each candidate item must be assigned to exactly one primary facet and may be assigned to secondary facets only when the dossier explains why the item remains interpretable.

Reviewers must judge whether each primary facet is represented by at least one clear item, whether the item pool overweights any facet without justification, and whether the retained set still covers the intended construct after revisions or exclusions. For scored-promotion eligibility, every required facet must have at least one item with item-level CVI at or above 0.78 and no unresolved construct-overlap flag. A facet with only failed, ambiguous, or ethically blocked items makes the item set ineligible for `approved_scored`.

## Construct Distinctiveness

Reviewers must evaluate whether each item measures the intended ANX-Bench construct rather than a neighboring construct, a general distress response, political attitude, news exposure, occupational insecurity unrelated to AI, generic trust, technological optimism or pessimism, or factual belief. Items may mention concrete AI scenarios, but the response target must be anxiety or unease about the construct, not agreement with a policy position or prediction.

Each item receives a construct-overlap flag status: `none`, `resolved`, or `unresolved`. An unresolved construct-overlap flag blocks scored-promotion eligibility regardless of CVI. Resolution requires a documented wording revision, facet reassignment, item exclusion, or narrowed interpretation approved by the reviewer panel before outcome inspection.

## Reading-Level Review

The review must verify that item stems, response prompts, and scenario language are comprehensible for the target population without requiring specialized AI knowledge unless the item set is explicitly designed for an expert population. Reviewers must assess reading burden, sentence length, ambiguity, double-barreled wording, hidden technical assumptions, uncommon jargon, and whether respondents can answer based on the information provided.

For general-population US English instruments, the target is plain language suitable for adult online survey administration. Any item above an eighth-grade reading target, or any item using unavoidable technical terms, must include a rationale and a comprehension mitigation such as simpler surrounding wording, a brief neutral definition, or exclusion from scored promotion. Reading-level approval is required before pilot or confirmation statistics can be used for `approved_scored`.

## Harm and Ethics Review

The dossier must include harm and ethics review for every candidate item. Reviewers must assess whether scenarios could create avoidable distress, imply clinical diagnosis, prime unsupported threat beliefs, stigmatize occupations or demographic groups, disclose sensitive personal information, manipulate respondents, or encourage individual-level decision use. The review must also confirm that consent, withdrawal, debriefing, distress guidance, privacy handling, and use limitations are proportionate to the item set.

Items can discuss serious AI-related concerns when those concerns are necessary to the construct, but wording must remain standardized, non-sensational, and empirically interpretable. An item with an unresolved ethics flag, unresolved participant-harm flag, or unresolved stigmatization flag cannot move to `approved_scored`.

## Rating Scale and CVI Rules

Each reviewer rates each item on four criteria: relevance to the intended construct, clarity for the target population, facet fit, and ethical acceptability. Ratings use a four-point ordinal scale:

| Rating | Meaning for CVI |
| ---: | --- |
| 1 | Not acceptable for scored use |
| 2 | Needs major revision before scored use |
| 3 | Acceptable with minor or no revision |
| 4 | Strongly acceptable for scored use |

The item-level content-validity index, or I-CVI, is the proportion of independent reviewers rating the item `3` or `4` on the criterion being evaluated. The dossier must report criterion-specific I-CVI values and an overall item I-CVI. The overall item I-CVI is the minimum of the criterion-specific I-CVI values unless the dossier preregisters a stricter rule.

The scale-level content-validity index, or S-CVI/Ave, is the mean overall item I-CVI across retained items. The dossier may also report S-CVI/UA, the proportion of retained items with unanimous acceptable ratings, but S-CVI/UA does not replace S-CVI/Ave for promotion decisions.

For `approved_scored` eligibility, the dossier must show all of the following:

- At least three independent reviewers.
- Every retained item has overall item-level CVI at least 0.78.
- The retained item set has scale-level CVI at least 0.90.
- Every required facet is covered by at least one retained item meeting the item-level CVI threshold.
- No retained item has an unresolved construct-overlap flag.
- No retained item has an unresolved reading-level, harm, ethics, or stigmatization flag.

When exactly three reviewers are used, an item needs unanimous acceptable ratings on each required criterion to meet the 0.78 I-CVI threshold because two of three acceptable ratings yields only 0.67. Larger panels may pass items under the same numeric threshold, but minority objections must still be documented and resolved when they concern construct overlap, participant harm, or ethics.

## Revision Decisions

Every item must receive one of four revision decisions: `retain_without_revision`, `retain_with_minor_revision`, `major_revision_required`, or `exclude`. Minor revisions may simplify wording, remove jargon, improve grammar, or clarify the scenario without changing the construct target, scoring direction, domain facet, response scale, or comparability claim. Minor revisions must be listed in the dossier and reviewed before scored promotion.

Major revisions include changing the response target, changing the scenario mechanism, adding or removing a facet, changing the scoring direction, changing population assumptions, or resolving a construct-overlap or ethics problem through substantive rewriting. Major revisions require a new item version and a renewed content-validity review before the item can support scored promotion.

Excluded items may remain in development archives only if they are clearly labeled as non-scored and are omitted from official scoring, longitudinal comparison, and event-study outcomes. An excluded item cannot be restored to a scored proposal without a new review dossier.

## Promotion and Audit

The content-validity dossier must be completed before the psychometric validation dossier recommends `approved_scored`. A release manifest that promotes an item set must checksum the applicable content-validity protocol, content-validity schema, completed dossier, psychometric protocol, psychometric dossier, preregistration, analysis plan, item files, and evidence provenance files.

Maintainers must audit content-validity dossiers whenever item wording changes, target population changes, administration language changes, response anchors change, construct definitions change, new facets are added, bridge evidence is used to support broader scoring, or an ethics concern is identified after fielding. If the audit finds that the old dossier no longer matches the item set, scored promotion is blocked until a renewed dossier passes this protocol.
