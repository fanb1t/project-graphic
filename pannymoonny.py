import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return int(x), int(y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))
    for angle in range(0, 360, 10):
        r = 100
        x, y = polar_to_cartesian(r, math.radians(angle))
        pygame.draw.circle(screen, (0, 0, 0), (400 + x, 300 + y), 2)

    pygame.display.flip()
    clock.tick(60)
