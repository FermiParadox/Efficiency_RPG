# -*- coding: utf-8 -*-

# Used for screenshots that match size of current screenshots in GooglePlay


if 1:
    from kivy.config import Config
    Config.set('graphics', 'width', '410')
    Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.button import Button as Button
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
import os


__version__ = '0.0.1'

APP_NAME = 'EffRpg'

# PASTE-TEMPLATE
"""

    def __init__(self, **kwargs):
        super(, self).__init__(**kwargs)

"""


# ---------------------------------------------------------------------------------------------------
OWN_IMAGES_DIR = 'own_images'
THIRD_PARTY_IMAGES_DIR = 'third_parties_images'


def image_path(im_name):
    if im_name in os.listdir(OWN_IMAGES_DIR):
        return os.path.join(OWN_IMAGES_DIR, im_name)
    elif im_name in os.listdir(THIRD_PARTY_IMAGES_DIR):
        return os.path.join(THIRD_PARTY_IMAGES_DIR, im_name)
    else:
        print('\nWARNING: Image name not found in directories. ({})\n'.format(im_name))


# ---------------------------------------------------------------------------------------------------
# Misc
CENTER_POS_HINT = {'center_x': .5, 'center_y': .5}

FAINT_BLACK = (0,0,0,.1)

POPULATING_DELAY = .3


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


# Paste-template
"""
_TimeData(description=,
    minutes_tpl=,
    hours_tpl=,
    completion_time=)

"""


# ---------------------------------------------------------------------------------------------------
# All actions should contain "Action" in their name,
# in order to avoid accidental overriding of methods in kivy-app.
class _Action(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def completion_ratio(cls, hours_invested):
        time_data = cls.TIME_DATA
        if time_data:
            completion_time = time_data.completion_time

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


class FocusAction(_Action):
    TITLE = 'Focus'
    ICON_IMAGE_NAME = 'aim.png'
    TIME_DATA = _TimeData(description="Mins wasted / 10' ",
                          minutes_tpl=(1, 2, 5),
                          hours_tpl=(),
                          completion_time=None)
    BAR_GOAL_HINT = 0
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class RunningAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'heart.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(5, 10, 30),
                          hours_tpl=(1,),
                          completion_time=1.)
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


class BreaksAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'resting.png'
    TIME_DATA = None
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class SleepStartAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'sleep_early.png'
    TIME_DATA = None
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = True
    DAYS_APPEARING = 'all'


class StudyScienceAction(_Action):
    TITLE = ''
    ICON_IMAGE_NAME = 'book_pictogram.png'
    TIME_DATA = _TimeData(description='',
                          minutes_tpl=(10, 30),
                          hours_tpl=(1, 2, 5),
                          completion_time=None)
    BAR_GOAL_HINT = 1
    MARK_WHEN_OMITTED = False
    DAYS_APPEARING = 'all'


