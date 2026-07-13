import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = {
    "mission",
    "why",
    "domains",
    "instrument",
    "global",
    "roadmap",
    "resources",
    "contact",
}
REQUIRED_PHRASES = {
    "We benchmark what AI can do",
    "Important",
    "Innovative",
    "Insightful",
    "If the constructs do not link, we do not publish the index.",
    "Not a clinical diagnostic",
}


class HomepageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.domain_buttons = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if element_id := attributes.get("id"):
            self.ids.add(element_id)
        if tag == "button" and "data-domain" in attributes:
            self.domain_buttons.append(attributes)
        if tag in {"a", "link", "script", "img"}:
            attribute = "href" if tag in {"a", "link"} else "src"
            if target := attributes.get(attribute):
                self.links.append(target)


class HomepageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.homepage = ROOT / "index.html"
        cls.html = cls.homepage.read_text(encoding="utf-8") if cls.homepage.exists() else ""
        cls.parser = HomepageParser()
        cls.parser.feed(cls.html)

    def test_homepage_contains_required_sections_and_copy(self):
        self.assertTrue(REQUIRED_SECTIONS <= self.parser.ids)
        for phrase in REQUIRED_PHRASES:
            self.assertIn(phrase, self.html)

    def test_homepage_exposes_accessible_domain_controls(self):
        self.assertEqual(len(self.parser.domain_buttons), 7)
        self.assertTrue(
            all(button.get("aria-controls") for button in self.parser.domain_buttons)
        )

    def test_local_assets_resolve(self):
        for path in ("assets/styles.css", "assets/app.js", "assets/observatory.svg"):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_styles_define_tokens_breakpoints_and_reduced_motion(self):
        css_path = ROOT / "assets/styles.css"
        css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
        for token in ("--void", "--bone", "--lime", "--cyan", "--amber"):
            self.assertIn(token, css)
        self.assertIn("@media (prefers-reduced-motion: reduce)", css)
        self.assertIn("@media (max-width: 768px)", css)

    def test_observatory_has_labeled_signals(self):
        svg_path = ROOT / "assets/observatory.svg"
        svg = svg_path.read_text(encoding="utf-8") if svg_path.exists() else ""
        self.assertIn('id="capability-signal"', svg)
        self.assertIn('id="response-signal"', svg)
        self.assertIn("<title>", svg)

    def test_script_is_progressive_and_updates_accessible_states(self):
        script_path = ROOT / "assets/app.js"
        script = script_path.read_text(encoding="utf-8") if script_path.exists() else ""
        self.assertIn("IntersectionObserver", script)
        self.assertIn("aria-expanded", script)
        self.assertIn("data-domain", script)
        self.assertNotIn("fetch(", script)

    def test_local_document_links_resolve(self):
        for target in self.parser.links:
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            path = target.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]
            self.assertTrue((ROOT / path).is_file(), target)


if __name__ == "__main__":
    unittest.main()
