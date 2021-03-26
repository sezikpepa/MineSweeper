from random import randint
from typing import Union

# pylint: disable=unsubscriptable-object
# pylint: disable=bad-indentation
# pylint: disable=trailing-whitespace
# pylint: disable=raise-missing-from

def generate_mines(number: int, x_size: int, y_size: int) -> list:
	if not isinstance(number, int) or number < 0:
		raise ValueError(f"ERROR: possible number types: int -> {number}")

	if not isinstance(x_size, int) or x_size < 0:
		raise ValueError(f"ERROR: possible x_size types: int -> {x_size}")

	if not isinstance(y_size, int) or y_size < 0:
		raise ValueError(f"ERROR: possible y_size types: int -> {y_size}")

	if number > x_size * y_size:
		raise ValueError(f"ERROR: number of mines to generate is greater than available space -> {number} > {x_size * y_size}")

	list_of_mines = []
	counter = 0
	while counter < number:
		mine = (randint(0, y_size - 1), randint(0, x_size - 1))
		if mine not in list_of_mines:
			counter += 1
			list_of_mines.append(mine)

	return list_of_mines

def possible_values(number: int, window_size: int) -> list:
	if not isinstance(number, int) or number < 0:
		raise ValueError(f"ERROR: possible number types: positive int -> {number}")

	if not isinstance(window_size, int) or window_size < 0:
		raise ValueError(f"ERROR: possible window_size types: positive int -> {window_size}")

	if number > window_size:
		raise ValueError(f"ERROR: number cannot be greater than window size {number} > {window_size}")

	results = []
	for i in range(number):
		result = window_size / number
		results.append(result * i)
	return results


def closest_smaller_number(number: Union[float, int], possible_numbers: list[int, float]) -> Union[int, list]:
	if not isinstance(number, (float, int)):
		raise ValueError(f"ERROR: possible number types: int, float -> {number}")

	if number < 0:
		raise ValueError(f"ERROR: number must not be negative {number}")

	if not possible_numbers:
		raise IndexError("ERROR: entry of possible numbers cannot be empty")

	try:
		possible_numbers = sorted(possible_numbers)
		for i in range(1, len(possible_numbers)):
			if number < possible_numbers[i]:
				return possible_numbers[i - 1]
	except TypeError:
		raise TypeError(f"ERROR: possible numbers must have include only: int, float -> {possible_numbers}")

	if possible_numbers[-1] > number:
		return None

	return possible_numbers[-1]

def mines_number(space: int, difficulty: int) -> int:
	if not isinstance(space, int) or space < 0:
		raise ValueError(f"ERROR: possible mines_number types: positive int -> {space}")

	if not isinstance(difficulty, int) or difficulty < 0:
		raise ValueError(f"ERROR: possible difficulty types: positive int -> {difficulty}")

	low_mines = int(space * 0.02)
	high_mines = int(space * 0.3)
	interval_mines = high_mines - low_mines
	part_mines = interval_mines / 10
	

	return int(part_mines * difficulty + low_mines)



if __name__ == "__main__":
	import unittest

	class Test(unittest.TestCase):

		def test_generate_mines(self):

			with self.assertRaises(ValueError):
				generate_mines(-1, 5, 5)
			with self.assertRaises(ValueError):
				generate_mines(1, -5, 5)
			with self.assertRaises(ValueError):
				generate_mines(1, 5, -5)
			with self.assertRaises(ValueError):
				generate_mines(100, 5, 5)

			self.assertEqual(len(generate_mines(5, 10, 10)), 5)

		def test_possible_values(self):
			with self.assertRaises(ValueError):
				possible_values(-1, 200)
			with self.assertRaises(ValueError):
				possible_values(1, -200)
			with self.assertRaises(ValueError):
				possible_values(-1, -200)
			with self.assertRaises(ValueError):
				possible_values(1.5, 6)
			with self.assertRaises(ValueError):
				possible_values(6, 4)

			self.assertEqual(possible_values(4, 400), [0, 100, 200, 300])
			self.assertEqual(possible_values(2, 29), [0, 14.5])


		def test_closest_smaller_number(self):

			self.assertEqual(closest_smaller_number(11.5, [-10, -0.5, 0, 10, 20, 10.5]), 10.5)
			self.assertEqual(closest_smaller_number(0, [-10, -0.5, 0, 10, 20, 10.5]), 0)
			self.assertEqual(closest_smaller_number(5.5, [-10, -0.5, 0, 10, 20, 10.5]), 0)
			self.assertEqual(closest_smaller_number(11, [-10, -0.5, 0, 10, 20, 10.5]), 10.5)
			self.assertEqual(closest_smaller_number(11, [10]), 10)
			self.assertEqual(closest_smaller_number(11, [12]), None)

			with self.assertRaises(ValueError):
				closest_smaller_number(-5, [-10, -0.5, 0, 10, 20, 10.5])
			with self.assertRaises(ValueError):
				closest_smaller_number("x", [-10, -0.5, 0, 10, 20, 10.5])
			with self.assertRaises(TypeError):	
				closest_smaller_number(5, [-10, -0.5, 0, 10, "x", 10.5])

			with self.assertRaises(IndexError):
				closest_smaller_number(5, [])

		def test_mines_number(self):
			with self.assertRaises(ValueError):
				mines_number(5.5, 6)
			with self.assertRaises(ValueError):
				mines_number(6, 5.5)
			with self.assertRaises(ValueError):
				mines_number(-6, 5)
			with self.assertRaises(ValueError):
				mines_number(6, -5)

			self.assertEqual(mines_number(400, 1), 19)

	unittest.main()