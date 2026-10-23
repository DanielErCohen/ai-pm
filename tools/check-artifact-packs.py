#!/usr/bin/env python3
"""Check packaged sources, page prompts, samples and JavaScript syntax."""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util,json,re,subprocess,tempfile,zipfile
SITE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('builder',SITE/'tools/build-artifact-packs.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.prompt=False;self.text='';self.downloads=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='textarea' and 'prompt' in a.get('class','').split():self.prompt=True
  if tag=='a' and 'download-pack' in a.get('class','').split():self.downloads.append(a['href'])
 def handle_endtag(self,tag):
  if tag=='textarea':self.prompt=False
 def handle_data(self,text):
  if self.prompt:self.text+=text

def check_zip(path,top,expected):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None, path.name
  assert len(z.namelist())==len(set(z.namelist())),path.name
  actual={n.removeprefix(top+'/'):z.read(n) for n in z.namelist()}
  assert all(n.startswith(top+'/') and '..' not in Path(n).parts for n in z.namelist())
  for name,data in expected.items():assert actual[name]==data,(path.name,name)
  return len(actual)

def main():
 files=0
 for item in json.loads((SITE/'tools/artifact-manifest.json').read_text()):
  root,paths=b.SOURCES[item['pack']]
  expected=b.checked_files(root,paths)
  expected['AGENT-ARTIFACT-GUIDE.md']=b.export_guide(root)
  expected['adaptation-prompt.txt']=item['prompt'].encode()
  path=SITE/'downloads'/f"{item['pack']}-artifact-pack.zip"
  files+=check_zip(path,item['pack'],expected)
  page=Page();page.feed((SITE/'toolkit'/f"{item['page']}.html").read_text())
  assert page.text==item['prompt'],item['page']
  assert page.downloads==[f'../downloads/{path.name}']*2,item['page']
 starter=b.HIW/'artifacts/development-review'
 expected=b.checked_files(starter,['starter.html','blank-data.json','sample-data.json','schema.json','adaptation-prompt.txt','validation-checklist.md','README.md','AGENTS.md','LICENSE','OFL.txt'])
 files+=check_zip(SITE/'downloads/development-starter-v1.zip','development-starter',expected)
 page=Page();page.feed((SITE/'toolkit/development-review.html').read_text())
 assert page.text==(starter/'adaptation-prompt.txt').read_text().rstrip('\n')
 assert page.downloads==['../downloads/development-starter-v1.zip']*2
 js=(SITE/'js/development-review.js').read_text()
 sample=json.loads(re.search(r'const SAMPLE=(.*?), EMPTY=',js)[1])
 assert sample==json.loads((starter/'sample-data.json').read_text())
 scripts=[p.read_text() for p in (SITE/'js').glob('*.js')]
 embedded=re.findall(r'<script[^>]*>(.*?)</script>',(starter/'starter.html').read_text(),re.S)
 scripts+=embedded
 for code in scripts:
  with tempfile.NamedTemporaryFile('w',suffix='.js') as f:
   f.write(code);f.flush();subprocess.run(['node','--check',f.name],check=True,capture_output=True)
 # Exercise the starter's actual pure validator, without a browser or file-picker action.
 validation=re.search(r'function validate\(x\).*?\n',(starter/'starter.html').read_text())[0]
 code='const assert=require("node:assert/strict");const labels={last_week:1,assessment:1,roadmap:1,achievements:1};\n'+validation
 code+='\nconst blank='+ (starter/'blank-data.json').read_text()+';const sample='+ (starter/'sample-data.json').read_text()+';\n'
 code+='validate(blank);validate(sample);let bad=structuredClone(sample);bad.extra=true;assert.throws(()=>validate(bad));bad=structuredClone(sample);bad.last_week[0].detail=1;assert.throws(()=>validate(bad));bad=structuredClone(sample);bad.period="x".repeat(201);assert.throws(()=>validate(bad));bad=structuredClone(sample);bad.last_week=Array(31).fill(bad.last_week[0]);assert.throws(()=>validate(bad));bad=structuredClone(sample);bad.last_week[0].limit="x".repeat(2001);assert.throws(()=>validate(bad));assert.throws(()=>validate(null));'
 subprocess.run(['node','-e',code],check=True,capture_output=True)
 print(f'PASS: nine packs, {files} members, nine page/pack prompts, two downloads per page, embedded sample parity, {len(scripts)} JavaScript syntax checks, eight validator cases.')
if __name__=='__main__':main()
