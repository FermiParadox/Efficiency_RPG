# -*- coding: utf-8 -*-

# Used for screenshots that match size of current screenshots in GooglePlay


if 1:
    from kivy.config import Config
    Config.set('graphics', 'width', '410')
    Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.button import Button as Button
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
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
import os
import datetime
import copy

import citations


__version__ = '0.0.6'

APP_NAME = 'Efficiency RPG'

# PASTE-TEMPLATE
"""

    def __init__(self, **kwargs):
        super(, self).__init__(**kwargs)

"""


# ---------------------------------------------------------------------------------------------------
OWN_IMAGES_DIR = 'own_images'
THIRD_PARTIES_IMAGES_DIR = 'third_parties_images'


def image_path(im_name):
    if im_name in os.listdir(OWN_IMAGES_DIR):
        return os.path.join(OWN_IMAGES_DIR, im_name)
    elif im_name in os.listdir(THIRD_PARTIES_IMAGES_DIR):
        return os.path.join(THIRD_PARTIES_IMAGES_DIR, im_name)
    else:
        print('\nWARNING: Image name not found in directories. ({})\n'.format(im_name))


# ---------------------------------------------------------------------------------------------------
# Misc
CENTER_POS_HINT = {'center_x': .5, 'center_y': .5}

FAINT_BLACK = (0,0,0,.1)

POPULATING_DELAY = .3

BACKGROUND_COLOR = .9,.9,1,1


# ---------------------------------------------------------------------------------------------------
class ButtonD(Button):
    re_enable_scheduled_event = ObjectProperty()

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)

    def disable_for(self, time):
        Clock.unschedule(self.re_enable_scheduled_event)
        self.disabled = True
        self.re_enable_scheduled_event = Clock.schedule_once(lambda *_: setattr(self, 'disabled', False), time)


# ---------------------------------------------------------------------------------------------------
class _TimeData(object):
    """
    Contains time values displayed as buttons when an action is being set as complete,
    along with required time for completion (if any).
    """

    def __init__(self, description, minutes_tpl, hours_tpl, completion_time):
        self.description = description
        self.minutes_tpl = minutes_tpl
        self.hours_tpl = hours_tpl
        self.completion_time = completion_time


# Added to minutes (floats) like "9.9999.." in order to display them correctly
# when the decimal part is ignored.
# WARNING !!! Values that are indeed less than "10." will become "10."
# but this should not be a problem in this program.
# WARNING !!! 10**-10 assumes the error occurs on the 11th decimal,
# that is, there are 5 or less significant integers.
# https://github.com/kivy/kivy/pull/4579#issuecomment-244723457
FLOAT_COMPENSATOR = 10**-10


def time_as_string(t):
    m = (t % 1) * 60
    m = int(m + FLOAT_COMPENSATOR)
    h = int(t)
    # Prohibits display of "0:59.9999" as "0:60"
    if m >= 60:
        h += 1
        m = 0
    return '{:0>1}:{:0>2}'.format(h, m)


# ---------------------------------------------------------------------------------------------------
# All actions should contain "Action" in their name,
# in order to avoid accidental overriding of methods in kivy-app.
class _Action(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def time_required(cls):
        t = 0
        time_data = cls.TIME_DATA
        if time_data:
            t = time_data.completion_time
        return t

    @classmethod
    def minutes_required(cls):
        t = cls.time_required()
        return int((t % 1) * 60)

    @classmethod
    def hours_required(cls):
        t = cls.time_required()
        return int(t)

    @classmethod
    def time_required_as_str(cls):
        return time_as_string(t=cls.time_required())

    @classmethod
    def completion_ratio(cls, hours_invested):
        completion_time = cls.time_required()
        if completion_time:
            ratio = float(hours_invested) / completion_time
            return min(ratio, 1.)

        return 'undefined'

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    # Displayed on action's icon. Can be empty str.
    @abc.abstractproperty
    def TITLE(self):
        pass

    @abc.abstractproperty
    def ICON_IMAGE_NAME(self):
        pass

    # `None` or "time_data_object". Used for time buttons when action is selected.
    @abc.abstractproperty
    def TIME_DATA(self):
        pass

    # Bar size ratio from 0. to 1.
    # e.g. if 3 actions with BAR_GOAL_HINTs 1., .5, .5,
    # then they ll take up 50%, 25%, 25%.
    @abc.abstractproperty
    def BAR_GOAL_HINT(self):
        pass

    # `bool`; Mark on subject's bar when this action is omitted (e.g. "Sleep time")
    @abc.abstractproperty
    def MARK_WHEN_OMITTED(self):
        pass

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


class RunningAction(_Action):
    TITLE = 'Cardio'
    ICON_IMAGE_NAME = 'heart.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 30),
                          hours_tpl=(1,),
                          completion_time=30/60.)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class UpperBodyAction(_Action):
    TITLE = 'Arms'
    ICON_IMAGE_NAME = 'arms_training.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class LowerBodyAction(_Action):
    TITLE = 'Legs'
    ICON_IMAGE_NAME = 'kick.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 15),
                          hours_tpl=(),
                          completion_time=15 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 3


