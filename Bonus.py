import pygame
import random
from ProgramControl import ProgramControl


class Bonus:
    size = (88, 88)
    gap = 1000

    # weapon.png
    weaponDoubleTime = 800

    # medical.png
    addLives = 2

    # protect.png
    protectorColor = (151, 255, 255)
    protectorTime = 800
    protectorWarnTime = 300

    def __init__(self, name):
        self.x = random.randint(0, ProgramControl.windowSize[0] - self.size[0])
        self.y = 0 - self.size[1] - 20

        self.image = pygame.image.load(name)

        self.speedX = 2
        self.speedY = 2

        self.function = name

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY
        if self.x >= ProgramControl.windowSize[0] - self.size[0] or self.x <= 0:
            self.speedX *= -1
