from .scene import Scene

class TransitionScene(Scene):
    def __init__(self, fromScenes, toScenes):
        self.currentPercentage = 0
        self.fromScenes = fromScenes
        self.toScenes = toScenes
    def update(self, sm):
        self.currentPercentage += 2
        if self.currentPercentage >= 100:
            sm.pop()
            for s in self.toScenes:
                sm.push(s)
        for scene in self.fromScenes:
            scene.update(sm)
        if len(self.toScenes) > 0:
            for scene in self.toScenes:
                scene.update(sm)
        else:
            if len(sm.scenes) > 1:
                sm.scenes[-2].update(sm)