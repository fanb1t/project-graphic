import math
from array import array

import pygame


class SoundManager:
    # Small generated-sound service so the game has feedback without audio files.
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.enabled = True
            self._build_sounds()
        except pygame.error:
            self.enabled = False

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def _build_sounds(self):
        self.sounds = {
            "startup": self._tone(660, 0.10, 0.18),
            "click": self._tone(520, 0.05, 0.12),
            "select": self._tone(740, 0.07, 0.14),
            "confirm": self._tone(880, 0.10, 0.16),
            "key": self._tone(980, 0.12, 0.16),
            "error": self._tone(180, 0.20, 0.18),
            "win": self._tone(1040, 0.22, 0.16),
        }

    def _tone(self, frequency, duration, volume):
        sample_rate = 44100
        samples = int(sample_rate * duration)
        data = array("h")
        fade_samples = max(1, int(sample_rate * 0.01))

        for index in range(samples):
            wave = math.sin(2 * math.pi * frequency * index / sample_rate)
            envelope = 1.0
            if index < fade_samples:
                envelope = index / fade_samples
            elif index > samples - fade_samples:
                envelope = max(0.0, (samples - index) / fade_samples)

            data.append(int(32767 * volume * envelope * wave))

        return pygame.mixer.Sound(buffer=data.tobytes())
