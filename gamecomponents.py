class Score:
    def __init__(self):
        self.score = 0

class Battle:
    def __init__(self):
        self.lives = 3

class Effect:
    def __init__(self, apply, timer, sound, end):
        self.apply = apply
        self.timer = timer
        self.sound = sound
        self.end = end
