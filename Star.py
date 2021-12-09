import pygame
from ProgramControl import ProgramControl
import random


class Star:
    amount = 50  # how many stars on the screen
    stdSpeedRange = [1, 3]
    speedRange = [1, 3]

    def __init__(self, y=-1):
        self.x = random.randint(0, ProgramControl.windowSize[0])
        self.y = random.randint(0, ProgramControl.windowSize[1]) if y == -1 else y

        self.sizeRange = (1, 5)
        self.size = random.randint(self.sizeRange[0], self.sizeRange[1])

        self.colorRange = (230, 255)
        self.color = tuple([random.randint(self.colorRange[0], self.colorRange[1]) for _ in range(3)])

        self.speed = random.randint(self.speedRange[0], self.speedRange[1])

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)

    def move(self):
        self.y += self.speed
