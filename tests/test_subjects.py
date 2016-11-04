from unittest import TestCase


class TestFILLER(TestCase):
    def test_non_duplicate_priorities(self):
        from main import ALL_SUBJECTS
        priorities = [subj.FILLER for subj in ALL_SUBJECTS if subj.FILLER]
        self.assertLessEqual(len(priorities), 1)

    def test_DISPLAYED_SUBJECTS_are__SUBJECTS(self):
        from main import ALL_SUBJECTS, DISPLAYED_SUBJECTS
        self.assertFalse(set(DISPLAYED_SUBJECTS) - set(ALL_SUBJECTS))


class TestIMPORTANCE(TestCase):
    def test_non_duplicate_priorities(self):
        from main import ALL_SUBJECTS
        for subj in ALL_SUBJECTS:
            self.assertLessEqual(subj.IMPORTANCE, 1)




