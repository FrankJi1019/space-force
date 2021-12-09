import pygame


class Explosion:

    def __init__(self, x, y, speedX, speedY, volume, startTime, duration=90, sound="EnemyDie.wav"):
        pygame.mixer.init()
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.image = pygame.image.load("./image/explosion.png")
        self.startTime = startTime
        self.durationTime = duration
        for i in range(volume):
            pygame.mixer.Sound("./sound/" + sound).play()

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

    def delete(self, now):
        return True if now - self.startTime >= self.durationTime else False
