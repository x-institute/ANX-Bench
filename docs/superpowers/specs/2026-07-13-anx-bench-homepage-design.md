# ANX-Bench Homepage Design

**Date:** 2026-07-13

**Direction:** Observatory Control Room

**Status:** Approved for implementation
**Source material:** `README.md` and `new-requirements.md`

## Purpose

The homepage turns the ANX-Bench 2027 proposal into a premium, cinematic scientific narrative. It must answer the proposal prompt directly: what we would build with unlimited resources, why it matters, what makes it innovative and insightful, how it would be built, and what resources each phase requires.

The experience should feel like a research observatory from the near future: precise, restrained, spatial, and quietly expensive. It must not resemble a crypto landing page, a game HUD, or a conventional academic project page. The science remains primary; motion and visual effects clarify the argument rather than decorate it.

## Core Story

The page is organized around one missing relationship:

> AI capability, deployment, and exposure are measured constantly. Human psychological response to those systems is not measured with the same longitudinal rigor.

The visual narrative begins with two independent signals—machine capability and human response—then joins them into the central ANX-Bench plot. Every later section explains what is required to make that plotted relationship defensible across domains, countries, populations, and time.

The homepage explicitly avoids presenting a single overall “AI Anxiety Index.” The seven response domains remain distinct unless psychometric evidence supports aggregation. This scientific refusal is a signature part of the brand.

## Audience and Desired Response

The primary audience is benchmark researchers, AI evaluation teams, funders, policy researchers, psychometricians, and technically literate members of the public. A first-time visitor should understand the project within 20 seconds and leave with three impressions:

1. ANX-Bench measures the missing human side of AI progress.
2. The proposal is unusually rigorous, concrete, and executable.
3. Its strongest feature is a willingness to block unsupported comparisons and headline scores.

## Visual Direction

### Palette

- **Void:** `#050706` — main canvas.
- **Carbon:** `#0b0f0d` — elevated panels and navigation.
- **Bone:** `#edf1e8` — primary text.
- **Mist:** `#9aa59d` — secondary text and metadata.
- **Signal lime:** `#c9ff45` — primary accent, active states, human-response signal.
- **Spectral cyan:** `#6ee7f2` — capability signal and scientific annotations.
- **Warning amber:** `#ffb45c` — gates, cautions, and blocked claims only.

The accent colors are sparse. Most of the page remains dark, neutral, and typographic so the scientific graphics carry visual authority.

### Typography

- A condensed display face for the hero and section statements.
- A neutral grotesk sans-serif for body copy and interface labels.
- A monospace face for phase labels, measurements, release states, axes, and small metadata.
- Headlines use tight tracking and deliberate line breaks. Body copy stays comfortably readable at 16–18 px with short line lengths.

Web fonts may be loaded from Google Fonts with robust local fallbacks. The proposed family is `Barlow Condensed` for display, `Inter` for interface and prose, and `IBM Plex Mono` for technical detail.

### Surface Language

The page uses hairline borders, faint grids, calibrated bloom, glass-like depth, and sparse orbital marks. Panels remain mostly flat and architectural. Large blurred gradients are used as ambient light, never as blobs behind every card.

Noise, scan lines, and grid textures are CSS-generated and extremely subtle. The site does not use stock photography or generic robot imagery.

## Page Architecture

### 1. Navigation

A translucent fixed navigation bar contains the ANX-Bench wordmark, a live-status indicator, links to Mission, Instrument, Roadmap, and Resources, plus a compact “View repository” action.

The bar is nearly invisible over the hero, then gains a dark glass surface after scrolling. On mobile it becomes a compact header with an accessible menu.

### 2. Hero — The Missing Axis

The opening viewport presents:

- Eyebrow: `THE GLOBAL AI PSYCHOLOGICAL RESPONSE OBSERVATORY / 2027`.
- Headline: `We benchmark what AI can do. Who measures what it does to us?`
- A compressed version of the proposal’s one-sentence answer.
- Primary action: `Explore the instrument`.
- Secondary action: `Read the 2027 proposal`.
- A compact status rail: seven domains, six countries, quarterly waves, five measurement layers.

