import pygame
from ProgramControl import ProgramControl
import math


class Knife:
    size = (100, 100)
    totalHP = 4
    speed = 5
    hpBarHeight = 10
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 205, 0)

    def __init__(self, x, y, speedX):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = math.sqrt(self.speed ** 2 - self.speedX ** 2)
        self.image = pygame.image.load("./image/bullet/bulletKnives.png")
        self.hp = self.totalHP
        self.damage = 3
        self.angle = 0

    def draw(self, window):
        newImage = pygame.transform.rotate(self.image, self.angle)
        self.angle -= 2
        newRect = newImage.get_rect(center=self.image.get_rect().move(self.x, self.y).center)
        window.blit(newImage, newRect)
        pygame.draw.rect(window, self.hpBackgroundColor, (self.x, self.y - self.hpBarHeight - 5, self.size[0],
                                                          self.hpBarHeight))
        pygame.draw.rect(window, self.hpColor, (self.x, self.y - self.hpBarHeight - 5,
                                                self.size[0] * self.hp / self.totalHP, self.hpBarHeight))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY
        if self.x <= 0 or self.x >= ProgramControl.windowSize[0] - self.size[0]:
            self.speedX = -self.speedX
        if self.y <= 0 or self.y >= ProgramControl.windowSize[1] - self.size[1]:
            self.speedY = -self.speedY


class ExplosiveBall:
    size = (104, 104)
    staysAtY = ProgramControl.windowSize[1] - size[1]
    damage = 3
    totalHP = 5
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 205, 0)
    hpBarHeight = 10
    speed = 3

    def __init__(self, x, y, speedX):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = math.sqrt(self.speed ** 2 - self.speedX ** 2)
        self.image = pygame.image.load("./image/bullet/bulletExplosive.png")
        self.hp = self.totalHP

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        pygame.draw.rect(window, self.hpBackgroundColor, (self.x, self.y - self.hpBarHeight - 5, self.size[0],
                                                          self.hpBarHeight))
        pygame.draw.rect(window, self.hpColor, (self.x, self.y - self.hpBarHeight - 5,
                                                self.size[0] * self.hp / self.totalHP, self.hpBarHeight))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY
        if self.x <= 0 or self.x >= ProgramControl.windowSize[0] - self.size[0]:
            self.speedX = -self.speedX
        if self.y <= 0 or self.y >= ProgramControl.windowSize[1] - self.size[1]:
            self.speedY = -self.speedY


class BossBullet:
    size = (30, 30)
    damage = 3

    def __init__(self, x, y, speedX, speedY):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.image = pygame.image.load("./image/bullet/bulletBoss2.png")

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY
