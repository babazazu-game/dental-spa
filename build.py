from pathlib import Path
import json, html, shutil, zipfile, re, os
from translations import price_kk, CATEGORIES, ARTICLE_KK_TEXT
ROOT=Path(__file__).parent
OUT=ROOT/'dist'; A=OUT/'assets'; A.mkdir(exist_ok=True)
BASE='/'+os.environ.get('SITE_BASE_PATH','').strip('/') if os.environ.get('SITE_BASE_PATH','').strip('/') else ''
for lang in ['ru','kz']:
 for color in ['white','color']:
  origin=ROOT.parent/f'logo_{lang}_{color}.png'
  if origin.exists():shutil.copyfile(origin,A/f'logo-{lang}-{color}.png')
if (ROOT.parent/'Montserrat.zip').exists():
 with zipfile.ZipFile(ROOT.parent/'Montserrat.zip') as z:
  for f in ['Montserrat-Regular.ttf','Montserrat-Medium.ttf','Montserrat-SemiBold.ttf','LICENSE.txt']:
   (A/f).write_bytes(z.read(f))
source=json.loads((ROOT/'source-content.json').read_text(encoding='utf-8'))
pages={p['url']:p for p in source['pages']}
def esc(s):return html.escape(str(s))
def tr(a,b,l):return a if l=='ru' else b
SERVICES=[
 ('diagnostika','Диагностика','Диагностика','01','Цифровая диагностика помогает врачу увидеть полную картину и составить план лечения.','Цифрлық диагностика дәрігерге толық көріністі бағалап, емдеу жоспарын жасауға көмектеседі.','Компьютерная томография · Панорамный снимок · Прицельный снимок · ТРГ','Компьютерлік томография · Панорамалық түсірілім · Нысаналы түсірілім · ТРГ'),
 ('lechenie-vzroslyh','Лечение под микроскопом','Микроскоппен емдеу','02','Увеличение и направленный свет для внимательной работы с тканями зуба и корневыми каналами.','Тіс тіндері мен түбір өзектерін мұқият емдеуге арналған үлкейту және бағытталған жарық.','Лечение кариеса · Эндодонтия · Восстановление зубов','Тісжегіні емдеу · Эндодонтия · Тістерді қалпына келтіру'),
 ('implantacziya','Имплантация','Имплантация','03','Восстановление отсутствующих зубов. Решение о методе и этапах принимает врач после диагностики.','Жоқ тістерді қалпына келтіру. Әдіс пен кезеңдерді дәрігер диагностикадан кейін анықтайды.','Консультация · Планирование · Имплантация · Протезирование','Кеңес алу · Жоспарлау · Имплантация · Протездеу'),
 ('orthodontiya','Ортодонтия','Ортодонтия','04','Исправление прикуса у детей и взрослых с индивидуальным планом ортодонтического лечения.','Балалар мен ересектердің тістемін жеке ортодонтиялық жоспар бойынша түзету.','Брекеты · Пластины · Ортодонтическая диагностика','Брекеттер · Пластиналар · Ортодонтиялық диагностика'),
 ('ustanovka-vinirov','Пародонтология','Пародонтология','05','Диагностика и лечение заболеваний дёсен и тканей, окружающих зуб.','Қызыл иек пен тіс айналасындағы тіндердің ауруларын диагностикалау және емдеу.','Здоровье дёсен · Профессиональная гигиена · Поддерживающий уход','Қызыл иек саулығы · Кәсіби гигиена · Қолдаушы күтім'),
 ('kosmeticheskaya-stomatologiya','Эстетическая стоматология','Эстетикалық стоматология','06','Работа с формой и оттенком зубов: реставрации, виниры и коронки по показаниям.','Тістердің пішіні мен реңкін жақсарту: көрсетілімдер бойынша реставрациялар, винирлер және сауыттар.','Виниры · Коронки · Реставрации','Винирлер · Сауыттар · Реставрациялар')]