Behind the copy, a canvas-free CSS/SVG observatory graphic plots two animated signal traces. The x-axis represents domain capability, deployment, and exposure. The y-axis represents invariance-linked human response. Sparse points appear as the visitor enters the page; axes and annotations remain legible without animation.

The fold ends with a cue reading `SCROLL TO LINK THE SIGNALS`.

### 3. Thesis Transition — Two Halves of the Stack

As the visitor scrolls, the hero plot separates into two columns:

- **What models can do:** capability benchmarks, task horizons, deployment, and exposure.
- **What people experience:** stated response, costly choices, arousal, proximity effects, and cultural context.

The two columns reconnect around the phrase `ANX-Bench closes the measurement gap.` The transition is scroll-linked on capable devices and a simple reveal under reduced-motion settings.

### 4. Why This Benchmark

Three large editorial panels answer the prompt directly:

- **Important:** decision-grade infrastructure for regulators, labs, and labor researchers.
- **Innovative:** versioned human-response measurement joined to domain-specific capability and exposure signals.
- **Insightful:** reveals proximity effects, stated-versus-revealed gaps, and cross-cultural differences whether the result is positive, negative, or null.

Each panel includes a short evidence statement and one visual motif. The section avoids generic marketing claims and preserves the proposal’s qualifications.

### 5. Seven-Domain Constellation

Seven nodes form an asymmetric constellation around a central `HUMAN RESPONSE` core:

- Economic / vocational
- Epistemic
- Relational
- Existential / identity
- Autonomy / surveillance
- Safety / catastrophic
- Somatic / ambient

Hover, focus, or tap reveals the domain definition and example questions. The layout communicates related but distinct constructs. A caption states that the program will not collapse these domains into one number unless the evidence permits it.

On small screens, the constellation becomes an ordered domain list with the same content and active-state affordances.

### 6. The Instrument — Five Measurement Layers

The five layers assemble vertically like an observatory sensor stack:

1. Population-representative panel survey
2. Behavioral tasks with real cost or effort
3. Psychophysiology as a bounded arousal indicator
4. Randomized framing and proximity experiments
5. Exploratory public-text nowcast

Each layer shows its role, artifact, evidence status, and limitation. The text-nowcast layer is explicitly marked exploratory; physiology is not presented as direct proof of anxiety. Connecting lines show that the panel remains the calibrated reference series.

### 7. Global Observatory

A stylized six-country projection highlights the United States, China, India, Germany, Nigeria, and Japan. It is a semantic SVG diagram rather than a geographic analytics product.

The supporting copy explains why six contrasting countries are more scientifically defensible than superficial coverage of thirty. A prominent invariance-gate label makes clear that comparison is earned, not assumed.

### 8. Mission Roadmap — Phases 0–G

The build plan becomes a horizontal mission sequence on desktop and a vertical sequence on mobile:

- Phase 0: Foundations and governance
- Phase A: Item development and content validity
- Phase B: Calibration, EFA, CFA, and IRT
- Phase C: Cross-domain and cross-country linking
- Phase D: Multi-method validation
- Phase E: Exploratory text nowcast
- Phase F: Event operations and causal design
- Phase G: Public release and governance

Each phase exposes timeframe, essential steps, artifact, release gate, resource estimate, and scientific rationale. The default view stays concise; details open through accessible disclosure controls.

### 9. The Scientific Refusal

A high-contrast interruption section states:

> If the constructs do not link, we do not publish the index.

An amber gate graphic closes across an attempted single-score output. Supporting text explains partial-scalar invariance, higher-order model fit, and why refusing a false headline is a successful scientific result.

This is the page’s emotional and intellectual climax.

### 10. Resources and Team

The resource summary appears as a compact mission ledger with six categories: probability panels, people, laboratory arm, compute, cross-cultural and ethics work, and public infrastructure.

The design emphasizes that compute is not the bottleneck. Probability sampling, psychometric expertise, cultural validity, and governance carry the real cost. A companion expertise grid names the roles required without turning into a staff directory.

### 11. Closing — Build the Missing Half

The final section returns to the joined two-axis plot and the statement `Build the missing half of the AI measurement stack.` It offers links to:

- Read the 2027 proposal
- Explore the benchmark README
- View release artifacts
- Open the repository

