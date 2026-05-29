class StateManager:
    # State Pattern: one active scene handles events, updates, and drawing.
    def __init__(self):
        self.current_scene = None
        self.running = True

    def set_scene(self, scene):
        self.current_scene = scene

    def quit(self):
        self.running = False

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self):
        if self.current_scene:
            self.current_scene.draw()