DOCTORS=[
 ('omarov-ilmurat-shahmuratovich','Омаров Ильмурат Шахмуратович','Терапевт · Хирург · Ортопед · Имплантолог · Гнатолог','Терапевт · Хирург · Ортопед · Имплантолог · Гнатолог','imagin1-2.webp','2014','Казахстанско-Российский медицинский университет.','Қазақстан-Ресей медицина университеті.'),
 ('aglepes-ajbek-kuanyshbekyly','Аглепес Айбек Куанышбекұлы','Хирург · Терапевт · Ортопед','Хирург · Терапевт · Ортопед','imagin1-5.webp','2021','Казахский национальный медицинский университет имени С. Д. Асфендиярова.','С. Д. Асфендияров атындағы Қазақ ұлттық медицина университеті.'),
 ('abu-bakir-moldir-ergenbaevna','Абу-Бакир Молдир Ергенбаевна','Терапевт · Ортодонт','Терапевт · Ортодонт','imagin1-6.webp','2020','Медицинский университет Астана, 2013–2019.','Астана медицина университеті, 2013–2019.'),
 ('kurmambaev-asylbek-sisenbaevich','Курмамбаев Асылбек Сисенбаевич','Терапевт · Ортодонт','Терапевт · Ортодонт','imagin1-3.webp','2019','Западно-Казахстанский медицинский университет имени Марата Оспанова.','Марат Оспанов атындағы Батыс Қазақстан медицина университеті.'),
 ('zhazbaev-dauit-konajyly','Жазбаев Дәуіт Қонайұлы','Хирург · Терапевт','Хирург · Терапевт','imagin1-4.webp','2022','Казахский национальный медицинский университет имени С. Д. Асфендиярова.','С. Д. Асфендияров атындағы Қазақ ұлттық медицина университеті.')]
NAV=[('service','Услуги','Қызметтер'),('specialist','Врачи','Дәрігерлер'),('o-nas','О клинике','Клиника туралы'),('prais','Цены','Бағалар'),('otzyvy','Отзывы','Пікірлер'),('novosti','Журнал','Журнал'),('contacts','Контакты','Байланыс')]
def link(l,path=''):return '/'+l+'/'+(path.strip('/')+'/' if path else '')
def button(l):return f'<button class="button" data-consult>{tr("Записаться на консультацию","Кеңес алуға жазылу",l)} <span>↗</span></button>'
def photo(name,alt,cls=''):return f'<img class="{cls}" src="/assets/{name}" alt="{esc(alt)}" loading="lazy" width="900" height="1200">'
def logo(l):
 f=f'/assets/logo-{ "ru" if l=="ru" else "kz"}-white.png'
 return f'<a class="brand" href="{link(l)}" aria-label="Dental Spa — {tr("главная","басты бет",l)}"><span class="brand-mark"><img src="{f}" alt="Dental Spa" width="1000" height="716"></span><span class="brand-type" aria-hidden="true"><img src="{f}" alt="" width="1000" height="716"></span></a>'
def doctor_cards(l,limit=5):
 return '<div class="doctor-grid">'+''.join(f'<a class="doctor-card" href="{link(l,"specialist/"+d[0])}"><div class="portrait">{photo(d[4],d[1])}<span class="round-arrow">↗</span></div><h3>{d[1]}</h3><p>{d[2] if l=="ru" else d[3]}</p></a>' for d in DOCTORS[:limit])+'</div>'
def service_rows(l):
 return '<div class="service-list">'+''.join(f'<a href="{link(l,"service/"+s[0])}"><span class="index">{s[3]}</span><h3>{s[1] if l=="ru" else s[2]}</h3><p>{s[4] if l=="ru" else s[5]}</p><span class="arrow">↗</span></a>' for s in SERVICES)+'</div>'
def section_head(l,eyebrow,title,path='',label=''):
 return f'<div class="section-head"><div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div>'+ (f'<a class="text-link" href="{link(l,path)}">{label} ↗</a>' if path else '')+'</div>'
