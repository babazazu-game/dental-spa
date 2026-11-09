import urllib.request, urllib.parse, re, json, html as H
from pathlib import Path
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
base=Path(r'D:\work\Сайты и автоматизация\Dental SPA\site')
class Parser(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.images=[]; self.text=[]; self.skip=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['script','style']: self.skip+=1
  if t=='a': self.links.append(a.get('href',''))
  if t=='img': self.images.append({k:a.get(k,'') for k in ['src','alt']})
 def handle_endtag(self,t):
  if t in ['script','style']: self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  d=d.strip()
  if d and not self.skip:self.text.append(d)
def get(u):return urllib.request.urlopen(u,timeout=30).read()
def page(path):
 try:
  u='https://dentalspa.kz'+path; raw=get(u).decode(); p=Parser();p.feed(raw)
  return {'url':u,'text':p.text,'links':p.links,'images':p.images}
 except Exception as e:return {'url':path,'error':str(e)}
paths=['/','/service/','/specialist/','/about/','/prais/','/reviews/','/news/','/service/diagnostika/','/service/implantacziya/','/service/kosmeticheskaya-stomatologiya/','/service/lechenie-vzroslyh/','/service/orthodontiya/','/service/ustanovka-vinirov/']
pages=list(ThreadPoolExecutor(6).map(page,paths))
extra=sorted(set(u for p in pages for u in p.get('links',[]) if re.match(r'https://dentalspa.kz/(specialist|news)/[^/]+/',u)))[:15]
pages+=list(ThreadPoolExecutor(6).map(page,[urllib.parse.urlparse(u).path for u in extra]))
assets={}; downloads=[]
for p in pages:
 for im in p.get('images',[]):
  u=im['src']
  if '/uploads/' in u and not u.endswith('.svg'):
   name=urllib.parse.unquote(urllib.parse.urlparse(u).path.split('/')[-1]); assets[u]='assets/'+name;downloads.append((u,name))
for name in ['img_0671-1.webp','img_3844_jpg-1.webp','img_0664-1.webp','img_3828_jpg-2-1.webp','1705572789.65a8f9b575827.mp4']:
 u='https://dentalspa.kz/wp-content/uploads/2024/03/'+name;assets[u]='assets/'+name;downloads.append((u,name))
def down(x):
 u,name=x
 try:
  dest=base/'dist/assets'/name
  if not dest.exists():dest.write_bytes(get(u))
  return name,dest.stat().st_size
 except Exception as e:return name,str(e)
results=list(ThreadPoolExecutor(6).map(down,sorted(set(downloads))))
(base/'source-content.json').write_text(json.dumps({'pages':pages,'assets':assets},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':[(p['url'],len(p.get('text',[]))) for p in pages],'downloads':results},ensure_ascii=False))
