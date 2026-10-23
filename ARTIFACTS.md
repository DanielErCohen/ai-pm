# Add or adapt a toolkit artifact

Each toolkit page uses the shared `assets/artifact-ui.css` and `js/artifact-ui.js`. Development review keeps its four-tab renderer in `js/development-review.js`. Keep the site navigation and contact footer outside the component.

## Page pattern

- Lead with the task, one short description, Download pack and Copy prompt. Repeat the actions below the preview.
- Show a synthetic example and an empty preview. Label configuration excerpts and layouts separately. State what the page saves and what stays in the user's own files.
- Keep setup steps, licenses, source links and the editable prompt in collapsed details. Preserve existing anchor links and keyboard access.
- Keep sample content wholly synthetic. Never turn private reviews, company numbers or source links into public examples by changing names.

The canonical source and agent guides live in [how-i-work](https://github.com/DanielErCohen/how-i-work/blob/main/ARTIFACTS.md) and [cv-tailor](https://github.com/DanielErCohen/cv-tailor/blob/main/ARTIFACTS.md). Add creation and adaptation instructions there when adding an artifact here. Include the editable source, prompt, validation notes and licenses in its pack. Existing installable skill ZIPs remain separate from artifact source packs.

## Build and check

Keep those two repositories as sibling folders. The sources for each pack are listed in `tools/build-artifact-packs.py`; page prompts and pack names are in `tools/artifact-manifest.json`. Edit a prompt in both the manifest and its page, then check parity.

```bash
python3 tools/build-artifact-packs.py
python3 tools/check-artifact-packs.py
python3 tools/linkcheck.py
```

Also run the private publication scrub policy outside this repository. Check the top and bottom downloads, copied-prompt feedback, empty/example controls, details, keyboard focus and narrow layouts in a browser. Verify all four Development review tabs and the starter's validation rules. Keep failed-import tests separate from claims about ordinary page navigation. Check reduced-motion rules and 200% zoom. Review changed copy independently before publication.

The site is static; no compilation is required. GitHub Pages publishes `main`. A merged commit is not proof that the matching page or download is live: check the Pages result and the public URLs after publishing.
