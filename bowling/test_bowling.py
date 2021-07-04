import unittest

from bowling import get_score, frames


class TestResults(unittest.TestCase):

    def test_normal(self):
        result = get_score('43X-/211744XX32--', 0)
        self.assertEqual(result, 106, 'ошибка: неверный подсчет очков')

    def test_frames(self):
        get_score('43X-/211744XX32--')
        result = frames
        self.assertEqual(result, 10, 'ошибка: количество фреймов не равно 10')

    def test_initial_data(self):
        with self.assertRaises(ValueError):
            val1 = get_score('43X-/211744XX32--1', 0)
        with self.assertRaises(ValueError):
            val2 = get_score('43X-/211744XX32-0', 0)
        with self.assertRaises(ValueError):
            val3 = get_score('/3X-/211744XX32--', 0)

    def test_normal_new_rules(self):
        result = get_score('-263X815/5/27-----6', 1)
        self.assertEqual(result, 81, 'ошибка: неверный подсчет очков')

    def test_initial_data_new_rules(self):
        with self.assertRaises(ValueError):
            val1 = get_score('-263X815/5/2799---6', 1)
        with self.assertRaises(ValueError):
            val2 = get_score('43X-/211744XX32-0', 1)
        with self.assertRaises(ValueError):
            val3 = get_score('/3X-/211744XX32--', 1)


if __name__ == '__main__':
    unittest.main()
