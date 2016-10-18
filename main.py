# -*- coding: utf-8 -*-

# Used for screenshots that match size of current screenshots in GooglePlay


if 1:
    from kivy.config import Config
    Config.set('graphics', 'width', '410')
    Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.label import Label as Label
from kivy.properties import ObjectProperty, DictProperty, NumericProperty, BooleanProperty, ListProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.uix.carousel import Carousel
from kivy import platform
from kivy.event import EventDispatcher

from functools import partial
import abc


__version__ = '0.0.1'

APP_NAME = 'EffRpg'

# PASTE-TEMPLATE
"""

    def __init__(self, **kwargs):
        super(, self).__init__(**kwargs)

"""


# ---------------------------------------------------------------------------------------------------
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


class _Action(EventDispatcher):
    __metaclass__ = abc.ABCMeta

    time_invested = NumericProperty(0.)
    completion_ratio = NumericProperty(0.)
    completed = BooleanProperty(False)

    @property
    def completion_ratio(self):
        if self.TIME_DATA:
            ratio = float(self.time_invested) / self.TIME_DATA.completion_time
            return min(ratio, 1.)

        return self.completed

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
        pass


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
    ICON_IMAGE_NAME = 'heart.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 30),
                          hours_tpl=(1,),
                          completion_time=1.)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class UpperBody(_Action):
    TITLE = 'Arms'
    ICON_IMAGE_NAME = 'arms_training.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class LowerBody(_Action):
    TITLE = 'Legs'
    ICON_IMAGE_NAME = 'kick.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class MMA(_Action):
    TITLE = 'MMA'
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='Watched MMA',
                          minutes_tpl=(5, 10),
                          hours_tpl=(),
                          completion_time=10 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course1(_Action):
    TITLE = '1st'
    ICON_IMAGE_NAME = 'book_pictogram_1.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=1)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course2(Course1):
    TITLE = '2nd'
    ICON_IMAGE_NAME = 'book_pictogram_2.png'


class Course3(Course1):
    TITLE = '3rd'
    ICON_IMAGE_NAME = 'book_pictogram_3.png'


class ProgrammingAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'programming.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class TeachingAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'teaching_pictogram.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Breaks(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'resting.png'
    TIME_DATA = _TimeData(description='min / hour',
                          minutes_tpl=(5, 10),
                          hours_tpl=(),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class SleepStart(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'sleep_early.png'
    TIME_DATA = None
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class ScienceAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = ''
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


# ---------------------------------------------------------------------------------------------------
class _Subject(EventDispatcher):
    """
    A subject (e.g. "athletics") contains various "actions" (e.g. aerobic).

    Non-"filler" subjects have their own bar (e.g. "athletics"),
    otherwise they fill existing bars (e.g. "failed_goals") and
    are taken into account in productivity estimation.
    """

    __metaclass__ = abc.ABCMeta

    goal_achieved_ratio = NumericProperty()

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
    # but cumulatively must reach a time value in order to achieve the subject.
    @abc.abstractproperty
    def CUMULATIVE_COMPLETION_TIME_AND_ACTIONS(self):
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

    @property
    def goal_achieved_ratio(self):
        return sum(a.completion_ratio * a.BAR_GOAL_HINT for a in self.actions)


# Paste-template
"""
class (_Subject):
    TITLE =
    FILLER_PRIORITY =
    BAR_COLOR =
    ICON_IMAGE_NAME =
    ACTIONS_SEQUENCE =
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS =

"""


class Athletics(_Subject):
    TITLE = 'Athletics'
    FILLER_PRIORITY = None
    BAR_COLOR = 'purple'
    ICON_IMAGE_NAME = 'fight_stance.png'
    ACTIONS_SEQUENCE = (Running,
                        UpperBody,
                        LowerBody,
                        MMA)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class Physics(_Subject):
    TITLE = 'Physics'
    FILLER_PRIORITY = None
    BAR_COLOR = 'blue'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (Course1,
                        Course2,
                        Course3,
                        Focus)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = (6, set(ACTIONS_SEQUENCE) - {Focus})


class Programming(_Subject):
    TITLE = 'Programming'
    FILLER_PRIORITY = None
    BAR_COLOR = 'green'
    ICON_IMAGE_NAME = 'programming.png'
    ACTIONS_SEQUENCE = (ProgrammingAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = (2, ACTIONS_SEQUENCE)


class Teaching(_Subject):
    TITLE = 'Teaching'
    FILLER_PRIORITY = 2
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = 'teaching_pictogram.png'
    ACTIONS_SEQUENCE = (TeachingAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class Health(_Subject):
    TITLE = 'Health'
    FILLER_PRIORITY = None
    BAR_COLOR = 'light_blue'
    ICON_IMAGE_NAME = 'medicine.png'
    ACTIONS_SEQUENCE = (SleepStart, Breaks,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class Science(_Subject):
    TITLE = 'Science'
    FILLER_PRIORITY = None
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = (ScienceAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class FailedGoals(_Subject):
    TITLE = 'Failed goals'
    FILLER_PRIORITY = 1
    BAR_COLOR = 'red'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = ()
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


ALL_SUBJECTS = frozenset(_Subject.__subclasses__())
DISPLAYED_SUBJECTS = (Athletics, Physics, Programming, Science, Health,)


# ---------------------------------------------------------------------------------------------------
class MyProgressBar(Widget):
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


# ---------------------------------------------------------------------------------------------------
class SubjectSelectionPage(GridLayout):
    def __init__(self, **kwargs):
        super(SubjectSelectionPage, self).__init__(cols=3, **kwargs)

    def populate_page(self):
        for subj in DISPLAYED_SUBJECTS:
            box = BoxLayout(orientation='vertical')
            box.add_widget(Image(source=subj.ICON_IMAGE_NAME))
            box.add_widget(Label(text=subj.TITLE))
            self.add_widget(box)


# ---------------------------------------------------------------------------------------------------
class SubjectBar(MyProgressBar):
    subj_obj = ObjectProperty(Athletics())      # Athletics() is a default value, needed only initially

    def __init__(self, **kwargs):
        super(SubjectBar, self).__init__(**kwargs)


class SubjectsBarsBox(BoxLayout):
    def __init__(self, **kwargs):
        super(SubjectsBarsBox, self).__init__(spacing='1sp', **kwargs)
        self.populate_box()

        self.popup_widg = SubjectSelectionPage()

    def populate_box(self):
        for subj in DISPLAYED_SUBJECTS:
            bar = SubjectBar()
            bar.subj_obj = subj()
            self.add_widget(bar)

    def on_touch_down(self, touch):
        self.popup_widg.open()


class MainWidget(Carousel):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


class EffRpgApp(App):
    def build(self):
        main_widg = MainWidget()
        return main_widg


if __name__ == '__main__':

    try:
        import ignore_build_ensure_images_cited
    except ImportError:
        pass

    EffRpgApp().run()
