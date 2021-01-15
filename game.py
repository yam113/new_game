import pygame
import math

# настройки игры
width = 1200
height = 800
polovina_width = width // 2
polovina_height = height // 2
fps = 60
razmer = 100
FPS_POS = (width - 65, 5)

# настройки отрисовки
oblast_vid = math.pi / 3
HALF_FOV = oblast_vid / 2
kol_luchei = 300
dalnost_prorisovki = 800
ugol_mezhdu_luchami = oblast_vid / kol_luchei
dist = kol_luchei / (2 * math.tan(HALF_FOV))
proj_coeff = 3 * dist * razmer
SCALE = width // kol_luchei

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


text_map = [
    '111111111111',
    '1.....2....1',
    '1.22.....2.1',
    '1..........1',
    '1.22.......1',
    '1.2......2.1',
    '1.....2....1',
    '111111111111'
]

world_map = {}
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == '1':
            world_map[(i * razmer, j * razmer)] = '1'
        elif char == '2':
            world_map[(i * razmer, j * razmer)] = '2'


class Player:
    def __init__(self):
        self.x, self.y = position_for_player
        self.angle = vzglyad_for_player
        
    # используем  property в качестве декоратора, т.е из атрибута класса в метод классa
    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        """В этой функции происходит процесс управления"""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += scorost_for_player * cos_a
            self.y += scorost_for_player * sin_a
        if keys[pygame.K_s]:
            self.x += -scorost_for_player * cos_a
            self.y += -scorost_for_player * sin_a
        if keys[pygame.K_a]:
            self.x += scorost_for_player * sin_a
            self.y += -scorost_for_player * cos_a
        if keys[pygame.K_d]:
            self.x += -scorost_for_player * sin_a
            self.y += scorost_for_player * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
            
            
def mapping(a, b):
    return (a // razmer) * razmer, (b // razmer) * razmer
            
            
def ray_casting(screen, player):
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    angle = player.angle - HALF_FOV
    for _ in range(kol_luchei):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        '''for i in range(dalnost_prorisovki):
            x = ox + i * cos_a
            y = oy + i * sin_a
            if (x // razmer * razmer, y // razmer * razmer) in world_map:
                i *= math.cos(player.angle - angle)
                proj_height = min(proj_coeff / (i + 0.0001), height)
                c = 255 / (1 + i * i * 0.0001)
                color = (c, c, c)
                pygame.draw.rect(screen, color, (_ * SCALE, polovina_height - proj_height // 2, SCALE, proj_height))
                break
        angle += ugol_mezhdu_luchami'''
        
      
class Drawing:
    def __init__(self, screen):
        self.sc = screen
        self.sc_map = sc_map

    def background(self):
        pygame.draw.rect(self.sc, biruzovui, (0, 0, width, polovina_height))
        pygame.draw.rect(self.sc, temno_serui, (0, polovina_height, width, polovina_height))

    def world(self, player):
        ray_casting(self.sc, player)
        

pygame.init()
screen = pygame.display.set_mode((width, height))

drawing = Drawing(screen)
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(chern) # вся поверхность в черный
    drawing.background
    drawing.world(player)
    pygame.display.flip()
