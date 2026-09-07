# Eme’s Cafe

A vibrant, photo-led website for Eme’s Cafe in Remuera, Auckland. Built from an evidence-based design plan with semantic HTML, responsive CSS and a small amount of progressive-enhancement JavaScript.

**GitHub Pages address:** https://prithiraj.github.io/eme-cafe/

**Release status:** public design preview, not an owner-verified official commercial website. The deployment workflow tests the site before publishing; its run result is the source of truth for current deployment status.

## Design and content

Rich forest green, cream, berry pink and butter yellow; large editorial headlines; actual Eme’s food, drink and cabinet photography. Clear directions, food exploration, telephone, email and social links. Responsive food filters and mobile navigation enhance the page without making JavaScript essential. No WebGL, tracking scripts, runtime framework, map embed or social-feed dependency.

- [Design plan — all 17 approved sections](docs/DESIGN_PLAN.md)
- [Photography source and rights register](docs/ASSET_REGISTER.md)
- [Editing, maintenance and launch checklist](docs/OPERATIONS.md)
- [Automated browser checks](tests/browser_checks.py)

The food section is **published highlights, not a current full menu**. No prices, review scores, booking services, dietary guarantees or other unverified facts are invented.

## Run locally

Python 3.10 or newer is sufficient for a normal build. The reviewed image variants and fonts are already stored in the repository, so a build needs no network access.

```sh
python scripts/build.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. Do not open `src/index.html` directly: it is a build template.

## Project structure

```text
content/site.json          Single source of business details and food highlights
content/images.json        Photo attribution, source URLs and permission status
src/index.html             Semantic homepage template
src/styles.css             Responsive design and reduced-motion behavior
src/app.js                 Navigation, food filters and honest image fallback
public/assets/             Self-hosted optimised photos, fonts and licence notices
scripts/build.py           Offline, standard-library static build
scripts/import-assets.py   Explicit one-time asset import; not a runtime dependency
tests/browser_checks.py    Browser, accessibility and no-JavaScript regression tests
docs/                      Design, evidence, rights and maintenance documentation
.github/workflows/pages.yml  Test-gated GitHub Pages deployment
```

## Browser checks

These dependencies are development-only; they are not shipped to visitors.

```sh
python -m pip install playwright==1.55.0
python -m playwright install --with-deps chromium
npm install --no-save --package-lock=false axe-core@4.10.3
python scripts/build.py
python tests/browser_checks.py
```

The tests serve the site under `/eme-cafe/`, check six screen widths, image and local-link loading, keyboard navigation, filters, reduced motion, no-JavaScript content and axe accessibility rules. Screenshots and JSON results are uploaded by GitHub Actions. Automated checks are not a substitute for a complete manual screen-reader audit or real-user performance measurements.

## Deployment

The **Build, test and publish Eme’s Cafe** workflow builds `dist/`, runs browser checks, uploads a Pages artifact and deploys it using GitHub’s official Pages actions. It then requests the live homepage and key assets to verify publication.

Commits to `main` trigger deployment, except documentation-only changes. The workflow can also be started manually from GitHub Actions. Site content uses relative asset links and works at the project path `/eme-cafe/`.

## Commercial launch gate

The preview deliberately uses `noindex, nofollow`. All current business photographs are marked **demo reference / permission pending** on the site and in the asset register. Their presence in this repository is not a grant of commercial image rights. Owner-published media may belong to a photographer; the creator gallery image retains its original overlay and gifted-visit disclosure.

Before commercial launch, confirm business details, resolve the 13/13A address variant, approve the current menu, and clear or replace every image. Set documented image statuses to `cleared` only with actual permission evidence. The build rejects `preview: false` unless `business_verified: true` and all image statuses are cleared. Review preview wording and the final official domain as part of that release; flipping a flag alone is not a complete content sign-off.

Font Open Font Licence notices are retained under `public/assets/fonts/`. No blanket project licence purports to relicense third-party business photography.
