import pygame
import random
# import math
from ProgramControl import ProgramControl
from Bonus import Bonus


class PlayerShip:

    maxHP, maxSpeed, maxDamage, maxMP, minShotGap, maxRecoverySpeed = (14, 16, 2.2, 700, 7, 0.026)
    minHP, minSpeed, minDamage, minMP, maxShotGap, minRecoverySpeed = (5, 5, 0, 300, 2, 0.01)
    mpBarColor = (0, 191, 255)
    mpBarColor2 = (0, 255, 255)
    reflectTime = 1400

    def __init__(self, name):

        # (imageSize, lives, speed, damage, mpTime, recoverySpeed, imageName, shotGap)
        playerInfo = {"./image/player/PlayerShipA.png": ((135, 85), 10, 11, 1.5, 480, 0.022, "bulletPlayerA.png", 10),
                      "./image/player/PlayerShipB.png": ((134, 87), 13, 7, 2, 550, 0.017, "bulletPlayerB.png", 10),
                      "./image/player/PlayerShipC.png": ((142, 86), 11, 9, 1.7, 650, 0.019, "bulletPlayerC.png", 10),
                      "./image/player/PlayerShipD.png": ((123, 90), 7, 14, 1, 520, 0.024, "bulletPlayerD.jpg", 9)}

        self.name = name
        self.image = pygame.image.load(name)
        self.size, self.hp, self.speed, self.damage, self.mpLoadTime, self.recoverySpeed, self.bullet, self.shotGap = \
            playerInfo[name]
        self.totalHP = self.hp
        self.bullet = "./image/bullet/" + self.bullet

        # the location of the player
        self.x = (ProgramControl.windowSize[0] - self.size[0]) / 2
        self.y = ProgramControl.windowSize[1] - self.size[1] - 50

        self.protect = False

        # player's HP bar related
        self.hpBarHeight = 20
        self.hpBarWidth = 1000
        self.hpBarY = 700
        self.hpNormalColor = (0, 200, 20)
        self.hpDangerColor = (255, 80, 80)
        self.fullHpColor = (0, 200, 20)

        self.mp = 0
        self.mpBarY = 670

    def draw(self, window, drawProtect, protectColor=Bonus.protectorColor):
        window.blit(self.image, (self.x, self.y))
        width = 4 if protectColor == Bonus.protectorColor else 5
        if self.protect and drawProtect:
            pygame.draw.circle(window, protectColor,
                               (round(self.x + self.size[0] / 2), round(self.y + self.size[1] / 2)),
                               round(self.size[0] / 2 + 10), width)

    def protection(self, status):
        self.protect = status

    def move(self, horizontal, vertical):
        self.x += horizontal * self.speed
        self.y += vertical * self.speed
        if self.x < -2 or self.x > ProgramControl.windowSize[0] - self.size[0]:
            self.x -= horizontal * self.speed
        if self.y < 0 or self.y > ProgramControl.windowSize[1] - self.size[1]:
            self.y -= vertical * self.speed

    def GetInfo(self):
        return {"speed": self.speed,
                "weapon": self.damage,
                "HP": self.hp}


class DisturbingShip:
    size = (123, 90)
    staysAt = ProgramControl.windowSize[1] - size[1] - 100
    totalHp = 20
    hpHeight = 10
    hpBackgroundColor = (190, 190, 190)
    hpColor = (0, 191, 255)

    def __init__(self):
        self.x = random.randint(0, ProgramControl.windowSize[0] - DisturbingShip.size[0])
        self.y = ProgramControl.windowSize[1] - 20
        self.speed = 3
        self.image = pygame.image.load("./image/player/DisturbShip.png")
        self.hp = DisturbingShip.totalHp

    def move(self):
        if self.y > DisturbingShip.staysAt:
            self.y -= self.speed

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        if self.y <= DisturbingShip.staysAt:
            pygame.draw.rect(window, self.hpBackgroundColor, (self.x, self.y + self.size[1],
                                                              self.size[0], self.hpHeight))
            pygame.draw.rect(window, self.hpColor, (self.x, self.y + self.size[1],
                                                    self.size[0] * (self.hp / self.totalHp), self.hpHeight))
            '''radius = math.sqrt((self.size[0]/2)**2 + (self.size[1]/2)**2)
            shipCenter = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
            pygame.draw.arc(window, self.hpColor,
                            (shipCenter[0] - radius, shipCenter[1] - radius + 14, radius*2, radius*2),
                            math.radians(0), math.radians(360 * self.hp / self.totalHp), 5)'''
