import pygame


class Bullet:
    size = (13, 13)

    def __init__(self, x, y, speedX, speedY, name):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.image = pygame.image.load(name)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY


class Blast:
    size = (850, 200)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedX = 0
        self.speedY = -15
        self.image = pygame.image.load("./image/bullet/wave.png")
        self.damage = 10

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

