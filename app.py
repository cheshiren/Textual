import random

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Grid, Container, Center
from textual.content import Content
from textual.message import Message
from textual.screen import Screen
from textual.theme import Theme
from textual.widgets import Button, Header, Footer, Placeholder, Markdown, Link, Static, Label

from texts import Cut, Photos, Photo

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

	def compose(self):
		yield Header()
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
		yield Header()
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
		yield Header()
		with Vertical(id="photo_column"):
			# yield Static("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя")
			with Grid(id="photo_panel"):
				for i in range(len(self.photos)):
					yield PhotoButton(self.photos[i].label, id=f"photo{i+1}", classes="photobutton")
			yield Center(Button("››", id="continue", classes="hidden1"))

	def on_mouse_move(self) -> None:
		# print(event.offset)
		self.query("PhotoButton").blur()
	
	class PhotoPressed(Message):
		def __init__(self, button_id: str|None):
			super().__init__()
			self.button_id = button_id

	@on(PhotoButton.Pressed, ".photobutton")
	def lets_see_the_photo(self, event: PhotoButton.Pressed):
		button_id = event.button.id
		# event.stop()
		self.post_message(self.PhotoPressed(button_id))
		if len(self.query("PhotoButton.seen")) == len(self.photos):
			self.query_one("#continue").remove_class("hidden")


class PhotoScreen(UnfocusedScreen):
	def __init__(self, name=None, id=None, classes=None, photo: Photo = Photo()):
		super().__init__(name, id, classes)
		self.photo = photo
	def compose(self):
		yield Header()
		with Vertical():
			yield Static(Content(self.photo.description))
			yield Center(Button("‹‹"))
	class ReturnPressed(Message):
		pass
	def on_button_pressed(self, event: Button.Pressed):
		event.stop()
		self.post_message(self.ReturnPressed())


class TestApp(App):

	CSS_PATH = "test.tcss"
	TITLE = TITLE
	# LABELS = ["Рынок", "Ме́ха", "Не более 67%", "Розовые пантеры Джайпура", "Красные платки", "三足狗", "Café hidropônico", "Один-пятьдесят восемь", "Фарм-принтер"]
	PHOTOS = Photos.photos

	def on_mount(self) -> None:
		# Register the theme
		self.register_theme(reckless_theme)
		# Set the app's theme
		self.theme = "reckless"

		# random.shuffle(self.PHOTOS) # UNCOMMENTME
		self.install_screen(StartScreen(), name="start_screen")
		self.install_screen(CutScreen(text=Cut.intro_text,
							next_screen="photos_screen"), name="intro_screen")
		self.install_screen(CutScreen(), name="interlude_screen")
		self.install_screen(CutScreen(), name="outro_screen")
		self.install_screen(PhotosScreen(
			photos=self.PHOTOS), name="photos_screen")
		for i in range(len(self.PHOTOS)):
			self.install_screen(PhotoScreen(
				photo=self.PHOTOS[i]), name=f"photo{i+1}_screen")

		self.push_screen("start_screen")
		self.push_screen("photos_screen") # DELETEME
		# self.push_screen("photo1_screen") # DELETEME

	def on_start_screen_start_pressed(self, event: StartScreen.StartPressed):
		self.push_screen("intro_screen")

	def on_cut_screen_next_pressed(self, event: CutScreen.NextPressed):
		self.push_screen(event.next_screen)
	
	def on_photos_screen_photo_pressed(self, event: PhotosScreen.PhotoPressed):
		self.push_screen(f"{event.button_id}_screen")

	def on_photo_screen_return_pressed(self, event: PhotoScreen.ReturnPressed):
		self.pop_screen()


EXAMPLE_MARKDOWN = """\
# Markdown Document

[wtf!!!](jjj)

This is an example of Textual's `Markdown` widget.

## Features

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!
- [Links](#Features)?
"""

TEXT1 = """\
Hello, [bold $text on $primary]World[/]!

[@click=app.notify('Hello, World!')]Click me[/]
"""


class MarkdownExampleApp(App):
	CSS = """
		Content Link {
			color: red;
			text-style: none;
			&:hover { color: $accent-lighten-1; }
		}
		Static {
			link-color: pink;
			link-style: bold;
			&:hover { color: $accent-lighten-1; }
		}
	"""

	def compose(self) -> ComposeResult:
		yield Link("ЖОПА!!!")
		yield Static(TEXT1)
		yield Markdown(EXAMPLE_MARKDOWN, id="md")


if __name__ == "__main__":
	app = TestApp()
	app.run()

# if __name__ == "__main__":
# 	app = MarkdownExampleApp()
# 	app.run()
