# ANX-Bench Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build a responsive, dependency-free, premium sci-fi homepage that translates the ANX-Bench README and 2027 proposal into an accurate visual narrative.

**Architecture:** A semantic static `index.html` contains the complete narrative and remains usable without JavaScript. One focused stylesheet owns the visual system, responsive layout, and reduced-motion behavior; one small script adds progressive navigation, section-reveal, and domain-constellation interactions. A reusable SVG supplies the central observatory plot without raster assets or runtime data fetching.

**Tech Stack:** HTML5, modern CSS, inline-accessible SVG, vanilla ES2020 JavaScript, Python `unittest`/`html.parser`, local static HTTP server.

## Global Constraints

- No frontend framework, package manager, build output, backend, form, account system, analytics dependency, or data fetch.
- Preserve the six-country scope, seven domains, five measurement layers, quarterly cadence, event-triggered waves, and phases 0–G.
- Do not imply all seven domains are validated, an overall ANX score exists, psychophysiology directly measures anxiety, or the text nowcast is population-representative.
- All essential content must remain visible and navigable without JavaScript.
- Keyboard use, visible focus, semantic landmarks, WCAG AA contrast, and `prefers-reduced-motion` behavior are release requirements.
- The implementation must work as static files served with `python3 -m http.server`.

---

### Task 1: Contract Tests and Semantic Page

**Files:**
- Create: `tests/test_homepage.py`
- Create: `index.html`

**Interfaces:**
- Consumes: `README.md`, `new-requirements.md`, and `docs/superpowers/specs/2026-07-13-anx-bench-homepage-design.md`.
- Produces: section IDs `mission`, `why`, `domains`, `instrument`, `global`, `roadmap`, `resources`, and `contact`; buttons with `[data-domain]`; local assets `assets/styles.css`, `assets/app.js`, and `assets/observatory.svg`.

- [x] **Step 1: Write the failing homepage contract test**

Create `tests/test_homepage.py` with a small `HTMLParser` collector and tests that assert:

```python
REQUIRED_SECTIONS = {
    "mission", "why", "domains", "instrument",
    "global", "roadmap", "resources", "contact",
}
REQUIRED_PHRASES = {
    "We benchmark what AI can do",
    "Important", "Innovative", "Insightful",
    "If the constructs do not link, we do not publish the index.",
    "Not a clinical diagnostic",
}

def test_homepage_contains_required_sections_and_copy(self):
    self.assertTrue(REQUIRED_SECTIONS <= self.parser.ids)
    for phrase in REQUIRED_PHRASES:
        self.assertIn(phrase, self.html)

def test_homepage_exposes_accessible_domain_controls(self):
    self.assertEqual(len(self.parser.domain_buttons), 7)
    self.assertTrue(all(button.get("aria-controls") for button in self.parser.domain_buttons))

def test_local_assets_resolve(self):
    for path in ("assets/styles.css", "assets/app.js", "assets/observatory.svg"):
        self.assertTrue((ROOT / path).is_file(), path)
```

- [x] **Step 2: Run the test and verify it fails**

Run: `python3 -m unittest tests.test_homepage -v`

Expected: FAIL because `index.html` and the required assets do not exist.

- [x] **Step 3: Build the semantic page**

Create `index.html` with:

```html
<header class="site-header" data-header>
  <a class="brand" href="#top" aria-label="ANX-Bench home">ANX<span>/</span>BENCH</a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" aria-label="Primary navigation">…</nav>
</header>
<main id="main-content">
  <section class="hero" id="top" aria-labelledby="hero-title">…</section>
  <section id="mission">…</section>
  <section id="why">…</section>
  <section id="domains">…seven data-domain buttons and one aria-live description…</section>
  <section id="instrument">…five measurement layers…</section>
  <section id="global">…six-country scope and invariance gate…</section>
  <section id="roadmap">…native details for phases 0 through G…</section>
  <section class="refusal">…scientific refusal statement…</section>
  <section id="resources">…resource ledger and expertise…</section>
  <section id="contact">…document and repository actions…</section>
</main>
<footer>…Not a clinical diagnostic…</footer>
```

The exact section copy must accurately compress the source documents and label proposed 2027 work as proposed rather than operational.

- [x] **Step 4: Run the content-specific tests**

Run: `python3 -m unittest tests.test_homepage.HomepageContractTests.test_homepage_contains_required_sections_and_copy tests.test_homepage.HomepageContractTests.test_homepage_exposes_accessible_domain_controls -v`

Expected: PASS.

### Task 2: Observatory Visual and Responsive Design System

**Files:**
- Create: `assets/styles.css`
- Create: `assets/observatory.svg`
- Modify: `tests/test_homepage.py`

**Interfaces:**
- Consumes: semantic class names and asset references from `index.html`.
- Produces: CSS tokens `--void`, `--carbon`, `--bone`, `--mist`, `--lime`, `--cyan`, and `--amber`; responsive breakpoints at 1200 px and 768 px; reduced-motion override; SVG IDs `capability-signal` and `response-signal`.

- [x] **Step 1: Add visual-system contract tests**

Add assertions:

```python
def test_styles_define_tokens_breakpoints_and_reduced_motion(self):
    css = (ROOT / "assets/styles.css").read_text()
    for token in ("--void", "--bone", "--lime", "--cyan", "--amber"):
        self.assertIn(token, css)
    self.assertIn("@media (prefers-reduced-motion: reduce)", css)
    self.assertIn("@media (max-width: 768px)", css)

def test_observatory_has_labeled_signals(self):
    svg = (ROOT / "assets/observatory.svg").read_text()
    self.assertIn('id="capability-signal"', svg)
    self.assertIn('id="response-signal"', svg)
    self.assertIn("<title>", svg)
```

