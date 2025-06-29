import types
from dataclasses import dataclass


class Cut():
	intro_text = "…Ты раскрываешь детскую книгу и из неё высыпается ворох цветных прямоугольников — с десяток фотографий разлетаются по кровати. Изображения на пластинках статичные, но судя по слабому ЭМИ, какая-то логика в них всё же вшита. Ты машинально делаешь несколько жестов пальцами и джинн сканирует каждый из прямоугольников. Всё чисто. Вздыхаешь, подключаешь мета-данные снимков к своему цифровому слою и тянешься к одному из ярлыков, повисших над фотографиями…"
	interlude_text = "…Ты замечаешь ещё одну фотографию под всеми остальными. Если бы не моргнувший ярлык, ты бы её даже не увидел…"
	outro_text = """…Ты задерживаешь внимание на неулыбчивом лице мужчины. Коротко остриженные, рано поседевшие волосы. Плотно сжатый рот. За взглядом серых глаз — затаённая бессильная ярость. Взгляд отца, который не в силах поставить своего ребёнка на ноги в несправедливом мире, полном технологических чудес.

«Да уж. Подвели мы тебя, а, Серёг?» — ты переводишь взгляд на единственное окно, за которым всё падает и падает снег. В погожий день отсюда — с самой вершины Сквота — наверное, отличный вид на весь Лихой Город.

Потом встряхиваешься, собираешь все фотографии обратно в книгу, даёшь команду джинну отослать все новые данные в офис и продолжаешь обыск. До конца дежурства ещё час, нужно успеть осмотреть остальное помещение…"""


class Shared():
	def __init__(self, seen: int = 0):
		self.seen = seen


class Photo():
	def __init__(self, label: str = "EMPTY_LABEL", description: str = "EMPTY_DESC",	shares: list[Shared] = []):
		self.label = label
		self.description = description
		self.shares = shares
		self.seen = False

	def first_seen(self):
		self.seen = True
		for s in self.shares:
			s.seen += 1
		self.compile_description()

	def compile_description(self):
		pass


cooling_towers = Shared()
boy = Shared()
man = Shared()
arm = Shared()
sack = Shared()
sideway = Shared()
inner_space = Shared()

market = Photo("Рынок")
market.shares = [cooling_towers]


def market_desc(self):
	self.description = f"""Практически идеально выверенная перспектива — главный проход, сжатый уступами прилавков, разрезает пространство рынка, начинаясь от места съёмки и устремляясь в туманный фокус. Зигзаги гирлянд и фонариков расчерчивают небо над проходом, пёстрая толпа покупателей перемешивается с многоцветием товаров.

{"Далеко на фоне поднимаются из тумана колоссы трёх градирен, уже более двадцати лет не работающих. Их серая вертикальная поверхность покрыта жилыми постройками [@click=app.note('squat')]сквоттеров[/], как киль корабля ракушками." if cooling_towers.seen == 1 else "Далеко на фоне поднимаются из тумана всё те же градирни, захваченные [@click=app.note('squat')]сквоттерами[/]."}

В воздухе висит желтоватая дымка [@click=app.note('pollen')]пыльцы[/]. Её разводы покрывают внутреннюю чашу самодельного влагоуловителя, чей блеск в углу — единственное, что нарушает симметрию снимка."""


market.compile_description = types.MethodType(market_desc, market)


mecha = Photo("Ме́ха")
mecha.shares = [cooling_towers, boy]


def mecha_desc(self):
	self.description = f"""Селфи. {"Веснушчатое лицо мальчика лет одиннадцати с копной рыжих волос." if boy.seen == 1 else "Снова рыжий мальчик."} Он щурится на ярком солнце и широко улыбается, возможно, смеётся. Рядом с ним жмурится и показывает язык другой мальчик, его виски выбриты, на скулах — характерные красные полосы от VR-гарнитуры. С другой стороны от оператора — задумчивая девушка в хиджабе держит на руках малолетнего брата. Малыш тянет в объектив свою игрушку — красно-белого пластикового робота-ме́ха без руки.

{"На фоне детей видны колоссы трёх градирен, уже более двадцати лет не работающих. Их серая вертикальная поверхность покрыта жилыми постройками [@click=app.note('squat')]сквоттеров[/], как киль корабля ракушками." if cooling_towers.seen == 1 else "На их фоне — всё те же градирни."}"""


