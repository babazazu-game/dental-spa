"""Check generated routes, assets, language alternates and deploy subpath."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import os,struct
root=Path(__file__).parent/'dist'
base='/'+os.environ.get('SITE_BASE_PATH','').strip('/') if os.environ.get('SITE_BASE_PATH','').strip('/') else ''
class Page(HTMLParser):
 def __init__(self):super().__init__();self.urls=[];self.h1=0;self.lang=None;self.noindex=False
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if t=='html':self.lang=a.get('lang')
  if t=='meta' and a.get('name')=='robots':self.noindex='noindex' in a.get('content','')
  for k in ['href','src','data-src']:
   if k in a:self.urls.append(a[k])
errors=[];count=0
for f in root.rglob('*.html'):
 p=Page();p.feed(f.read_text(encoding='utf-8'));count+=1
 if not p.noindex:errors.append(f'{f}: noindex missing')
 if f.parent!=root:
  if p.h1!=1:errors.append(f'{f}: expected one h1, got {p.h1}')
  if p.lang not in ['ru','kk']:errors.append(f'{f}: language missing')
 for url in p.urls:
  if not url.startswith('/'):continue
  route=unquote(urlsplit(url).path)
  if base:
   if not route.startswith(base+'/'):errors.append(f'{f}: missing base path: {url}');continue
   route=route[len(base):]
  target=root/route.lstrip('/')
  if not target.is_file() and not (target/'index.html').is_file():errors.append(f'{f}: broken target {url}')
for name in ['user-tooth.bin','licensed-tooth.bin']:
 data=(root/'assets'/name).read_bytes();nv,ni=struct.unpack('<II',data[:8]);assert len(data)==8+nv*12+ni*4
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {count} pages, all internal links and media resolve; languages, noindex and both 3D binaries checked.')
