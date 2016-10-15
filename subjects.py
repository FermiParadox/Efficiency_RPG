import abc

import actions


class _Subject(object):
    """
    A subject (e.g. "athletics") contains various "actions" (e.g. aerobic).

    Non-"filler" subjects have their own bar (e.g. "athletics"),
    otherwise they fill existing bars (e.g. "failed_goals") and
    are taken into account in productivity estimation.
    """

    __metaclass__ = abc.ABCMeta

    # `None` if subject is not a filler, otherwise an `int` indicating bar display-priority.
    @abc.abstractproperty
    def TITLE(self):
        pass

    @abc.abstractproperty
    def FILLER_PRIORITY(self):
        pass

    @abc.abstractproperty
    def BAR_COLOR(self):
        pass

    @abc.abstractproperty
    def ICON_IMAGE_NAME(self):
        pass

    # Sequence of all actions contained in a subject.
    @abc.abstractproperty
    def ACTIONS_SEQUENCE(self):
        pass
    
    # `False` or `tuple`: (time_val, relevant_actions_lst)
    # Used when actions of a subject can have an arbitrary time individually,
    # but cumulatively must reach or exceed a time value.
    @abc.abstractproperty
    def OPTIONAL_COMPLETION_TIME_AND_ACTIONS(self):
        pass

    def __init__(self):
        # Actions classes are converted to instances.
        self.actions = []
        self._actions_classes_to_instances()

    def _actions_classes_to_instances(self):
        for cls in self.ACTIONS_SEQUENCE:
            self.actions.append(cls())

    def time_invested(self):
        return sum(a.time_invested for a in self.actions)

    def goal_achieved_ratio(self):
        return sum(a.time_invested * a.BAR_GOAL_HINT for a in self.actions)


# Paste-template
"""
class (_Subject):
    TITLE =
    FILLER_PRIORITY =
    BAR_COLOR =
    ICON_IMAGE_NAME =
    ACTIONS_SEQUENCE =
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = 

"""


class Athletics(_Subject):
    TITLE = 'Athletics'
    FILLER_PRIORITY = None
    BAR_COLOR = 'purple'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.Running,
                        actions.UpperBody,
                        actions.LowerBody,
                        actions.MMA)
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = False


class Physics(_Subject):
    TITLE = 'Physics'
    FILLER_PRIORITY = None
    BAR_COLOR = 'blue'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.Course1,
                        actions.Course2,
                        actions.Course3,
                        actions.Focus)
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = (6, set(ACTIONS_SEQUENCE)-{actions.Focus})


class Programming(_Subject):
    TITLE ='Programming'
    FILLER_PRIORITY = None
    BAR_COLOR = 'green'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.Programming,)
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = (2, ACTIONS_SEQUENCE)


class Teaching(_Subject):
    TITLE = 'Teaching'
    FILLER_PRIORITY = 2
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.Teaching, )
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = False


class Resting(_Subject):
    TITLE = 'Resting'
    FILLER_PRIORITY = None
    BAR_COLOR = 'light_blue'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.SleepStart, actions.Breaks, )
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = False


class Science(_Subject):
    TITLE = 'Science'
    FILLER_PRIORITY = None
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (actions.Science, )
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = False


class FailedGoals(_Subject):
    TITLE = 'Failed goals'
    FILLER_PRIORITY = 1
    BAR_COLOR = 'red'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = ()
    OPTIONAL_COMPLETION_TIME_AND_ACTIONS = False


ALL_SUBJECTS = frozenset(_Subject.__subclasses__())