def video(l):return f'<div class="video-block"><video id="clinic-video" playsinline preload="none" poster="/assets/img_0671-1.webp" data-src="/assets/1705572789.65a8f9b575827.mp4" aria-label="Dental Spa"></video><button data-video aria-label="{tr("Смотреть видео о клинике","Клиника туралы бейнені көру",l)}"><span class="play">▶</span><span>{tr("Познакомьтесь с Dental Spa","Dental Spa-мен танысыңыз",l)}</span></button></div>'
def contacts(l):return f'<div class="contact-grid"><div><p class="eyebrow">DENTAL SPA · {tr("АКТАУ","АҚТАУ",l)}</p><h2>{tr("Будем рады<br>познакомиться","Танысқанымызға<br>қуаныштымыз",l)}</h2><a class="big-phone" href="tel:+77008889988">+7 (700) 888-99-88</a><p>{tr("Актау, 17-й микрорайон, 104<br>ЖК «Асыл Парк»","Ақтау, 17-шағын аудан, 104<br>«Асыл Парк» ТК",l)}</p><a class="text-link" href="https://2gis.kz/aktau/firm/70000001061546858" target="_blank" rel="noopener">{tr("Построить маршрут","Бағыт құру",l)} ↗</a></div><div class="contact-panel"><p class="eyebrow">{tr("ЧАСЫ РАБОТЫ","ЖҰМЫС УАҚЫТЫ",l)}</p><p>{tr("Пн–Пт","Дс–Жм",l)} <b>10:00 — 22:00</b></p><p>{tr("Суббота","Сенбі",l)} <b>10:00 — 21:00</b></p><p>{tr("Воскресенье","Жексенбі",l)} <b>{tr("Выходной","Демалыс",l)}</b></p><a href="mailto:info@dentalspa.kz">info@dentalspa.kz</a>{button(l)}</div></div>'
def home(l):
 return f'''<section class="hero"><div class="hero-arch"></div><div class="hero-copy"><p class="eyebrow">DENTAL SPA · {tr('АКТАУ','АҚТАУ',l)}</p><h1>{tr('Искусство заботы<br>о вашей улыбке','Күлкіңізге қамқорлық<br>жасау өнері',l)}</h1><p class="hero-desc">{tr('Точная работа. Внимание к деталям.<br>Забота о вас.','Дәлдік. Әр бөлшекке мән беру.<br>Сізге деген қамқорлық.',l)}</p><div class="hero-actions">{button(l)}<a class="text-link" href="{link(l,'service')}">{tr('Услуги клиники','Клиника қызметтері',l)} ↗</a></div></div><div id="scene" role="img" aria-label="{tr('Объёмная модель зуба','Тістің көлемді моделі',l)}"><img src="/assets/user-tooth-fallback.png" alt="" width="720" height="900" fetchpriority="high"></div><div class="hero-bottom"><a href="tel:+77008889988">+7 (700) 888-99-88</a><span>{tr('Актау, 17-й микрорайон, 104','Ақтау, 17-шағын аудан, 104',l)}</span><a href="#directions">{tr('Листайте вниз','Төмен жылжытыңыз',l)} ↓</a></div></section>
 <section class="section" id="directions">{section_head(l,tr('01 / НАПРАВЛЕНИЯ','01 / БАҒЫТТАР',l),tr('От первого вопроса —<br>к вашей улыбке','Алғашқы сұрақтан —<br>жарқын күлкіге дейін',l),'service',tr('Все услуги','Барлық қызметтер',l))}{service_rows(l)}</section>
 <section class="section light about-teaser"><p class="eyebrow">02 / DENTAL SPA</p><div class="about-columns"><h2>{tr('Лечить.<br>Заботиться.<br><em>Оберегать.</em>','Емдеу.<br>Қамқор болу.<br><em>Аялау.</em>',l)}</h2><div><p class="lead">{tr('Внимание к человеку — основа нашей работы. От диагностики до завершения лечения мы уделяем значение каждой детали.','Адамға көңіл бөлу — жұмысымыздың негізі. Диагностикадан бастап емдеу аяқталғанға дейін әр бөлшекке мән береміз.',l)}</p><p>{tr('В Dental Spa работают терапевты, ортодонты, хирурги и имплантологи. В клинике есть собственная лаборатория и центр 3D-визуализации.','Dental Spa-да терапевтер, ортодонттар, хирургтер және имплантологтер жұмыс істейді. Клиникада жеке зертхана және 3D-визуализация орталығы бар.',l)}</p><a class="text-link" href="{link(l,'o-nas')}">{tr('О клинике','Клиника туралы',l)} ↗</a></div></div>{video(l)}</section>
 <section class="section">{section_head(l,tr('03 / КОМАНДА','03 / КОМАНДА',l),tr('Люди, которым<br>вы доверяете улыбку','Күлкіңізді сеніп<br>тапсыратын мамандар',l),'specialist',tr('Все врачи','Барлық дәрігерлер',l))}{doctor_cards(l,3)}</section>
 <section class="section journal-teaser">{section_head(l,tr('04 / ЖУРНАЛ','04 / ЖУРНАЛ',l),tr('О здоровье —<br>понятным языком','Денсаулық туралы —<br>түсінікті тілмен',l),'novosti',tr('Читать журнал','Журналды оқу',l))}{articles_grid(l,3)}</section><section class="section light">{contacts(l)}</section>'''
