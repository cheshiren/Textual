import random

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Grid, Container, Center
from textual.content import Content
from textual.message import Message
from textual.screen import Screen, ModalScreen
from textual.theme import Theme
from textual.widgets import Button, Header, Placeholder, Static, Label

from texts import Cut, Photos, Photo, Notes, Note, photo10

TITLE = "Поход за покупками в Лихой Город"
AUTHOR = "Вячеслав Добранов"

reckless_theme = Theme(
	name="reckless",
	primary="#0D2B45",
	secondary="#8D697A",
	accent="#D08159",
	foreground="#203C56",
	background="#FFECD6",
	success="#A3BE8C",
	warning="#EBCB8B",
	error="#BF616A",
	surface="#FFD4A3",
	panel="#FFD4A3",
	dark=True,
	variables={
		"block-cursor-text-style": "none",
		"footer-key-foreground": "#0D2B45",
		# "input-selection-background": "#81a1c1 35%",
	},
)


class PhotoButton(Button):
	
	def action_press(self):
		self.add_class("seen")

	async def on_click(self) -> None:
		await self.run_action("press()")


class UnfocusedScreen(Screen):

	def on_show(self, event):
		self.set_focus(None)


class StartScreen(UnfocusedScreen):
	def on_mount(self):
		self.title = ""
	def compose(self):
		yield Header(classes="-tall", icon="•••")
		with Vertical(id="column-start-screen"):
			yield Label(TITLE.upper(), id="title-start-screen")
			yield Label(AUTHOR, id="author-start-screen")
			yield Button("Начать игру", classes="blur")
		# yield Footer()

	class StartPressed(Message):
		pass

	def on_button_pressed(self, event: Button.Pressed):
		event.stop()
		self.post_message(self.StartPressed())


class CutScreen(UnfocusedScreen):

	def __init__(self, name=None, id=None, classes=None, text: str = "CUTSCENE", next_screen: str = "start_screen"):
		super().__init__(name, id, classes)
		self.text = text
		self.next_screen = next_screen

	def compose(self):
		yield Header(classes="-tall", icon="•••")
		with Vertical():
			yield Static(self.text)
			yield Center(Button("››"))

	class NextPressed(Message):
		def __init__(self, next_screen: str):
			super().__init__()
			self.next_screen = next_screen

	def on_button_pressed(self, event: Button.Pressed):
		event.stop()
		self.post_message(self.NextPressed(self.next_screen))


class PhotosScreen(UnfocusedScreen):

	def __init__(self, name=None, id=None, classes=None, photos: list[Photo] = []):
		super().__init__(name, id, classes)
		self.photos = photos

	def compose(self) -> ComposeResult:
		yield Header(classes="-tall", icon="•••")
		with Vertical(id="photo_column"):
			# yield Static("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя")
			with Grid(id="photo_panel"):
				for i in range(len(self.photos)):
					yield PhotoButton(self.photos[i].label, id=f"photo{i+1}", classes="photobutton")
			yield Center(Button("››", id="continue", classes="hidden"))

	def on_mouse_move(self) -> None:
		# print(event.offset)
		self.query("Button").blur()

	def on_screen_resume(self):
		# Если все фотокнопки были нажаты - убираем скрытый класс с кнопки Дальше
		if len(self.query("PhotoButton.seen")) == len(self.photos):
			self.query_one("#continue").remove_class("hidden")
	
	class PhotoPressed(Message):
		def __init__(self, button_id: str|None):
			super().__init__()
			self.button_id = button_id

	def action_lets_see_the_photo(self, event: PhotoButton.Pressed):
		button_id = event.button.id
		self.post_message(self.PhotoPressed(button_id))

	@on(PhotoButton.Pressed, ".photobutton")
	def lets_see_the_photo(self, event: PhotoButton.Pressed):
		self.action_lets_see_the_photo(event)
	
	class ContinuePressed(Message):
		pass

	@on(Button.Pressed, "#continue")
	def goto_interlude(self):
		self.post_message(self.ContinuePressed())
	
	def key_enter(self):
		try:
			button = self.query_one("#continue")
			if button.style.display != 'none':
				self.post_message(self.ContinuePressed())
		except:
			pass
		try:
			button = self.query("PhotoButton:focus, PhotoButton:hover")[0]
			self.action_lets_see_the_photo(Button.Pressed(button))
		except: pass


class PhotoScreen(UnfocusedScreen):
	def __init__(self, name=None, id=None, classes=None, photo: Photo = Photo()):
		super().__init__(name, id, classes)
		self.photo = photo
	def compose(self):
		yield Header(classes="-tall", icon="•••")
		with Vertical():
			# yield Label(f"«{self.photo.label.upper()}»")
			yield Static(Content(self.photo.description), id="description")
			if self.photo != photo10:
				yield Center(Button("‹‹"))
			else:
				yield Center(Button("››"))
	def on_mount(self):
		self.title = self.photo.label
		if not self.photo.seen:
			self.photo.first_seen()
		self.query_one("#description").update(Content.from_markup(self.photo.description))
	class ReturnPressed(Message):
		pass
	class ContinuePressed(Message):
		pass
	def on_button_pressed(self, event: Button.Pressed):
		# event.stop()
		if self.photo != photo10:
			self.post_message(self.ReturnPressed())
		else:
			self.post_message(self.ContinuePressed())
	def key_backspace(self):
		if self.photo != photo10:
			self.post_message(self.ReturnPressed())
	