mecha.compile_description = types.MethodType(mecha_desc, mecha)


_67 = Photo("Не более 67%")
_67.description = """Под оранжевым навесом из поликарбоната — террасы лотков с фруктами. Манго, ананасы, бананы, гуава, апельсины, ямс, рамбутан, мангустины, абрикосы, гранаты, киви, личи, инжир, маракуйя, папайя. Солнечный оранжевый свет, пропущенный сквозь навес, преломляется в водяной взвеси, распыляемой невидимыми форсунками. Над душистыми, росяными развалами висит минирадуга.

На ближние к выходу пирамидки орехов брошены несколько мятых листов так, чтобы их было видно от главного прохода. На листах, периодически меняя язык, мигают сообщения:  
«Все фрукты одного производителя! Идентичные естественно выращенным!»
«Содержание генно-модифицированных тканей — не более 67%!»"""

jaipur = Photo("Розовые пантеры Джайпура")
jaipur.shares = [sideway]
def jaipur_desc(self):
	self.description = f"""{"Вид сквозь боковой проход:" if sideway.seen == 1 else "Вид сквозь ещё один боковой проход:"} редкая толпа окружила площадку, на которой группа подростков играет в [@click=app.note('kabaddi')]кабадди[/]. Снимок сделан как раз в тот момент, когда нападающий одной из команд прыгает, чтобы вернуться на свою половину. Его загорелая рука вытянулась к разделительной линии, пытаясь достать её самыми кончиками пальцев. Двое оппонентов повисли у него на ногах, третий тянет за поношенную розовую джерси с логотипом [@click=app.note('jpp')]«Jaipur Pink Panthers»[/].

Предельное напряжение на мокрых от пота лицах, белозубые оскалы, пыльные руки. Глаз не видно — все участники в линзах, через которые ИскИн показывает им состояние игры: счёт, границы площадки, статистику игроков. За отдельную плату — тренерские советы и отключение рекламы. За отдельную договорённость с устроителями — развесовку ставок."""

jaipur.compile_description = types.MethodType(jaipur_desc, jaipur)

red = Photo("Красные платки")
red.shares = [boy, man, arm, inner_space]
def red_desc(self):
	self.description = f"""{"Снимок, снятый внутри уличной закусочной." if inner_space.seen == 1 else "Снова снимок изнутри помещения. На этот раз уличной закусочной."} На переднем плане — белый кафель прилавка, заставленного суповыми чашками, специями, упаковками палочек, соусными бутылками, салфетницами. За прилавком — тесная кухня, в которой быстро и ловко — как танцовщики — работают сутулый старик и его помощница-подросток: тянут лапшу из брикетов мицелия, шинкуют яркие овощи с тиснёнными [@click=app.note('logos')]лого[/], нарезают круглые ломтики из цилиндров искусственной говядины. В другом углу кухни, в клубах пара, робот-манипулятор переливает горячий бульон из кастрюли в кастрюлю. На его верхний сустав повязан красный платок, такой же как у хозяев.

Задняя стенка закусочной — зеркальная, в ней отражается {"веснушчатый рыжий мальчик лет одиннадцати" if boy.seen == 1 else "рыжий мальчик"}, снимающий из-за прилавка на большой антикварный [@click=app.note('polaroid')]Полароид[/], и {"угрюмый" if man.seen == 1 else "тот же"} седой мужчина рядом. {"Вместо правой руки у мужчины — восьмипалый [@click=app.note('prothesis')]протез[/] бывшего военного." if arm.seen == 1 else "Видно, что уже знакомый восьмипалый протез — это правая рука мужчины."} Четыре палочки, зажатые в нём, удерживают сразу полчашки лапши. За их спинами — очередь посетителей и слепящий полуденный зной."""
red.compile_description = types.MethodType(red_desc, red)