ARTICLE_KK=['Тісті жұлғаннан кейін не істеу керек','Тіс имплантациясының кезеңдері','Клиникада тіс имплантациясы қалай жасалады','Имплантациядан кейін ауызды күту','Имплантациядан кейінгі шектеулер','Имплантациядан кейін темекі шегуге бола ма','Имплантациядан кейінгі асқынулар','Имплантациядан кейінгі ісіну','Неліктен тіссіз ұзақ жүруге болмайды','Имплантациядан кейінгі ұсынымдар','Имплантациядан кейінгі тігістер','Тіс ауруының себептері']
articles=[]
for p in source['pages']:
 if '/news/' not in p['url'] or not p.get('text'):continue
 t=p['text'];title=t[19] if len(t)>19 else t[0];slug=p['url'].rstrip('/').split('/')[-1]
 text=[s for s in t[20:] if len(s)>95 and 'cookie' not in s.lower() and 'соглас' not in s.lower()][:4]
 image=next((i['src'].split('/')[-1] for i in p.get('images',[]) if '/uploads/' in i['src'] and not any(w in i['src'] for w in ['168561','svg','imagin'])),'dentist-analyzes-x-ray-photo.webp')
 articles.append({'slug':slug,'title':title,'kk':ARTICLE_KK[len(articles)%len(ARTICLE_KK)],'text':text,'image':image,'url':p['url']})
def articles_grid(l,limit=30):
 return '<div class="article-grid">'+''.join(f'<a class="article-card" href="{link(l,"novosti/"+a["slug"])}">{photo(a["image"],a["title"] if l=="ru" else a["kk"])}<p class="eyebrow">DENTAL SPA / {tr("ЖУРНАЛ","ЖУРНАЛ",l)}</p><h3>{esc(a["title"] if l=="ru" else a["kk"])} ↗</h3></a>' for a in articles[:limit])+'</div>'
def inner(l,title,content,sub=''):
 return f'<section class="page-title section"><a class="breadcrumb" href="{link(l)}">{tr("Главная","Басты бет",l)} / DENTAL SPA</a><h1>{title}</h1>{"<p class=lead>"+sub+"</p>" if sub else ""}</section><section class="section page-content">{content}</section>'
