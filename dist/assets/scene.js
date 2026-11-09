import * as T from './vendor/three.module.js';
const host=document.querySelector('#scene'),fallback=host.querySelector('.tooth-placeholder');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let renderer;
try{renderer=new T.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});}catch{throw new Error('Static hero fallback active');}
renderer.setPixelRatio(Math.min(devicePixelRatio,1.6));renderer.setClearColor(0,0);renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.92;
renderer.domElement.setAttribute('aria-hidden','true');host.append(renderer.domElement);
const scene=new T.Scene(),camera=new T.PerspectiveCamera(35,1,.1,80);camera.position.set(0,.1,7.8);
// Procedural softbox environment: no external textures or tracking requests.
const env=document.createElement('canvas');env.width=512;env.height=256;const ctx=env.getContext('2d');ctx.fillStyle='#171512';ctx.fillRect(0,0,512,256);
for(const [x,y,w,h,color] of [[60,25,45,175,'#fff4df'],[280,50,12,155,'#caa16c'],[420,30,60,90,'#fff9ee']]){ctx.fillStyle=color;ctx.fillRect(x,y,w,h);}
const tex=new T.CanvasTexture(env);tex.mapping=T.EquirectangularReflectionMapping;tex.colorSpace=T.SRGBColorSpace;const pmrem=new T.PMREMGenerator(renderer);scene.environment=pmrem.fromEquirectangular(tex).texture;tex.dispose();pmrem.dispose();
scene.add(new T.HemisphereLight(0xfff0da,0x20160c,1.3));
function light(c,i,x,y,z){const l=new T.DirectionalLight(c,i);l.position.set(x,y,z);scene.add(l);}light(0xfff4e2,3,-3,5,5);light(0xe6b36e,4,4,1,-2);light(0xffffff,1,-4,-1,2);
const group=new T.Group();scene.add(group);
const response=await fetch(new URL('./licensed-tooth.bin',import.meta.url));if(!response.ok)throw new Error('Model unavailable');const buf=await response.arrayBuffer(),head=new Uint32Array(buf,0,2),geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.BufferAttribute(new Float32Array(buf,8,head[0]*3),3));geometry.setIndex(new T.BufferAttribute(new Uint32Array(buf,8+head[0]*12,head[1]),1));geometry.computeVertexNormals();
const tooth=new T.Mesh(geometry,new T.MeshPhysicalMaterial({color:0xf1e7d6,roughness:.22,metalness:0,clearcoat:.65,clearcoatRoughness:.13,envMapIntensity:1.3}));tooth.rotation.set(.07,-.45,-.13);group.add(tooth);
const shadowCanvas=document.createElement('canvas');shadowCanvas.width=128;shadowCanvas.height=128;const sc=shadowCanvas.getContext('2d'),sg=sc.createRadialGradient(64,64,0,64,64,64);sg.addColorStop(0,'rgba(197,147,79,.2)');sg.addColorStop(.4,'rgba(197,147,79,.07)');sg.addColorStop(1,'rgba(197,147,79,0)');sc.fillStyle=sg;sc.fillRect(0,0,128,128);const glow=new T.Mesh(new T.PlaneGeometry(5.2,1.0),new T.MeshBasicMaterial({map:new T.CanvasTexture(shadowCanvas),transparent:true,depthWrite:false}));glow.position.set(0,-2.12,-.1);scene.add(glow);
let targetX=0,targetY=0,visible=true,dirty=true,raf=0;
function resize(){const r=host.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.position.z=camera.aspect<.8?8.5:7.7;camera.updateProjectionMatrix();dirty=true;}new ResizeObserver(resize).observe(host);resize();
// Static scene: render only on resize or visibility changes.
function frame(){raf=requestAnimationFrame(frame);if(document.hidden||!visible||!dirty)return;renderer.render(scene,camera);dirty=false;if(fallback)fallback.style.opacity='0';}
new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;dirty=true;}).observe(host);reduced.addEventListener('change',()=>{dirty=true;});
renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(raf);renderer.domElement.style.display='none';if(fallback)fallback.style.opacity='1';});frame();
