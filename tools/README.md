# Site tools

Five scripts for checking the site and building the skill zips. Run each from this repository's root folder. The site itself has no build step.

## linkcheck.py

Checks every internal link, `#anchor`, `aria-controls` and `aria-labelledby` reference, CSS `url()`, duplicate id and third-party font reference. Exit code 1 on any finding.

```bash
python3 tools/linkcheck.py
```

## screens.py

Takes a full-page screenshot of every page at 1280 px and 390 px. Files are named by page path and width, for example `principles-index-390.png`. It needs the Playwright Python package (`pip install playwright`) and finds Chromium on its own: Playwright's browser, the `CHROME_PATH` environment variable, the Playwright browser caches, then Google Chrome on a Mac. Exit code 1 when a page fails to load or scrolls sideways.

```bash
python3 tools/screens.py /path/to/screens-folder
```

## build-skill-zips.sh

Builds one zip per Claude skill into `downloads/<skill-name>.zip`, with the skill folder at the top of each zip. It builds from a staging copy, so the source repositories stay untouched. In the staged `SKILL.md` it removes the `effort:` and `argument-hint:` lines, because the Claude app accepts only the keys `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`. It adds `guides/07-ats-checks.md` to the cv-review and cv-tailor zips as `ats-checks.md`. It stops if a source is missing, if another frontmatter key remains or if a private `.local.md` file would end up inside. distill-to-gh-issue has no zip, because it needs `gh` and a local repository and so works in Claude Code only.

It requires sibling checkouts named `how-i-work` and `cv-tailor`. Run it after changing a skill in those repositories, then commit the changed zips.

```bash
bash tools/build-skill-zips.sh
```

## Artifact packs

Run `python3 tools/build-artifact-packs.py` after editing artifact sources or adaptation prompts. It builds reproducible source packs from sibling how-i-work and cv-tailor checkouts. Run `python3 tools/check-artifact-packs.py` to check source and prompt parity. See [ARTIFACTS.md](../ARTIFACTS.md).
