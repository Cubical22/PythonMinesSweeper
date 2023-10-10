from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color

from generation import *
from globalVal import LAYOUT_CHANGE_BREAK_POINT,\
    VERTICAL_SCROLL_VIEW_MAX_HEIGHT,VERTICAL_SCROLL_VIEW_MIN_HEIGHT, HORIZONTAL_LABEL_MIN_WIDTH, PARTICLE_COUNT
from classes.Particle import Particle
from classes.CellButton import CellButton

# even though this button is not used, it needs to be included for the kv file
from classes.HelperButton import HelperButton

import random
import math

Window.size = (902, 451)

class OverlayHolder(RelativeLayout):
    currentTime = 0
    timerInterval = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timerInterval = Clock.schedule_interval(self.addToTime, 1/60)

    def won(self):
        self.ids.modal.ids.popupText.text = "you have won"
        self.activateModal(2)

    def lost(self):
        self.ids.modal.ids.popupText.text = "you have lost"
        self.activateModal(1)

    def activateModal(self,state):
        if self.timerInterval is not None:
            self.timerInterval.release() # stopping the timer if your die or win
        self.ids.modal.ids.timeText.text = "Time: " + self.getTimerText()
        self.ids.modal.opacity = 1
        self.ids.modal.disabled = False
        App.get_running_app().currentState = state

    def addToTime(self,dt):
        if dt:
            self.currentTime += dt

        # this section is used to update the time for the timer display label
        self.ids.mainLayout.ids.massage_label.text = self.getTimerText()

    def getTimerText(self):
        return str(math.floor(self.currentTime * 10) / 10)

    def restartTimer(self):
        self.currentTime = 0
        if self.timerInterval is not None:
            self.timerInterval.release() # stopping the timer if your die or win
        self.timerInterval = Clock.schedule_interval(self.addToTime, 1/60)

class DialogModal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = False # note that here setting the disabled to True seems to make this act as a blocker
        # I might take advantage of that
        self.opacity = 0

class HelpersLayout(BoxLayout):
    # NOTE: the resize functionality on this guy, and
    # possibly everything else in this app, is handled on MainLayout
    # since we only need a single resize method, confirmed, it is on MainLayout
    # Absolutely not because that is where it was from the start
    def toggle(self, button): # the button var, refers to the button used to toggle the display on the helpers layout
        ratio = self.parent.width / self.parent.height
        if ratio < LAYOUT_CHANGE_BREAK_POINT: # the button does not exist while working with horizontal layout
            return

        self.opacity = 1 if self.disabled else 0
        self.disabled = not self.disabled

        # here we are toggling the distance from top, between the HelpersLayout height and the const dp(10) using
        # the disabled property set above
        button.pos = (dp(10), self.parent.height - button.height - (self.height if not self.disabled else dp(10)))
        
    def on_touch_down(self, touch):
        if self.opacity == 1:
            return super().on_touch_down(touch)
        else:
            super().on_touch_down(touch)

class MainModal(Widget):
    def restartGame(self):
        self.opacity = 0
        self.disabled = True

        # restarting the new timer
        self.parent.restartTimer()

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

    isOnFocusMode = False
    focusRect = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_interval(self.update, 1/60)

    # region particles
    def particleInit(self, width):
        for _ in range(PARTICLE_COUNT):
            x = random.random()
            g = random.random() # g stands for color gradient
            self.particles.append(Particle(x, 0, g, self.height, self.width))

    def update(self, dt):
        for particle in self.particles:
            particle.update(self.canvas.before, dt, self.height)

    def redrawAllParticles(self):
        for particle in self.particles:
            particle.rect = None # setting the rect to None makes the particle redraw the rect itself

    # endregion

    def on_parent(self, *args):
        self.on_size()

    #this function is used to toggle the background of the application to make ability stand out
    def toggleBackgroundForAbility(self):
        # toggle the helpers option first of all

        if not self.isOnFocusMode:
            self.parent.ids.HelpersLayout.toggle(self.parent.ids.HelpersDisplayButton)
            self.isOnFocusMode = True
            with self.canvas.before:
                Color(rgba=(0.1,0.1,0.1,0.9))
                self.focusRect = Rectangle(size=self.size, pos=self.pos)
        else:
            self.canvas.before.clear()
            self.redrawAllParticles()
            self.isOnFocusMode = False

    def resetBoard(self):
        self.parent.ids.HelpersLayout.toggle(self.parent.ids.HelpersDisplayButton)
        self.parent.ids.modal.restartGame() # since the restart was already implemented on the modal, I just reused it

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

            # this section is used to make the helpers layout and the activation button be disabled or enabled upon
            # resize
            disableFlag = ratio >= LAYOUT_CHANGE_BREAK_POINT
            opacityFlag = ratio < LAYOUT_CHANGE_BREAK_POINT
            self.parent.ids.HelpersLayout.disabled = disableFlag
            self.parent.ids.HelpersLayout.opacity = 1 if opacityFlag else 0
            self.parent.ids.HelpersDisplayButton.disabled = not disableFlag
            self.parent.ids.HelpersDisplayButton.opacity = 0 if opacityFlag else 1
            self.parent.ids.HelpersDisplayButton.pos = (dp(10), self.height -
                                                        self.parent.ids.HelpersDisplayButton.height - dp(10))

        if self.isOnFocusMode:
            self.focusRect.size = self.size
            self.focusRect.pos= self.pos

        for particle in self.particles:
            particle.xMultiplier = self.width

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
            # if self.parent.height < VERTICAL_SCROLL_VIEW_MIN_HEIGHT:
            #     self.parent.height = VERTICAL_SCROLL_VIEW_MIN_HEIGHT
            # elif self.parent.height > VERTICAL_SCROLL_VIEW_MAX_HEIGHT:
            #     self.parent.height = VERTICAL_SCROLL_VIEW_MAX_HEIGHT
            self.parent.height = max(min(self.parent.height, VERTICAL_SCROLL_VIEW_MAX_HEIGHT),
                                     VERTICAL_SCROLL_VIEW_MIN_HEIGHT)
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

    usingCellReveal = False
    usingSafeClick = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Mines Sweeper"

MinesSweeperApp().run()