import unittest

from converter import int_to_roman, roman_to_int
from gui import RomanConverterApp


class ConverterTests(unittest.TestCase):
    def test_decimal_to_roman(self):
        self.assertEqual(int_to_roman(1), "I")
        self.assertEqual(int_to_roman(944), "CMXLIV")
        self.assertEqual(int_to_roman(3999), "MMMCMXCIX")

    def test_roman_to_decimal(self):
        self.assertEqual(roman_to_int("I"), 1)
        self.assertEqual(roman_to_int("cmxliv"), 944)
        self.assertEqual(roman_to_int("MMMCMXCIX"), 3999)

    def test_decimal_range_is_enforced(self):
        for value in (0, -1, 4000):
            with self.subTest(value=value), self.assertRaises(ValueError):
                int_to_roman(value)

    def test_decimal_type_is_enforced(self):
        for value in (True, 1.5, "10", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                int_to_roman(value)

    def test_invalid_roman_numerals_are_rejected(self):
        for value in ("", "IIII", "VX", "IC", "MCM\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                roman_to_int(value)

    def test_roman_type_is_enforced(self):
        for value in (None, 10, True):
            with self.subTest(value=value), self.assertRaises(TypeError):
                roman_to_int(value)


class InputValidationTests(unittest.TestCase):
    def test_decimal_input_accepts_only_four_ascii_digits(self):
        validate = RomanConverterApp._validate_decimal
        for value in ("", "1", "3999", "0001"):
            with self.subTest(value=value):
                self.assertTrue(validate(None, value))
        for value in ("40000", "12a", "²", "١", "１"):
            with self.subTest(value=value):
                self.assertFalse(validate(None, value))

    def test_roman_input_accepts_only_roman_letters_up_to_limit(self):
        validate = RomanConverterApp._validate_roman
        self.assertTrue(validate(None, ""))
        self.assertTrue(validate(None, "mmmdccclxxxviii"))
        self.assertFalse(validate(None, "X1"))
        self.assertFalse(validate(None, "M" * 16))


if __name__ == "__main__":
    unittest.main()
