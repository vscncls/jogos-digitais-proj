import pygame


class SoundController:
    def __init__(self) -> None:
        self.muted = False
        pygame.mixer.init()
        pygame.mixer.music.load("src/assets/background-music.ogg")
        self.music_volume = 0.1
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play()

    def toggle(self):
        self.muted = not self.muted
        if self.is_muted():
            pygame.mixer.music.set_volume(0)
        else:
            self.play_music()

    def is_muted(self):
        return self.muted

    def play(self, sound: pygame.mixer.Sound):
        if not self.muted:
            sound.play()

    def play_music(self):
        pygame.mixer.music.set_volume(self.music_volume)
