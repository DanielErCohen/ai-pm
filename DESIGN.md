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
- **Why I built it** (tools and projects): one closed line under the lede that opens to three to five bullets.
- **Used in How I work: step N** (tools that serve a step).
- **Actions:** the first is `.btn.primary`, at most two more `.btn`; a lone action is primary. Tool pages keep download and copy in a right column on wide screens. Long case pages may add a row of small jump links (`.btn.sm`).
- **Facts strip (projects, when known):** type and role; status and dates live in the meta line.

## Sections

- `.sec` blocks with `.sec.alt` alternating backgrounds; 60px vertical padding (44px on phones).
- A section heading is an h2, optionally with an eyebrow above it and one sentence below (`.sec-head`). No markers before headings.

## Components

- **Buttons:** pill-shaped `.btn` (ink outline), `.btn.primary` (teal), `.btn.sm` for secondary controls inside cards.
- **Cards:** white or tinted surface, `--r` corners, an 8px top or left edge in the item's color (`.tile`, `.pj`, `.stepcard`, `.ring-panel`, `.trycard`). Small list cards (people, books, facts) use a 5 to 6px edge.
- **Chips and badges:** pills with a color dot (`.chip`), small outlined labels (`.badge`).
- **Code and prompts:** dark `.codeblock` with a caption and one amber copy button.
- **Pager:** `.pn` with Previous, All and Next where they exist, at the foot of detail pages, always visible.
- **Footer:** the same dark footer on every page.

## Rules

- Dates show as Mmm 'YY. Timelines whose entries share a month use D Mmm 'YY; a year alone is fine when only the year is known.
- No em-dashes or spaced en-dashes in copy.
- Light mode only.
- Change a token or component here first, then in `style.css`, then on the pages.
