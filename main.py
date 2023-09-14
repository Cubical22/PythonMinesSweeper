from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from classes.CellButton import CellButton
from kivy.properties import ObjectProperty
from generation import *

Window.size = (600,600)

class MainLayout(BoxLayout):
    massage_label = ObjectProperty()

    def on_parent(self, *args):
        self.on_size()

    def on_size(self, *args):
        ratio = self.width/ self.height
        if ratio < 0.87:
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

        self.update_massage_display(ratio < 0.87)

    def update_massage_display(self, is_vertical):
        if is_vertical:
            self.massage_label.size_hint = (1,None)
            self.massage_label.height = "50dp"
        else:
            self.massage_label.size_hint = (1,1)

class GridDisplay(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = CELLCOUNT
        self.cellsInit()
        self.spacing = str(MAIN_INTERFACE_SPACE) + "dp"
        self.padding = str(MAIN_INTERFACE_SPACE) + "dp"

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

        print("generated")


class MinesSweeperApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Mines Sweeper"


MinesSweeperApp().run()