class MMAAction(_Action):
    TITLE = 'MMA'
    ICON_IMAGE_NAME = 'mma_pictogram.png'
    TIME_DATA = _TimeData(description='Watched MMA',
                          minutes_tpl=(5, 10),
                          hours_tpl=(),
                          completion_time=10 / 60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class GunsTrainingAction(_Action):
    TITLE = 'Guns'
    ICON_IMAGE_NAME = 'handgun.jpg'
    TIME_DATA = _TimeData(description='Operated guns (simulation)',
                          minutes_tpl=(5,10),
                          hours_tpl=(),
                          completion_time=10/60.)
    BAR_GOAL_HINT = .5
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course1Action(_Action):
    TITLE = '1st'
    ICON_IMAGE_NAME = 'book_pictogram_1.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=1.)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class Course2Action(Course1Action):
    TITLE = '2nd'
    ICON_IMAGE_NAME = 'book_pictogram_2.png'


class Course3Action(Course1Action):
    TITLE = '3rd'
    ICON_IMAGE_NAME = 'book_pictogram_3.png'


class ProgrammingAction(_Action):
    TITLE = 'Programming'
    ICON_IMAGE_NAME = 'programming.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=2)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class TeachingAction(_Action):
    TITLE = 'Teaching'
    ICON_IMAGE_NAME = 'teaching_pictogram.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=9)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class BreaksAction(_Action):
    TITLE = 'Breaks'
    ICON_IMAGE_NAME = 'resting.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1,),
                          completion_time=5/60. * 8)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class SleepStartAction(_Action):
    TITLE = 'Sleep'
    ICON_IMAGE_NAME = 'sleep_early.png'
    TIME_DATA = None
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class TeethAction(_Action):
    TITLE = 'Teeth'
    ICON_IMAGE_NAME = 'toothpaste_toothbrush.jpg'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 15),
                          hours_tpl=(),
                          completion_time=15/60.)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


class StudyScienceAction(_Action):
    TITLE = 'General science'
    ICON_IMAGE_NAME = 'book_pictogram.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=1)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


