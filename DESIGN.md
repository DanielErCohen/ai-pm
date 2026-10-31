# Design system

The site follows the home page and the section pages built with it (Toolkit, Projects, Personal, About). Every page uses the tokens in `style.css` `:root`, one page header, one section pattern and the components below. Tool pages also load `assets/artifact-ui.css` for their previews; its last block makes their header, actions and container follow this system.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | #F7F4EE | Page background |
| `--surface` | #FFFFFF | Cards, panels |
| `--ink` / `--muted` | #1F2A2E / #5B6266 | Text / secondary text |
| `--line` | #E2DDD2 | Borders, rules |
| `--accent` | #0F6E6E | Links, primary buttons |
| `--amber` | #E8A33D | Highlights, decorative circles |
| `--serif` | Source Serif 4, 700 | Headings |
| `--sans` | System UI stack | Body, labels, buttons |
| `--max` / `.wrap` | 1120px, 24px side padding | Every container, tool pages included |
| `--r` | 16px | Cards and panels |

Section colors mark where a reader is. Each section has a color for the circle and a text color for its eyebrow (AA contrast on the page background):

| Section | Circle | Eyebrow text | Class |
|---|---|---|---|
| Toolkit | teal `--accent` | teal | `.pagehead.s-toolkit` |
| Projects | amber `--amber` | ochre #8A5A00 | `.pagehead.s-projects` |
| How I work | blue `--c-method` | blue | `.pagehead.s-method` |
| Personal | berry `--c-personal` | berry | `.pagehead.personal` |
| Home, About | amber and teal | muted | `.hero`, `.about-hero` |

