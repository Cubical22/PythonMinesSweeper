from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.app import App

class HelperButton(Button):
    abilityIndex = NumericProperty()
    # Ability Indexes:
    # 0: Cell Reveal, 1: Safe Click, 2: Board Change

    mainLayout = None

    def helperPressed(self):
        app = App.get_running_app()
        match self.abilityIndex:
            case 0:
                if not app.usingCellReveal:
                    app.usingCellReveal = True
                    if self.mainLayout is None:
                        self.mainLayout = self.parent.parent.parent.ids.mainLayout

                    self.mainLayout.toggleBackgroundForAbility()
            case 1:
                print("case 1 is not done yet")
            case 2:
                print("case 2 is not done yet")