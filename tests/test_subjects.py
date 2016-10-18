from unittest import TestCase


class TestFILLER_PRIORITY(TestCase):
    def test_non_duplicate_priorities(self):
        from main import ALL_SUBJECTS
        priorities = [subj.FILLER_PRIORITY for subj in ALL_SUBJECTS if subj.FILLER_PRIORITY]
        self.assertEquals(len(priorities), len(set(priorities)))

    def test_DISPLAYED_SUBJECTS_are__SUBJECTS(self):
        from main import ALL_SUBJECTS, DISPLAYED_SUBJECTS
        self.assertFalse(set(DISPLAYED_SUBJECTS) - set(ALL_SUBJECTS))



