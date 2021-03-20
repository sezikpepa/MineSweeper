from PySide6.QtWidgets import QLabel

# pylint: disable=bad-indentation
class Chunk(QLabel):
	def __init__(self, x, y, mine):
		super().__init__()

		self.x: int = x
		self.y: int = y

		self.mine: bool = mine
		self.discovered: bool = False
		self.mines_number_surroundings: int = 0
		self.marked: bool = False
