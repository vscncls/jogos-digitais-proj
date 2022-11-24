class SoundController():
    def __init__(self) -> None:
        self.muted = False

    def toggle(self):
        self.muted = not self.muted

    def is_muted(self):
        return self.muted
