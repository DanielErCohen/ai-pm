# Add or adapt a toolkit artifact

Each toolkit page uses the shared `assets/artifact-ui.css` and `js/artifact-ui.js`. Personal development review keeps its four-tab renderer in `js/development-review.js`. Keep the site navigation and contact footer outside the component.

## Page pattern

- Open with the task and one sentence. Directly under the header, before the preview, put the Start here block (`id="start"`, `.start`): one short line per assistant that says exactly what to do first, Claude app first where its route gives the whole tool and needs no terminal, and one primary button as the first action (a download, or a jump link with `data-tab` that opens the install tab it names). A prompt that works in any chat with nothing installed goes inside the block, written out in full (role, steps and output format), so it never depends on an installed skill.
- The pack is a secondary link and never the first action. The last row of Start here and the row below the preview both carry "Download editable pack" (two `a.download-pack` links per page, which `tools/check-artifact-packs.py` expects) and "Copy adaptation prompt". Only the Start here row adds the line "Use the pack to adapt the tool to your work." and a sentence that says where the install steps are ("Install steps are under Setup and support.", or "in Start here and under Setup and support" where Start here shows an install block, as Skills does). Never write "above" unless the steps really are above. Each Claude Code tab opens with the terminal line from DESIGN.md. Set `data-default="app"` on a tab group when its app route needs no terminal.
- Show a made-up example and an empty preview. Label configuration excerpts and layouts separately. State what the page saves and what stays in the user's own files.
- Keep setup steps, licenses, source links and the editable prompt in collapsed details. Preserve existing anchor links (`#setup-support`, `#start`, `#start-readers`, `#product-sparring`, `#recipient-panel`) and keyboard access.
- A tool whose source is its own repo (Project start) links to the repo's GitHub ZIP instead of a pack, keeps "Copy prompt" as the primary action and sets `data-copy-message` on `.artifact` for its copy feedback. Personal development review's pack holds the starter page, so its download is the primary action.
- Name things one way on every page: one chat per reader, recipient panel, kill line (the result, written before the test, that means stop), editable pack, the nine steps.
- Install blocks on a page repeat the blocks in the repository READMEs. Change both together: chmod only the hook files a block copied, `cp -n` for anything a reader may already have, and a git identity set before a first commit only when none exists.
- Make sample content up from scratch. Never turn private reviews, company numbers or source links into public examples by changing names.

The canonical source and agent guides live in [how-i-work](https://github.com/DanielErCohen/how-i-work/blob/main/ARTIFACTS.md) and [cv-tailor](https://github.com/DanielErCohen/cv-tailor/blob/main/ARTIFACTS.md). Add creation and adaptation instructions there when adding an artifact here. Include the editable source, prompt, validation notes and licenses in its pack. Existing installable skill ZIPs remain separate from the editable packs.

## Build and check

Keep those two repositories as sibling folders. The sources for each pack are listed in `tools/build-artifact-packs.py`; page prompts and pack names are in `tools/artifact-manifest.json`. Edit a prompt in both the manifest and its page, then check parity.

```bash
python3 tools/build-artifact-packs.py
python3 tools/check-artifact-packs.py
python3 tools/linkcheck.py
```

Also run the private publication scrub policy outside this repository. Check the top and bottom downloads, copied-prompt feedback, empty/example controls, details, keyboard focus and narrow layouts in a browser. Verify all four Personal development review tabs and the starter's validation rules. Keep failed-import tests separate from claims about ordinary page navigation. Check reduced-motion rules and 200% zoom. Review changed copy independently before publication.

The site is static; no compilation is required. GitHub Pages publishes `main`. A merged commit is not proof that the matching page or download is live: check the Pages result and the public URLs after publishing.
