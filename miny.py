from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QSlider

from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtCore import QTime

import sys

from gameStructures import Chunk
from gameFunctions import generate_mines
from gameFunctions import possible_values
from gameFunctions import closest_smaller_number
from gameFunctions import mines_number


X_SIZE = 20
Y_SIZE = 20

NUMBER_OF_LABELS = Y_SIZE * X_SIZE


FIELD_SQUARE_SIZE = 20
Y_GRID_SIZE = FIELD_SQUARE_SIZE * Y_SIZE
X_GRID_SIZE = FIELD_SQUARE_SIZE * X_SIZE

X_WINDOW_SIZE = X_GRID_SIZE + 100
Y_WINDOW_SIZE = Y_GRID_SIZE + 40

X_POSSIBLE_VALUES = possible_values(X_SIZE, X_GRID_SIZE)
Y_POSSIBLE_VALUES = possible_values(Y_SIZE, Y_GRID_SIZE)


LIGHT_THEME = {
	"undiscovered_color": "#999999",
	"discovered_color": "#ffffff",
	"win_timer_color": "#e30e0e",
	"lose_timer_color": "#0cc431"
}

DARK_THEME = {
	"undiscovered_color": "#000000",
	"discovered_color": "#d9d9d9",
	"win_timer_color": "#e30e0e",
	"lose_timer_color": "#0cc431"
}


# pylint: disable=bad-indentation
# pylint: disable=no-member
# pylint: disable=arguments-out-of-order
# pylint: disable=trailing-whitespace

