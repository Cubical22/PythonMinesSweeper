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

        if self.mainLayout is None:
            self.mainLayout = self.parent.parent.parent.ids.mainLayout

        match self.abilityIndex:
            case 0:
                if not app.usingCellReveal:
                    app.usingCellReveal = True

                    self.mainLayout.toggleBackgroundForAbility()
            case 1:
                if not app.usingSafeClick:
                    app.usingSafeClick = True

                    self.mainLayout.toggleBackgroundForAbility()
            case 2:
                self.mainLayout.resetBoard()