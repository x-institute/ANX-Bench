# ANX-Bench 2027: A Global AI Psychological Response Benchmark and Dataset

**Prompt.** *If given unlimited resources (money, compute, people, experts, time), what benchmark or dataset would you build for 2027? Show the step-by-step plan and the resources needed for each. Show why it is important, innovative, and insightful.*

**Answer, in one sentence.** I would build the instrument that lets us plot a family of series not currently assembled in one dataset: **domain-specific human psychological response to AI on one axis, domain-specific AI capability, deployment, and exposure on the other, by population, by country, quarter over quarter, from 2027 onward**, with each comparison across time, place, and person admitted only after a measurement-invariance gate.

Two framing choices are made up front, because they are where the discipline lives. First, the deliverable is deliberately **not** a single "AI Anxiety Index" number. AI-related response is not one latent quantity; it spans rational risk appraisal, affective arousal, privacy preference, economic insecurity, and political attitude, and the program's Phase C gate can and will refuse a combined index if the data do not support one. Second, "capability" is **not** a single x-axis: public response tracks *perceived* capability, deployment, media salience, and personal exposure, not a raw benchmark score, so the capability side is itself a small panel of domain-specific indices.

The seven-domain taxonomy, versioned release contract, promotion gates, event-study locking, and revealed-behavior schema in this repository (`README.md`) provide a 2026 prototype. The 2027 program extends that prototype and names the artifacts needed to turn it into a public benchmark and dataset.

---

## 1. Why this is the benchmark worth building

### 1.1 The asymmetry

