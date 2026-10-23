#!/usr/bin/env python3
"""Reproducible artifact source packs from the sibling public repositories."""
from pathlib import Path
import json
import re
import zipfile
SITE = Path(__file__).resolve().parent.parent
ROOT = SITE.parent
HIW, CV = ROOT / 'how-i-work', ROOT / 'cv-tailor'
SOURCES = {
 'claude-setup': (HIW, ['claude', 'LICENSE', 'THIRD-PARTY-NOTICES.md']),
 'skills': (HIW, ['skills', 'artifacts/examples/product-sparring.md', 'LICENSE', 'THIRD-PARTY-NOTICES.md']),
 'second-brain': (HIW, ['second-brain', 'artifacts/examples/memory-note.md', 'LICENSE']),
 'routines': (HIW, ['routines', 'LICENSE']),
 'meeting-review': (HIW, ['meeting-review', 'LICENSE']),
 'cv-tailor': (CV, ['my-cv', 'applications/_template', 'examples', 'skills', 'guides', 'CLAUDE.md', 'LICENSE']),
 'page-saving-extension': (HIW, ['small-builds/page-saving-extension', 'artifacts/examples/saved-page.md', 'LICENSE', 'THIRD-PARTY-NOTICES.md']),
 'decision-record': (HIW, ['templates/decision-record.md', 'templates/decision-example.md', 'templates/problem-outline.md', 'LICENSE']),
}
def checked_files(root, paths):
 files = {}
 for name in paths:
  path = root / name
  if not path.exists(): raise SystemExit(f'Missing public source: {path}')
  for item in sorted(path.rglob('*')) if path.is_dir() else [path]:
   if item.is_symlink(): raise SystemExit(f'Symlink is not a public source file: {item}')
   if item.is_file():
    rel = item.relative_to(root)
    if '.git' in rel.parts or item.name == '.DS_Store' or '.local.' in item.name:
     raise SystemExit(f'Unexpected private or generated source: {rel}')
    files[str(rel)] = item.read_bytes()
 return files

def archive(path, top, files):
 with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
  for name, content in sorted(files.items()):
   info = zipfile.ZipInfo(f'{top}/{name}', date_time=(2026, 10, 23, 0, 0, 0))
   info.compress_type = zipfile.ZIP_DEFLATED
   info.external_attr = 0o100644 << 16
   z.writestr(info, content)

def export_guide(root):
 text = (root/'ARTIFACTS.md').read_text()
 repo = root.name
 return re.sub(r'(\[[^\]]*\]\()((?!https?://|#)[^)]+)(\))', lambda m: m[1] + f'https://github.com/DanielErCohen/{repo}/blob/main/' + m[2] + m[3], text).encode()

def main():
 for item in json.loads((SITE/'tools/artifact-manifest.json').read_text()):
  root, paths = SOURCES[item['pack']]
  files = checked_files(root, paths)
  files['AGENT-ARTIFACT-GUIDE.md'] = export_guide(root)
  files['adaptation-prompt.txt'] = item['prompt'].encode()
  files['README.md'] = (
   f"# {item['pack']} artifact source pack\n\n"
   "1. Read AGENT-ARTIFACT-GUIDE.md, then the matching source README or SKILL.md. Guide links point to the canonical public source.\n"
   "2. Copy adaptation-prompt.txt into your assistant and attach only the files needed for your task. Replace the bracketed context.\n"
   "3. Review the result and save it in your own private folder.\n\n"
   "This is a source pack, separate from an installable skill ZIP. It does not install, schedule, send or publish anything. Public examples are synthetic; configuration and layout excerpts are labeled separately. Keep real personal and company inputs private.\n"
  ).encode()
  archive(SITE/'downloads'/f"{item['pack']}-artifact-pack.zip", item['pack'], files)
  print(f"{item['pack']}: {len(files)} files")
 starter = HIW/'artifacts/development-review'
 files = checked_files(starter, ['starter.html','blank-data.json','sample-data.json','schema.json','adaptation-prompt.txt','validation-checklist.md','README.md','AGENTS.md','LICENSE','OFL.txt'])
 archive(SITE/'downloads/development-starter-v1.zip', 'development-starter', files)
 (SITE/'downloads/development-review-prompt.txt').write_bytes((starter/'adaptation-prompt.txt').read_bytes())
 for name in ['decision-record.md','decision-example.md','problem-outline.md']:
  (SITE/'downloads'/name).write_bytes((HIW/'templates'/name).read_bytes())
 print(f'development-review: {len(files)} files')
if __name__ == '__main__': main()
