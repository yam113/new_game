import pygame
import math

# настройки игры
width = 1200
height = 800
polovina_width = width // 2
polovina_height = height // 2
razmer = 100
FPS_POS = (width - 65, 5)

#  настройки игрока
position_for_player = (polovina_width // 4, polovina_height - 50)  # начальное положение игрока
vzglyad_for_player = 0  # направление взгляда игрока
scorost_for_player = 2  # скорость игрока

# цвета
bel = (255, 255, 255)
chern = (0, 0, 0)
krasnui = (220, 0, 0)
zelenui = (0, 80, 0)
sinui = (0, 0, 255)
temno_serui = (40, 40, 40)
fioletovui = (120, 0, 120)
biruzovui = (0, 186, 255)
zheltui = (220, 220, 0)
pesok = (244, 164, 96)
temno_korichnevui = (97, 61, 25)
temno_oranzhevui = (255, 140, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill(chern) # вся поверхность в черный
    
    pygame.draw.circle(screen, zelenui, position_for_player, 10)
    
    pygame.display.flip()
    clock.tick()
