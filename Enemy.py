import pygame
import random
from ProgramControl import ProgramControl


def validX(x, enemies):
    for e in enemies:
        if abs(x - e.x) <= EnemyShip.size[0] - 20:
            return False
    return True


class EnemyShip:
    generatingGap = 150  # frequency of generating new enemies
    speed = (3, 7)
    size = (110, 90)
    collisionErrorTolerance = 10
    damage = 2

    # HP related
    hpHeight = 10
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 205, 0)
    score = 2

    def __init__(self, imageName, enemies):

        # x and y location of the enemy
        self.x = random.randint(0, ProgramControl.windowSize[0] - self.size[0])
        while not validX(self.x, enemies):
            self.x = random.randint(0, ProgramControl.windowSize[0] - self.size[0])
        self.y = -50

        self.totalHP = 3
        self.hp = self.totalHP
        self.speed = random.randint(self.speed[0], self.speed[1])
        self.image = pygame.image.load(imageName)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        pygame.draw.rect(window, self.hpBackgroundColor, (self.x, self.y - self.hpHeight, self.size[0],
                                                          self.hpHeight))
        pygame.draw.rect(window, self.hpColor,
                         (self.x, self.y - self.hpHeight, self.size[0] * (self.hp / self.totalHP), self.hpHeight))

    def move(self):
        self.y += self.speed

    def getShot(self, player):
        self.hp -= player.damage
