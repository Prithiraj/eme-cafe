# Eme’s Cafe — release QA report

**Date:** 7 September 2026  
**Release:** public, non-indexable design preview  
**Published URL:** https://prithiraj.github.io/eme-cafe/  
**Tested/deployed commit:** `baf403606fbcb3ecbc8b28e381d8e1b49c908640`  
**Successful workflow:** https://github.com/Prithiraj/eme-cafe/actions/runs/34084191598

The build, browser checks, GitHub Pages deployment, live HTTP verification and performance-audit jobs all completed successfully. Subsequent documentation/research-workflow cleanup does not change the deployed application assets.

## Browser and accessibility checks

Python Playwright 1.55.0 with Chromium; axe-core 4.10.3. The test server deliberately uses `/eme-cafe/`, matching the GitHub Pages project path.

| Viewport | Horizontal overflow | Broken business images |
|---|---|---|
| 320 × 800 | None | 0 |
| 375 × 812 | None | 0 |
| 390 × 844 | None | 0 |
| 768 × 1024 | None | 0 |
| 1024 × 900 | None | 0 |
| 1440 × 1000 | None | 0 |

Passed checks:

- Mobile navigation opens using the keyboard, closes with Escape and returns focus to its control.
- Food filters select the expected items, announce the count and restore all seven highlights when reset.
- Reduced-motion mode removes smooth scrolling and decorative transitions.
- All homepage internal links and anchors resolve under the project subpath.
- The no-JavaScript page exposes navigation, all food highlights, contact details and hours.
- JSON-LD parses and agrees with the centrally maintained regular hours and exact Maps place CID. No invented rating or price range is present.
- The preview’s `noindex, nofollow` directive is present.
- No captured JavaScript runtime errors.
- **Zero axe violations** for the tested WCAG A/AA rule tags on the homepage, photo-credits page and privacy page.

Visual review used rendered desktop, tablet and phone layouts with the actual locally hosted business photography. The initial tablet decorative-halo overflow was corrected, the mobile headline was resized to keep the hero compact, and the mobile navigation toggle was restricted to the appropriate viewport.

## Live-site Lighthouse measurements

Lighthouse **12.8.2**, three mobile runs using its simulated throttling against the **public GitHub Pages URL**, after deployment. SEO scoring was deliberately excluded because this preview is not intended to be indexed.

| Run | Performance | Automated accessibility | Best practices | LCP | CLS | Total blocking time |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 99 | 100 | 100 | 1,236.579 ms | 0.068941 | 0 ms |
| 2 | 100 | 100 | 100 | 1,653.144 ms | 0.003531 | 0 ms |
| 3 | 99 | 100 | 100 | 1,653.779 ms | 0.068941 | 0 ms |

**Median mobile performance score: 99/100.** The raw Lighthouse JSON and summary are available in the workflow’s `live-performance-results` artifact for its configured 14-day retention period. This Markdown record persists in repository history.

These are laboratory measurements, not a guarantee for every visitor or proof of field Core Web Vitals. Total blocking time is not an INP measurement. No real-user field INP or percentile result is claimed.

## Build measurements

Measured from the deployed build’s `build-info.json`:

| Item | Bytes |
|---|---:|
| Homepage HTML | 21,845 |
| Stylesheet, gzip | 6,506 |
| JavaScript, gzip | 1,225 |
| Self-hosted WOFF2 fonts | 104,236 |
| Entire deployment, including every image variant | 1,666,621 |

The entire deployment size is **not** the initial page transfer. Responsive image selection and lazy loading mean visitors do not download every stored photo variant. The font total is approximately 102 KiB, marginally above the approximate 100 KB planning target; the measured page performance remains above the 90-point target.

## Publication verification

After deployment, the workflow requested the live homepage and confirmed the expected hero text, exact directions CID and preview noindex status. It also confirmed HTTP 200 responses for the stylesheet, script, a real business photo and both supporting pages. All three Lighthouse audits subsequently loaded the published site successfully.

## Remaining commercial-launch gates

The site is public but remains an **independent design preview**, not an owner-verified official business website. Confirm the 13/13A address variant, current regular/special hours and current menu information with the owner. Clear or replace all permission-pending photographs before commercial use. Review visible preview language and the official canonical domain when preparing that release.

A complete manual screen-reader audit, real-device browser matrix, user testing and field-performance study were not performed. Automated scores alone do not certify complete WCAG conformance. The site does not collect analytics, so no conversion lift or completed-visit metrics are claimed.

See [the design plan](DESIGN_PLAN.md), [asset-rights register](ASSET_REGISTER.md) and [operating instructions](OPERATIONS.md).