- [x] **Step 2: Run the visual-system tests and verify failure**

Run: `python3 -m unittest tests.test_homepage.HomepageContractTests.test_styles_define_tokens_breakpoints_and_reduced_motion tests.test_homepage.HomepageContractTests.test_observatory_has_labeled_signals -v`

Expected: FAIL until both assets contain the required contracts.

- [x] **Step 3: Implement the visual system and plot**

Create a stylesheet beginning with the exact palette:

```css
:root {
  --void: #050706;
  --carbon: #0b0f0d;
  --bone: #edf1e8;
  --mist: #9aa59d;
  --lime: #c9ff45;
  --cyan: #6ee7f2;
  --amber: #ffb45c;
}
@media (max-width: 768px) { /* single-column flow, vertical roadmap, menu */ }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
```

Implement the dark observatory composition, fixed glass navigation, hero typography, two-signal transition, editorial benefit panels, radial domain constellation, stacked sensor layers, country projection, roadmap, refusal gate, resource ledger, keyboard focus states, and mobile variants. Create an accessible SVG with a title, plot grid, axes, two labeled paths, nodes, and decorative orbital geometry.

- [x] **Step 4: Run the visual-system tests**

Run: `python3 -m unittest tests.test_homepage -v`

Expected: asset and CSS contract tests PASS; JavaScript contract may still fail.

### Task 3: Progressive Interaction and Motion

**Files:**
- Create: `assets/app.js`
- Modify: `tests/test_homepage.py`

**Interfaces:**
- Consumes: `[data-header]`, `[data-reveal]`, `[data-domain]`, `[data-domain-copy]`, and `.nav-toggle` elements.
- Produces: `.is-scrolled`, `.is-visible`, and `.is-active` states; updated domain copy; mobile navigation `aria-expanded` state.

- [x] **Step 1: Add interaction contract tests**

Add:

```python
def test_script_is_progressive_and_updates_accessible_states(self):
    script = (ROOT / "assets/app.js").read_text()
    self.assertIn("IntersectionObserver", script)
    self.assertIn("aria-expanded", script)
    self.assertIn("data-domain", script)
    self.assertNotIn("fetch(", script)
```

- [x] **Step 2: Run the interaction test and verify failure**

Run: `python3 -m unittest tests.test_homepage.HomepageContractTests.test_script_is_progressive_and_updates_accessible_states -v`

Expected: FAIL because `assets/app.js` is absent or incomplete.

- [x] **Step 3: Implement progressive enhancement**

Implement:

```javascript
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const reveals = document.querySelectorAll('[data-reveal]');
if (!reducedMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({ isIntersecting, target }) => {
      if (isIntersecting) target.classList.add('is-visible');
    });
  }, { threshold: 0.14 });
  reveals.forEach((element) => observer.observe(element));
} else {
  reveals.forEach((element) => element.classList.add('is-visible'));
}
```

Also implement the scrolled header state, mobile navigation toggle with synchronized `aria-expanded`, domain button selection with active state and descriptive-copy updates, Escape-to-close, and navigation close after link activation. Do not fetch data or hide essential content before script execution.

- [x] **Step 4: Run the complete contract suite**

Run: `python3 -m unittest tests.test_homepage -v`

Expected: PASS.

### Task 4: Browser QA and Release

**Files:**
- Modify only files found defective during QA.

**Interfaces:**
- Consumes: the complete static homepage.
- Produces: a verified website commit on `main` and no remaining non-main branches.

- [x] **Step 1: Run repository and homepage checks**

Run:

```bash
python3 -m unittest tests.test_homepage -v
python3 -m pytest -q
git diff --check
```

Expected: homepage tests PASS, existing repository tests PASS, and `git diff --check` prints no output.

- [x] **Step 2: Serve and inspect the site**

Run: `python3 -m http.server 4173`

Inspect `http://127.0.0.1:4173/` at approximately 1440×1000 and 390×844. Confirm hero hierarchy, navigation, all eight narrative sections, domain interactions, roadmap disclosures, link targets, no horizontal clipping, and no console errors.

- [x] **Step 3: Verify accessibility and reduced motion**

Use keyboard-only navigation through every control. Emulate `prefers-reduced-motion: reduce` and confirm continuous/scroll-linked motion is absent while content stays visible. Disable JavaScript and confirm the complete narrative remains readable and navigable.

- [x] **Step 4: Commit and push the implementation atomically**

Run:

```bash
git add index.html assets/styles.css assets/app.js assets/observatory.svg tests/test_homepage.py docs/superpowers/plans/2026-07-13-anx-bench-homepage.md
git commit -m "Build ANX-Bench observatory homepage"
git push origin main
```

Expected: one implementation commit is pushed to `origin/main` after the already-pushed design commit.

- [x] **Step 5: Remove obsolete branches and audit completion**

Verify the old proposal branch tip is already an ancestor of `main`, then remove `origin/bench2027-premature`. Confirm `git branch --all` shows only `main` and `origin/main`, and confirm `git status --short --branch` is clean and synchronized.

## Execution Notes

- Homepage contract suite: 7/7 passed.
- Browser fallback suite: 3/3 passed at 1440×1000 and 390×844, including domain interaction, roadmap disclosure, mobile navigation, reduced motion, JavaScript-disabled content, overflow, and console checks.
- The in-app browser plugin was present but could not start because required sandbox metadata was unavailable; Playwright 1.59.1 provided the documented fallback, and the live preview was also opened in the macOS browser.
- Full repository suite: 136 passed, 1 skipped, 8 pre-existing failures in release-fixture, future-date, and frozen-checksum tests unrelated to the homepage files. Those benchmark artifacts were deliberately left unchanged.
