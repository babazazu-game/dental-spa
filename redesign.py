"""Presentation layer for the November Dental Spa redesign."""
def apply(g):
    tr,link,button,photo,head=(g[k] for k in ('tr','link','button','photo','section_head'))
    services,articles=g['SERVICES'],g['articles']
    positions={0:'0% 0%',1:'50% 100%',2:'50% 0%',3:'100% 0%',4:'100% 100%',5:'0% 100%'}
    selected=[articles[i] for i in (0,1,8,11)]
    for i,a in enumerate(selected):a['editorial']=i

    def service_rows(l):
        cards=[]
        for i in (0,2,3,5,1,4):
            s=services[i]
            cards.append(f'<a class="service-tile" href="{link(l,"service/"+s[0])}"><span class="service-art" style="background-position:{positions[i]}" aria-hidden="true"></span><span class="tile-copy"><span class="index">{s[3]} / DENTAL SPA</span><h3>{s[1] if l=="ru" else s[2]}</h3></span><span class="round-arrow">↗</span></a>')
        return '<div class="service-gallery">'+''.join(cards)+'</div>'

    def video(l):
        return f'''<div class="video-block"><video id="clinic-video" playsinline muted loop preload="metadata" poster="/assets/img_0671-1.webp" data-src="/assets/1705572789.65a8f9b575827.mp4" aria-label="{tr('Видео клиники Dental Spa','Dental Spa клиникасының бейнесі',l)}"></video><div class="video-caption"><span>{tr('Почувствуйте атмосферу Dental Spa','Dental Spa атмосферасын сезініңіз',l)}</span><div class="video-controls"><button data-video aria-label="{tr('Воспроизвести','Ойнату',l)}">▶</button><button data-sound aria-label="{tr('Включить звук','Дыбысты қосу',l)}" aria-pressed="false">{tr('Звук выкл.','Дыбыс өшірулі',l)}</button></div></div><p class="video-status" role="status" hidden></p></div>'''

    old_contacts=g['contacts']
    def contacts(l):
        return old_contacts(l)+f'''<div class="map-panel"><iframe title="{tr('Карта: Dental Spa, Актау, 17-й микрорайон, 104','Карта: Dental Spa, Ақтау, 17-шағын аудан, 104',l)}" src="https://yandex.kz/map-widget/v1/?ll=51.158600%2C43.681500&amp;z=15&amp;mode=search&amp;text=Dental%20Spa%20%D0%90%D0%BA%D1%82%D0%B0%D1%83%2017%20104" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe><a class="map-link" href="https://2gis.kz/aktau/firm/70000001061546858" target="_blank" rel="noopener">{tr('Открыть в 2ГИС','2GIS-те ашу',l)} ↗</a></div>'''

    def articles_grid(l,limit=4):
        cards=[]
        for a in selected[:limit]:
            pos=['0% 0%','100% 0%','0% 100%','100% 100%'][a['editorial']]
            cards.append(f'<a class="article-card" href="{link(l,"novosti/"+a["slug"])}"><span class="news-art" style="background-position:{pos}" aria-hidden="true"></span><p class="eyebrow">DENTAL SPA / {tr("ЖУРНАЛ","ЖУРНАЛ",l)}</p><h3>{g["esc"](a["title"] if l=="ru" else a["kk"])}</h3><span class="text-link">{tr("Читать материал","Мақаланы оқу",l)} ↗</span></a>')
        return '<div class="article-grid">'+''.join(cards)+'</div>'

    def assistant(l):
        return f'''<section class="section assistant-section"><div class="assistant-orb" aria-hidden="true"><span>✦</span><small>DENTAL SPA</small></div><div><p class="eyebrow">{tr('ВАШ ПЕРВЫЙ ШАГ','АЛҒАШҚЫ ҚАДАМЫҢЫЗ',l)}</p><h2>{tr('Знакомство начинается<br>с одного вопроса','Танысу бір сұрақтан<br>басталады',l)}</h2><p>{tr('Узнайте о направлениях лечения и подготовьтесь к первому визиту с нашим ИИ-администратором.','ИИ-әкімшімен емдеу бағыттарын біліп, алғашқы келуге дайындалыңыз.',l)}</p><button class="button" data-assistant>{tr('Задать вопрос','Сұрақ қою',l)} <span>↗</span></button><span class="demo-label">{tr('Демонстрация помощника','Көмекшінің демонстрациясы',l)}</span></div></section>'''

    def home(l):
        return f'''<section class="hero"><div class="hero-arch"></div><div class="hero-copy"><p class="eyebrow">DENTAL SPA · {tr('АКТАУ','АҚТАУ',l)}</p><h1>{tr('Искусство заботы<br>о вашей улыбке','Күлкіңізге қамқорлық<br>жасау өнері',l)}</h1><p class="hero-desc">{tr('Современная стоматология.<br>Точность в деталях. Забота о вас.','Заманауи стоматология.<br>Бөлшектердегі дәлдік. Сізге қамқорлық.',l)}</p><div class="hero-actions">{button(l)}<a class="text-link" href="#clinic">{tr('Познакомиться с клиникой','Клиникамен танысу',l)} ↗</a></div><div class="hero-values"><span>01 <b>{tr('Внимание<br>к человеку','Адамға<br>көңіл бөлу',l)}</b></span><span>02 <b>{tr('Цифровая<br>диагностика','Цифрлық<br>диагностика',l)}</b></span><span>03 <b>{tr('Комфорт<br>и забота','Жайлылық<br>және қамқорлық',l)}</b></span></div></div><div id="scene" role="img" aria-label="{tr('Жемчужная 3D-модель зуба','Тістің інжу түсті 3D-моделі',l)}"><span class="tooth-placeholder" aria-hidden="true"></span></div><div class="hero-bottom"><span>DENTAL SPA / {tr('СТОМАТОЛОГИЯ С ЗАБОТОЙ','ҚАМҚОРЛЫҚҚА НЕГІЗДЕЛГЕН СТОМАТОЛОГИЯ',l)}</span><a href="#clinic">{tr('Листайте вниз','Төмен жылжытыңыз',l)} ↓</a></div></section>
        <section class="section light clinic-intro" id="clinic"><div class="clinic-photo">{photo('img_0664-1.webp',tr('Интерьер Dental Spa','Dental Spa интерьері',l))}<span>DENTAL SPA / {tr('ПРОСТРАНСТВО ЗАБОТЫ','ҚАМҚОРЛЫҚ КЕҢІСТІГІ',l)}</span></div><div class="clinic-copy"><p class="eyebrow">01 / {tr('О КЛИНИКЕ','КЛИНИКА ТУРАЛЫ',l)}</p><h2>{tr('Место, где<br>можно <em>выдохнуть.</em>','Өзіңізді жайлы<br><em>сезінетін орын.</em>',l)}</h2><p class="lead">{tr('Внимание к человеку — основа нашей работы. От знакомства до завершения лечения.','Адамға көңіл бөлу — жұмысымыздың негізі. Танысудан бастап емдеу аяқталғанға дейін.',l)}</p><p>{tr('Команда специалистов, собственная лаборатория и центр 3D-визуализации — в одном пространстве.','Мамандар тобы, жеке зертхана және 3D-визуализация орталығы — бір кеңістікте.',l)}</p><a class="text-link" href="{link(l,'o-nas')}">{tr('Подробнее о клинике','Клиника туралы толығырақ',l)} ↗</a></div></section>
        <section class="section light directions" id="directions">{head(l,tr('02 / НАПРАВЛЕНИЯ ЛЕЧЕНИЯ','02 / ЕМДЕУ БАҒЫТТАРЫ',l),tr('Забота о вашей улыбке.<br><em>В каждой детали.</em>','Күлкіңізге қамқорлық.<br><em>Әр бөлшекте.</em>',l),'service',tr('Все услуги','Барлық қызметтер',l))}{service_rows(l)}</section>
        <section class="section atmosphere"><div class="section-head"><div><p class="eyebrow">03 / DENTAL SPA</p><h2>{tr('Увидеть. Почувствовать.<br><em>Довериться.</em>','Көру. Сезіну.<br><em>Сену.</em>',l)}</h2></div><p class="atmosphere-note">{tr('Небольшое знакомство<br>с нашей клиникой','Клиникамызбен<br>қысқаша танысу',l)}</p></div>{video(l)}</section>
        <section class="section light team-section">{head(l,tr('04 / НАША КОМАНДА','04 / БІЗДІҢ КОМАНДА',l),tr('За каждой улыбкой —<br>человек, которому доверяют','Әр күлкінің артында —<br>сенім артқан маман',l),'specialist',tr('Все врачи','Барлық дәрігерлер',l))}{g['doctor_cards'](l,5)}</section>
        <section class="comfort-section"><div class="comfort-copy"><p class="eyebrow">DENTAL SPA / {tr('ФИЛОСОФИЯ ЗАБОТЫ','ҚАМҚОРЛЫҚ ФИЛОСОФИЯСЫ',l)}</p><h2>{tr('Ваша улыбка.<br>Ваше спокойствие.<br><em>Ваш Dental Spa.</em>','Сіздің күлкіңіз.<br>Сіздің тыныштығыңыз.<br><em>Сіздің Dental Spa.</em>',l)}</h2>{button(l)}</div><img src="/assets/comfort-portrait.webp" alt="" loading="lazy" width="1072" height="1448"></section>
        <section class="section light journal-teaser">{head(l,tr('05 / ЖУРНАЛ КЛИНИКИ','05 / КЛИНИКА ЖУРНАЛЫ',l),tr('Перед первым визитом','Алғашқы келуге дейін',l),'novosti',tr('Все материалы','Барлық материалдар',l))}{articles_grid(l,4)}</section>{assistant(l)}<section class="section light">{contacts(l)}</section>'''

    def assistant_dialog(l):
        topics=tr(['Услуги','Первый визит','Как записаться'],['Қызметтер','Алғашқы келу','Қалай жазылуға болады'],l)
        return f'''<dialog id="assistant" class="assistant-dialog"><button class="close" data-close aria-label="{tr('Закрыть','Жабу',l)}">×</button><p class="eyebrow">DENTAL SPA / {tr('ИИ-АДМИНИСТРАТОР','ИИ-ӘКІМШІ',l)}</p><h2>{tr('Начнём со знакомства','Танысудан бастайық',l)}</h2><p class="note">{tr('Демо-режим: готовые ответы о клинике. Запись подтверждает администратор.','Демо-режим: клиника туралы дайын жауаптар. Жазылуды әкімші растайды.',l)}</p><div class="chat-history" role="log" aria-live="polite"><p class="chat-bubble">{tr('Здравствуйте! Помогу познакомиться с Dental Spa. Выберите, что вас интересует.','Сәлеметсіз бе! Dental Spa-мен танысуға көмектесемін. Өзіңізді қызықтыратын тақырыпты таңдаңыз.',l)}</p></div><div class="chat-topics">{''.join(f'<button data-topic="{i}">{label}</button>' for i,label in enumerate(topics))}</div><a class="text-link" href="tel:+77008889988">{tr('Позвонить администратору','Әкімшіге қоңырау шалу',l)} ↗</a></dialog>'''

    original_body=g['body_for']
    def body_for(l,path):
        content,title=original_body(l,path)
        if path=='materials':
            credit='<p>3D: BodyParts3D / Anatomography, © DBCLS. Adapted by OrganUI; selected, recentered, uniformly scaled and styled by Dental Spa concept. <a class="text-link" href="https://creativecommons.org/licenses/by-sa/2.1/jp/">CC BY-SA 2.1 Japan</a>. <a class="text-link" href="/assets/MODEL_ATTRIBUTION.md">Attribution</a></p>'
            content=content.replace('</div>',credit+'</div>',1)
            content=content.replace('3D-модель зуба предоставлена заказчиком.','Исходная модель зуба предоставлена заказчиком. В новой версии используется BodyParts3D.').replace('Тістің 3D-моделін тапсырыс беруші ұсынды.','Бастапқы 3D-модельді тапсырыс беруші ұсынды. Жаңа нұсқада BodyParts3D қолданылған.')
            content=content.replace('</div>','<p>'+tr('Иллюстрации услуг и журнала, портрет в декоративном блоке — сгенерированные изображения. Фотографии врачей и клиники — с сайта клиники.','Қызметтер мен журнал суреттері, сәндік блоктағы портрет — генерацияланған суреттер. Дәрігерлер мен клиника фотолары клиника сайтынан алынған.',l)+'</p></div>',1)
        if path.startswith('novosti/'):
            a=next(a for a in articles if a['slug']==path.split('/')[1])
            if 'editorial' in a:
                import re
                pos=['0% 0%','100% 0%','0% 100%','100% 100%'][a['editorial']]
                content=re.sub(r'<article class="reading"><img[^>]+>',f'<article class="reading"><span class="news-art" style="background-position:{pos};max-width:600px;margin:0 auto 40px" aria-hidden="true"></span>',content,count=1)
        return content,title

    g.update(service_rows=service_rows,video=video,contacts=contacts,articles_grid=articles_grid,home=home,assistant_dialog=assistant_dialog,body_for=body_for)