dog = Photo("三足狗")
dog.description = """Инженерная [@click=app.note('aic')]«Айка»[/] лежит под прилавком, прячась от зноя. Когда-то в прошлом — боевая единица, полудрон-полусобака. В последствии, после отключения от сети и тактического джинна — только полусобака.

Вместо правой передней лапы — титановая полусфера на тонкой, сложносочленённой конечности. К матово-гладкому титановому черепу прикреплены пара неуклюжих глаз — явный новодел, уступающий изяществу старых военных протезов. Эмпатическая попытка хозяина восстановить зрение отключённому инвалиду. Заодно, может быть, и слух. Но точно не нюх.  
На нагруднике, поверх едва угадываемой эмблемы ЧВК, кто-то нацарапал ехидное [@click=app.note('three')]«三足狗»[/].

Весь этот титан и кремний наверняка ещё числятся где-то на орбитальный серверах, тысячи раз сменившие владельцев и тысячи раз забытые, архивированные с примечанием «Вернуть после окончания службы и/или смерти животного»."""

coffee = Photo("Café hidropônico")
coffee.shares = [arm, sack]
def coffee_desc(self):
	self.description = f"""{"Крупный план старого военного [@click=app.note('prothesis')]протеза[/] с восемью пальцами, которые сжимают" if arm.seen == 1 else "Крупный план: в восьмипалом протезе зажат"} {"полукилограммовый джутовый мешок" if sack.seen == 1 else "джутовый мешок с прошлого снимка"}. Сверху мешок прострочен красной нитью, её концы спаяны круглой печатью с оттиском радиальной [@click=app.note('datamatrix')]датаматрицы[/]. Красными же чернилами на мешок нанесена надпись: [@click=app.note('hydro')]«Café hidropônico de São Paulo»[/].

Сбоку к мешку подвязан пучок коричных палочек, слишком одинаковых, чтобы быть натуральными.

{"На одном из" if arm.seen == 1 else "При таком увеличении на одном из восьми"} титановых пальцев различима кольцевая гравировка: «Спаси и сохрани»."""
coffee.compile_description = types.MethodType(coffee_desc, coffee)


_158 = Photo("Один-пятьдесят восемь")
_158.shares = [sideway]
def _158_desc(self):
	self.description = f"""Снимок {"другого " if sideway.seen > 1 else ""}бокового проулка. В центре — молодой рабочий показывает в камеру жест с оттопыренными большим пальцем и мизинцем. На его плечах — по стокилограммовой бухте кабеля. На лицо надета «маска должника»: несъёмный респиратор с контейнерами нейролептика. Расширенные зрачки спрятаны от полуденного солнца за чёрными линзами. На лбу — широкий кусок пластыря с цифрами [@click=app.note('theft')]«158»[/]. Ремни плохо подогнанного экзоскелета натёрли кожу. Голый тощий торс мокрый от пота, цветастые шорты, сланцы.

За его спиной двое других рабочих в точно таких же масках и экзоскелетах откапывают старую кабельную трассу. Над ними висит микродрон с чёрным зрачком камеры — кто-то удалённо следит за работой.

Ни федеральная, ни муниципальная власть, ни корпоративные суверенитеты не распространяются на территорию Лихого Города, поэтому рабочие, скорее всего, отрабатывают свой долг перед местным синдикатом."""
_158.compile_description = types.MethodType(_158_desc, _158)


