Proposal: doctoral-lifecycle benchmark with ARA as the dissertation format (working title: "The Last Human-Gotten PhD")

https://github.com/ARA-Labs/Agent-Native-Research-Artifact/issues/8

## Summary

This is a proposal to apply the ARA protocol as the backbone of a longitudinal benchmark we want to build with, or alongside, this team: a **doctoral-lifecycle evaluation** testing whether an AI agent can pass the full PhD sequence (qualifying exam, thesis proposal, original research execution, dissertation, oral defense) as one stateful unit, with the human baseline anchored in graduation metrics aggregated from 1000+ universities. Our working title is *"The Last Human-Gotten PhD"*, an explicit homage to your paper; if the team would rather we not echo the title, we will happily rename it, the design does not depend on the name.

ARA is load-bearing in this design, not decorative: the dissertation the agent must produce IS an ARA, the execution stage is captured live with `research-manager` (so the exploration layer with dead ends accrues as a byproduct, exactly as the protocol intends), and the defense gate is achieving Seal Level 2 via `rigor-reviewer` plus a human committee.

## Why this does not exist yet (we checked)

Before writing this we searched for prior art. The doctoral experience is benchmarked only in segments: GPQA/HLE as quals proxies, PaperBench/MLR-Bench/MLE-bench/RE-Bench/AI-Scientist-v2 for the research-to-paper pipeline, viva-style oral evals for defense. We found no benchmark that evaluates the sequential gauntlet as a single stateful unit where later stages interrogate commitments made in earlier ones, and none that anchors AI research-capability evaluation to institutional completion data (NSF Survey of Earned Doctorates style: completion rates, attrition, time-to-degree) the way GDPval anchors task evals to occupational data. If we missed something, please point us to it and we will close this.

## Design sketch

1. **Lifecycle as the unit.** One agent, persistent state, staged gates: quals (closed-book domain exam) -> proposal (committee-judged, falsifiable claims required) -> execution (months-compressed research with budget metering, recorded via `research-manager`) -> dissertation (emitted as an ARA: claims with falsification criteria, exploration graph including dead ends, evidence bindings) -> defense (a committee of agents plus a human, stress-testing the ARA's own cross-layer bindings). The anti-concatenation property matters: because the defense probes the proposal's commitments and the dissertation's recorded dead ends, the benchmark cannot be gamed as a sequence of independent evals.
2. **Institutional anchoring.** Human baselines from public aggregate data across 1000+ universities: completion probability, time-to-degree distributions, attrition stage profiles. We are upfront about the known hard problem, construct validity: human attrition is largely funding, advisor relationship, and welfare, while agent failure is context exhaustion and loops. We propose to separate capability attrition from institutional attrition explicitly rather than blur them.
3. **The institutional layer exists already.** One of us (Wu) has a preprint grounding a bilateral venture-capital contract model of PhD programs (staging, contingent control, mutual diligence, exit lattices): "Research grounding for a bilateral venture capital model of PhD programs", DOI [10.5281/zenodo.19040077](https://zenodo.org/records/19040077), plus a frozen, versioned scenario battery (hold-up, multitask distortion, matching axes) with weighted rubrics, blinding, and a written evaluation protocol. That battery supplies the socio-institutional axis the capability benchmarks above all lack: whether an agent-as-candidate survives the contractual hazards that drive real attrition, not just the technical milestones.

## Speculative extensions (flagged as such; testable, not asks)

- **ARA-native credentialing**: a credential whose requirement is "produce an ARA that achieves Seal Level 2 and survives committee defense", with time-to-degree becoming a measured capability variable rather than a residency constant.
- **Attrition-profile comparison**: run the bilateral scenario battery on agent candidates under degraded conditions (budget cuts mid-run as funding loss; advisor-policy shifts as hold-up) and compare the resulting failure-stage profile against the human attrition curve.
- **The substitution frontier**: per-stage human-vs-agent deltas yield a map of which components of doctoral training AI can already perform (literature synthesis, proposal drafting) and which it cannot (committee persuasion, problem taste). This is the empirical core of the "can AI substitute for doctoral training" question, answered per-stage instead of rhetorically.
- **Agents as advisors**: the same harness inverted, agent advisors paired with human candidates, scored on the candidate-welfare rubrics from the bilateral battery.

## Asks

1. Is a doctoral-lifecycle benchmark with ARA as the mandated dissertation format something ARA-Labs would want as a collaboration, a sanctioned extension, or neither?
2. If yes: we would draft the stage-gate spec with `rigor-reviewer` as the Seal Level 2 defense gate, and contribute the scenario battery + protocol as the institutional axis.
3. If the team prefers ARA not be associated with this framing at all, that is genuinely useful signal too, and we will build it independently without the title homage.

(Context: this builds on the incentive-layer discussion in #6; same proposer. Separately submitted small fix in #7.)
