import abc


class _TimeData(object):
    """
    Contains time values displayed as buttons when an action is being set as complete,
    along with required time for completion (if any).
    """

    def __init__(self, description, minutes_tpl, hours_tpl, completion_time):
        self.description = description
        self.minutes = minutes_tpl
        self.hours = hours_tpl
        self.completion_time = completion_time

# Paste-template
"""
_TimeData(description=,
    minutes_tpl=,
    hours_tpl=,
    completion_time=)

"""


class _Action(object):
    __metaclass__ = abc.ABCMeta

    # Displayed on action's icon. Can be empty str.
    @abc.abstractproperty
    def TITLE(self):
        raise NotImplementedError

    @abc.abstractproperty
    def ICON_IMAGE_NAME(self):
        raise NotImplementedError

    # `None` or "time_data_object". Used for time buttons when action is selected.
    @abc.abstractproperty
    def TIME_DATA(self):
        raise NotImplementedError

    # Bar size ratio from 0. to 1.
    # e.g. if 3 actions with BAR_GOAL_HINTs 1., .5, .5,
    # then they ll take up 50%, 25%, 25%.
    @abc.abstractproperty
    def BAR_GOAL_HINT(self):
        raise NotImplementedError

    # `bool`; Mark on subject's bar when this action is omitted (e.g. "Sleep time")
    @abc.abstractproperty
    def MARK_WHEN_OMITTED(self):
        raise NotImplementedError

    # 'all' or `tuple` of specific days the action is a goal or `int` of days per week
    @abc.abstractproperty
    def DAYS_APPEARING(self):
        pass

    def __init__(self):
        self.time_invested = 0

    def goal_achieved_ratio(self):
        ret


# Paste-template
"""
class (_Action):
    TITLE =
    ICON_IMAGE_NAME = 
    TIME_DATA = _TimeData(description=,
                            minutes_tpl=,
                            hours_tpl=,
                            completion_time=)
    BAR_GOAL_HINT = 
    MARK_WHEN_OMITTED = 
    DAYS_APPEARING = 
    
"""


class Focus(_Action):
    TITLE = 'Focus'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description="Mins wasted / 10' ",
                          minutes_tpl=(1, 2, 5),
                          hours_tpl=(),
                          completion_time=None)
    BAR_GOAL_HINT = 0
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class Running(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 30),
                          hours_tpl=(1,),
                          completion_time=1.)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class UpperBody(_Action):
    TITLE = 'Arms'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15/60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class LowerBody(_Action):
    TITLE = 'Legs'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15/60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class MMA(_Action):
    TITLE = 'MMA'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='Watched MMA',
                          minutes_tpl=(5, 10),
                          hours_tpl=(),
                          completion_time=10/60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course1(_Action):
    TITLE = '1st'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=1)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course2(Course1):
    TITLE = '2nd'
    ICON_IMAGE_NAME = ''


class Course3(Course1):
    TITLE = '3rd'
    ICON_IMAGE_NAME = ''


class Programming(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Teaching(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1,2,5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Breaks(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='min / hour',
                          minutes_tpl=(5, 10),
                          hours_tpl=(),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class SleepStart(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = None
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class Science(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'
