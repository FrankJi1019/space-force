import pygame
from ProgramControl import ProgramControl
import random


class Boss:
    gap = 1000
    stdTotalHP = 40
    totalHP = 40
    size = (274, 220)
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 205, 0)
    hpHeight = 15
    score = 15

    # attack related
    attackGap = 120
    bulletDamage = 2
    bulletSpeed = 5

    def __init__(self):
        self.x = random.randint(0, ProgramControl.windowSize[0] - self.size[0])
        self.y = -self.size[1] - 20
        self.staysAtY = 40
        self.speed = 2
        self.image = pygame.image.load("./image/Boss.png")
        self.hp = self.totalHP

    def draw(self, window):
        if self.speed == 0:
            pygame.draw.rect(window, self.hpBackgroundColor,
                             (self.x, self.y - self.hpHeight - 20, self.size[0], self.hpHeight))
            pygame.draw.rect(window, self.hpColor,
                             (self.x, self.y - self.hpHeight - 20, self.size[0] * self.hp / self.totalHP,
                              self.hpHeight))
        window.blit(self.image, (self.x, self.y))

    def move(self):
        if self.y >= self.staysAtY:
            self.speed = 0
        self.y += self.speed
