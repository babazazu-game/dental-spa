const menu=document.querySelector('#menu');
document.querySelector('#menu-toggle')?.addEventListener('click',e=>{const open=e.currentTarget.getAttribute('aria-expanded')!=='true';e.currentTarget.setAttribute('aria-expanded',String(open));menu.hidden=!open;});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.hidden=true;document.querySelector('#menu-toggle')?.setAttribute('aria-expanded','false');document.querySelector('dialog[open]')?.close();}});
document.querySelectorAll('[data-consult]').forEach(b=>b.addEventListener('click',()=>document.querySelector('#consult').showModal()));
document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
document.querySelector('#consult')?.addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close();});
const search=document.querySelector('#price-search');
search?.addEventListener('input',()=>{const q=search.value.trim().toLocaleLowerCase();let n=0;document.querySelectorAll('[data-price-row]').forEach(r=>{r.hidden=!r.textContent.toLocaleLowerCase().includes(q);if(!r.hidden)n++;});document.querySelector('#price-empty').hidden=n>0;});
const video=document.querySelector('#clinic-video');
const kk=document.documentElement.lang==='kk';
if(video){
 const playButton=document.querySelector('[data-video]'),soundButton=document.querySelector('[data-sound]');
 let userPaused=false,inView=false;
 const load=()=>{if(!video.getAttribute('src'))video.src=video.dataset.src;};
 const status=document.querySelector('.video-status');
 const play=async()=>{load();try{await video.play();status.hidden=true;}catch{playButton.textContent='▶';playButton.setAttribute('aria-label',kk?'Ойнату':'Воспроизвести');}};
 const toggle=()=>{if(video.paused){userPaused=false;play();}else{userPaused=true;video.pause();}};
 video.muted=true;
 video.addEventListener('click',toggle);playButton.addEventListener('click',toggle);
 video.addEventListener('play',()=>{playButton.textContent='Ⅱ';playButton.setAttribute('aria-label',kk?'Үзіліс':'Пауза');});
 video.addEventListener('pause',()=>{playButton.textContent='▶';playButton.setAttribute('aria-label',kk?'Ойнату':'Воспроизвести');});
 video.addEventListener('error',()=>{status.hidden=false;status.textContent=kk?'Бейнені жүктеу мүмкін болмады. Қайталап көріңіз.':'Не удалось загрузить видео. Нажмите воспроизведение ещё раз.';video.removeAttribute('src');});
 soundButton.addEventListener('click',()=>{video.muted=!video.muted;soundButton.textContent=video.muted?(kk?'Дыбыс өшірулі':'Звук выкл.'):(kk?'Дыбыс қосулы':'Звук вкл.');soundButton.setAttribute('aria-pressed',String(!video.muted));soundButton.setAttribute('aria-label',video.muted?(kk?'Дыбысты қосу':'Включить звук'):(kk?'Дыбысты өшіру':'Выключить звук'));});
 new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(inView&&!userPaused&&!document.hidden)play();else if(!inView)video.pause();},{threshold:.35}).observe(video);
 document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else if(inView&&!userPaused)play();});
}
const assistant=document.querySelector('#assistant');
document.querySelectorAll('[data-assistant]').forEach(b=>b.addEventListener('click',()=>assistant.showModal()));
assistant?.addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close();});
const answers=kk?[
 'Клиникада диагностика, терапия, имплантация, ортодонтия, пародонтология және эстетикалық стоматология бағыттары бар. Емдеу жоспарын дәрігер тексеруден кейін анықтайды.',
 'Алғашқы кеңесте дәрігермен сұрақтарыңызды талқылай аласыз. Бар болса, бұрынғы түсірілімдеріңізді алып келіңіз. Қажетті диагностика мен дайындықты әкімші нақтылайды.',
 'Әкімшіге +7 (700) 888-99-88 нөмірі арқылы хабарласыңыз. Ол қызметті және қолжетімді уақытты нақтылайды. Бұл демо қабылдауға жазбайды.'
]:[
 'В клинике представлены диагностика, терапия, имплантация, ортодонтия, пародонтология и эстетическая стоматология. Конкретный план лечения врач составляет после осмотра.',
 'На первой консультации вы сможете обсудить с врачом свои вопросы. Если у вас есть предыдущие снимки, возьмите их с собой. Нужную диагностику и подготовку уточнит администратор.',
 'Позвоните администратору: +7 (700) 888-99-88. Он уточнит услугу и доступное время. Эта демонстрация не создаёт запись на приём.'
];
document.querySelectorAll('[data-topic]').forEach(b=>b.addEventListener('click',()=>{const log=assistant.querySelector('.chat-history');for(const [text,user] of [[b.textContent,true],[answers[Number(b.dataset.topic)],false]]){const p=document.createElement('p');p.className='chat-bubble'+(user?' user':'');p.textContent=text;log.append(p);}log.scrollTop=log.scrollHeight;}));
if(document.querySelector('#scene'))import('./scene.js').catch(()=>{});
