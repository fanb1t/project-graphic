class BaseScene:
    # Base interface for every screen/state in the game.
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.assets = app.assets
        self.state_manager = app.state_manager

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

