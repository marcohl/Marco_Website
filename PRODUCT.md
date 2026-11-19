# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- Primary: peers in energy and data (engineers, analysts, data people) who arrive from a LinkedIn post about a new project. They skim on phone or desktop, open one chart, and decide in seconds whether the author is worth following.
- Secondary: recruiters and hiring managers who land on the home page from the LinkedIn profile.

## Product Purpose

Marco Herbas Lopez's personal site: small data-analysis and science-outreach projects, each built around one interactive chart. Success is reputation: peers follow, share and remember Marco as someone who ships data products, not someone who dabbles. There is no sales or hiring funnel to optimise.

## Positioning

An electrical and nuclear engineer (10+ years in high-voltage systems, nuclear engineering and renewables; MSc Nuclear Engineering, Politecnico di Milano) who turns real energy and science data into finished, verified, explorable charts. The domain knowledge and the source-checked numbers are what a generic data-viz portfolio cannot copy.

## Operating Context

- Each project follows the method in CLAUDE.md: brief, data, form, build, words, QA, publish. Project pages are numbered MHL-00N.
- New projects are announced on LinkedIn with link-preview images in `public/og/`.
- Built with Astro, d3 and Python; deployed on Cloudflare Workers on every push to main.

## Capabilities and Constraints

- Four published projects: uranium enrichment (MHL-001), Olympic freestyle sprint (MHL-002), nuclear reactors of the world, Bolivia power plants.
- Every chart has a data-table alternative, keyboard operation and a no-JS fallback; keep these.
- Open: final `site` URL in `astro.config.mjs`; custom domain undecided.

## Brand Commitments

- Name shown as "Marco Herbas Lopez".
- Voice: relaxed and human, but credible. Marco explicitly does not want the site to feel rigid or overly precise; casual asides that undercut credibility (e.g. "I like good coffee and AI") should go.
- Public contact: email and LinkedIn only. The phone number is never published.

## Evidence on Hand

- The published projects on this site are the only evidence of "data products". Do not mention or imply professional/employer data work, clients, testimonials or a downloadable CV; none are available.
- Credentials above (experience, MSc, languages: Spanish, Italian, English, French) are confirmed in the existing About copy.

## Product Principles

1. Show the work first: a visitor should see a real chart or project before reading about Marco.
2. Shipped, not exploring: every claim and number is sourced and verified; the site reads as finished products.
3. Relaxed, not rigid: approachable language and layout, without losing credibility.
4. One primary action: write to Marco by email; LinkedIn is secondary.

## Accessibility & Inclusion

Charts must stay usable by keyboard and screen reader (data tables, live reading cards) and respect reduced motion. Target WCAG 2.1 AA contrast in both themes.
