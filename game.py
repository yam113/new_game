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

# настройки текстур
texture_width = 1200
texture_height = 1200
texture_scale = texture_width // razmer

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
            
            
def ray_casting(screen, player, textures):
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    angle = player.angle - HALF_FOV
    for _ in range(kol_luchei):
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        # вертикаль
        x, dx = (xm + razmer, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, width, razmer):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * razmer
            
        # горизонтально
        y, dy = (ym + razmer, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, height, razmer):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * razmer
            
        # проекция
        i, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % razmer
        i *= math.cos(player.angle - angle)
        proj_height = min(proj_coeff / (i + 0.0001), height)
        
        wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
        #  Позиция стены
        wall_pos = (_ * SCALE, polovina_height - proj_height // 2)
        #  Добавялем стены
        walls.append((depth, wall_column, wall_pos))
        angle += ugol_mezhdu_luchami

      
class Drawing:
    def __init__(self, screen):
        self.sc = screen
        self.sc_map = world_map
        self.textures = {'1': pygame.image.load('img/wall1.png').convert(),
                         '2': pygame.image.load('img/wall2.png').convert(),
                         'S': pygame.image.load('img/sky3.png').convert()
                         }

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % width
        self.sc.blit(self.textures['S'], (sky_offset, 0))
        self.sc.blit(self.textures['S'], (sky_offset - width, 0))
        self.sc.blit(self.textures['S'], (sky_offset + width, 0))
        pygame.draw.rect(self.sc, temno_serui, (0, polovina_height, width, polovina_height))

    def world(self, player):
        ray_casting(self.sc, player, self.textures)
        

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
    drawing.background(player.angle)
    drawing.world(player)
    pygame.display.flip()
