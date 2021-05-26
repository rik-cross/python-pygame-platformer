from .ui_text import *
from .colours import *
import engine
import pygame

class Text:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.row = 0
        self.delay = 5
        self.delayTimer = self.delay
        self.finished = False
        self.finalTimer = 300
        self.autoFinish = True
        self.destroy = False
        self.overhead = True
        self.width = 20
        self.sound = True
        self.textList = []

        row = ''
        for char in self.text:
            row = row + char
            if len(row) >= self.width and char == ' ':
                self.textList.append(row[:-1])
                row = ''
        if len(row) > 0:
            self.textList.append(row)

    def update(self):
        if not self.finished:
            self.delayTimer -= 1
            if self.delayTimer <= 0:
                self.delayTimer = self.delay
                self.index += 1
                if self.sound:
                    engine.soundManager.playSound('blip', engine.soundManager.soundVolume / 2)
                if self.index >= len(self.textList[self.row]):
                    self.index = 0
                    self.row += 1
                    if self.row >= len(self.textList):
                        if self.autoFinish:
                            self.finished = True
                        else:
                            # if button pressed for entity:
                            pass

        if self.finished:
            if self.autoFinish is True:
                self.finalTimer -= 1
                if self.finalTimer <= 0:
                    self.destroy = True
            else:
                pass

    def draw(self, screen, x, y):
        rows = 30 * len(self.textList)
        if self.overhead:

            for i,l in enumerate(self.textList):

                if i == self.row:
                    drawText(screen, l[0:self.index], x, y-10-rows+(i*30), WHITE, 255)
                elif i < self.row:
                    drawText(screen, l, x, y-10-rows+(i*30), WHITE, 255)
        else:

            screenWidth, screenHeight = pygame.display.get_surface().get_size()
            r = pygame.rect.Rect(screenWidth-510, 10, screenWidth-10, 210)
            pygame.draw.rect(screen, DARK_GREY, r)
            drawText(screen, self.text[:self.index], screenWidth-500, 20, WHITE, 255)

            for i,l in enumerate(self.textList):

                if i == self.row:
                    drawText(screen, l[0:self.index], screenWidth-500, 20+(i*30), WHITE, 255)
                elif i < self.row:
                    drawText(screen, l, screenWidth-500, 20+(i*30), WHITE, 255)