The footer includes the repository status, methodology-first positioning, and an explicit `Not a clinical diagnostic` note.

## Motion and Transitions

Motion serves three narrative functions:

1. **Linking:** separate signals join into a shared coordinate system.
2. **Gating:** unsupported claims visibly stop at scientific gates.
3. **Accumulation:** the five methods and eight phases assemble into a system.

Implementation uses CSS transforms, opacity, SVG stroke animation, and a small intersection-observer controller. No animation library is required. Pointer parallax is limited to decorative hero layers and disabled on touch or reduced-motion devices.

All essential content is present in the initial document and visible without JavaScript. With `prefers-reduced-motion: reduce`, scroll-linked and continuous movement is removed while section hierarchy, diagrams, and state labels remain intact.

## Interaction Model

- Navigation uses standard anchor links and visible focus states.
- Domain nodes are real buttons with synchronized descriptive content.
- Roadmap details use native `details` and `summary` elements where possible.
- Numerical counters do not invent live data; they communicate fixed program scope only.
- External document links are descriptive and do not rely on icon-only controls.
- The page contains no form, account system, analytics dependency, or data fetch.

## Technical Architecture

The repository currently contains no frontend toolchain. The homepage will therefore use a small, dependency-free static architecture:

```text
index.html            Semantic page structure and content
assets/
  styles.css          Tokens, layout, responsive states, motion
  app.js              Navigation, reveal states, constellation interaction
  observatory.svg     Reusable scientific visual and plot geometry
```

This avoids introducing a framework, package manager, build output, or dependency lockfile for a single narrative page. The site can be served from any static host or previewed with `python3 -m http.server`.

The HTML content is adapted from the proposal and README rather than copied wholesale. Long scientific details remain available through links and roadmap disclosures.

## Responsive Behavior

- **Wide desktop (≥1200 px):** full spatial compositions, sticky narrative panels, horizontal phase sequence.
- **Tablet (768–1199 px):** two-column sections simplify, constellation retains radial structure, roadmap scrolls horizontally with clear affordance.
- **Mobile (<768 px):** single-column editorial flow, domain list replaces constellation geometry, roadmap becomes vertical, fixed navigation becomes a compact menu.

No critical text is placed inside a raster image. SVG labels scale responsively or are mirrored in semantic HTML.

## Accessibility and Performance

- Meet WCAG AA contrast for text and actionable controls.
- Provide keyboard access and visible focus indicators for every interaction.
- Use semantic headings, landmarks, buttons, lists, and disclosure controls.
- Preserve all meaning without animation, hover, or JavaScript.
- Honor reduced-motion and high-contrast preferences.
- Avoid autoplay audio and video.
- Keep the initial page lightweight: no framework runtime, no large image payload, and minimal font weights.
- Target a strong Lighthouse result and a responsive experience on mid-range mobile hardware.

## Content Accuracy Rules

- Do not imply that all seven domains currently have validated scores.
- Do not present an overall ANX score as available or inevitable.
- Do not label psychophysiology as direct measurement of anxiety.
- Do not label the text nowcast as population-representative.
- Distinguish the current 2026 repository skeleton from the proposed 2027 program.
- Retain the six-country scope, five measurement layers, quarterly cadence, event-triggered waves, and phases 0–G.
- Link claims about current releases back to the README and proposal instead of silently simplifying their scope.

## Verification Criteria

The implementation is complete when:

1. Every page section described above exists and works at desktop and mobile widths.
2. The page answers what, why, how, phases, resources, innovation, and insight from the proposal.
3. Interactive controls work by keyboard and pointer.
4. Reduced-motion mode removes nonessential motion.
5. The page remains readable and navigable with JavaScript disabled.
6. All local links resolve and the browser console has no errors.
7. Automated HTML, accessibility, and responsive smoke checks pass where local tooling permits.
8. A local visual review confirms hierarchy, clipping, contrast, and transition quality at representative desktop and mobile sizes.

## Explicit Non-Goals

- Building a research dashboard with real observed data
- Adding participant recruitment, accounts, or survey collection
- Creating a single aggregate ANX score
- Replacing the detailed README or 2027 proposal
- Introducing a frontend framework or backend service
- Presenting proposed 2027 artifacts as already operational
