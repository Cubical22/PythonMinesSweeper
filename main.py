from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty
from kivy.clock import Clock

from generation import *
from globalVal import LAYOUT_CHANGE_BREAK_POINT, VERTICAL_SCROLL_VIEW_MAX_HEIGHT,VERTICAL_SCROLL_VIEW_MIN_HEIGHT, HORIZONTAL_LABEL_MIN_WIDTH, PARTICLE_COUNT
from classes.Particle import Particle
from classes.CellButton import CellButton

import random

Window.size = (902, 451)

class MainModal(Widget):
    pass

class MainLayout(BoxLayout):
    massage_label = ObjectProperty()
    Grid = ObjectProperty()

    particles = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update, 1/60)

    def particleInit(self, width):
        for _ in range(PARTICLE_COUNT):
            x = random.random() * width
            g = random.random() # g stands for color gradient
            self.particles.append(Particle(x, 0, g, self.height))

    def update(self, dt):
        for particle in self.particles:
            particle.update(self.canvas.before, dt, self.height)

    def on_parent(self, *args):
        self.on_size()

    def on_size(self, *args):
        ratio = self.width/ self.height
        if ratio < LAYOUT_CHANGE_BREAK_POINT:
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

        self.update_massage_display(ratio < LAYOUT_CHANGE_BREAK_POINT)

        if len(args) != 0 and len(self.particles) < PARTICLE_COUNT:
            self.particleInit(args[1][0])

        # There are probably better ways to do this, but for now
        # since on the resize function, you get the size of your parent
        # I am using this to simply spawn particles

        if len(self.ids) != 0:
            self.ids.Grid.shouldResize = True

    def update_massage_display(self, is_vertical):
        if is_vertical:
            self.massage_label.size_hint = (1,None)
            self.massage_label.height = "50dp"
        elif self.massage_label is not None:
            self.massage_label.size_hint = (1,1)

class GridDisplay(GridLayout):
    lastRatio = None
    shouldResize = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = CELLCOUNT
        self.cellsInit()
        self.spacing = str(MAIN_INTERFACE_SPACE) + "dp"
        self.padding = str(MAIN_INTERFACE_SPACE) + "dp"

        Clock.schedule_interval(self.update, 1/60)

    def cellsInit(self):
        # generating all the buttons
        for y in range(CELLCOUNT):
            row = []
            for x in range(CELLCOUNT):
                button = CellButton(text="", background_color=(.5,.5,.5,1))
                button.xIndex = x
                button.yIndex = y
                button.bind(on_press=button.callCell)
                self.add_widget(button)
                row.append(button)
            cells.append(row)

        generateBombs()
        updateAdjBombs()

    def update(self, *args):
        screen = self.parent.parent.parent
        ratio = screen.width / screen.height # the `parent.parent` refers to the main holder

        if self.lastRatio == ratio and not self.shouldResize:
            self.shouldResize = False
            return

        self.lastRatio = ratio

        if ratio < LAYOUT_CHANGE_BREAK_POINT:
            self.size_hint = (1, None)
            self.height = self.width

            self.parent.size_hint = (1, None)
            self.parent.height = self.height

            #making maximum and minimum sizes for the `ScrollView`
            if self.parent.height < VERTICAL_SCROLL_VIEW_MIN_HEIGHT:
                self.parent.height = VERTICAL_SCROLL_VIEW_MIN_HEIGHT
            elif self.parent.height > VERTICAL_SCROLL_VIEW_MAX_HEIGHT:
                self.parent.height = VERTICAL_SCROLL_VIEW_MAX_HEIGHT
        else:
            self.size_hint = (None, 1)
            self.width = self.height

            self.parent.size_hint = (None, 1)
            self.parent.width = self.width

            # making a minimum width for the score display label
            # by limiting the width of the scroll view
            gridMaxWidth = self.parent.parent.width - HORIZONTAL_LABEL_MIN_WIDTH
            if self.parent.width > gridMaxWidth:
                self.parent.width = gridMaxWidth

class MinesSweeperApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Mines Sweeper"

MinesSweeperApp().run()