pharm = Photo("Фарм-принтер")
pharm.shares = [man, sack, inner_space]
def pharm_desc(self):
	self.description = f"""{"Снимок, снятый внутри тесной аптеки." if inner_space.seen == 1 else "Снова снимок изнутри помещения. На этот раз уличной аптеки."} Прозрачная перегородка отделяет зону покупателей от остального помещения. На переднем плане, за перегородкой — стеклянный куб фарм-принтера. Стробоскопические вспышки в его рабочем объёме — «печатается» заказанное кем-то лекарство: нужные молекулы спекаются из газообразного сырья по инструкциям из лицензионного рецепта.

На ближайшей стенке принтера — большая наклейка с текстом, каждые пару минут сменяющим язык:
• Предупреждение об уголовной ответственности за использование нелицензионных матриц;
• Предупреждение о федеральном законе по защите авторских прав, допускающему вред здоровью нарушителя;
• Реклама тестовых препаратов по низким ценам.

На заднем плане — шкафы, заставленные склянками с надписями [@click=app.note('devanagari')]деванагари[/]. Под ними старик-аптекарь что-то мешает в каменной ступке, не обращая внимания на покупателей.

В правой стороне снимка — {"угрюмый седой мужчина" if man.seen == 1 else "уже знакомый седой мужчина"} изучает рецепт на листе пластика, криво приклеенного с внутренней стороны перегородки. Подмышкой мужчина держит {"джутовый мешок с неразличимой надписью" if sack.seen == 1 else	"мешок с кофе"} и красный [@click=app.note('cig')]сигаретный блок[/]."""
pharm.compile_description = types.MethodType(pharm_desc, pharm)

photo10 = Photo("Папа")
photo10.description = """Групповое фото у входа на Рынок. Все дети собрались для общего снимка. В центре — рыжий мальчик в инвалидной коляске. Улыбается, машет в камеру, держит на коленях подаренного робота-ме́ха. Седой ветеран стоит рядом, положив левую — здоровую — руку мальчику на плечо. Он не улыбается, просто смотрит в камеру. В другой руке у него — белый пакет с покупками.

За их спинами сквот, облепивший градирни, выпускает первых воздушных змеев, чтобы поймать вечерние восходящие потоки.

Пора возвращаться домой."""


class Photos():
	photos: list[Photo] = [
		market,
		mecha,
		_67,
		jaipur,
		red,
		dog,
		coffee,
		_158,
		pharm
	]


@dataclass
class Note():
	name: str = "EMPTY_NAME"
	label: str = "EMPTY LABEL"
	text: str = """EMPTY TEXT"""

squat = Note("squat", "Сквот")
squat.text = """Незаконные постройки на территории бывшей ТЭЦ-21 по адресу: Москва, ул. Ижорская, 9.

ТЭЦ выведена из эксплуатации в 2031 году, с тех пор территория официально заброшена.

С 2036 происходит стихийный самозахват маргинальными элементами, ускоренный послевоенным кризисом.

Основная часть населения — беженцы с Индийского субконтинента и Юго-Восточной Азии.

В прошлом году коллегией ЮИИ по САО г. Москвы принято решение по продаже территории бывшей ТЭЦ в собственность ▒▒▒▒▒▒▒▒▒▒▒▒▒▒ с установлением там корпоративного суверенитета.

Ликвидация незаконного жилья и снос строений запланированы на будущий год."""

pollen = Note("pollen", "Пыльца")
pollen.text = """Пыльца одной из мутаций берёзы пушистой. Появление новых, обильно пылящих, видов — побочный фактор глубокой генной модификации сельскохозяйственных культур на территории Китайской Сибири.

В 2042 году создан межкорпоративный орган для поиска решений по сохранению «старых» видов флоры и купированию распространения новых."""

kabaddi = Note("kabaddi", "Кабадди")
kabaddi.text = """Командная игра с элементами борьбы и салок. Одна из древнейших известных игр, изначально распространённая среди народов Индии.

Повсеместное распространение получила с потоками беженцев, расселившихся по миру.
		
Популярность обусловлена так же отсутствием необходимого спортинвентаря — достаточно ровной прямоугольной площадки."""

jpp = Note("jpp", "Jaipur Pink Panthers")
jpp.text = """Изначально, JPP — команда Профессиональной Лиги Кабадди из Джайпура, штат Раджастхан, Индия.

До закрытия «старой» Лиги — обладательница пяти чемпионских титулов.
		
После воссоздания ПЛК в 2036 году трижды выходила в полуфинал, но титулы не выигрывала.

Характерна агрессивной игрой с упором на силовые и акробатические приёмы. Соотношение физических и конгитивных приращений у игроков: 64/36.

Штаб-квартира расположена в городе Перт, Западная Австралия. Главным спонсором выступает конгломерат «Маккуори-COSCO Юг»."""