# ---------------------------------------------------------------------------------------------------
class _Subject(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @abc.abstractproperty
    def TITLE(self):
        pass

    # Filler-subjects have no requirements.
    @abc.abstractproperty
    def FILLER(self):
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

    # From 0 to 1; used as a weight factor for goal completion ratio
    @abc.abstractproperty
    def IMPORTANCE(self):
        pass


# Paste-template
"""
class (_Subject):
    TITLE =
    FILLER =
    BAR_COLOR =
    ICON_IMAGE_NAME =
    ACTIONS_SEQUENCE =
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS =
    IMPORTANCE =

"""


class AthleticsSubject(_Subject):
    TITLE = 'Athletics'
    FILLER = None
    BAR_COLOR = 'purple'
    ICON_IMAGE_NAME = 'fight_stance.png'
    ACTIONS_SEQUENCE = (RunningAction,
                        UpperBodyAction,
                        LowerBodyAction,
                        MMAAction,
                        GunsTrainingAction)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False
    IMPORTANCE = 1


class PhysicsSubject(_Subject):
    TITLE = 'Physics'
    FILLER = None
    BAR_COLOR = 'blue'
    ICON_IMAGE_NAME = 'nasa_sun.png'
    ACTIONS_SEQUENCE = (Course1Action,
                        Course2Action,
                        Course3Action)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = (6, set(ACTIONS_SEQUENCE))
    IMPORTANCE = 1


class ProgrammingSubject(_Subject):
    TITLE = 'Programming'
    FILLER = None
    BAR_COLOR = 'green'
    ICON_IMAGE_NAME = 'programming.png'
    ACTIONS_SEQUENCE = (ProgrammingAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = None
    IMPORTANCE = 1


class TeachingSubject(_Subject):
    TITLE = 'Teaching'
    FILLER = True
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = 'teaching_pictogram.png'
    ACTIONS_SEQUENCE = (TeachingAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False
    IMPORTANCE = 0


class HealthSubject(_Subject):
    TITLE = 'Health'
    FILLER = False
    BAR_COLOR = 'light_blue'
    ICON_IMAGE_NAME = 'medicine.png'
    ACTIONS_SEQUENCE = (SleepStartAction, BreaksAction, TeethAction)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False
    IMPORTANCE = 1


class ScienceSubject(_Subject):
    TITLE = 'Science'
    FILLER = False
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = 'science.png'
    ACTIONS_SEQUENCE = (StudyScienceAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False
    IMPORTANCE = .5


ALL_SUBJECTS = sorted(_Subject.__subclasses__())
DISPLAYED_SUBJECTS = (AthleticsSubject, PhysicsSubject, ProgrammingSubject, ScienceSubject, HealthSubject, TeachingSubject)

# (Needed only for initializations)
DUMMY_SUBJ_CLASS = DISPLAYED_SUBJECTS[0]
DUMMY_ACTION_CLASS = DISPLAYED_SUBJECTS[0].ACTIONS_SEQUENCE[0]


# ---------------------------------------------------------------------------------------------------
class MyProgressBar(Widget):
    DEFAULT_FILLED_COLOR = 0,1,0,1
    DEFAULT_EMPTY_COLOR = 1,0,0,1
    filled_color = ListProperty(DEFAULT_FILLED_COLOR)
    empty_color = ListProperty(DEFAULT_EMPTY_COLOR)
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


class ConfinedTextLabel(Label):
    pass


# Class code below (including the corresponding in .kv file)
# by Alexander Taylor
# from https://github.com/kivy/kivy/wiki/Scrollable-Label
class ScrollLabel(ScrollView):
    pass


class CitationsBox(BoxLayout):
    # TODO: Grid buttons need to maintain ratio, without resorting to fixed size.
    def __init__(self, **kwargs):
        super(CitationsBox, self).__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text='Citations', size_hint_y=.2, bold=True))
        self.grid = GridLayout(cols=3)
        self.add_widget(self.grid)
        self.populate_grid()
        self.popup = Popup(title='', size_hint=[.9, .7], separator_color=(0, 0, 0, 0))
        self.popup_image = Image(source='')
        self.popup_text_label = ScrollLabel(text='')
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.popup_image)
        box.add_widget(self.popup_text_label)
        self.popup.add_widget(box)

    @staticmethod
    def image_path(im_name):
        return '/'.join([THIRD_PARTIES_IMAGES_DIR, im_name])

    def populate_grid(self):
        for im_name, citation_obj in citations.FIRST_IMAGE_TO_CITATION_MAP.items():
            im_path = self.image_path(im_name=im_name)
            b = Button(background_normal=im_path, size_hint=(None, None), width='50sp', height='50sp', border=(0,0,0,0))
            b.image_name = im_name
            b.image_text = citation_obj.full_text()
            b.bind(on_release=self.update_popup_and_open)
            self.grid.add_widget(b)

    def update_popup_and_open(self, *args):
        im_name = args[0].image_name
        self.popup_image.source = self.image_path(im_name=im_name)
        self.popup_text_label.text = args[0].image_text
        self.popup.open()


class PaintedLabel(Label):
    pass


# ---------------------------------------------------------------------------------------------------
class SubjectSelectionSlide(GridLayout):
    subj = ObjectProperty(DISPLAYED_SUBJECTS[0])

    def __init__(self, **kwargs):
        super(SubjectSelectionSlide, self).__init__(cols=3, spacing=('2sp', '2sp'), **kwargs)
        self.populate_page()

    def set_slide_to_actions(self, *args):
        self.parent.parent.load_next()

    def populate_page(self, *args):
        for subj in DISPLAYED_SUBJECTS:
            box = BoxLayout(orientation='vertical', pos_hint=CENTER_POS_HINT)
            im_path = image_path(im_name=subj.ICON_IMAGE_NAME)
            box.add_widget(Image(source=im_path))
            box.add_widget(Label(text=subj.TITLE))
            float_layout = FloatLayout()
            button = Button(pos_hint=CENTER_POS_HINT)
            button.bind(on_release=lambda _, subj=subj: setattr(self, 'subj', subj))
            button.bind(on_release=self.set_slide_to_actions)
            float_layout.add_widget(button)
            float_layout.add_widget(box)
            self.add_widget(float_layout)
        self.add_widget(Label())


class SubjectBar(MyProgressBar):
    subj = ObjectProperty(DUMMY_SUBJ_CLASS)
    subj_dict = DictProperty()

    def __init__(self, **kwargs):
        super(SubjectBar, self).__init__(**kwargs)


class SubjectBarBox(BoxLayout):
    subj = ObjectProperty(DUMMY_SUBJ_CLASS)
    image_path = StringProperty()

    def __init__(self, **kwargs):
        super(SubjectBarBox, self).__init__(**kwargs)
        self.on_subj()

    def on_subj(self, *args):
        self.image_path = image_path(im_name=self.subj.ICON_IMAGE_NAME)


class SubjectsBarsBox(BoxLayout):

    def __init__(self, **kwargs):
        super(SubjectsBarsBox, self).__init__(spacing='1sp', **kwargs)
        self.populate_box()

    def populate_box(self, *args):
        for subj in DISPLAYED_SUBJECTS:
            widg = SubjectBarBox()
            widg.subj = subj
            im_name = subj.ICON_IMAGE_NAME
            widg.image_path = image_path(im_name=im_name)
            self.add_widget(widg)


class ActionImageAndLabels(BoxLayout):
    action = ObjectProperty()


class ActionsGrid(GridLayout):
    subj = ObjectProperty(DUMMY_SUBJ_CLASS)
    action = ObjectProperty()

    def __init__(self, **kwargs):
        super(ActionsGrid, self).__init__(cols=3, **kwargs)
        self.populate_grid()

    def populate_grid(self):
        self.clear_widgets()

        for act in self.subj.ACTIONS_SEQUENCE:
            button = Button(pos_hint=CENTER_POS_HINT)
            button.bind(on_release=lambda _, act=act: setattr(self, 'action', act))
            float_layout = FloatLayout()
            float_layout.add_widget(button)
            float_layout.add_widget(ActionImageAndLabels(action=act, pos_hint=CENTER_POS_HINT))
            self.add_widget(float_layout)

        self.action = self.subj.ACTIONS_SEQUENCE[0]


class TimesButtonsBox(BoxLayout):
    # "h" or "'"
    measuring_unit = StringProperty()
    times_seq = ListProperty()
    time_added = NumericProperty()

    def increase_time_added(self, btn):
        self.time_added += btn.time_val

    def on_times_seq(self, *args):
        self.clear_widgets()

        for t in self.times_seq:
            txt = '{}{}'.format(t, self.measuring_unit)
            button = Button(text=txt)

            if self.measuring_unit == 'h':
                pass
            elif self.measuring_unit == "'":
                t /= 60.
            else:
                raise NotImplementedError('Unexpected measuring unit. ({})'.format(self.measuring_unit))
            button.time_val = t
            button.bind(on_release=self.increase_time_added)
            self.add_widget(button)

    def reset_time_added(self, time):
        Clock.schedule_once(lambda *_: setattr(self, 'time_added', 0), time)


class ActionTimesBox(BoxLayout):
    action = ObjectProperty(DUMMY_ACTION_CLASS)
    description = StringProperty()
    minutes_lst = ListProperty()
    hours_lst = ListProperty()

    def __init__(self, **kwargs):
        super(ActionTimesBox, self).__init__(**kwargs)
        self.set_times_lists()

    def reset_times_lists(self, *args):
        self.minutes_lst = ()
        self.hours_lst = ()

    def set_times_lists(self, *args):
        time_data = self.action.TIME_DATA
        if not time_data:
            self.reset_times_lists()
            return

        self.minutes_lst = time_data.minutes_tpl
        self.hours_lst = time_data.hours_tpl


class FocusButton(Button):
    focus_percent = NumericProperty()

    def __init__(self, **kwargs):
        super(FocusButton, self).__init__(**kwargs)
        self.popup = Popup(title='Focus percentage: ', title_color=(0,0,0,1),
                           size_hint=[.9, .7], separator_color=(0, 0, 0, 0))
        self.buttons_box = GridLayout(cols=3)
        self.popup.add_widget(self.buttons_box)
        self.populate_buttons_box()
        self.bind(on_release=self.popup.open)

    def populate_buttons_box(self, *args):
        for n in xrange(10, 101, 10):
            b = Button(text=str(n))
            b.val = n
            b.bind(on_release=self.set_focus_percent_and_dismiss)
            self.buttons_box.add_widget(b)

    def set_focus_percent_and_dismiss(self, *args):
        self.focus_percent = args[0].val
        self.popup.dismiss()


class DayLabel(Label):
    def __init__(self, **kwargs):
        super(DayLabel, self).__init__(**kwargs)


class DayBox(FloatLayout):
    focus = NumericProperty()
    hours = NumericProperty()
    goals = NumericProperty()

    def __init__(self, **kwargs):
        super(DayBox, self).__init__(**kwargs)


class CalendarPage(BoxLayout):
    previous_goals_hours_focus_dct = {}
    MAX_DAYS_DISPLAYED = 30

    def __init__(self, **kwargs):
        super(CalendarPage, self).__init__(**kwargs)
        self.days_grid = GridLayout(cols=5)
        self.add_widget(self.days_grid)
        self.day_label = DayLabel(size_hint_y=.2)
        self.add_widget(self.day_label)
        self.add_widget(CreateHistoryButton(size_hint=(.5, .1)))

    def update_averages_label(self, *args):
        self.day_label.focus = self.average_focus
        self.day_label.hours = self.average_hours
        self.day_label.goals = self.average_goals

    def _average_x_attr(self, attr_name):
        n = len(self.previous_goals_hours_focus_dct) or 1
        tot = sum((d[attr_name] for d in self.previous_goals_hours_focus_dct.values()))
        return tot / float(n)

    @property
    def average_hours(self):
        return self._average_x_attr(attr_name='hours')

    @property
    def average_goals(self):
        return self._average_x_attr(attr_name='goals')

    @property
    def average_focus(self):
        """Average focus is calculated differently.
        Since 0-valued focus is impossible unless omitted, 0-valued focus is ignored."""
        n = 0
        tot = 0
        for d in self.previous_goals_hours_focus_dct.values():
            focus_val = d['focus']
            if focus_val:
                tot += focus_val
                n += 1
        if n:
            return tot / float(n)
        else:
            return '?'

    def populate_or_update_days_grid(self, *args):
        self.days_grid.clear_widgets()
        store = self.app.stored_data
        day = datetime.date.today() - datetime.timedelta(days=self.MAX_DAYS_DISPLAYED)
        for n in xrange(0, self.MAX_DAYS_DISPLAYED):
            day += datetime.timedelta(days=1)
            day_as_str = day.isoformat()
            if day_as_str in store:
                day_store = store[day_as_str]
                hours = day_store['productive_hours']
                focus = day_store['focus_percent']
                goals = day_store['goal_ratio']
                if len(self.days_grid.children) == self.MAX_DAYS_DISPLAYED:
                    child = self.days_grid.children[n]
                    child.hours = hours
                    child.focus = focus
                    child.goals = goals
                else:
                    day_box = DayBox()
                    day_box.hours = hours
                    day_box.focus = focus
                    day_box.goals = goals
                    self.days_grid.add_widget(day_box)
                self.previous_goals_hours_focus_dct[day_as_str] = dict(hours=hours, goals=goals, focus=focus)
            else:
                self.days_grid.add_widget(PaintedLabel(label_background=(0,0,0,1)))


class CreateHistoryButton(Button):
    """
    Used for setting history to default history,
    when for example the app is installed for the first time on a device.
    """
    def __init__(self, **kwargs):
        super(CreateHistoryButton, self).__init__(text='Restore old history', background_color=(1,.5,0,1), **kwargs)
        self.popup_widg = None

    def create_popup(self, *args):
        self.popup_widg = Popup(title='[b]Replace existing history with default?[/b] \n(this can [b]not[/b] be undone)',
                                size_hint=[.9, .3], separator_color=(0, 0, 0, 0), title_color=(0,0,0,1))
        yes_button = Button(text='YES', background_color=[1, 0, 0, 1])
        yes_button.bind(on_release=self.popup_widg.dismiss)
        yes_button.bind(on_release=self.app.replace_history_with_default)
        no_button = Button(text='NO', background_color=[0, 2, 0, 1])
        no_button.bind(on_release=self.popup_widg.dismiss)
        popup_box = BoxLayout()
        popup_box.add_widget(yes_button)
        popup_box.add_widget(no_button)
        self.popup_widg.add_widget(popup_box)

    def on_release(self, *args):
        if not self.popup_widg:
            self.create_popup()
        self.popup_widg.open()


class TodayPage(Carousel):
    def __init__(self, **kwargs):
        super(TodayPage, self).__init__(loop=True, **kwargs)


class MainWidget(Carousel):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


# ---------------------------------------------------------------------------------------------------
class EffRpgApp(App):
    DEFAULT_STORAGE_NAME = 'storage.json'
    LOWERCASE_SUBJECTS_NAMES = []
    # Each change adds 1 in order to be able to constantly use the Property,
    # without redundant checks, and val reset.
    subj_dicts_changed = NumericProperty(0)
    focus_percent = NumericProperty(0)
    goal_ratio = 0
    productive_hours = 0

    def build(self):
        main_widg = MainWidget()
        return main_widg

    def on_pause(self, *args):
        return True

    def __init__(self, **kwargs):
        super(EffRpgApp, self).__init__(**kwargs)
        self.increment_subj_dicts_changed_scheduled_event = None
        self.today = ''
        self.set_today()
        Clock.schedule_interval(self.set_today, 30*60)
        # Storage file is checked/stored in different dir on androids
        # to avoid overwriting it during updates.
        storage_file_name = self.DEFAULT_STORAGE_NAME
        if platform == 'android':
            storage_file_name = '/'.join([str(self.user_data_dir), storage_file_name])
        elif platform in ('ios', 'win'):
            raise NotImplementedError('Platform not implemented. Storage will be overridden on updates.')
        self.stored_data = JsonStore(storage_file_name, indent=4, sort_keys=True)
        if self.stored_data and (self.today in self.stored_data):
            self.add_subjs_and_acts_added_by_new_version()
            self.update_subjs_dicts_from_store()
        else:
            self.store_today_data()
        self.storage_scheduled_event = None

    def replace_history_with_default(self, *args):
        default_history = JsonStore(self.DEFAULT_STORAGE_NAME)
        self.stored_data.clear()
        for k in default_history:
            self.stored_data[k] = default_history[k]

    def update_subjs_dicts_from_store(self):
        for k1, v1 in self.stored_data[self.today].items():
            if k1 != 'subjects_dict':
                setattr(self, k1, copy.deepcopy(v1))
            else:
                for k2, v2 in v1.items():
                    setattr(self, k2, copy.deepcopy(v2))

    def schedule_storing(self, time=None):
        time = time or 2.
        if self.storage_scheduled_event:
            self.storage_scheduled_event.cancel()
        self.storage_scheduled_event = Clock.schedule_once(self.store_today_data, time)

    def add_subjs_and_acts_added_by_new_version(self):
        today_subjs_dct = self.stored_data[self.today]['subjects_dict']
        for s_name in self.LOWERCASE_SUBJECTS_NAMES:
            subj_dct = today_subjs_dct.setdefault(s_name, {})
            for act_name in getattr(self, s_name):
                subj_dct.setdefault(act_name, DEFAULT_ACTION_VALUE_IN_STORE)

    def day_dict(self):
        self.daily_goal_ratio_and_time()    # (creates hours and goals)
        day_dct = {'focus_percent': self.focus_percent,
                   'productive_hours': self.productive_hours,
                   "goal_ratio": self.goal_ratio,
                   'subjects_dict': {}}
        for s_name in self.LOWERCASE_SUBJECTS_NAMES:
            day_dct['subjects_dict'].update({s_name: getattr(self, s_name)})
        return day_dct

    def store_today_data(self, *args):
        self.stored_data[self.today] = self.day_dict()

    def set_today(self, *args):
        self.today = datetime.date.today().isoformat()

    def on_focus_percent(self, *args):
        self._on_subj_dict_base()

    def modify_action(self, subj, act, time_added):
        """Modifies subject's DictProperty.

        :param subj: (class)
        :param act: (class)
        :param time_added: (float)
        :return: (None)
        """
        subj_n = subj.name()
        act_n = act.name()
        # (e.g. athletics[cardioaction])
        old_time, old_compl_ratio = getattr(self, subj_n)[act_n]
        tot_time = time_added + old_time

        compl_ratio = act.completion_ratio(hours_invested=tot_time)
        if compl_ratio == 'undefined':
            compl_ratio = not old_compl_ratio
            tot_time = 1.
        subj_dct = getattr(self, subj_n)
        subj_dct[act_n] = (tot_time, compl_ratio)

    def subj_goal_ratio_and_time(self, subj):
        subj_dct = getattr(self, subj.name())
        acts_seq = subj.ACTIONS_SEQUENCE
        n = 0
        tot_ratio_achieved = 0.
        tot_hours = 0.

        cumulative_compl_tpl = subj.CUMULATIVE_COMPLETION_TIME_AND_ACTIONS
        if cumulative_compl_tpl:
            # (cumulative time is considered as a hint==1)
            cumulative_compl_time = cumulative_compl_tpl[0]
            n += cumulative_compl_time
            relevant_actions = cumulative_compl_tpl[1]
            relevant_acts_time = 0
            for a in relevant_actions:
                a_name = a.name()
                hint = a.BAR_GOAL_HINT
                hours = subj_dct[a_name][0]
                tot_hours += hours
                relevant_acts_time += hours
                tot_ratio_achieved += subj_dct[a_name][1] * hint
                n += hint
            tot_ratio_achieved += min(cumulative_compl_time, relevant_acts_time)
        else:
            for a in acts_seq:
                a_name = a.name()
                hint = a.BAR_GOAL_HINT
                tot_hours += subj_dct[a_name][0]
                tot_ratio_achieved += subj_dct[a_name][1] * hint
                n += hint

        n = n or 1  # (avoid ZeroDivisionError)
        return tot_ratio_achieved/n, tot_hours

    def daily_goal_ratio_and_time(self):
        n = 0.
        ratios_sum = 0.
        tot_hours = 0.
        for s in ALL_SUBJECTS:
            subj_importance = s.IMPORTANCE
            n += subj_importance
            subj_ratio, subj_time = self.subj_goal_ratio_and_time(subj=s)
            tot_hours += subj_time
            if not s.FILLER:
                ratios_sum += subj_ratio * subj_importance
        self.goal_ratio = ratios_sum/n
        self.productive_hours = tot_hours
        return self.goal_ratio, tot_hours

    def _on_subj_dict_base(self, *args):
        # Scheduling used in order to avoid lots of redundant operations during storage.
        if self.increment_subj_dicts_changed_scheduled_event:
            self.increment_subj_dicts_changed_scheduled_event.cancel()
        self.increment_subj_dicts_changed_scheduled_event = Clock.schedule_once(self.increment_subj_dicts_changed, .2)

    def on_subj_dicts_changed(self, *args):
        self.schedule_storing()

    def increment_subj_dicts_changed(self, *args):
        self.subj_dicts_changed += 1

# Create tracked properties of all subjects and their actions.
DEFAULT_ACTION_VALUE_IN_STORE = (0., False)

def actions_dct_for_storage(subj):
    return {a.name(): DEFAULT_ACTION_VALUE_IN_STORE for a in subj.ACTIONS_SEQUENCE}

SUBJS_DICTS_DCT = {}
for s in ALL_SUBJECTS:
    s_name = s.name()
    act_d = {a.name(): DEFAULT_ACTION_VALUE_IN_STORE for a in s.ACTIONS_SEQUENCE}
    setattr(EffRpgApp, s_name, DictProperty(act_d))
    setattr(EffRpgApp, 'on_' + s_name, EffRpgApp._on_subj_dict_base)
    EffRpgApp.LOWERCASE_SUBJECTS_NAMES.append(s_name)
    SUBJS_DICTS_DCT.update({s_name: act_d})


if __name__ == '__main__':

    try:
        import ignore_build_ensure_images_cited
    except ImportError:
        pass

    EffRpgApp().run()
