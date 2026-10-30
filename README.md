# Daniel Cohen: PM tools and practice

Free PM tools, each built for a problem in my own work, with a nine-step PM workflow and the principles behind it. It is a static site with no build step.

Live site: [danielercohen.github.io/ai-pm](https://danielercohen.github.io/ai-pm/)

## Serve locally

```bash
python3 -m http.server --bind 127.0.0.1
```

Run it in this folder and open http://localhost:8000.

## Check

- `python3 tools/linkcheck.py` checks internal links, anchors and accessibility references.
- `python3 tools/screens.py <output-folder>` takes desktop and mobile screenshots. It needs Playwright and Chromium.

## Artifact previews

All ten toolkit pages use the shared preview, download and copy pattern. [ARTIFACTS.md](ARTIFACTS.md) explains how to add an artifact, keep its source and agent guidelines aligned, build the packs and verify publication.

## Where the skills come from

The skill zips in `downloads/` are built by `tools/build-skill-zips.sh` from [how-i-work](https://github.com/DanielErCohen/how-i-work) and [cv-tailor](https://github.com/DanielErCohen/cv-tailor). Those repositories hold the sources and the third-party notices.

## Licence

The code and text are MIT, copyright Daniel Cohen 2026. The portrait, the product logos and the screenshots are not covered by the MIT licence. The fonts are under the SIL Open Font License, which sits beside them in `assets/fonts/`.
