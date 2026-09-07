# Eme’s Cafe — website design and implementation plan

Research date: **7 September 2026**. Repository: `Prithiraj/eme-cafe`.

## Approval and release status

The 17-part research-led design proposal was approved in the conversation. The implementation instruction adds a **more vibrant visual treatment**, real photography, permission to use complementary Three.js, and publication through GitHub Pages. This document is the maintained implementation version of that plan.

Publication is authorised. Business-owner verification and commercial image rights are **not** established by that authorisation. Accordingly the first deployment is a clearly labelled, non-indexable **website preview**, not an owner-verified official commercial launch. Photography requiring approval is identified in captions, the credits page, and the asset register. No ratings, prices, services, founder story, policies, or current stock will be invented.

## 1. Evidence baseline

| Fact | Source and confidence | Implementation treatment |
|---|---|---|
| Eme’s Cafe, Remuera | Owner Instagram [1] | Display business name and neighbourhood. |
| 13A Shore Road | Owner Instagram [1]; other listings use 13 Shore Road [4] | Use the owner-profile variant, mark details as published rather than independently confirmed; retain the discrepancy for owner sign-off. |
| Monday–Friday 6:30 am–3 pm; Saturday–Sunday 7 am–3 pm | Owner profile [1] | Visible grouped hours and matching JSON-LD from one data file. |
| Kitchen closes at 2 pm | Owner profile [1] | Separate kitchen note, never confused with café closing time. |
| +64 9 522 2783 | Owner posts [3] | Click-to-call link; no booking promise. |
| emescafe688@gmail.com | Owner profile [1] | Visible email link. |
| Chicken Karaage Croffle; Creamy Portobello Mushroom | Owner Facebook [2] | Food highlights, not an assertion of current availability. |
| Coffee, iced blueberry matcha, matcha with Thai tea | Owner posts [1–3] | Drink highlights; no supplier, ingredient, or origin claims. |
| Cabinet baking | Business Too Good To Go listing [4] | Real photographic reference; no guarantee of today's selection. |
| Historical delivery menu | Uber Eats [5] | Not used as a current menu or live ordering service. Storefront says closed on Uber Eats from 15 May 2026; this does not establish physical closure. |
| Gifted creator coverage | Kat’s Food Diary [6] | Not repackaged as independent testimonials. |

Unverified and excluded: current prices/full menu; ratings/review count; parking; accessibility facilities; dietary suitability; pet policy; reservations; catering; delivery; Wi-Fi; ownership history; in-house baking claims; official domain. Legacy Shore Road Cafe facts are not silently carried over.

## 2. Audience

Needs-based hypotheses, not measured demographics: nearby visitors checking hours/directions, friends choosing a brunch stop, and social-media visitors recognising a dish or drink. Prioritise fast practical answers while allowing relaxed visual exploration. Avoid assumptions about income, age, family status, or visit frequency.

## 3. Conversion goals

Primary: **Get directions** to the supplied business location. Secondary: **Explore the food**. Supporting: **Call the café**. The wording intentionally does not promise a complete current menu. Instagram and email are lower-priority links. No inactive Uber Eats ordering, fictitious reservations, newsletter, checkout, or contact form.

Keep a clear desktop header CTA, two hero actions, visit CTA, and a safe-area-aware mobile action bar. No analytics in the preview. Any later measurement should describe directions/phone clicks as intent signals, not confirmed store visits or sales.

## 4. Creative direction

**Good mornings. Better brunch.** Warm editorial design, made more vibrant with rich green, berry, pale pink, butter yellow and generous cream. Large expressive serif type, crisp sans-serif utility text, asymmetric photographic compositions, restrained rounded forms and small flower/spark motifs. Photography remains the main storytelling element.

A real Eme’s plate/counter image anchors the hero. This is a proposed visual identity, not a claim about an established official logo. Use a typographic name, with no invented establishment date. Authentic source photos may be cropped and colour-balanced lightly, never altered to add ingredients, people, portions or a fictional space.

The proposal’s focused competitor check found Rosie’s menu/contact navigation and external menu documents, and Knead on Benson’s contact/social/newsletter content. Eme’s response is readable on-page information and fewer exits before directions—not copied branding or unsupported superiority claims. [7–8]

## 5. Color system