By 2027 the field will have many benchmarks for what models can do, including MMLU, SWE-bench, GPQA, ARC-AGI, and the [METR task-horizon suite](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/). Human response is already measured at meaningful scale, so the novelty claim must be narrower. Pew fielded nationally representative AI-attitude surveys in [25 countries in 2025](https://www.pewresearch.org/global/2025/10/15/how-people-around-the-world-view-ai/). The Stanford AI Index also reports repeated Ipsos measures across countries in its [2026 public-opinion chapter](https://hai.stanford.edu/ai-index/2026-ai-index-report/public-opinion). In the United States, Pew's American Trends Panel and Ipsos KnowledgePanel use probability recruitment; international surveys use country-specific mixtures of telephone, face-to-face, and online designs.

ANX-Bench would add a combination those programs were not designed to provide: construct-level psychometric validation, explicit cross-wave and cross-language comparability gates, respondent-level exposure measures, domain-matched capability and deployment covariates, incentive-compatible behavioral outcomes, and prospectively registered event modules. The contribution is therefore a linked measurement system, not the first survey of AI attitudes. A percentage such as "worried about AI" remains useful descriptively, but it cannot by itself establish that the same latent construct was measured across wording changes, languages, modes, and years.

The gap matters because policy, labor markets, and lab deployment decisions are already being made against the human-response side using instruments not built for cross-time, cross-country comparison. A longitudinal, invariance-linked, capability-indexed human-response benchmark is the missing piece of the AI measurement stack.

### 1.2 The figure family the program is built to defend

The program is organized around producing and defending a family of series (not one headline number), of which the load-bearing view is a domain-resolved capability-versus-response plot:

```
   Domain response (latent, invariance-linked, per construct)
   ^
   |                                        . epistemic (journalists)
   |                              .    .
   |                    .    .              . economic (knowledge workers)
   |          .    .                 .   .
   |   .  .              .   .    .            somatic (general pop)
   +-------------------------------------------------> Domain capability / exposure index
     synthetic-media   labor-task    long-horizon    (per-domain: perceived capability,
     capability        automation    autonomy          deployment, media salience, exposure)
```

The x-axis is deliberately plural: for each domain it is a small index combining a domain-relevant *objective* capability signal (e.g. METR task-horizon or a synthetic-media quality benchmark), a *deployment/exposure* signal (adoption, labor-task exposure), and a *perceived*-capability item measured on the same respondents. Producing any of these series credibly requires exactly the machinery this repo enforces: a latent score that is invariance-linked across waves (so the y-axis means the same thing in 2027 and 2029), a capability index rather than a single benchmark number, and event registries locked before outcome inspection so that spikes are not silently reinterpreted after the fact. **The defensible figure is the deliverable; the invariance gates are what make it defensible.**

### 1.3 Why "important, innovative, insightful," precisely

- **Important:** it is decision-relevant infrastructure. Regulators debating deployment, labs writing responsible-scaling policies, and labor economists modeling displacement all need a calibrated, non-partisan read on human response. A public, versioned, methodologically transparent series can serve that role the way the Michigan Index of Consumer Sentiment serves economic forecasting: a slow, comparable, auditable reference rather than a headline of the week. Whether it earns that standing is an empirical question the gates decide, not a promise this document can make.
- **Innovative:** the novelty is in the combination, not any single part. (a) Treating *human response to AI* as a versioned benchmark with promotion gates and locked event registries, not a re-worded poll. (b) Pairing stated response with *revealed-behavior* tasks and a psychophysiology arm inside a multitrait-multimethod validation model, so self-report is corroborated rather than taken at face value. (c) Indexing the human series against domain-specific capability, deployment, and exposure measures so the two halves of the AI measurement stack can be joined. Each ingredient exists somewhere in the literature; assembling all three under one invariance-gated release contract is what is new.
- **Insightful:** the questions the instrument is built to answer are substantive regardless of which way they resolve. The **stated-versus-revealed gap** (whether people who report calm nonetheless pay to avoid AI, or the reverse) is informative in either direction. The **proximity effect** (whether response to AI doing *your* specific task differs, and how much, from response to AI in the abstract) speaks directly to the displacement debate. The **cross-cultural map** (whether societies metabolize the same capability shock as threat or as tool) is a first-order input to global AI governance. The value is that the design can return a null or a surprise with the same authority as a headline finding.

---

## 2. Design principles carried over from the 2026 skeleton

The 2027 program inherits, and does not relax, six commitments already encoded in this repository. They are what stop the program from collapsing into "we ran a big survey."

1. **Versioned, not ad hoc.** Every wave is a frozen release with a machine-readable manifest, checksum-bound instruments, and a promotion gate. See the release contract in `README.md`.
2. **Invariance is release-blocking.** If the scale does not pass measurement-invariance gates across waves and populations, the time series is not comparable and the claim is blocked. This is the difference between a benchmark and a tracking poll.
3. **Event registries lock before outcome inspection.** A wave cannot be retroactively reinterpreted as an event study after someone sees a spike they like. `event_locked_before_outcome_inspection: true` is enforced in the schema.
4. **Revealed behavior is first-class.** `schema/behavioral_response.schema.json` and the `revealed_ai_review_allocation_v1` task exist so stated anxiety is always checkable against a costly choice.
5. **Distinct from general and dispositional anxiety.** The [GAD-7](https://doi.org/10.1001/archinte.166.10.1092) measures recent generalized-anxiety symptoms, not trait anxiety. ANX-Bench therefore requires discriminant evidence against GAD-7, a validated dispositional-anxiety measure, technophobia, privacy preference, and institutional distrust.
6. **Panel conditioning is a tracked threat, not an afterthought.** Refreshment samples and retest waves (already in the v0.3.2 line) exist to detect and correct measurement reactivity.

The 2027 build adds scale (global, high-frequency, multi-modal) **without** buying that scale by dropping any of these six. That is the entire discipline of the plan.

---

## 3. The 2027 instrument: five measurement layers

The 2026 repository contains a citable, US-English online somatic/ambient scale plus staged behavioral and retest infrastructure. Its public artifacts report observed validation, although the restricted respondent file cannot be independently reanalyzed from this repository alone. The 2027 instrument adds four measurement modalities. No modality is treated as ground truth. The panel survey (L1) remains the reference series because it is the only modality designed for probability-based population coverage.

| Layer | What it measures | Role in the evidence model | New repo artifacts |
|---|---|---|---|
| **L1 Panel survey** | Stated response, 7 domains, invariance-linked multi-item scales | Reference series; the only population-representative modality | Promote domains that pass validation from candidate to `approved_scored`; extend `constructs/` and `items/` |
| **L2 Behavioral tasks** | Costly choices: WTP for human-over-AI review, bonus sacrificed to keep data out of training, AI-disclosed trust games | Criterion variables; convergent but confounded with privacy, quality expectations, risk aversion | Extend `schema/behavioral_response.schema.json`; add `behavioral/` task battery + payout-ledger schema |
| **L3 Psychophysiology** | Electrodermal activity, HRV, and pupillometry during standardized capability demos, on a lab subsample | Arousal indicator, *not* an anxiety anchor: these signals index nonspecific arousal, effort, and novelty and only bound the affective component | New `psychophys/` protocol, device-provenance schema, demo-stimulus registry |
| **L4 Framing & proximity experiments** | Randomized manipulation of proximity, controllability, oversight, and capability information; plus a personalized-demo delta | Mechanism identification via randomization (cleaner than real-world events) | New `experiments/` preregistrations + distress protocol |
| **L5 Passive text nowcast** | High-frequency AI-response signal in public text | Aggregate external indicator, kept outside the respondent-level MTMM model and exploratory until prospective validation against future panel waves | New `ticker/` classifier card + out-of-sample calibration linking plan |

Layers L1–L2 extend what the repo already contracts. L3–L5 are new. L1–L4 can be connected at the respondent level when the same participant completes the relevant modules. L5 is platform-level public text, so treating it as another respondent-level MTMM indicator would commit an ecological error. It is instead validated prospectively as an aggregate nowcast. L3 measures nonspecific arousal rather than anxiety, and L5 is not a population signal unless future evidence supports that interpretation.

### 3.1 The dataset that will be released

The benchmark needs a defined data product, not only a research program. Each quarterly release contains five linkable but separately governed tables:

| Table | Unit of observation | Core fields | Public access |
|---|---|---|---|
| `respondent_wave` | one respondent per wave | country, mode, design weight, panel/refreshment status, demographics, AI use and exposure | de-identified public-use file with disclosure controls |
| `item_response` | one respondent-item administration | versioned item ID, raw response, scored response, language, order, missingness and exclusion flags | public where cell-risk rules pass |
| `behavioral_trial` | one incentivized choice | task version, randomized prices or endowments, choice, comprehension checks, payout | public with coarsened linkage keys |
| `experiment_trial` | one randomized exposure | stimulus version, assignment, manipulation checks, pre/post outcomes, adverse-event fields | controlled or public depending on disclosure risk |
| `country_domain_wave` | one country-domain-wave estimate | weighted latent mean, uncertainty, invariance status, capability/deployment/exposure covariates, permitted claim scope | public benchmark table |

Physiology, voice, and personalized job-task materials remain in controlled-access enclaves because combinations of biometric and occupational data can be identifying. Raw platform text is redistributed only when licensing and consent permit; otherwise the release contains post IDs or aggregate features. Every table ships with a schema, data dictionary, provenance record, checksum, code to reproduce published estimates, and a manifest that states which comparisons are permitted. Benchmark tasks are prediction of held-out future panel estimates, estimation of stated-versus-revealed gaps, and transport across countries or modes. Splits are temporal and country-held-out rather than random respondent splits, which reduces leakage and tests the generalization claims the benchmark is meant to support.

---

## 4. Scope decisions (the taste calls)

Unlimited resources is a trap: it invites building everything and validating nothing. The leadership content of this proposal is in what it **refuses** to do.

- **Construct blueprint before item generation.** Before a single item is written, the program freezes a construct blueprint per domain: the target construct, its exclusions, its nomological network, discriminant constructs, and prohibited interpretations. Discriminant measures include recent generalized-anxiety symptoms, dispositional anxiety, technophobia, institutional distrust, privacy preference, and partisan attitude. The blueprint defines the seven domains as related but distinct constructs. Phase C tests, rather than assumes, whether any higher-order score is defensible.
- **Countries: 6 contrast cases, conditional on a feasibility gate.** The initial candidates are the United States, China, India, Germany, Nigeria, and Japan. They span different labor structures, media systems, survey modes, and levels of reported AI optimism. Country selection is finalized only after an independent feasibility audit documents coverage, mode, languages, researcher and participant safety, data localization, censorship risk, and lawful data release. If a country cannot support safe probability sampling or candid responses, it is retained for within-country work only or replaced. Six is a design choice, not a psychometric maximum; invariance is evaluated for each proposed comparison rather than claimed for the set as a whole.
- **Domains: the 7 already in the taxonomy.** Economic/vocational, epistemic, relational, existential/identity, autonomy/surveillance, safety/catastrophic, somatic/ambient. No new domains in 2027; the work is validating and linking the seven, not inventing an eighth.
- **Frequency: quarterly panel waves + event-triggered waves + an exploratory continuous text nowcast.** Not monthly full panels (panel conditioning and cost), not annual (too coarse to catch capability shocks). Quarterly is the base cadence; the event machinery fires an extra locked wave around qualifying shocks.
- **Sampling: probability-based, mode-appropriate per country.** The US can use an address-recruited panel such as NORC AmeriSpeak. Other countries require the strongest feasible local frame, which may be random-digit-dial telephone sampling or area-probability face-to-face sampling. Pew's [2025 international methodology](https://www.pewresearch.org/2025/10/15/methodology-ai-global/) demonstrates why a single online mode is not credible across all six settings. A nonprobability sample may be used for instrument development, but it cannot support population prevalence estimates. Mode equivalence is tested in bridge studies.
- **Estimands stated before analysis.** Each reported quantity names its estimand: the target population, the weighting scheme, the reference baseline, the handling of measurement error, and the multiplicity correction. "Anxiety moved by X SD" is not a permitted claim; "the weighted population-mean latent epistemic-response score among employed journalists in country C moved by X SD (95% CI) relative to the pre-event baseline, family-wise error controlled across domains" is the shape of a permitted claim.
- **The flagship confirmatory hypothesis.** One hypothesis gets confirmatory-preregistration priority: *proximity increases AI response nonlinearly* (personal-task exposure produces a response disproportionate to abstract-AI response), tested primarily through the **randomized** framing/proximity experiment (L4), not through observational contrasts. It is the most falsifiable and decision-relevant candidate. The stated-vs-revealed gap and the cross-cultural map are reported as preregistered-but-secondary, with their own multiplicity control.

---

## 5. Step-by-step build plan, with resources per phase

Eight phases define the 24-month core build and the later expansion. Each phase lists its steps, repository artifact, gate, and resources. Costs are order-of-magnitude planning figures rather than vendor quotes.

### Phase 0: Foundations and governance (Months −3 to 0)
*Mostly already done in this repo; listed so the plan is self-contained.*

- **Steps:** Freeze the seven-domain construct registry; finalize `schema/` contracts; stand up the promotion-gate validators (`tools/validate_*.py`); write the multi-country IRB master protocol and the distress/debrief protocol; appoint the psychometrics lead and the ethics board liaison.
- **Artifact:** the existing `schema/`, `constructs/`, `docs/psychometric_validation_protocol.md`, plus a new `governance/irb_master_protocol.md`.
- **Gate:** all v0.1–v0.8 validators pass on CI; IRB master protocol drafted.
- **Resources:** 1 PI, 1 psychometrician, 1 research-ethics lawyer, 2 research engineers. ~$0.4M, 3 months. Compute: negligible (CI only).
- **Why first:** every downstream cost is wasted if the measurement contract and the ethics spine are not locked before a single participant is recruited.

### Phase A: Item development and content validity, 7 domains × 6 countries (Months 0–5)
- **Steps:** Qualitative interviews (~20 per domain per country = ~840 interviews) to generate candidate items grounded in how people *actually* talk about AI anxiety locally, not translated from US English. Expert content-validity panel per domain (I-CVI / S-CVI/Ave, already schema-backed via `validate_content_validity_dossier.py`). Forward/back translation + cognitive interviewing per locale. Produce the item pool: target ~12 candidate items per domain to survive to ~6 retained.
- **Artifact:** expanded `items/` pools per domain; per-locale `content_validity_dossier.json`; translation provenance records.
- **Gate:** content-validity validator passes for every domain × locale before any fielding.
- **Resources:** 7 domain experts, 6 country leads, ~30 local interviewers, translation vendors, qualitative-analysis software. ~$1.8M, 5 months. Compute: modest (LLM-assisted transcript coding, human-verified).
- **Why:** if items are conceived in English and shipped abroad, cross-cultural invariance fails and the whole linked index dies at Phase C. Content validity is cheaper than a failed invariance test.

### Phase B: Calibration fielding: EFA → CFA → IRT per domain (Months 4–11)
- **Steps:** Sample sizes are set by **simulation-based power analysis, not rules of thumb.** Before fielding, simulate the full measurement model under the planned complex-survey design (polytomous items, design weights, occupation and country strata, repeated waves, and the smallest DIF/invariance and event effects the program cares to detect) and choose N to hit target power for CFA fit, IRT item-parameter recovery, DIF detection, and invariance tests. The `N≈500` pilot / `N≈1000` confirmation figures inherited from the 2026 skeleton are a *lower bound* for a single-country single-domain scale; the cross-country, weighted, DIF-screened design will require substantially more, and the simulation says how much. Sequence: US first (fastest fieldable design) → EFA and item reduction → independent confirmation → CFA, omega, IRT calibration, DIF screening → replicate the confirmation design in each other country using that country's mode. Field the L2 behavioral battery on the same respondents so criterion validity is estimated within-person.
- **Artifact:** a preregistered `power/` simulation study per domain; per-domain validation dossiers (`validate_validation_dossier.py`); promoted `approved_scored` items; updated `constructs/` registries; released per-domain manifests.
- **Gate:** each domain must pass its dossier thresholds (EFA structure, CFA fit, omega, IRT fit, DIF) **estimated under design-based standard errors**, before it can enter the cross-domain bridge. Domains that fail stay `development_only` and are not forced into any index.
- **Resources:** probability-sample fielding is the dominant cost and varies by country and mode (online panels are cheaper than the in-person/CATI designs required in lower-coverage settings). Budget on the order of $4–6M for calibration fielding across domains and countries, plus ~$1.2M analysis staff, 7 months. Compute: moderate (Bayesian IRT/CFA, resampling CIs, multi-locale DIF; a modest cluster, since this is statistics, not model training).
- **Why:** this is the phase reviewers judge hardest. Design-appropriate power and calibration are what make the later comparisons defensible; skipping them is how a program like this fails peer review.

### Phase C: Cross-domain and cross-country linking (Months 10–15)
- **Steps:** Co-administer all validated domains plus L2 behavior in one independent bridge sample per country (the `v0.7`/`v0.8` bridge machinery, scaled). Link repeated versions within each domain, test whether a higher-order structure exists, and test measurement invariance across waves, languages, modes, and proposed country comparisons while incorporating the complex survey design. Distinct domains are not forced onto one IRT scale. A combined index is a hypothesis, not a target.
- **Artifact:** `linking/` plans (`validate_longitudinal_linking_plan.py`), a preregistered aggregate-score proposal (the template already exists at `proposals/v0.8/`), cross-country invariance evidence, and response-style diagnostics (acquiescence, extreme responding) so cross-country mean differences are not confounded with response style.
- **Gate:** An overall score requires a preregistered higher-order model, adequate reliability, and stable interpretation in held-out data. A cross-country latent-mean comparison requires prespecified anchors, adequate scalar or defensible approximate invariance, bounded noninvariance in sensitivity analyses, and agreement across reasonable identification choices. Partial invariance is not a permission slip by itself. If the result depends on which constraints are freed, the program reports within-country trends and item-level contrasts rather than a country ranking. The gate follows the literature on [invariance and latent-mean comparison](https://doi.org/10.3389/fpsyg.2017.01823).
- **Resources:** bridge fielding across six countries (order $2–3M given mixed modes), 2 senior psychometricians, 6 months. Compute: heaviest statistical load (multi-group IRT linking, invariance search); cluster-scale, not training-scale.
- **Why:** this phase decides whether "seven scales, six countries" can be joined at all. It is also the phase most likely to fail honestly, which is why its gate is the strictest and why a null here still ships as a usable set of domain series.

### Phase D: Multi-method validation: psychophysiology and framing/proximity experiments (Months 8–18, parallel)
- **Steps (L3):** In lab sites across ≥3 countries, run a lab subsample through a standardized capability-demo battery (an AI cloning the participant's voice; an AI performing a slice of their real job) while recording electrodermal activity, HRV, and pupillometry. These signals bound the affective-arousal component and enter the respondent-level MTMM model as one imperfect method. They also track effort, novelty, and attention, so they cannot identify anxiety by themselves. **(L4):** randomly assign participants to abstract or personal-task exposure and to manipulations of controllability, human oversight, and standardized capability information. Add a personalized-demo before/after contrast. Randomization identifies the assigned framing and proximity contrasts, subject to attrition, noncompliance, and interference checks. Full consent, distress protocol, debrief, ethics-board supervision.
- **Artifact:** `psychophys/` protocol + device-provenance schema; `experiments/` preregistrations; a standardized stimulus registry (so demos are comparable across occupations, waves, and countries, the point where naive "AI does your job" comparability would otherwise break).
- **Gate:** L4 experiments must clear their ethics gate before fielding. L3 results do not determine whether the survey scale exists; they determine whether the scale may be interpreted as containing an affective-arousal component. A null association narrows that interpretation and is reported. Occupation heterogeneity in the personalized demo is reported rather than averaged away.
- **Resources:** 3 lab sites, psychophysiology hardware + technicians, per-participant incentives, and the AI demo-generation stack (voice cloning, job-task automation). ~$2.2M, 10 months. Compute: the only phase with a nontrivial model-inference bill: real GPU inference for on-demand personalized-demo generation.
- **Why:** L3/L4 answer the "this is just people performing on a survey" objection by corroboration and randomization, converting a survey program into a multi-method one, without overclaiming that any one method is decisive.

### Phase E: Exploratory text nowcast (Months 6–20, continuous)
- **Steps:** Build a domain-labeled AI-response text classifier, calibrate it against the panel's latent scores, and run it over public text to produce a high-frequency, domain-resolved *nowcast*. Preregister an **out-of-sample** validation: the nowcast's mapping is fit on past waves and its predictions are scored against *future, not-yet-collected* panel waves before any population claim is entertained.
- **Artifact:** `ticker/classifier_card.md` (with drift-monitoring and documented biases), an out-of-sample calibration linking plan, and a clearly-labeled exploratory daily series.
- **Gate:** the nowcast is presented as an **exploratory between-wave signal only**, never as a population measurement, unless and until it passes prospective out-of-sample validation. Its known contaminants (platform skew, bot and AI-generated text, mobilized/political content, language coverage, censorship in some locales) are documented on the classifier card and repeated wherever the series is shown.
- **Resources:** 2 ML engineers, licensed text-stream access, an annotation budget. ~$0.9M, ongoing. Compute: continuous classifier inference (cheap relative to Phase D).
- **Why:** quarterly waves are too slow to catch a 72-hour post-shock movement. The nowcast is a fast but weak instrument; the panel remains the calibrated ground truth, and the nowcast never substitutes for it.

### Phase F: Event operations and causal design (Months 0–24, standing capability)
- **Steps:** Maintain a standing shock-classification desk that watches for qualifying events (major model releases, AI-attributed mass layoffs, viral deepfake incidents), classifies them against the frozen rubric, **locks the event registry before any outcome is inspected**, and triggers a rapid baseline/follow-up wave pair. Because AI releases are bundled with marketing, press, policy debate, and market moves, **preregistration alone does not buy causal identification.** The design therefore adds an explicit causal-inference layer: preregistered pre-trend checks, negative-control outcomes (constructs that should *not* move), negative-control events (non-AI news of comparable salience), measured exposure and media-salience covariates, anticipation-window modeling, and synthetic-control comparisons where a clean comparison group exists. Each event is linked to the *capability index* (per-domain objective + deployment + perceived signals), not to a single benchmark number.
- **Artifact:** locked `events/` registries per shock; event-study analysis plans (`validate_event_study_evidence.py`) that include the negative-control and pre-trend specifications; a capability-linkage table joining each event to the relevant domain capability/exposure indices.
- **Gate:** preregistration prevents undisclosed analytic flexibility but does not identify a causal effect. A quasi-causal claim requires a stated counterfactual, a credible comparison group or discontinuity, no major co-occurring treatment, anticipation analysis, negative controls, multiplicity correction, and sensitivity bounds for violations of identifying assumptions. A nonsignificant pre-trend test is insufficient because such tests can have low power and can distort inference when used as a filter ([Roth, 2022](https://doi.org/10.1257/aeri.20210236)). Most release and incident analyses will therefore be labeled descriptive interrupted time series or event-aligned associations.
- **Resources:** a small standing rapid-response team + reserved fielding capacity for surprise waves. ~$1.5M/yr standby. Compute: negligible.
- **Why:** the causal layer is what separates "response and capability rose together" (cheap, and usually confounded) from a defensible statement that a class of release moved a specific domain response among a specific population within a specific window. Most candidate event findings will not clear this bar, and the design says so up front.

### Phase G: Public release, dashboard, governance (Months 18–24 and ongoing)
- **Steps:** Ship the public **AI Psychological Response Observatory** dashboard (domain- and country-resolved series, capability/exposure overlay, event annotations, full methodology and every promotion gate exposed, and an explicit "how not to read this" panel), release privacy-protected open data and open analysis code under a documented data-governance model, stand up an external methods-advisory board, and publish results as protocol-and-findings papers.
- **Artifact:** public dashboard, versioned open-data releases with a per-modality privacy plan (survey, occupation, country, physiology, voice, public text, and job-task demos each have distinct disclosure risks and are handled separately), reproducibility bundle, methods-board charter, and the prohibited-uses statement (Section 8).
- **Gate:** nothing is published as a benchmark claim unless its manifest is `release_status: citable` and every validator in `README.md` passes; nothing is released as open data until its per-modality disclosure-risk review passes.
- **Resources:** front-end + data-eng team, comms, per-locale legal review for data release. ~$1.2M + ongoing hosting. Compute: dashboard serving only.
- **Why:** the series only becomes trustworthy infrastructure if it is public, transparent, continuously governed, and shipped with its own misuse guardrails. A private series nobody can audit is a private opinion.

---

## 6. Resource summary

| Resource class | What it buys | Order-of-magnitude |
|---|---|---|
| **Probability panels** | The single largest and least-negotiable cost; calibration + bridge + quarterly + event waves across 6 countries | ~$10–12M over the program |
| **People** | PI + 3 senior psychometricians + 6 country leads + 7 domain experts + ~6 research engineers/ML + rapid-response + ethics/legal | ~$8–10M for the 24-month core; expansion budgeted separately |
| **Lab arm (L3/L4)** | Psychophysiology sites, hardware, technicians, per-participant incentives | ~$2.2M |
| **Compute** | *Not* the bottleneck. Statistics run on a modest cluster; the only real inference bill is Phase D personalized-demo generation + Phase E continuous ticker classification | Low-to-moderate; a mid-size GPU allocation, not a training run |
| **Translation / cross-cultural / IRB** | 6-locale translation, cognitive interviewing, multi-country ethics | ~$2M |
| **Public infrastructure** | Dashboard, open-data pipeline, hosting, methods board | ~$1.5M + ongoing |

**Total order of magnitude:** roughly $25–35M for the 24-month three-country core, followed by a separately gated $10–15M expansion through month 42. Sampling costs remain uncertain because in-person and telephone designs can cost multiples of an online panel. Probability sampling and psychometric labor, rather than model training, dominate the budget.

The schedule has two decision stages. Months 0–24 deliver a US-plus-two-country core: validated domains, the first bridge studies, the experimental arm, and the public dataset. Months 25–42 add the remaining countries only where the feasibility and measurement gates pass. The six-country series is therefore a 42-month target, while the first citable benchmark release remains a 24-month target. Money cannot fully compress ethics review, translation, fieldwork, or cross-cultural psychometric iteration.

---

## 7. Team and expertise (who has to be in the room)

- **Psychometrician (card-carrying), as co-lead, not advisor.** Reviewers smell bolted-on measurement theory instantly. Invariance, IRT linking, and DIF have to be owned, not outsourced.
- **Survey methodologist** for probability-panel design, weighting, and nonresponse.
- **Cross-cultural / cultural psychologist** for the 6-country arm and translation-invariance judgment calls.
- **Psychophysiologist** for L3.
- **Behavioral/experimental economist** for the L2 revealed-preference wagers and incentive-compatibility.
- **ML engineers** for L5 classifier + Phase D demo generation.
- **Research-ethics lead + local IRB liaisons** in every country.
- **AI-capability evaluation liaison** (the METR-shaped role) to keep the domain-specific capability and exposure indices honest and current.
- **Data engineers** for the versioned-release pipeline and public dashboard.

The org chart is itself an argument: a serious human-response benchmark is a *psychometrics-and-survey-methods* program with an AI-evaluation liaison, not an AI lab with a survey bolted on. Getting that inversion right is most of the leadership call.

---

## 8. Risks and how the design already answers them

| Risk | Mitigation (mostly already in the repo) |
|---|---|
| **Measurement drift** (the y-axis silently changes meaning) | Invariance gates are release-blocking; drift thresholds in linking plans; anchor items carried across waves |
| **Panel conditioning** (asking induces the anxiety) | Rotating refreshment samples + retest waves (v0.3.2 line); "does measuring AI anxiety induce it?" is run as an explicit supplementary study |
| **Reverse causation / p-hacking** on event studies | Event registries locked pre-outcome; analysis plans frozen pre-outcome; `event_locked_before_outcome_inspection: true` |
| **Cross-cultural non-comparability** | Content validity generated locally (Phase A); partial-invariance fallback; refusal to ship a false headline index (Phase C gate) |
| **Cheap-talk self-report** | L2 behavioral tasks test criterion relations; L3 physiology tests the narrower affective-arousal interpretation; no modality is treated as ground truth |
| **Confounding constructs** (generalized-anxiety symptoms, dispositional anxiety, technophobia, privacy preference, partisan attitude) | Discriminant validity against each required before scoring; construct blueprint fixes the exclusions in advance |
| **Response-style differences across cultures** (acquiescence, extreme/modest responding, state-fear underreporting) | Anchoring vignettes + response-style diagnostics so cross-country mean differences are not mistaken for true differences |
| **Semantic drift of anchor items** (AI changes what an item means over time) | Anchor-item obsolescence review each wave; drift thresholds; refusal to link across a break the invariance test rejects |
| **Ethical harm from the demo/experiment arm** | Ethics-board-supervised consent + distress protocol + debrief; L4 cannot field until its gate clears |
| **Political capture / advocacy misuse** | Full method transparency, open data/code, external methods board, an explicit prohibited-uses statement (Section 8.1), and visible willingness to publish *null* and *lower-than-feared* results |

An instrument that can only move one direction, or that is built to justify a predetermined policy, is worthless. The value of this program is precisely that its gates let it report "concern here is smaller and more stable than the discourse assumes" with the same authority as "this release was associated with a rise in epistemic response among journalists." A measure that can surprise its own authors is a measure worth trusting.

### 8.1 Prohibited uses

The program ships with an explicit statement of what its outputs may **not** be used to claim, because a psychological-response series is unusually easy to weaponize:

- It may not be used to argue that a population is "irrationally anxious," nor that low measured response means a deployment is safe. Response and warranted risk are different quantities; the instrument measures the former and takes no position that it should track the latter.
- It may not be used for individual-level or subgroup-targeting decisions (hiring, insurance, credit, policing, content targeting). All releases are population-descriptive; individual-level use is blocked in the release contract.
- Cross-country comparisons may not be used to rank or stigmatize populations, and are suppressed entirely where reporting a subgroup's AI or surveillance attitudes could expose respondents to state or employer retaliation.
- No party (regulator, lab, or advocacy group) may present a single number as "the" AI-anxiety level when the Phase C gate has not authorized a combined index.

These are not aspirations; they are release-blocking conditions and dashboard-level labels, governed by the external methods board.

---

## 9. Dissemination

The natural homes for the work, stated as *fit* rather than as expected acceptances: a psychometric-validation-and-invariance paper for a measurement or human-behavior venue (the instrument itself); a findings paper for a general-science or field venue once a result survives confirmatory preregistration (most likely the proximity effect or the stated-vs-revealed gap); and a datasets-and-benchmarks release for the ML community (dataset, protocol, capability-linkage methodology, public dashboard). Which findings clear their preregistered bars is unknown in advance, so this section is deliberately about where the work would belong, not about what it will land. The durable output is the standing series and its open protocol, which outlast any single paper.

---

## 10. Why this reflects the right taste

The instinct under "unlimited resources" is to maximize scale: thirty countries, monthly waves, every domain, one grand headline number. This plan deliberately does the opposite where it counts. It fixes a construct blueprint before writing items, caps at six contrast-chosen countries, refuses to invent new domains, insists on mode-appropriate probability samples over cheap scale, sizes those samples by simulation rather than rule of thumb, spends its budget on psychometric and survey labor rather than compute, treats every non-survey modality as a fallible indicator rather than a proof, separates preregistration from causal identification, and, most tellingly, **builds explicit gates whose job is to forbid the combined index, the cross-country comparison, and the causal claim whenever the data do not earn them.** The hard part of measuring human response to AI is not gathering opinions; it is earning the right to compare them across time, place, and person. This program is organized around earning that right, and around the discipline to say "not yet" when it has not been earned, encoded as machine-checkable gates rather than left to good intentions. That restraint is the whole idea.

---

## References

Jiang, G., Mai, Y., and Yuan, K.-H. (2017). Advances in measurement invariance and mean comparison of latent variables. Frontiers in Psychology, 8, 1823. https://doi.org/10.3389/fpsyg.2017.01823

Pew Research Center. (2025). How people around the world view AI. https://www.pewresearch.org/global/2025/10/15/how-people-around-the-world-view-ai/

Pew Research Center. (2025). Methodology: How people around the world view AI. https://www.pewresearch.org/2025/10/15/methodology-ai-global/

Roth, J. (2022). Pretest with caution: Event-study estimates after testing for parallel trends. American Economic Review: Insights, 4(3), 305–322. https://doi.org/10.1257/aeri.20210236

Spitzer, R. L., Kroenke, K., Williams, J. B. W., and Lowe, B. (2006). A brief measure for assessing generalized anxiety disorder: The GAD-7. Archives of Internal Medicine, 166(10), 1092–1097. https://doi.org/10.1001/archinte.166.10.1092

Stanford Institute for Human-Centered Artificial Intelligence. (2026). AI Index Report 2026: Public opinion. https://hai.stanford.edu/ai-index/2026-ai-index-report/public-opinion

Kwa, T., West, B., Becker, J., et al. (2025). Measuring AI ability to complete long tasks. METR. https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