# ---------------------------------------------------------------------------------------------------
class _Subject(object):
    """
    A subject (e.g. "athletics") contains various "actions" (e.g. aerobic).

    Non-"filler" subjects have their own bar (e.g. "athletics"),
    otherwise they fill existing bars (e.g. "failed_goals") and
    are taken into account in productivity estimation.
    """

    __metaclass__ = abc.ABCMeta

    @classmethod
    def name(cls):
        return cls.__name__.lower()

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
    ACTIONS_SEQUENCE = (RunningAction,
                        UpperBodyAction,
                        LowerBodyAction,
                        MMAAction)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class Physics(_Subject):
    TITLE = 'Physics'
    FILLER_PRIORITY = None
    BAR_COLOR = 'blue'
    ICON_IMAGE_NAME = 'nasa_sun.png'
    ACTIONS_SEQUENCE = (Course1Action,
                        Course2Action,
                        Course3Action,
                        FocusAction)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = (6, set(ACTIONS_SEQUENCE) - {FocusAction})


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
    ACTIONS_SEQUENCE = (SleepStartAction, BreaksAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class Science(_Subject):
    TITLE = 'Science'
    FILLER_PRIORITY = None
    BAR_COLOR = 'light_green'
    ICON_IMAGE_NAME = 'science.png'
    ACTIONS_SEQUENCE = (StudyScienceAction,)
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


class FailedGoals(_Subject):
    TITLE = 'Failed goals'
    FILLER_PRIORITY = 1
    BAR_COLOR = 'red'
    ICON_IMAGE_NAME = ''
    ACTIONS_SEQUENCE = ()
    CUMULATIVE_COMPLETION_TIME_AND_ACTIONS = False


ALL_SUBJECTS = sorted(_Subject.__subclasses__())
DISPLAYED_SUBJECTS = (Athletics, Physics, Programming, Science, Health,)

# (Needed only for initializations)
DUMMY_SUBJ_CLASS = DISPLAYED_SUBJECTS[0]


# ---------------------------------------------------------------------------------------------------
class MyProgressBar(Widget):
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


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
            if subj == FailedGoals:
                continue
            box = BoxLayout(orientation='vertical', pos_hint=CENTER_POS_HINT)
            im_path = image_path(im_name=subj.ICON_IMAGE_NAME)
            box.add_widget(Image(source=im_path))
            box.add_widget(Label(text=subj.TITLE, text_size=self.size, valign='top', halign='center'))
            float_layout = FloatLayout()
            float_layout.add_widget(box)
            button = Button(background_color=FAINT_BLACK, pos_hint=CENTER_POS_HINT)
            button.bind(on_release=lambda _, subj=subj: setattr(self, 'subj', subj))
            button.bind(on_release=self.set_slide_to_actions)
            float_layout.add_widget(button)
            self.add_widget(float_layout)


# ---------------------------------------------------------------------------------------------------
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


class ActionsGrid(GridLayout):
    subj = ObjectProperty(DUMMY_SUBJ_CLASS)
    action = ObjectProperty()

    def __init__(self, **kwargs):
        super(ActionsGrid, self).__init__(cols=3, **kwargs)
        self.populate_grid()

    def populate_grid(self):
        self.clear_widgets()

        for act in self.subj.ACTIONS_SEQUENCE:
            im_path = image_path(im_name=act.ICON_IMAGE_NAME)
            float_layout = FloatLayout()
            float_layout.add_widget(Image(source=im_path, pos_hint=CENTER_POS_HINT))
            button = Button(background_color=FAINT_BLACK, pos_hint=CENTER_POS_HINT)
            button.bind(on_release=lambda _, act=act: setattr(self, 'action', act))
            float_layout.add_widget(button)
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
    action = ObjectProperty()
    description = StringProperty()
    minutes_lst = ListProperty()
    hours_lst = ListProperty()

    def __init__(self, **kwargs):
        super(ActionTimesBox, self).__init__(**kwargs)

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





class TodayPage(Carousel):
    pass


class MainWidget(Carousel):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


# ---------------------------------------------------------------------------------------------------
"""# Storage file is checked/stored in different dir on androids
# to avoid overwriting it during updates.
storage_file = 'storage.json'
if platform == 'android':
    storage_file = '/'.join([str(App.user_data_dir), storage_file])
elif platform in ('ios', 'win'):
    raise NotImplementedError('Platform not implemented. Storage will be overridden on updates.')
_store = JsonStore(storage_file)
if not _store:
   """

class EffRpgApp(App):
    # Each change adds 1 in order to be able to constantly use the Property,
    # without redundant checks, and val reset.
    SUBJS_LOWER_NAMES = []
    subj_dicts_changed = NumericProperty(0)

    def build(self):
        main_widg = MainWidget()
        return main_widg

    def modify_action(self, subj, act, time_added):
        """Modifies subject's DictProperty.

        :param subj: (class)
        :param act: (class)
        :param time_added: (float) or 'same'
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
        print '====='
        print subj_n, act, (tot_time, compl_ratio)
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
        print tot_ratio_achieved, n, subj
        return tot_ratio_achieved/n, tot_hours

    def daily_goal_ratio_and_time(self):
        n = len(ALL_SUBJECTS)
        tot_ratio_achieved = 0.
        tot_hours = 0.
        for s in ALL_SUBJECTS:
            new_t, new_r = self.subj_goal_ratio_and_time(subj=s)
            tot_ratio_achieved += new_t
            tot_hours += new_r
        return tot_ratio_achieved/n, tot_hours

    def _on_subj_dict_base(self, *args):
        self.subj_dicts_changed += 1

# Create tracked properties of all subjects and their actions.
DEFAULT_ACTION_VALUE_IN_STORE = (0., False)

for s in ALL_SUBJECTS:
    s_name = s.name()
    d = {a.name(): DEFAULT_ACTION_VALUE_IN_STORE for a in s.ACTIONS_SEQUENCE}
    setattr(EffRpgApp, s_name, DictProperty(d))
    setattr(EffRpgApp, 'on_' + s_name, EffRpgApp._on_subj_dict_base)
    EffRpgApp.SUBJS_LOWER_NAMES.append(s_name)


if __name__ == '__main__':

    try:
        import ignore_build_ensure_images_cited
    except ImportError:
        pass

    EffRpgApp().run()