| Token | Hex | Role |
|---|---|---|
| Cream | `#FBF7EC` | Page background and light text panels |
| Forest | `#244633` | Brand text, principal actions, dark sections |
| Berry | `#963D53` | Editorial emphasis and supporting actions |
| Pink | `#F1BFCB` | Vibrant bands, cards and accents |
| Butter | `#F4D875` | Small tags and decorative marks |
| Ink | `#292D26` | Body text |
| Muted | `#58604F` | Supporting text |

Use dark text on light accents, never white text on pink/yellow. Test actual contrast, including focus, hover and selected states. No colour overlay that distorts food.

## 6. Typography

**Fraunces** for expressive headlines; **DM Sans** for body, menu, hours and controls. Self-host a limited Latin WOFF2 subset at build time where available; preserve upstream OFL notices. System fallbacks must keep the page usable if fonts fail.

Fluid headline sizes, approximately 48–64 px on phones and 88–112 px on large screens. Body 16–18 px, labels at least 14 px where practical. Comfortable leading and reading width. No fixed-height text boxes or script fonts for essential information.

## 7. Image strategy

Use actual photographs verifiably associated with Eme’s, not unrelated stock or AI food. Prefer owner-published originals. Source pages, attribution, visual descriptions, processing and permission status go in `content/images.json` and `docs/ASSET_REGISTER.md`.

Owner publication does not prove ownership. Platform and review imagery remains **demo/editorial reference only** pending appropriate permission. Give visible photo-credit links and a clear site-wide preview notice. Do not imply an unverified image depicts a named dish. If a photo is unavailable, use an honest designed fallback, not a different café’s photograph.

Generate responsive WebP and JPEG variants, explicit intrinsic sizes and useful alt text. Do not upscale beyond the source. Prefer six strong images over a repetitive or autoplay gallery. Use real current space/team images only when obtained; otherwise keep the story short and factual.

## 8. Information architecture

One substantial homepage: header → hero → food-led value proposition → food/drink highlights → the real café → gallery → visit/contact/hours → closing CTA/footer. Navigation: The food / The café / Find us. Additional lightweight pages: photo credits and preview privacy notes. Stable anchors and ordinary links are always available.

## 9. Section-by-section layout

### Header and hero

A slim preview/status line, simple wordmark, three navigation links and obvious directions CTA. Hero pairs large green/berry typography with a real café image and a small secondary photographic composition where suitable. Short location eyebrow, concise supporting copy and directions/food actions. Practical hours/kitchen note without an unreliable ‘Open now’ badge.

### Value proposition and food

A playful colour band introduces brunch, coffee/matcha and cabinet treats. A readable highlights section uses confirmed published product names, distinct category labels and real photographs. Optional filter buttons progressively enhance the static content; with no JavaScript all items remain visible. Clearly explain that these are published highlights, not today’s full menu or live stock. No invented prices or dietary tags.

### Café and gallery

A contrasting forest-green editorial section pairs genuine space/counter photography with a short invitation to spend a little time on Shore Road. Do not fabricate a team/founder story. Follow with a still photographic grid and Instagram link; every relevant image has a source/rights note. No testimonial module without verified independent text and permission.

### Visit and closing CTA

A pink/cream composition presents the published address, phone, email and grouped hours. Explicit kitchen cutoff, public-holiday caveat and directions link. No invented map geography, free parking or walking-time claims. A large closing wordmark/CTA makes the page feel complete. Footer includes social links, image credits and preview/privacy status.

## 10. Three.js and animation

Three.js is permitted but **not required**. The chosen implementation does not add WebGL: photography, typography and colour carry the story more effectively, with lower transfer and accessibility cost. Decorative SVG/CSS accents supplement actual images, never replace them.

Keep hover/focus transitions around 150–220 ms. No parallax, autoplay carousel, scroll hijack, custom cursor, rotating food, loading gate or continuous particle scene. Respect `prefers-reduced-motion`; all primary content exists in the initial HTML and is visible without scripts.

## 11. Responsive behavior

Mobile-first, tested at 320/375/390/768/1024/1440 px plus landscape. Single column on phones; editorial split layouts on wider screens; max-width container. Deliberate image focal points. Wrappable addresses and email. Mobile directions/food bar respects safe areas, reserves layout space, and is suppressed in short viewports where it would obstruct content. No horizontal document overflow.

## 12. Accessibility

Target WCAG 2.2 AA. Semantic landmarks, one H1, ordered headings, skip link, meaningful image alt, decorative SVG hidden from assistive technology. Visible keyboard focus, correctly named buttons, sufficient contrast and generous touch targets. Functional navigation disclosure with Escape/focus handling, truthful category filter status, no content hidden only for animation.

Test keyboard navigation, no-JS behavior, reduced motion, responsive reflow and automated axe checks. Automated checks are not a claim of complete WCAG conformance; record manual screen-reader/zoom checks separately and honestly.

## 13. Performance

Static HTML/CSS/vanilla JavaScript; no runtime framework or unnecessary dependencies. Python builds the site and optimises photos. Self-host published media and fonts; no social embeds, map embed, autoplay video or tracking scripts.

Aim for initial mobile transfer ≤700 KB, hero ≤200 KB mobile /350 KB desktop, compressed CSS ≤30 KB, JS ≤20 KB, fonts around 100 KB. Responsive image source sets, eager prioritised hero, lazy lower images and reserved dimensions. Target Lighthouse mobile performance ≥90. Field CWV targets: LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1 at the 75th percentile once real traffic is available. These are goals until measured.

## 14. SEO and local discovery

Useful title/description, canonical GitHub Pages preview URL, Open Graph metadata, favicon and `CafeOrCoffeeShop` JSON-LD generated from the same business data as visible hours/contact details. No invented priceRange, ratings, reviews, reservation or offer data. Do not use the 2 pm kitchen cutoff as business closing time.

Preview has `noindex, nofollow` and no discoverability promotion. Business details remain attributed to published sources. Enable indexability, final commercial OG photography and an official canonical domain only after owner/content/rights sign-off. A preview URL must not be presented as the established official domain. Rich results and search ranking are not guaranteed.

## 15. Rights/licensing notes

Publicly accessible does not mean commercially licensed. Record original source, rights holder when known, permission status, required credit and intended use. Do not remove watermarks or erase gifted/ad disclosures. No all-encompassing open-source licence covering third-party photos. Retain font OFL text. Demo media is visibly marked and must be licensed/replaced before commercial launch.

## 16. Implementation sequence

1. Inspect repository and preserve existing files.
2. Document approved plan and vibrant preview addendum.
3. Collect and visually verify actual business photography and sources.
4. Implement semantic templates, single-source content and design tokens.
5. Build responsive photo variants and metadata; add restrained enhancements.
6. Run browser, no-JS, mobile, reduced-motion, link, image and accessibility tests.
7. Review rendered screenshots; correct visual/layout defects.
8. Publish through a least-privilege GitHub Pages workflow; verify deployment and live page.
9. Record measured QA, release status, and maintenance/rights tasks in Markdown.

## 17. Acceptance criteria

- A vibrant and recognisably Eme’s, photo-led site rather than a generic template.
- Actual business imagery, exact source records and visible permission-pending disclosure.
- Clear directions, food exploration, telephone/email and social navigation.
- Honest menu scope; no invented prices, reviews, facilities or availability.
- Published hours and kitchen cutoff accurately separated and centrally maintained.
- No broken internal links/images, console errors or horizontal overflow in tested sizes.
- Usable keyboard focus, reduced motion and no-JS fallback.
- Fast static delivery and valid metadata/structured-data syntax.
- Markdown plan, asset register, maintenance instructions and actual test results in the repository.
- Successful GitHub Pages deployment verified before claiming it is live.
- Commercial launch remains gated on owner verification and photo rights clearance.

## Sources

[1] https://www.instagram.com/emescafe.akl/ — owner profile and published hours/contact.

[2] https://www.facebook.com/p/Emescafeakl-61568487993875/ — owner food promotions.

[3] https://www.facebook.com/61568487993875/posts/iced-blueberry-matcha-at-emescafeakl-emes-cafe-13-shore-road-remuera-auckland-10/122154617126616266/ — phone and blueberry matcha.

[4] https://www.toogoodtogo.com/en-nz/find/auckland/emescafe/bakedgoods/surprisebags-176618356905439523 — business cabinet reference and address variant.

[5] https://www.ubereats.com/nz/store/emes-cafe/ee9m3BjoVkinN-g8RzcuiQ — inactive delivery listing and historical menu.

[6] https://www.lemon8-app.com/@kain.kat/7545374036445446674?region=nz — gifted creator coverage; not independent rating evidence.

[7] https://www.rosieparnell.nz/rosie-menu — competitor content architecture reference.

[8] https://www.kneadonbenson.co.nz/ — competitor navigation/content reference.

Technical references: https://www.w3.org/TR/WCAG22/ ; https://schema.org/CafeOrCoffeeShop ; https://developers.google.com/search/docs/appearance/structured-data/local-business ; https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
