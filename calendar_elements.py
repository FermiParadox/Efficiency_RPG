import calendar


class Day(object):
    def __init__(self, date, subjects_seq):
        self.date = date
        # Subjects classes are converted to instances.
        self._subjects_seq = subjects_seq
        self.subjects = []
        self._subjects_classes_to_instances()

    def _subjects_classes_to_instances(self):
        for cls in self._subjects_seq:
            self.subjects.append(cls())

    def productivity(self):
        None

    def goals_achieved_ratio(self):
        None


class Week(object):
    def __init__(self, first_day_of_week_date, subjects_seq):
        self.first_day_of_week_date = first_day_of_week_date
        self.subjects_seq = subjects_seq


