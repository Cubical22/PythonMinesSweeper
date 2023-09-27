from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.app import App

class HelperButton(Button):
    abilityIndex = NumericProperty()
    # Ability Indexes:
    # 0: Cell Reveal, 1: Safe Click, 2: Board Change

    def helperPressed(self):
        app = App.get_running_app()
        if self.abilityIndex == 0: # Cell Reveal
            if not app.usingCellReveal:
                print("using cell reveal")
                app.usingCellReveal = True