from unittest import TestCase


class TestFILLER_PRIORITY(TestCase):
    def test_non_duplicate_priorities(self):
        from subjects import ALL_SUBJECTS
        priorities = [subj.FILLER_PRIORITY for subj in ALL_SUBJECTS if subj.FILLER_PRIORITY]
        self.assertEquals(len(priorities), len(set(priorities)))
