from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Digits, Button

class TimeDisplay(Digits):
	start_time = reactive(monotonic)
	time = reactive(0.0)
	total = reactive(0.0)

	def on_mount(self) -> None:
		self.update_timer = self.set_interval(1/60, self.update_time, pause=True)
	
	def update_time(self) -> None:
		self.time = self.total + monotonic() - self.start_time
	
	def watch_time(self, time:float) -> None:
		minutes, seconds = divmod(time, 60)
		hours, minutes = divmod(minutes, 60)
		self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")
	
	def start(self) -> None:
		self.start_time = monotonic()
		self.update_timer.resume()

	def stop(self) -> None:
		self.update_timer.pause()
		self.total += monotonic() - self.start_time
		self.time = self.total
	
	def reset(self) -> None:
		self.total = 0
		self.time = 0

class Stopwatch(HorizontalGroup):
	def on_button_pressed(self, event: Button.Pressed) -> None:
		button_id = event.button.id
		time_display = self.query_one(TimeDisplay)

		if button_id == "start":
			time_display.start()
			self.add_class("started")
		elif button_id == "stop":
			time_display.stop()
			self.remove_class("started")
		elif button_id == "reset":
			time_display.reset()

	def compose(self) -> ComposeResult:
		yield Button("Старт", id="start", variant="success")
		yield Button("Стоп", id="stop", variant="error")
		yield Button("Сброс", id="reset")
		yield TimeDisplay()

class StopwatchApp(App):
	
	CSS_PATH="stopwatch.tcss"
	BINDINGS = [
		("d", "toggle_dark", "Переключить тёмный режим"),
		("a", "add_stopwatch", "Добавить таймер"),
		("r", "remove_stopwatch", "Удалить таймер"),
		]
	
	def compose(self) -> ComposeResult:
		yield Header()
		yield Footer()
		yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")
	
	def action_add_stopwatch(self) -> None:
		new_stopwatch = Stopwatch()
		self.query_one("#timers").mount(new_stopwatch)
		new_stopwatch.scroll_visible()

	def action_remove_stopwatch(self) -> None:
		timers = self.query("Stopwatch")
		if timers:
			timers.last().remove()

	def action_toggle_dark(self):
		self.theme = (
			"textual-dark" if self.theme == "textual-light" else "textual-light"
		)


if __name__ == "__main__":
	app = StopwatchApp()
	app.run()