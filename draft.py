import pygame
import math


pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()


def DrawPentagon(centerX, centerY, length, color, width=None):
    # first point
    one = (centerX, centerY - length[0])
    # second point
    two = (centerX - length[1] * math.cos(math.radians(18)), centerY - length[1] * math.sin(math.radians(18)))
    # third point
    three = (centerX - length[2] * math.sin(math.radians(36)), centerY + length[2] * math.cos(math.radians(36)))
    # fourth point
    four = (centerX + length[3] * math.sin(math.radians(36)), centerY + length[3] * math.cos(math.radians(36)))
    # fifth point
    five = (centerX + length[4] * math.cos(math.radians(18)), centerY - length[4] * math.sin(math.radians(18)))
    if width is not None:
        pygame.draw.polygon(window, color, (one, two, three, four, five), width)
    else:
        pygame.draw.polygon(window, color, (one, two, three, four, five))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    window.fill((255, 255, 255))

    DrawPentagon(250, 250, [100 for i in range(5)], (0, 0, 0), 4)
    pygame.draw.circle(window, (255, 0, 0), (250, 250), 2)

    pygame.display.update()
    clock.tick(100)