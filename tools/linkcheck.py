#!/usr/bin/env python3
"""Internal link checker for the static site: files, #anchors, aria id references, CSS url(), duplicate ids.

Usage: python3 linkcheck.py [site-folder]
The site folder defaults to the folder above this script. Exit code 0 means clean, 1 means a finding.
"""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

SITE = os.path.realpath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SKIP = ('http:', 'https:', 'mailto:', 'tel:', 'data:', 'javascript:', '//')


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []      # (kind, value)
        self.idrefs = []    # (attr, id)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and a.get('name'):
            self.ids.append(a['name'])
        for k in ('href', 'src'):
            if k in a and a[k] is not None:
                self.refs.append((f'{tag}[{k}]', a[k]))
        for k in ('aria-controls', 'aria-labelledby', 'aria-describedby'):
            if k in a and a[k]:
                for i in a[k].split():
                    self.idrefs.append((k, i))


def pages():
    out = []
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
        for f in files:
            if f.endswith('.html'):
                out.append(os.path.join(root, f))
    return sorted(out)


def main():
    parsed = {}
    for p in pages():
        pr = P()
        pr.feed(open(p, encoding='utf-8').read())
        parsed[p] = pr
    broken_files, broken_anchors, broken_idrefs, dup_ids, external_fonts = [], [], [], [], []
    nref = 0
    for p, pr in parsed.items():
        rel = os.path.relpath(p, SITE)
        seen = set()
        for i in pr.ids:
            if i in seen:
                dup_ids.append((rel, i))
            seen.add(i)
        for kind, i in pr.idrefs:
            if i not in seen:
                broken_idrefs.append((rel, kind, i))
        for kind, ref in pr.refs:
            if ref.startswith(SKIP):
                if 'fonts.googleapis.com' in ref or 'fonts.gstatic.com' in ref:
                    external_fonts.append((rel, ref))
                continue
            nref += 1
            u = urlsplit(ref)
            path, frag = unquote(u.path), u.fragment
            if path == '':
                target = p
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(p), path))
                if path.endswith('/'):
                    target = os.path.join(target, 'index.html')
            if not (target.startswith(SITE) and os.path.isfile(target)):
                broken_files.append((rel, kind, ref))
                continue
            if frag and frag != 'top' and target.endswith('.html'):
                if target not in parsed:
                    pr2 = P(); pr2.feed(open(target, encoding='utf-8').read()); parsed[target] = pr2
                if frag not in parsed[target].ids:
                    broken_anchors.append((rel, ref))
    # css url()
    css = open(os.path.join(SITE, 'style.css'), encoding='utf-8').read()
    css_broken = []
    for m in re.finditer(r'url\(["\']?([^)"\']+)["\']?\)', css):
        u = m.group(1)
        if u.startswith(SKIP):
            if 'fonts.g' in u:
                external_fonts.append(('style.css', u))
            continue
        if not os.path.isfile(os.path.join(SITE, u)):
            css_broken.append(u)
    # whole-site third-party font references, any file type
    for root, dirs, files in os.walk(SITE):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if f.endswith(('.html', '.css', '.js')):
                t = open(os.path.join(root, f), encoding='utf-8').read()
                if 'fonts.googleapis.com' in t or 'fonts.gstatic.com' in t:
                    external_fonts.append((os.path.relpath(os.path.join(root, f), SITE), 'font host string'))
    print(f'pages checked: {len(pages())}, internal references checked: {nref}')
    print(f'broken internal links: {len(broken_files)}')
    for x in broken_files: print('  ', x)
    print(f'broken #anchors: {len(broken_anchors)}')
    for x in broken_anchors: print('  ', x)
    print(f'broken aria id references: {len(broken_idrefs)}')
    for x in broken_idrefs: print('  ', x)
    print(f'duplicate ids: {len(dup_ids)}')
    for x in dup_ids: print('  ', x)
    print(f'broken css url(): {len(css_broken)}', css_broken)
    print(f'third-party font references: {len(set(external_fonts))}')
    for x in sorted(set(external_fonts)): print('  ', x)
    bad = len(broken_files) + len(broken_anchors) + len(broken_idrefs) + len(dup_ids) + len(css_broken) + len(set(external_fonts))
    sys.exit(1 if bad else 0)


main()