logos = Note("logos", "Лого")
logos.text = """«Xianbeilia Agricultural Equipment»

«Bayer CropScience»

«COFCO Россия»"""

polaroid = Note("polaroid", "Полароид")
polaroid.text = """Точно не оригинальный аппарат. Кустарная модификация с заменой и расширением исходного функционала: современной технологией моментальных снимков и прикреплением к ним мета-данных.

Базовой моделью для модификации послужил «Polaróid 636 Closeup»."""

prothesis = Note("prothesis", "Протез")
prothesis.text = """Одна из поздних модификаций изделия ХФ-1312 «Спрут».

В период 30-х годов — стандартное приращение для участников боевых действий, потерявших конечности ниже локтя. Реже — добровольная замена биологических рук.

В исходном варианте: гаптическая обратная связь, стандартные протоколы подключения тактических ИскИнов, десятки вшитых сценариев при автономной работе.

Так как протез используется вне военной сферы, очевидно, установлена кустарная прошивка.

Физический серийный номер сбит, цифровые метки, скорее всего, тоже очищены."""

aic = Note("aic", "Айка")
aic.text = """От «AIC» — «Artificial Intelligence Canine».

Общее название программ модификации собак для применения в боевых действиях.

Животные с физическими и когнитивными приращениями использовались там, где это было более экономически целесообразно, чем применение полностью искусственных агентов с аналогичными возможностями: в разведке, саперных работах, поиске раненых и тому подобном.

Данный экземпляр, судя по приращениям, был частью так называемой «штурмовой стаи» — группы собак, управляемых одним тактическим ИскИном. Такие стаи первыми запускались на позиции противника в условиях плотной городской застройки."""

three = Note("three", "三足狗")
three.text = """«Трёхлапая собака» (кит. упр. 三足狗, пиньинь [i]sān zú gǒu[/])."""

datamatrix = Note("datamatrix", "Датаматрица")
datamatrix.text = """Кофейные зёрна сорта Арабуста46.

Номер патента: CN339981151.

Завод-изготовитель: Агрокластер «Нэй-Мэнгу 11»

Степень обжарки: итальянская.

Масса нетто: 498 г.

Количество зёрен: 2357.

Дата изготовления: 204410240315.

Срок годности: 24 месяца."""

hydro = Note("hydro", "Café hidropônico de São Paulo")
hydro.text = """«Гидропонный кофе из Сан-Паулу» (порт. [i]Café hidropônico de São Paulo[/]).

«Сан-Паулу», в данном случае, не место производства, а торговая марка. Гидропонные технологии позволяют выращивать нужные культуры в любых географиях.

Среднегодовые температуры окружающей среды в мире не позволяют растить кофе большими урожаями. Натурально выращенный кофе относится к продуктам премиум-сегмента."""

theft = Note("theft", "158")
theft.text = """Отсылка к старой редакции УК РФ, статье 158 «Кража».

Территория находится вне федеральной юрисдикции, поэтому данная отсылка — лишь часть внутреннего культурного кода и криминальной традиции локальных преступных группировок."""

devanagari = Note("devanagari", "Деванагари")
devanagari.text = """Слоговая азбука для записи самых распространённых индоарийских языков. В данном случае хинди.

Анализ надписей показывает, что это лекарства традиционной индийской медицины — аюрведы."""

cig = Note("cig", "Сигареты")
cig.text = """Сигареты марки «Двойное счастье» (кит. упр. 喜喜, лигатура 囍, пиньинь [i]shuāngxǐ[/])

Традиционно одна из самых дорогих марок, как правило, используется не для собственного курения, а в качестве подарка. Часто — как взятка."""


class Notes():
	notes: list[Note] = [
		squat,
		pollen,
		kabaddi,
		jpp,
		logos,
		polaroid,
		prothesis,
		aic,
		three,
		datamatrix,
		hydro,
		theft,
		devanagari,
		cig
	]