class NoteScreen(ModalScreen):
	def __init__(self, name = None, id = None, classes = None, note: Note = Note()):
		super().__init__(name, id, classes)
		self.note = note
	def compose(self):
		with Center():
			with Container():
				yield Static(self.note.text)
				yield Center(Button("‹‹"))
	def on_mount(self):
		self.query_one(Container).border_title = self.note.label.upper()
		self.query_one(Container).border_subtitle = "ИскИн — справка"
	def on_button_pressed(self):
		app.pop_screen()
	def on_key(self):
		app.pop_screen()

class LastPhotoScreen(UnfocusedScreen):

	def compose(self) -> ComposeResult:
		yield Header(classes="-tall", icon="•••")
		with Vertical(id="photo_column"):
			with Grid(id="photo_panel"):
				yield Placeholder(classes="noopacity")
				yield Placeholder(classes="noopacity")
				yield Placeholder(classes="noopacity")
				yield Placeholder(classes="noopacity")
				yield PhotoButton(photo10.label, id="photo10", classes="photobutton")
			yield Center(Button("››", id="continue", classes="hidden"))

	def on_mouse_move(self) -> None:
		# print(event.offset)
		self.query("Button").blur()
	
	class PhotoPressed(Message):
		def __init__(self, button_id: str|None):
			super().__init__()
			self.button_id = button_id

	def action_lets_see_the_photo(self, event: PhotoButton.Pressed):
		button_id = event.button.id
		self.post_message(self.PhotoPressed(button_id))

	@on(PhotoButton.Pressed, ".photobutton")
	def lets_see_the_photo(self, event: PhotoButton.Pressed):
		self.action_lets_see_the_photo(event)
	
	def key_enter(self):
		try:
			button = self.query("PhotoButton:focus, PhotoButton:hover")[0]
			self.action_lets_see_the_photo(Button.Pressed(button))
		except: pass

class TheEndScreen(Screen):
	def compose(self):
		yield Center(Label("КОНЕЦ"))
		yield Center(Label(f"{AUTHOR}, 2025"), id="end")
	def on_mount(self):
		self.query_one("#end").styles.dock = "bottom"
		self.query_one("#end").styles.margin = [3, 0]


class TestApp(App):

	CSS_PATH = "styles.tcss"
	TITLE = TITLE
	# LABELS = ["Рынок", "Ме́ха", "Не более 67%", "Розовые пантеры Джайпура", "Красные платки", "三足狗", "Café hidropônico", "Один-пятьдесят восемь", "Фарм-принтер"]
	PHOTOS = Photos.photos
	NOTES = Notes.notes

	def on_mount(self) -> None:
		# Register the theme
		self.register_theme(reckless_theme)
		# Set the app's theme
		self.theme = "reckless"

		random.shuffle(self.PHOTOS) # UNCOMMENTME
		self.install_screen(StartScreen(), name="start_screen")
		self.install_screen(CutScreen(text=Cut.intro_text,
							next_screen="photos_screen"), name="intro_screen")
		self.install_screen(CutScreen(text=Cut.interlude_text, next_screen="last_photo_screen"), name="interlude_screen")
		self.install_screen(CutScreen(text=Cut.outro_text, next_screen="end_screen"), name="outro_screen")
		self.install_screen(PhotosScreen(
			photos=self.PHOTOS), name="photos_screen")
		for i in range(len(self.PHOTOS)):
			self.install_screen(PhotoScreen(
				photo=self.PHOTOS[i]), name=f"photo{i+1}_screen")
		self.install_screen(LastPhotoScreen(), name="last_photo_screen")
		self.install_screen(PhotoScreen(photo=photo10), name="photo10_screen")
		for n in self.NOTES:
			self.install_screen(NoteScreen(
				note=n), name=f"{n.name}_screen")
		self.install_screen(TheEndScreen, name="end_screen")

		self.push_screen("start_screen")
		# self.push_screen("photos_screen") # DELETEME
		# self.push_screen("interlude_screen") # DELETEME

	def on_start_screen_start_pressed(self, event: StartScreen.StartPressed):
		self.push_screen("intro_screen")

	def on_cut_screen_next_pressed(self, event: CutScreen.NextPressed):
		self.push_screen(event.next_screen)
	
	def on_photos_screen_photo_pressed(self, event: PhotosScreen.PhotoPressed):
		self.push_screen(f"{event.button_id}_screen")

	def on_last_photo_screen_photo_pressed(self, event: PhotosScreen.PhotoPressed):
		self.push_screen(f"{event.button_id}_screen")

	def on_photo_screen_return_pressed(self, event: PhotoScreen.ReturnPressed):
		self.pop_screen()

	def on_photo_screen_continue_pressed(self, event: PhotoScreen.ReturnPressed):
		self.push_screen("outro_screen")
	
	def action_note(self, note: str):
		self.push_screen(f"{note}_screen")
	
	def on_photos_screen_continue_pressed(self):
		self.push_screen("interlude_screen")

if __name__ == "__main__":
	app = TestApp()
	app.run()