def pricing(l):
 t=pages.get('https://dentalspa.kz/prais/',{}).get('text',[]);rows=[]
 for i,s in enumerate(t):
  if re.fullmatch(r'[\d\s,.]+₸',s) and i>=2 and t[i-2] not in ['Аванс имплантация','Возврат неиспользованных средств','Носки белые для персонала']:rows.append((t[i-2],t[i-1],s))
 data='<div class="price-tools"><label for="price-search">'+tr('Поиск по прайсу','Прайс бойынша іздеу',l)+'</label><input id="price-search" type="search" placeholder="'+tr('Например, консультация','Мысалы, консультация',l)+'"></div>'
 data+='<p class="note">'+tr('Прайс перенесён с dentalspa.kz. Актуальность стоимости и состав лечения уточняйте в клинике.','Прайс dentalspa.kz сайтынан алынды. Бағалар мен емдеу құрамын клиникадан нақтылаңыз.',l)+'</p>'
 data+='<div class="price-scroll"><table><thead><tr><th>'+tr('Услуга','Қызмет',l)+'</th><th>'+tr('Направление','Бағыт',l)+'</th><th>'+tr('Цена','Бағасы',l)+'</th></tr></thead><tbody>'+''.join(f'<tr data-price-row><td>{esc(a if l=="ru" else price_kk(a))}</td><td>{esc(b if l=="ru" else CATEGORIES.get(b,b))}</td><td>{esc(c)}</td></tr>' for a,b,c in rows)+'</tbody></table></div><p id="price-empty" hidden>'+tr('Ничего не найдено','Ештеңе табылмады',l)+'</p>'
 return data
