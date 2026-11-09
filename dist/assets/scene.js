import * as T from './vendor/three.module.js';
const host=document.querySelector('#scene'),fallback=host.querySelector('img');
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
const response=await fetch(new URL('./user-tooth.bin',import.meta.url));if(!response.ok)throw new Error('Model unavailable');const buf=await response.arrayBuffer(),head=new Uint32Array(buf,0,2),geometry=new T.BufferGeometry();geometry.setAttribute('position',new T.BufferAttribute(new Float32Array(buf,8,head[0]*3),3));geometry.setIndex(new T.BufferAttribute(new Uint32Array(buf,8+head[0]*12,head[1]),1));geometry.computeVertexNormals();
const tooth=new T.Mesh(geometry,new T.MeshPhysicalMaterial({color:0xf1e7d6,roughness:.22,metalness:0,clearcoat:.65,clearcoatRoughness:.13,envMapIntensity:1.3}));tooth.rotation.set(.07,-.45,-.13);group.add(tooth);
const gold=new T.MeshStandardMaterial({color:0xc29867,metalness:.65,roughness:.3,emissive:0x6a3b12,emissiveIntensity:.12});
for(let k=0;k<1;k++){const pts=[];for(let i=0;i<=160;i++){const a=i/160*Math.PI*2;pts.push(new T.Vector3(Math.cos(a)*2.15,Math.sin(a)*.76,Math.sin(a)*1.2));}const ribbon=new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts),160,.006,5,false),gold);ribbon.rotation.z=.52;ribbon.rotation.x=.22;group.add(ribbon);}
// Background arch is a separate spatial layer behind the tooth.
const archShape=new T.Shape();archShape.absarc(0,0,3.8,-.4,Math.PI*1.25,false);archShape.absarc(0,0,3.45,Math.PI*1.25,-.4,true);archShape.closePath();
const arch=new T.Mesh(new T.ExtrudeGeometry(archShape,{depth:.20,bevelEnabled:true,bevelSegments:3,steps:1,bevelSize:.025,bevelThickness:.02,curveSegments:96}),new T.MeshStandardMaterial({color:0x8c714e,metalness:.38,roughness:.48}));arch.position.set(.8,-.35,-3.1);arch.rotation.z=-.45;scene.add(arch);
const shadowCanvas=document.createElement('canvas');shadowCanvas.width=128;shadowCanvas.height=128;const sc=shadowCanvas.getContext('2d'),sg=sc.createRadialGradient(64,64,0,64,64,64);sg.addColorStop(0,'rgba(197,147,79,.2)');sg.addColorStop(.4,'rgba(197,147,79,.07)');sg.addColorStop(1,'rgba(197,147,79,0)');sc.fillStyle=sg;sc.fillRect(0,0,128,128);const glow=new T.Mesh(new T.PlaneGeometry(5.2,1.0),new T.MeshBasicMaterial({map:new T.CanvasTexture(shadowCanvas),transparent:true,depthWrite:false}));glow.position.set(0,-2.12,-.1);scene.add(glow);
let targetX=0,targetY=0,visible=true,dirty=true,raf=0;
function resize(){const r=host.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.position.z=camera.aspect<.8?8.5:7.7;camera.updateProjectionMatrix();dirty=true;}new ResizeObserver(resize).observe(host);resize();
host.closest('.hero').addEventListener('pointermove',e=>{if(e.pointerType==='touch')return;const r=host.getBoundingClientRect();targetX=Math.max(-1,Math.min(1,(e.clientX-r.left)/r.width*2-1))*.09;targetY=Math.max(-1,Math.min(1,(e.clientY-r.top)/r.height*2-1))*.045;dirty=true;});
host.closest('.hero').addEventListener('pointerleave',()=>{targetX=targetY=0;dirty=true;});
const clock=new T.Clock();function frame(){raf=requestAnimationFrame(frame);if(document.hidden||!visible)return;const time=clock.getElapsedTime();if(reduced.matches&&!dirty)return;group.rotation.y=reduced.matches?0:Math.sin(time*.16)*.22+targetX;group.rotation.x=reduced.matches?0:targetY;group.position.y=reduced.matches?0:Math.sin(time*.32)*.04;arch.rotation.y=reduced.matches?0:targetX*.2;renderer.render(scene,camera);dirty=false;if(fallback){fallback.style.opacity='0';}}
new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;dirty=true;}).observe(host);reduced.addEventListener('change',()=>{dirty=true;});
renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();cancelAnimationFrame(raf);renderer.domElement.style.display='none';fallback.style.opacity='1';});frame();
