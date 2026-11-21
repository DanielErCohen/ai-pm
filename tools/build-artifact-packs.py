#!/usr/bin/env python3
"""Reproducible editable artifact packs from the sibling public repositories."""
from pathlib import Path
import json
import posixpath
import re
import zipfile
SITE = Path(__file__).resolve().parent.parent
ROOT = SITE.parent
HIW, CV = ROOT / 'how-i-work', ROOT / 'cv-tailor'
SOURCES = {
 'claude-setup': (HIW, ['claude', 'skills/recipient-panel', 'templates/code-repo/CLAUDE.md', 'LICENSE', 'THIRD-PARTY-NOTICES.md']),
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

def localize_links(files, repo):
 """Point relative Markdown links whose target is not in the pack to the file on GitHub."""
 names = set(files)
 def in_pack(path):
  return path in names or any(n.startswith(path + '/') for n in names)
 def fix(m, here):
  target = m[2]
  path, hash_, frag = target.partition('#')
  if not path or re.match(r'[a-z][a-z0-9+.-]*:|//', path, re.I): return m[0]
  full = posixpath.normpath(posixpath.join(posixpath.dirname(here), path))
  if full.startswith('..') or in_pack(full): return m[0]
  return m[1] + f'https://github.com/DanielErCohen/{repo}/blob/main/{full}{hash_}{frag}' + m[3]
 out = {}
 for name, data in files.items():
  if name.endswith('.md'):
   lines, fenced = [], False
   for line in data.decode().split('\n'):
    if line.lstrip().startswith(('```', '~~~')): fenced = not fenced
    elif not fenced:
     code = [m.span() for m in re.finditer(r'`[^`]*`', line)]
     line = re.sub(r'(\[[^\]]*\]\()([^)\s]+)(\))', lambda m: m[0] if any(a <= m.start() < b for a, b in code) else fix(m, name), line)
    lines.append(line)
   data = '\n'.join(lines).encode()
  out[name] = data
 return out

DESCRIPTIONS = {
 'adaptation-prompt.txt': 'the prompt that adapts the tool. Paste it into your assistant.',
 'AGENT-ARTIFACT-GUIDE.md': 'background for an AI agent that turns a tool\'s output into a page like the one on the site. Optional reading.',
 'LICENSE': 'the MIT license for the source files.',
 'THIRD-PARTY-NOTICES.md': 'credits and licenses for third-party material.',
}

def pack_readme(pack, files):
 tops = {}
 for name in files:
  if name == 'README.md': continue
  tops.setdefault(name.split('/')[0], []).append(name)
 first = [n for n in DESCRIPTIONS if n in tops]
 lines = []
 for n in first + sorted(set(tops) - set(first)):
  if n in DESCRIPTIONS: text = DESCRIPTIONS[n]
  elif len(tops[n]) == 1 and tops[n][0] == n: text = 'source file.'
  else: text = f'source folder, {len(tops[n])} file' + ('s' if len(tops[n]) != 1 else '') + '.'
  lines.append(f'- `{n}`: {text}')
 extension = ''
 if pack == 'page-saving-extension':
  extension = '\n`small-builds/page-saving-extension` is the Chrome extension folder. Choose it under "Load unpacked" on the Chrome extensions page.\n'
 return (
  f'# {pack} editable artifact pack\n\n'
  f"This pack holds the editable source files of the {pack} tool and a prompt that adapts them to your work. It installs, schedules, sends and publishes nothing.\n\n"
  '## What is in it\n\n' + '\n'.join(lines) + '\n' + extension + '\n'
  '## What to do\n\n'
  '1. Copy `adaptation-prompt.txt` into your assistant and attach the files your task needs.\n'
  '2. Review the result.\n'
  '3. Keep it in your own private folder.\n\n'
  'Public examples are made up. Keep real personal and company inputs private.\n'
 ).encode()

def pack_files(item):
 root, paths = SOURCES[item['pack']]
 files = checked_files(root, paths)
 files['AGENT-ARTIFACT-GUIDE.md'] = export_guide(root)
 files['adaptation-prompt.txt'] = item['prompt'].encode()
 files = localize_links(files, root.name)
 files['README.md'] = pack_readme(item['pack'], files)
 return files

def main():
 for item in json.loads((SITE/'tools/artifact-manifest.json').read_text()):
  files = pack_files(item)
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
