const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const header = document.querySelector('[data-header]');
const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('#site-nav');
const reveals = document.querySelectorAll('[data-reveal]');

document.documentElement.classList.add('js');

const updateHeader = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 24);
};

updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

const setNavigation = (open) => {
  if (!navToggle || !nav) return;
  navToggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
  document.body.classList.toggle('nav-open', open);
};

navToggle?.addEventListener('click', () => {
  setNavigation(navToggle.getAttribute('aria-expanded') !== 'true');
});

nav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => setNavigation(false));
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setNavigation(false);
});

if (!reducedMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(({ isIntersecting, target }) => {
        if (isIntersecting) {
          target.classList.add('is-visible');
          observer.unobserve(target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -6% 0px' },
  );
  reveals.forEach((element) => observer.observe(element));
} else {
  reveals.forEach((element) => element.classList.add('is-visible'));
}

const domainContent = {
  economic: {
    index: '01',
    title: 'Economic / vocational',
    copy: 'Job displacement, skill obsolescence, wage pressure, retraining, and occupational status—stratified by the work people actually do.',
    question: 'What changes when AI can perform a task that defines your livelihood?',
  },
  epistemic: {
    index: '02',
    title: 'Epistemic',
    copy: 'Deepfakes, synthetic news, expert conflict, and the growing uncertainty around whether digital evidence can still be trusted.',
    question: 'What happens when seeing is no longer sufficient grounds for believing?',
  },
  relational: {
    index: '03',
    title: 'Relational',
    copy: 'AI companions, mediated friendships, partner-confidant displacement, and human attachment shifting toward synthetic agents.',
    question: 'How does intimacy change when an artificial system is always available?',
  },
  existential: {
    index: '04',
    title: 'Existential / identity',
    copy: 'Human judgment, creativity, status, purpose, and the boundaries people draw around personhood and meaningful work.',
    question: 'What remains distinctly human when systems can imitate valued human capacities?',
  },
  autonomy: {
    index: '05',
    title: 'Autonomy / surveillance',
    copy: 'Personalized behavior nudging, institutional scoring, workplace monitoring, and public-space tracking powered by AI.',
    question: 'How does agency feel when systems continually observe, predict, and steer behavior?',
  },
  safety: {
    index: '06',
    title: 'Safety / catastrophic',
    copy: 'Cyber cascades, biosecurity misuse, military escalation, systemic harm, and perceived loss of meaningful human control.',
    question: 'How do people price low-probability harms with consequences they cannot personally contain?',
  },
  somatic: {
    index: '07',
    title: 'Somatic / ambient',
    copy: 'Sleep disruption, bodily vigilance, background dread, avoidance, and low-grade unease after credible capability news.',
    question: 'What does AI progress register in the body before a person can fully articulate it?',
  },
};

const domainButtons = document.querySelectorAll('[data-domain]');
const domainIndex = document.querySelector('[data-domain-index]');
const domainTitle = document.querySelector('[data-domain-title]');
const domainCopy = document.querySelector('[data-domain-copy]');
const domainQuestion = document.querySelector('[data-domain-question]');

domainButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const content = domainContent[button.dataset.domain];
    if (!content) return;
    domainButtons.forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle('is-active', active);
      candidate.setAttribute('aria-pressed', String(active));
    });
    if (domainIndex) domainIndex.textContent = content.index;
    if (domainTitle) domainTitle.textContent = content.title;
    if (domainCopy) domainCopy.textContent = content.copy;
    if (domainQuestion) domainQuestion.textContent = content.question;
  });
});
