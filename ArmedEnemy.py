import pygame
from ProgramControl import ProgramControl
import random


def validX(x, enemies):
    for e in enemies:
        if abs(x - e.x) <= ArmedEnemy.size[0] + 20:
            return False
    return True


class ArmedEnemy:
    setup = ProgramControl()
    collisionErrorTolerance = 10
    hpHeight = 10
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 205, 0)
    size = (110, 171)
    gap = 300
    stayAtY = 70  # where the ship stops moving forward
    score = 6
    maxAmount = 3
    shotGap = 170   # time gap between two round of shooting
    shotGap2 = 13   # time gap between the first and the second bullet in each shooting round
    damage = 1

    def __init__(self, imageName, enemies):

        self.x = random.randint(20, self.setup.windowSize[0] - self.size[0] - 20)
        while not validX(self.x, enemies):
            self.x = random.randint(0, self.setup.windowSize[0] - self.size[0])
        self.y = 0 - self.size[1] - 30

        self.speed = 4
        self.image = pygame.image.load(imageName)

        self.totalHP = 5
        self.hp = self.totalHP

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        pygame.draw.rect(window, self.hpBackgroundColor, (self.x, self.y - self.hpHeight - 5, self.size[0],
                                                          self.hpHeight))
        pygame.draw.rect(window, self.hpColor, (self.x, self.y - self.hpHeight - 5,
                                                self.size[0] * (self.hp / self.totalHP),
                                                self.hpHeight))

    def move(self):
        if self.y <= self.stayAtY:
            self.y += self.speed

    def getShot(self, player):
        self.hp -= player.damage
