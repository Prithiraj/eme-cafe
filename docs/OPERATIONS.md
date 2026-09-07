# Editing and operating the Eme’s Cafe website

## Routine content changes

Edit `content/site.json`, build, test and commit. Business hours are defined once and used for both visible text and JSON-LD. Do not edit the generated `dist/` files. Keep the café closing time separate from the kitchen cutoff. Add special-hours information only when confirmed; give temporary notices an explicit expiry and remove them when no longer relevant.

The phone uses `tel:+6495222783`; email uses an ordinary `mailto:` link. The Maps CID is `5759762822561383577`, calculated from the exact place identifier in the supplied Google Maps URL. Do not substitute the map viewport’s centre for the café’s location.

The current food section is intentionally a selection of published highlights. To publish a real menu, obtain current names, descriptions, prices and any dietary/allergen wording from the owner. Update CTA labels from “Explore the food” to “View menu” only when there is an actual approved menu destination. Do not silently use the inactive Uber Eats menu as current content.

## Photography

`content/images.json` is the provenance and permission record. `public/assets/media/manifest.json` records local dimensions, responsive variants and original-file hashes. The matching Markdown source register is `docs/ASSET_REGISTER.md`.

Prefer original files provided with written permission by the owner or photographer. A social-media repost is not proof that the business owns the copyright. For each replacement, record the source, original creator, permission evidence, allowed use, required credit and approval date. Confirm alt text against the actual photograph. Do not fabricate food, portions, people, interiors or a team biography.

`scripts/import-assets.py` is an explicit import utility, not part of normal builds. Its source URLs may expire. The live site serves committed local variants and does not depend on those URLs. Do not repeatedly run the importer against stale social-media URLs. When replacing assets, supply reviewed original sources, regenerate responsive variants and update the register. The import workflow has repository-content write permission only so it can store the approved import output; the Pages deploy job has no repository-content write permission.

No permission-pending photo is used in the Open Graph card. That card is an original typographic preview graphic.

## Design changes

Design tokens and responsive rules are in `src/styles.css`. Main colors are cream `#FBF7EC`, forest `#244633`, berry `#963D53`, pink `#F1BFCB` and butter `#F4D875`. Keep the real photographs prominent. Decorative CSS/SVG shapes are not a replacement for business imagery.

Do not add continuous animation, scroll hijacking or a loading screen. Respect `prefers-reduced-motion`; all essential content must remain visible without JavaScript. A future Three.js feature must have a genuine storytelling purpose and a static fallback, rather than being a dependency for reading the page.

## QA and deployment

Run the standard-library build and the browser checks described in the root README. The test server uses the `/eme-cafe/` path so root-relative asset mistakes are caught before GitHub Pages deployment. Test screenshots and JSON reports are available in each Actions run’s `browser-test-results` artifact.

The Pages workflow runs on relevant `main` changes. Documentation-only changes do not rebuild the live site. To republish unchanged code, use the workflow’s manual trigger. A successful deployment must include a working homepage, stylesheet, script, photo and supporting pages at the actual published URL; a successful build alone is not a verified launch.

Preserve the previous working revision. To roll back, revert the relevant content/code commit in GitHub and let the same tests and deployment workflow run again. Avoid force-pushing the main branch.

## Before owner-approved commercial launch

1. Obtain owner approval for name, preferred 13/13A address, phone, email, opening hours, kitchen cutoff and current food content. Record date and approver in the evidence register.
2. Clear or replace every photograph. Change `status` to `cleared` only with actual permission evidence, and update source credits accordingly. Remove demo-only assets from deployed output rather than merely hiding their labels.
3. Confirm the official domain, update `site_url`, title, descriptions, Open Graph and visible preview language. Add `business_verified: true` and set `preview: false` only after the previous steps. The build enforces the verification and photo-status gate, but visible copy still requires deliberate editorial review.
4. Review privacy wording against any actual analytics, form, booking or payment implementation. Do not claim services that are not implemented.
5. Run manual keyboard, screen-reader, zoom/reflow and mobile checks in addition to automated axe. Verify meaningful alt text, live contact links and image rights. Re-run performance measurements after any media or dependency change.
6. Verify the deployed release before promoting it. After enough traffic exists, assess field Core Web Vitals; laboratory numbers do not establish a field pass.

## What this preview does not do

No payments, reservation system, contact form, newsletter, live stock/menu, live “open now” badge, analytics or advertising tracking. It does not claim to be the owner-verified official site. Directions/telephone clicks are not measured as completed visits or sales.