Detail pages take the eyebrow color of what they show: a tool's category color, or a project's status color (live olive `--s-live`, stopped gray `--s-stopped`, work in progress ochre #8A5A00 for text and amber for the pill). Tool categories have their own colors (teal Setup, plum Skills, olive Routines, rust Career, ochre Small builds, blue Template), some shared with sections; the breadcrumb and nav carry the section. The nine steps use the home page's group colors: blue Understand, plum Choose, teal Deliver.

Type scale: h1 `clamp(2rem, 4.2vw, 3.1rem)` with -.01em tracking on every page, h2 `clamp(1.5rem, 2.6vw, 2rem)`, h3 1.2 to 1.4rem, body 17px/1.6, lede 1.2rem, eyebrow .78rem bold uppercase with .09em tracking.

## Page headers

One header per page, on the page background. Three variants share the eyebrow, h1, lede and actions:

- **Hero** (Home, About): two circles and a visual on the right.
- **Landing** (`.pagehead` with a section class; Toolkit, Projects, How I work, Personal): one 320px circle top right in the section color at .22 opacity. No breadcrumb.
- **Detail** (`.pagehead.detail`; projects, Habits and principles; tool pages use `.artifact .intro`, styled the same): a breadcrumb bar above (`Section / Page`), no circle. The eyebrow names the kind of page: the tool category, "Side project", "How I work".

Header parts, in order:

- **Eyebrow**, then on project pages a **meta line** (status pill and dates), then the **h1** and one **lede** paragraph.
- **Why I built it** (tools and projects): one closed line under the lede that opens to three to five bullets. On tool pages it opens the collapsed Setup and support panel (`.artifact-support`, below the preview), which holds the tool's own sections, Came from and the setup steps.
- **Used in the nine steps: step N** (tools that serve a step).
- **Actions:** the first is `.btn.primary`, at most two more `.btn`; a lone action is primary. Long case pages may add a row of small jump links (`.btn.sm`).
- **Start here** (tool pages only): the first block under the header, before the preview, with `id="start"`. See Tool pages below.
- **Facts strip (projects, when known):** type and role; status and dates live in the meta line.

## Tool pages

Nine of the ten tool pages follow one order: header (eyebrow, h1, one-sentence lede, used-in line), Start here, preview, the collapsed Setup and support panel (`#setup-support`), pager. Personal development review has no Setup and support panel and no "Why I built it" line: its option rows and pack row sit under the preview, then the pager. The header carries no buttons.

- **Start here** (`.start`, card with an 8px left edge in the tool's category color, on phones too): an h2, then one line per assistant in a `.start-list`, each led by a small uppercase label (`.start-k`). Order: Claude app first where its route gives the whole tool and needs no terminal, then Claude Code, then other assistants. A tool with a different route (a text editor, a browser, an API key) names that route in the label instead. A prompt that works with nothing installed sits in the block as a `.codeblock`; a second prompt, such as the Skills reader brief, follows it with a `.start-note` line and its own id.
- **First action:** the first row ends with one primary `a.button` (44px minimum height, same look as the pack pills): the download, or a jump to the install block. A jump link carries `data-tab="app"`, `"code"` or `"other"` so the install tab it names opens first. Three pages keep their primary elsewhere in the block: Skills (the amber Copy prompt button), Project start and Personal development review (the pack row). Text links inside a sentence are exempt from the 44px minimum; every button and standalone control meets it.
- **Editable pack** (`.start-pack`, last row of the Start here card and again below the preview): a secondary pill link "Download editable pack" with a "Copy adaptation prompt" button. The Start here row adds one line, "Use the pack to adapt the tool to your work." plus a sentence that says where the install steps are: "Install steps are under Setup and support." or, on Skills, which shows its Claude Code install block in the Start here row, "Install steps are in Start here and under Setup and support." (no install sentence on Decision record, which has nothing to install); the row below the preview carries no line. Two exceptions: Project start has no pack and offers its GitHub ZIP as the secondary link beside a primary "Copy prompt"; Personal development review's pack holds the starter page itself, so its download is the primary pill.
- **Works with labels** (toolkit index cards, `.badge.need` in a `.needs` row, white with an ink border): "Any chat", "Paid Claude plan", "Claude Code" and, for the page-saving extension only, "An AI API key". The row reads as alternatives, so its badges are joined by a muted "or" and a card carries every label whose route in that page's Start here gives the tool's first result; a route that gives only part of the tool (second-brain's instruction file pasted into a chat) stays out. A label may add a qualifier ("Claude Code to schedule it" on Routines). The filter row uses the same four labels, named "Works with", and shows a card that carries any chosen label.
- **Install tabs:** Claude app, Claude Code and Other, in that order, in one row at every width, each 44px high. "Other" reads "Other assistants" to screen readers. A group with no app route starts with Claude Code. Set `data-default="app"` on a tab group when its app route needs no terminal, and `data-default="code"` when Claude Code should open first. Each Claude Code tab opens with "These commands run in Terminal on macOS or Linux, or Git Bash on Windows."
- **Reader tabs** (`.tabs.reader-tabs`): a prompt that starts subagents carries two tabs in the same block, "Claude app: one chat per reader" first and open by default, then "Claude Code: subagents". The app version is built on the one-chat-per-reader brief and says to paste it once per reader and merge the reports by hand. The labels may wrap to two lines on phones. Cycle steps 2, 4, 5 and 8 and Habits and principles cards 1 and 3 use them.
- **Links into hidden content:** `js/site.js` opens every closed `details` around a link target, on click, on load and on hash change, and selects the tab whose panel holds it. A link with `data-tab` also selects the install tab it names. A tool page's Setup and support panel therefore opens from any Start here link into it.
- **Disclosures** (`details`): every summary is at least 44px high and shows its state with a chevron or a plus. Five styles are in use. Panel: `.artifact-support` and `.options`, a bordered card with a bold summary and a teal chevron on the right. Inline: `details.sources` and `details.terms`, a teal semibold summary with a small chevron. Why line: `.whyline`, a plus or minus marker, one sentence and "Read more". Step card: `details.stepcard` on the nine steps. Example record: `.entry details`, a teal 13px summary inside a preview. `.professional-reading` on Personal is a bordered card with a native marker. Merging them onto the panel and inline styles is open work.

## Sections

- `.sec` blocks with `.sec.alt` alternating backgrounds; 60px vertical padding (44px on phones).
- A section heading is an h2, optionally with an eyebrow above it and one sentence below (`.sec-head`). No markers before headings.

## Components

- **Buttons:** pill-shaped `.btn` (ink outline), `.btn.primary` (teal), `.btn.sm` for secondary controls inside cards.
- **Cards:** white or tinted surface, `--r` corners, an 8px top or left edge in the item's color (`.tile`, `.pj`, `.stepcard`, `.ring-panel`, `.trycard`). Small list cards (people, books, facts) use a 5 to 6px edge. On tool pages the Start here card and the preview card (`.demo`) share the 16px radius and the 8px left edge in the tool's category color, and the made-up example entry inside the preview takes the same color. The Setup and support panel is the one place where sections use 28px of vertical padding instead of 60px.
- **Toolkit index helpers:** `.gloss` is one term-definition paragraph (a closed `details.terms` holds the terms); `.pick-list` and `#at-work` are the "Pick the tool" list and the "Using these at work" section. `.start-note` is a muted note line inside Start here; `.note-list` is a short list of facts under a preview.
- **Chips and badges:** pills with a color dot (`.chip`), small outlined labels (`.badge`).
- **Code and prompts:** dark `.codeblock` with a caption and one amber copy button, 44px high, with a white focus ring on the dark block.
- **Pager:** `.pn` with Previous, All and Next where they exist, at the foot of detail pages, always visible.
- **Footer:** the same dark footer on every page.

## Rules

- Status labels: live, stopped, work in progress. A paused project whose site stays up reads "online, development paused".
- Dates show as Mmm 'YY. Timelines whose entries share a month use D Mmm 'YY; a year alone is fine when only the year is known.
- No em-dashes or spaced en-dashes in copy.
- Light mode only.
- Reduced motion: transitions and animations are off, pseudo-elements included, and smooth scrolling falls back to instant.
- Anchor targets clear the sticky header with `scroll-margin-top` (84px, 96px on phones). Do not add `scroll-padding` on `html`: the two offsets add up.
- Change a token or component here first, then in `style.css`, then on the pages.