def body_for(l,path):
 if not path:return home(l),tr('Искусство заботы о вашей улыбке','Күлкіңізге қамқорлық жасау өнері',l)
 title=next((tr(a,b,l) for p,a,b in NAV if p==path),None)
 if path=='service':return inner(l,title,service_rows(l)),title
 if path.startswith('service/'):
  s=next(s for s in SERVICES if s[0]==path.split('/')[1]);title=s[1] if l=='ru' else s[2]
  items=s[6 if l=='ru' else 7].split(' · ')
  c=f'<div class="detail-grid"><div><p class="eyebrow">DENTAL SPA / {s[3]}</p><h2>{tr("Внимание к каждой детали","Әр бөлшекке мән береміз",l)}</h2><p class="lead">{s[4] if l=="ru" else s[5]}</p><ul class="feature-list">'+''.join('<li>'+i+'</li>' for i in items)+f'</ul>{button(l)}<p class="note">{tr("План лечения и стоимость определяются после осмотра и диагностики.","Емдеу жоспары мен құны тексеру және диагностикадан кейін анықталады.",l)}</p></div><div class="detail-art">{photo("img_0671-1.webp",tr("Диагностика в Dental Spa","Dental Spa-дағы диагностика",l))}</div></div><div class="steps">'+''.join(f'<div><span>0{i+1}</span><h3>{v}</h3></div>' for i,v in enumerate(tr(['Знакомство и осмотр','Диагностика и план','Лечение и рекомендации'],['Танысу және тексеру','Диагностика және жоспар','Емдеу және ұсынымдар'],l)))+'</div>'
  return inner(l,title,c),title
 if path=='specialist':return inner(l,title,doctor_cards(l)),title
 if path.startswith('specialist/'):
  d=next(d for d in DOCTORS if d[0]==path.split('/')[1]);title=d[1]
  c=f'<div class="profile-grid">{photo(d[4],d[1])}<div><p class="eyebrow">DENTAL SPA</p><h2>{d[2] if l=="ru" else d[3]}</h2><p class="lead">{tr("Практика с ","Тәжірибесі ",l)}{d[5]}{tr(" года"," жылдан",l)}</p><h3>{tr("Образование","Білімі",l)}</h3><p>{d[6] if l=="ru" else d[7]}</p>{button(l)}<p class="note">{tr("Данные профиля — с сайта клиники. Доступное время уточняет администратор.","Профиль деректері клиника сайтынан алынды. Қолжетімді уақытты әкімші нақтылайды.",l)}</p></div></div>'
  return inner(l,title,c),title
 if path=='o-nas':
  c=f'<div class="about-columns"><h2>{tr("Лечить.<br>Заботиться.<br><em>Оберегать.</em>","Емдеу.<br>Қамқор болу.<br><em>Аялау.</em>",l)}</h2><div><p class="lead">{tr("Наши принципы разделяет каждый специалист Dental Spa. Мы уделяем особенное внимание подготовке врачей и заботе о пациентах.","Dental Spa қағидаларын әр маман ұстанады. Дәрігерлерді даярлауға және пациенттерге қамқорлық көрсетуге ерекше мән береміз.",l)}</p><p>{tr("Собственная лаборатория, центр 3D-визуализации и команда специалистов разных направлений помогают выстраивать комплексный подход к лечению.","Жеке зертхана, 3D-визуализация орталығы және әртүрлі бағыттағы мамандар емдеуге кешенді тәсіл қолдануға көмектеседі.",l)}</p></div></div>{video(l)}<a class="text-link" href="https://kuula.co/share/collection/7MmzF" target="_blank" rel="noopener">{tr("Виртуальный тур по клинике","Клиникаға виртуалды саяхат",l)} ↗</a>'
  return inner(l,title,c),title
 if path=='prais':return inner(l,title,pricing(l)),title
 if path=='contacts':return inner(l,title,contacts(l)),title
 if path=='otzyvy':
  c=f'<h2>{tr("Ваш опыт важен","Сіздің тәжірибеңіз маңызды",l)}</h2><p class="lead narrow">{tr("Отзывы пациентов помогают познакомиться с клиникой до первого визита. Посмотрите актуальные оценки и впечатления на независимых площадках.","Пациенттердің пікірлері алғашқы келуге дейін клиникамен танысуға көмектеседі. Өзекті бағалар мен әсерлерді тәуелсіз платформалардан оқыңыз.",l)}</p><div class="review-links"><a href="https://2gis.kz/aktau/firm/70000001061546858" target="_blank" rel="noopener">2ГИС <span>↗</span></a><a href="https://yandex.kz/maps/org/dental_spa/87506491974/" target="_blank" rel="noopener">{tr("Яндекс Карты","Яндекс Карталар",l)} <span>↗</span></a></div>'
  return inner(l,title,c),title
 if path=='novosti':return inner(l,title,articles_grid(l)),title
 if path.startswith('novosti/'):
  a=next(a for a in articles if a['slug']==path.split('/')[1]);title=a['title'] if l=='ru' else a['kk']
  text=''.join('<p>'+esc(s)+'</p>' for s in a['text']) if l=='ru' else '<p>'+ARTICLE_KK_TEXT[articles.index(a)]+'</p>'
  c=f'<article class="reading">{photo(a["image"],title)}{text}<p class="note">{tr("Информация носит ознакомительный характер и не заменяет консультацию специалиста.","Ақпарат танысу мақсатында берілген және маман кеңесін алмастырмайды.",l)}</p><a class="text-link" href="{a["url"]}" target="_blank" rel="noopener">{tr("Полная статья на сайте клиники","Толық мақала клиника сайтында",l)} ↗</a></article>'
  return inner(l,title,c),title
 if path=='materials':
  title=tr('Материалы и лицензии','Материалдар мен лицензиялар',l)
  return inner(l,title,'<div class="reading"><p>'+tr('3D-модель зуба предоставлена заказчиком. Фото, видео, сведения о врачах, услугах и прайс — dentalspa.kz. Демонстрационная концепция, не официальный сайт клиники.','Тістің 3D-моделін тапсырыс беруші ұсынды. Фото, бейне, дәрігерлер, қызметтер және прайс туралы деректер — dentalspa.kz. Бұл клиниканың ресми сайты емес, демонстрациялық тұжырымдама.',l)+'</p><p>Three.js — MIT. Montserrat — SIL Open Font License.</p></div>'),title
 raise ValueError(path)
import runpy
if (ROOT/'reference-models/bodyparts-teeth.glb').exists():
 runpy.run_path(str(ROOT/'prepare_licensed_model.py'))
else:
 assert (A/'licensed-tooth.bin').exists() and (A/'MODEL_ATTRIBUTION.md').exists(), 'Licensed tooth asset missing'
