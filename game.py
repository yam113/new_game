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
        self.angle %= DOUBLE_PI
            

class Sprites:
    """Здесь хранятся типы и карта спрайтов"""

    def __init__(self):
        #  типы спрайтов
        self.sprite_types = {
            'barrel': pygame.image.load('sprites/barrel/0.png').convert_alpha(),
            'pedestal': pygame.image.load('sprites/pedestal/0.png').convert_alpha(),
            'devil': [pygame.image.load(f'sprites/devil/{i}.png').convert_alpha() for i in range(8)]
        }            
        #  Карта спрайтов
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['barrel'], True, (5.9, 2.1), 1.8, 0.4),
            SpriteObject(self.sprite_types['pedestal'], True, (8.8, 2.5), 1.6, 0.5),
            SpriteObject(self.sprite_types['pedestal'], True, (8.8, 5.6), 1.6, 0.5),
            SpriteObject(self.sprite_types['devil'], False, (7, 4), -0.2, 0.7),
        ]
 

class SpriteObject:
        """В этом классе вычисляем положение спрайта и его проекционные характеристики"""

    def __init__(self, object, static, pos, shift, scale):
        """ object - тип
            static - является ли он статичной картинкой без угла обзора или нет
            pos - его положение
            sdvig - сдвиг по вертикали
            scale - масштабирование
            """
        self.object = object
        self.static = static
        #  координаты спрайта задаем в системе координат карты, на случай изменения расширения проекта
        self.pos = self.x, self.y = pos[0] * razmer, pos[1] * razmer
        self.shift = sdvig
        #  на тот случай, если придется масштабировать картинку
        self.scale = scale
        #
        if not static:
            # диапазоны углов для каждого спрайта, так как картинок 8, то на каджый спрайт приходится диапазон в
            # 45 градусов
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            # так как это ключи в словаре, то для быстрого поиска будем использовать "замороженные" множества
            # обычные множества не получится использовать из-за того, что это изменяемый тип данных и ключами словаря
            # быть не могут
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}
     
    def object_locate(self, player, walls):
        """На вход идет экземпляр класса игрок и словарь с номерами лучей и расстоянииями до стен"""
        # создадим 2 списка
        # в 1 списке у нас будут фейковые лучи со значениями параметров от 1 настоящего луча
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        # во втором списке будут значения от полседнего луча
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        # добавляем слева и справа эти списски к основному списску стен
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y  # разницы координат между игроком и спрайтом
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)  # вычисляем рассотяние до него

        theta = math.atan2(dy, dx)  # углы
        gamma = theta - player.angle  # углы
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:  # условие, при котором угол
            # гамма находится в нужном нам пределах для дальнейших вычислений(корректируем угол гамма прибавляем
            # переменную 2-пи
            gamma += DOUBLE_PI
        # находим смещене спрайта относительно центрального луча
        delta_rays = int(gamma / ugol_mezhdu_luchami)
        current_ray = CENTER_RAY + delta_rays
        # корректируем расстояние для спрайта, чтобы не было эффекта рыбьего глаза иначе спрайт будет не ровно
        #
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * ugol_mezhdu_luchami)
        # получаем возможность отображать нащ спрайт на фейковых лучах за пределами экрана, тем самым спрайт не будет
        # исчезать а плавно будет уходить за экран
        fake_ray = current_ray + FAKE_RAYS
        # проверим попадает ли луч, на котором находится спрайт в наш диапазон лучей а так же если на том же луче
        # есть припятсвие то выясним будет ли спрайт ближе к нам чем стена
        if 0 <= fake_ray <= kol_luchei - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            # рассчет проекционной высоты спрайта
            proj_height = min(int(proj_coeff / distance_to_sprite * self.scale), 2 * height)
            # внедряем коэффициент его масштабирования
            half_proj_height = proj_height // 2
            # механизм регулирования спрайта по высоте
            shift = half_proj_height * self.shift
            # алгоритм выбора правильного спрайта в зависимости от угла theta
            if not self.static:
                if theta < 0:
                    # тут корректируем угол
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))
                # проходимся по спискам с углами и как только угол попадает в один из диапазонов, то нужным
                # спрайтом будет значение в словаре по ключу от этого угла
                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break
            # вычисляем позицию спрайта относительно его луча, для этого совмещаем центр спрайта с его лучом
            sprite_pos = (current_ray * SCALE - half_proj_height, polovina_height - half_proj_height + shift)
            # определим положение по высоте, с учетом заданного сдвига и смасштабируем спрайт по размеру его проекции
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            # вернем кортеж параметров, аналогичный в функции ray_casting, если условие не выполнилось, то вернем
            # ложное значение
            return distance_to_sprite, sprite, sprite_pos
        else:
            return (False,)

            

            
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

sprites = Sprites() 
drawing = Drawing(screen)
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(chern) # вся поверхность в черный
    drawing.background(player.angle)
    walls = ray_casting(player, drawing.textures)  # список стен, получаемый из функции райкаст
    drawing.world(walls + [obj.object_locate(player, walls) for obj in sprites.list_of_objects])  # отрисовка мира
    pygame.display.flip()
    
