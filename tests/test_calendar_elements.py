from unittest import TestCase

import calendar_elements


class TestDay(TestCase):
    def setUp(self):
        from main import ALL_SUBJECTS
        self.ALL_SUBJECTS = ALL_SUBJECTS
        self.Day = calendar_elements.Day

    def test___init__(self):
        self.Day(date='', subjects_seq=self.ALL_SUBJECTS)
