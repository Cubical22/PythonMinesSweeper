from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty
from kivy.clock import Clock

from generation import *
from globalVal import LAYOUT_CHANGE_BREAK_POINT, VERTICAL_SCROLL_VIEW_MAX_HEIGHT,VERTICAL_SCROLL_VIEW_MIN_HEIGHT, HORIZONTAL_LABEL_MIN_WIDTH, PARTICLE_COUNT
from classes.Particle import Particle
from classes.CellButton import CellButton

import random
import math

Window.size = (902, 451)

class OverlayHolder(RelativeLayout):
    currentTime = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.addToTime, 1/60)

    def won(self):
        self.ids.modal.ids.popupText.text = "you have won, with the time of {}"
        self.activateModal(2)

    def lost(self):
        self.ids.modal.ids.popupText.text = "you have lost"
        self.activateModal(1)

    def activateModal(self,state):
        self.ids.modal.opacity = 1
        self.ids.modal.disabled = False
        App.get_running_app().currentState = state

    def addToTime(self,dt):
        if dt:
            self.currentTime += dt

        # this section is used to update the time for the timer display label
        self.ids.mainLayout.ids.massage_label.text = str(math.floor(self.currentTime * 10) / 10)

class MainModal(Widget):
    def restartGame(self):
        self.opacity = 0
        self.disabled = True

        # region resetting the cells

        for y in range(CELLCOUNT):
            for x in range(CELLCOUNT):
                cells[x][y].background_color = (0.5,0.5,0.5,1)
                cells[x][y].text = ""
                cells[x][y].cellState = 0
                cells[x][y].cellHiddenState = 0
                cells[x][y].adjBombCount = 0

        generateBombs()
        updateAdjBombs()

        # endregion

        App.get_running_app().currentState = 0
        
    def on_touch_down(self, touch):
        if self.disabled:
            super().on_touch_down(touch) # touch happening over the modal
        else:
            return super().on_touch_down(touch) # only touch happening on the modal

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

    # region Main Sizing Functions
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

        if len(self.ids) != 0 and len(args) != 0:
            self.ids.Grid.updateSize({"width": args[1][0], "height": args[1][1]})

    def update_massage_display(self, is_vertical):
        if is_vertical:
            self.massage_label.size_hint = (1,None)
            self.massage_label.height = "50dp"
        elif self.massage_label is not None:
            self.massage_label.size_hint = (1,1)

    # endregion

class GridDisplay(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = CELLCOUNT
        self.cellsInit()
        self.spacing = str(MAIN_INTERFACE_SPACE) + "dp"
        self.padding = str(MAIN_INTERFACE_SPACE) + "dp"

    def cellsInit(self):
        # region generating all the buttons
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
        # endregion

        generateBombs()
        updateAdjBombs()

    def updateSize(self, screen):
        ratio = screen["width"] / screen["height"] # the `parent.parent` refers to the main holder

        if ratio < LAYOUT_CHANGE_BREAK_POINT:
            # region Horizontal Sizing for the grid and the scrollView
            self.size_hint = (1, None)
            self.height = self.width

            self.parent.size_hint = (1, None)
            self.parent.height = self.height

            #making maximum and minimum sizes for the `ScrollView`
            if self.parent.height < VERTICAL_SCROLL_VIEW_MIN_HEIGHT:
                self.parent.height = VERTICAL_SCROLL_VIEW_MIN_HEIGHT
            elif self.parent.height > VERTICAL_SCROLL_VIEW_MAX_HEIGHT:
                self.parent.height = VERTICAL_SCROLL_VIEW_MAX_HEIGHT
            # endregion
        else:
            # region Vertical Sizing for the grid and scrollView
            self.size = (screen["height"], screen["height"])

            self.parent.size_hint = (None, 1)
            self.parent.size = self.size

            print(screen["height"], self.parent.size)

            # making a minimum width for the score display label
            # by limiting the width of the scroll view
            gridMaxWidth = screen["width"] - HORIZONTAL_LABEL_MIN_WIDTH
            if self.parent.width > gridMaxWidth:
                self.parent.width = gridMaxWidth
                self.size_hint = (None , 1) # honestly, I don't understand anymore how any of these works
                # but, as long as it works, that's what matters
                self.width = self.height
            # endregion

class MinesSweeperApp(App):
    currentState = 0  # 0: none 1: lost 2: won

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Mines Sweeper"

MinesSweeperApp().run()