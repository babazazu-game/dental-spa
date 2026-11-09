import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.join(path.dirname(fileURLToPath(import.meta.url)),'dist');
export async function handler(req,res){
 try{
  let route=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(route==='/dental-spa')route='/';
  if(route.startsWith('/dental-spa/'))route=route.slice('/dental-spa'.length);
  let file=path.resolve(root,'.'+route);
  if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return;}
  let stat=await fs.stat(file);if(stat.isDirectory()){file=path.join(file,'index.html');stat=await fs.stat(file);}
  const data=await fs.readFile(file);
  const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.webp':'image/webp','.svg':'image/svg+xml','.mp4':'video/mp4','.json':'application/json','.bin':'application/octet-stream','.ttf':'font/ttf'}[path.extname(file)]||'application/octet-stream';
  const headers={'Content-Type':mime,'Accept-Ranges':'bytes','Cache-Control':'no-store'};
  const range=/^bytes=(\d+)-(\d*)$/.exec(req.headers.range||'');
  if(range){const start=Number(range[1]),end=range[2]?Math.min(Number(range[2]),data.length-1):data.length-1;if(start> end){res.writeHead(416,{'Content-Range':`bytes */${data.length}`});res.end();return;}res.writeHead(206,{...headers,'Content-Length':end-start+1,'Content-Range':`bytes ${start}-${end}/${data.length}`});res.end(data.subarray(start,end+1));}
  else{res.writeHead(200,{...headers,'Content-Length':data.length});res.end(data);}
 }catch{res.writeHead(404);res.end('Not found');}
}
if(typeof process!=='undefined'&&process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))http.createServer(handler).listen(4173,()=>console.log('http://localhost:4173/dental-spa/ru/'));