from redesign import apply
apply(globals())
routes=['']+[n[0] for n in NAV]+['service/'+s[0] for s in SERVICES]+['specialist/'+d[0] for d in DOCTORS]+['novosti/'+a['slug'] for a in articles]+['materials']
for l in ['ru','kk']:
 for path in routes:
  content,title=body_for(l,path);other='kk' if l=='ru' else 'ru'
  nav=''.join(f'<a {"aria-current=page" if path==p else ""} href="{link(l,p)}">{tr(a,b,l)}</a>' for p,a,b in NAV)
  full=f'''<!doctype html><html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{esc(title)} · Dental Spa</title><meta name="description" content="{tr('Демонстрационная концепция Dental Spa в Актау. Услуги, врачи, цены и контакты.','Ақтаудағы Dental Spa демонстрациялық тұжырымдамасы. Қызметтер, дәрігерлер, бағалар және байланыс.',l)}"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/assets/style.css"><link rel="alternate" hreflang="{other}" href="{link(other,path)}"></head><body class="{ 'is-home' if not path else 'is-inner'}"><a class="skip-link" href="#main">{tr('К содержимому','Мазмұнға өту',l)}</a><header>{logo(l)}<nav class="desktop-nav" aria-label="{tr('Основная навигация','Негізгі навигация',l)}">{nav}</nav><div class="header-end"><a class="language" href="{link(other,path)}" aria-label="{tr('Қазақша нұсқа','Русская версия',l)}">{'RU <span>/ ҚАЗ</span>' if l=='ru' else 'ҚАЗ <span>/ RU</span>'}</a><button id="menu-toggle" aria-label="{tr('Меню','Мәзір',l)}" aria-expanded="false" aria-controls="menu"><span></span><span></span></button></div><nav id="menu" hidden>{nav}</nav></header><main id="main">{content}</main><footer><div>{logo(l)}<p>{tr('Демонстрационная дизайн-концепция.<br>Не официальный сайт клиники.','Демонстрациялық дизайн тұжырымдамасы.<br>Клиниканың ресми сайты емес.',l)}</p></div><nav>{nav}</nav><div><a href="tel:+77008889988">+7 (700) 888-99-88</a><a href="mailto:info@dentalspa.kz">info@dentalspa.kz</a><a class="fine" href="{link(l,'materials')}">{tr('Материалы и лицензии','Материалдар мен лицензиялар',l)}</a></div><p class="medical">{tr('Имеются противопоказания. Проконсультируйтесь со специалистом.','Қарсы көрсетілімдер бар. Маманмен кеңесіңіз.',l)}</p></footer><dialog id="consult"><button class="close" data-close aria-label="{tr('Закрыть','Жабу',l)}">×</button><p class="eyebrow">DENTAL SPA</p><h2>{tr('Начните<br>с консультации','Кеңес алудан<br>бастаңыз',l)}</h2><p>{tr('Это демонстрация сайта. Для реальной записи свяжитесь с администратором клиники.','Бұл сайттың демонстрациясы. Нақты жазылу үшін клиника әкімшісімен байланысыңыз.',l)}</p><a class="button" href="tel:+77008889988">+7 (700) 888-99-88 ↗</a><p class="note">{tr('Администратор уточнит услугу и подтвердит время приёма.','Әкімші қызметті нақтылап, қабылдау уақытын растайды.',l)}</p></dialog><script type="module" src="/assets/app.js"></script></body></html>'''
  full=full.replace('</head>','<link rel="stylesheet" href="/assets/redesign.css"></head>')
  full=full.replace('</body>',assistant_dialog(l)+'</body>')
  full=re.sub(r'(?<![\w-])(href|src|data-src)="/',lambda m:m[1]+'="'+BASE+'/',full)
  dest=OUT/l/path;dest.mkdir(parents=True,exist_ok=True);(dest/'index.html').write_text(full,encoding='utf-8')
(OUT/'index.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url=/ru/"><title>Dental Spa</title><a href="/ru/">Dental Spa · Русский</a> · <a href="/kk/">Қазақша</a></html>',encoding='utf-8')
entry=(OUT/'index.html').read_text(encoding='utf-8').replace('url=/','url='+BASE+'/').replace('href="/','href="'+BASE+'/');(OUT/'index.html').write_text(entry,encoding='utf-8')
(OUT/'.nojekyll').write_text('')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#17191b"/><text x="12" y="44" fill="#c29867" font-family="serif" font-size="36">D</text></svg>')
print(f'Built {len(routes)*2+1} static pages in RU / KK')
