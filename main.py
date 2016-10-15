# -*- coding: utf-8 -*-

# Used for screenshots that match size of current screenshots in GooglePlay
if 0:
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

from functools import partial


__version__ = '0.0.1'

APP_NAME = 'EffRpg'

# PASTE-TEMPLATE
"""

    def __init__(self, **kwargs):
        super(, self).__init__(**kwargs)

"""


# ---------------------------------------------------------------------------------------------------
class MyProgressBar(Widget):
    filled_ratio = NumericProperty(.01)
    empty_ratio = NumericProperty(.01)


class SubjectBarsBox(BoxLayout):
    def __init__(self, subj_obj, **kwargs):
        super(SubjectBarsBox, self).__init__(**kwargs)
        self.subj_obj = subj_obj


class EffRpgApp(App):
    def build(self):
        main_widg = MyProgressBar()
        return main_widg


if __name__ == '__main__':
    EffRpgApp().run()