class MineSweeper(QMainWindow):
	def __init__(self):
		super().__init__()

		self.undiscovered_color = "#000000"
		self.discovered_color = "#d9d9d9"
		self.win_timer_color = "#e30e0e"
		self.lose_timer_color = "#0cc431"


		self.curr_time = QTime(00,00,00)
		self.timer = QTimer()
		self.timer.timeout.connect(self.time)
		self.timer_already_started = False

		self.solved: bool = False
		
		self.player_ended: bool = False

		self.theme: str = "dark"

		self.list_of_mines = []

		self.difficulty_slider_default_value: int = 2
		self.number_of_mines = mines_number(NUMBER_OF_LABELS, self.difficulty_slider_default_value)


		self.create_GUI()


	def create_GUI(self) -> None:
		self.setWindowTitle("MineSweeper 1.1")

		self.win_massage = QMessageBox(self)
		self.win_massage.setText("Gratuluji, dokázal jsi nalézt všechny miny")

		self.setMouseTracking(True)

		centralWidget = QWidget(self)
		centralWidget.setStyleSheet("background: white")
		self.setCentralWidget(centralWidget)
		self.setFixedSize(X_WINDOW_SIZE + 20, Y_WINDOW_SIZE)

		layout = QGridLayout(centralWidget)
		layout.setSpacing(0)
		layout.setContentsMargins(0, 0, 0, 0)
		centralWidget.setLayout(layout)

		self.list_of_labels = []

		self.list_of_mines = generate_mines(self.number_of_mines, X_SIZE, Y_SIZE)


		self.reset_button = QPushButton(centralWidget)
		self.reset_button.setText("RESET")
		self.reset_button.clicked.connect(self.reset)
		self.reset_button.setStyleSheet("margin: 3px")
		self.reset_button.setMinimumSize(0, 50)


		self.timer_label = QLabel(centralWidget)
		self.timer_label.setText(f"{self.curr_time.minute():0>2}:{self.curr_time.second():0>2}")
		self.timer_label.setAlignment(Qt.AlignHCenter)
		self.timer_label.setStyleSheet("font: 34px")

		self.difficulty_slider = QSlider(centralWidget)
		self.difficulty_slider.setOrientation(Qt.Horizontal)
		self.difficulty_slider.setFixedHeight(30)
		self.difficulty_slider.setRange(1, 10)
		self.difficulty_slider.setTickInterval(1)
		self.difficulty_slider.setValue(self.difficulty_slider_default_value)
		self.difficulty_slider.valueChanged.connect(self.difficulty_label_set)
		self.difficulty_slider.sliderReleased.connect(self.new_mines_set)

		self.difficulty_label = QLabel(centralWidget)
		self.difficulty_label.setText(str(self.difficulty_slider_default_value))
		self.difficulty_label.setAlignment(Qt.AlignCenter)
		self.difficulty_label.setStyleSheet("font: 20px")
		
		

		for i in range(Y_SIZE):
			row = []
			for j in range(X_SIZE):
				if (i, j) in self.list_of_mines:
					mine = True
				else:
					mine = False

				label = Chunk(j, i, mine)
				label.setFixedSize(FIELD_SQUARE_SIZE, FIELD_SQUARE_SIZE)
				label.setStyleSheet(f"background: {self.undiscovered_color}; border: 1px solid grey")
				layout.addWidget(label, i, j)
				row.append(label)
			self.list_of_labels.append(row)


		self.color_theme_combobox = QComboBox(centralWidget)
		self.color_theme_combobox.addItem("Dark theme", "dark")
		self.color_theme_combobox.addItem("Light theme", "light")
		self.color_theme_combobox.currentIndexChanged.connect(self.theme_change)
		self.color_theme_combobox.setMinimumHeight(FIELD_SQUARE_SIZE * 2)
		if self.theme == "dark":
			self.color_theme_combobox.setCurrentIndex(0)
		else:
			self.color_theme_combobox.setCurrentIndex(1)
		layout.addWidget(self.color_theme_combobox, Y_SIZE - 2, X_SIZE, 2, 1)

		layout.addWidget(self.timer_label, 0, X_SIZE, 3, 1)
		layout.addWidget(self.reset_button, 2, X_SIZE, 3, 1)
		layout.addWidget(self.difficulty_slider, Y_SIZE, 1, 1, X_SIZE - 2)
		layout.addWidget(self.difficulty_label, Y_SIZE, X_SIZE, 1, 1)

		self.mines_number_surroundings_calculate()

	def theme_change(self) -> None:
		if self.color_theme_combobox.currentData() == "light":
			self.undiscovered_color = LIGHT_THEME["undiscovered_color"]
			self.discovered_color = LIGHT_THEME["discovered_color"]
			self.win_timer_color = LIGHT_THEME["win_timer_color"]
			self.lose_timer_color = LIGHT_THEME["lose_timer_color"]
			self.theme = "light"
	
		if self.color_theme_combobox.currentData() == "dark":	
			self.undiscovered_color = DARK_THEME["undiscovered_color"]
			self.discovered_color = DARK_THEME["discovered_color"]
			self.win_timer_color = DARK_THEME["win_timer_color"]
			self.lose_timer_color = DARK_THEME["lose_timer_color"]
			self.theme = "dark"

		for y in range(Y_SIZE):
			for x in range(X_SIZE):	 
				if (self.list_of_labels[y][x].discovered and self.list_of_labels[y][x].mine) or self.list_of_labels[y][x].marked:
					pass

				elif not self.list_of_labels[y][x].discovered:
					self.list_of_labels[y][x].setStyleSheet(f"background: {self.undiscovered_color}; border: 1px solid grey")

				elif self.list_of_labels[y][x].discovered and not self.list_of_labels[y][x].mine:
					self.list_of_labels[y][x].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")

		
	def difficulty_label_set(self):
		self.difficulty_label.setText(str(self.difficulty_slider.value()))

	def mousePressEvent(self, QMouseEvent) -> None:
		if not self.player_ended:

			y = QMouseEvent.pos().x()
			x = QMouseEvent.pos().y()

			if not (x > X_GRID_SIZE or y > Y_GRID_SIZE):

				x = closest_smaller_number(x, Y_POSSIBLE_VALUES)
				y = closest_smaller_number(y, X_POSSIBLE_VALUES)

				x = int(x // FIELD_SQUARE_SIZE)
				y = int(y // FIELD_SQUARE_SIZE)

				if QMouseEvent.button() == Qt.LeftButton:
					if self.list_of_labels[x][y].mine:				
						self.stop_timer()
						if not self.player_ended:
							self.list_of_labels[x][y].discovered = True
							self.list_of_labels[x][y].setStyleSheet("background: red; border: 1px solid grey")
							self.win_massage.about(self, "PROHRA", "Tentokrát se to bohužel nepovedlo, snad to vyjde příště.")
					
						self.player_ended = True
					else:
						if not self.timer_already_started:
							self.start_timer()

						self.timer_already_started = True
						self.list_of_labels[x][y].discovered = True
						self.list_of_labels[x][y].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")

						self.reveal_area(y, x)

					self.solved_check()

				else:
					if not self.list_of_labels[x][y].discovered:
						if self.list_of_labels[x][y].marked:
							self.list_of_labels[x][y].setStyleSheet(f"background: {self.undiscovered_color}; border: 1px solid grey")
							self.list_of_labels[x][y].marked = False

						else:
							self.list_of_labels[x][y].setStyleSheet("background: orange; border: 1px solid grey")
							self.list_of_labels[x][y].marked = True

	def mines_number_surroundings_calculate(self) -> None:
		for x in range(X_SIZE):
			for y in range(Y_SIZE):
				self.list_of_labels[x][y].mines_number_surroundings = 0
				for i in range(x - 1, x + 2):
					for j in range(y - 1, y + 2):
						try:
							if self.list_of_labels[i][j].mine and i >= 0 and j >= 0:
								if not (i == x and j == y):
									self.list_of_labels[x][y].mines_number_surroundings += 1
						except IndexError:
							pass

	def new_mines_set(self):
		self.number_of_mines = mines_number(NUMBER_OF_LABELS, self.difficulty_slider.value())
		self.list_of_mines = generate_mines(self.number_of_mines, X_SIZE, Y_SIZE)
		for y in range(Y_SIZE):
			for x in range(X_SIZE):
				if (y, x) in self.list_of_mines:
					self.list_of_labels[y][x].mine = True
				else:
					self.list_of_labels[y][x].mine = False

		self.mines_number_surroundings_calculate()
		self.label_set()

	def label_set(self) -> None:
		for y in range(Y_SIZE):
			for x in range(X_SIZE):
				if self.list_of_labels[y][x].discovered:
					if self.list_of_labels[y][x].mines_number_surroundings == 0:
						pass
					else:
						self.list_of_labels[y][x].setText(str(self.list_of_labels[y][x].mines_number_surroundings))

	def reveal_area(self, x, y) -> None:
		if self.list_of_labels[y][x].mines_number_surroundings == 0:		
			try:
				extract = self.list_of_labels[y - 1][x]

				if not extract.mine and Y_SIZE > y - 1 >= 0 and not extract.discovered:
					self.list_of_labels[y - 1][x].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")
					self.list_of_labels[y - 1][x].discovered = True
					if extract.mines_number_surroundings == 0:
						self.reveal_area(x, y - 1)

			except IndexError:
				pass

			try:
				extract = self.list_of_labels[y + 1][x]

				if not extract.mine and Y_SIZE > y + 1 >= 0 and not extract.discovered:
					self.list_of_labels[y + 1][x].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")
					self.list_of_labels[y + 1][x].discovered = True
					if extract.mines_number_surroundings == 0:
						self.reveal_area(x, y + 1)

			except IndexError:
				pass

			try:
				extract = self.list_of_labels[y][x + 1]

				if not extract.mine and X_SIZE > x + 1 >= 0 and not extract.discovered:
					self.list_of_labels[y][x + 1].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")
					self.list_of_labels[y][x + 1].discovered = True
					if extract.mines_number_surroundings == 0:
						self.reveal_area(x + 1, y)

			except IndexError:
				pass

			try:
				extract = self.list_of_labels[y][x - 1]

				if not extract.mine and X_SIZE - 1 > x  - 1 >= 0 and not extract.discovered:
					self.list_of_labels[y][x - 1].setStyleSheet(f"background: {self.discovered_color}; border: 1px solid grey")
					self.list_of_labels[y][x - 1].discovered = True
					if extract.mines_number_surroundings == 0:
						self.reveal_area(x - 1, y)

			except IndexError:
				pass

		self.label_set()

	def solved_check(self) -> None:
		for element in self.list_of_labels:
			for part in element:
				if not part.mine and not part.discovered:
					return

		self.solved = True
		self.stop_timer()

		if not self.player_ended:
			self.player_ended = True
			self.win_massage.about(self, "VÝHRA", f"Gratuluji, zvládl/a jsi vyřešit tento problém. Zvládl/a jsi to za {self.curr_time.minute():0>2}:{self.curr_time.second():0>2}")
		
	def reset(self) -> None:
		self.timer = QTimer()
		self.curr_time = QTime(00,00,00)
		self.timer.timeout.connect(self.time)
		self.solved = False
		self.timer_already_started = False
		self.player_ended = False
		self.difficulty_slider.setDisabled(False)
		self.difficulty_slider_default_value = self.difficulty_slider.value()
		self.create_GUI()

	def start_timer(self) -> None:
		self.difficulty_slider.setDisabled(True)
		self.timer.start(1000)
		
	def stop_timer(self) -> None:
		self.timer.stop()
		if not self.solved:
			self.timer_label.setStyleSheet(f"font: 34px; color: {self.win_timer_color}")
		else:
			self.timer_label.setStyleSheet(f"font: 34px; color: {self.lose_timer_color}")

	def time(self) -> None:
		self.curr_time = self.curr_time.addSecs(1)
		self.timer_label.setText(f"{self.curr_time.minute():0>2}:{self.curr_time.second():0>2}")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MineSweeper()
	window.show()
	sys.exit(app.exec_())
