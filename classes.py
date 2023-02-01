import pygame.transform
import pytmx
import os

from constants import *


gameover_group = pygame.sprite.Group()
all_sprites1 = pygame.sprite.Group()


def start_music(filename):
    pygame.mixer.music.load(f"{DATA_DIR}/{SOUNDS_DIR}/{filename}")
    pygame.mixer.music.play(loops=-1)


def load_image(name=None, color_key=None, image=None):
    if name is not None:
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname).convert()
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_sound(name, volume=1.0):
    sound = pygame.mixer.Sound(f"{DATA_DIR}/{SOUNDS_DIR}/{name}")
    sound.set_volume(volume)
    return sound


pygame.mixer.init()
hero_run = [pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_001.png'),
            pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_002.png'),
            pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_003.png'),
            pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_004.png'),
            pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_005.png'),
            pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/run/image_part_006.png'), ]

hero_stay = [pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_001.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_002.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_003.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_004.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_005.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/stay/image_part_006.png')]

hero_attack = [pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_001.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_002.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_003.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_004.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_005.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_006.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_007.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_008.png'),
               pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/attack/image_part_009.png')]

enemy_run = [pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_001.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_002.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_003.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_004.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_005.png'),
             pygame.image.load(f'{DATA_DIR}/{SPRITE_DIR}/monstr_new/image_part_004.png')]


run = False
anim_count_run = 0
anim_count_stay = 0
anim_count_run1 = 0
run_enemy = True
anim_count_run_enemy = 0


class Map:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'{DATA_DIR}/{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile
        self.side = 1

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def f(self):  #чтобы просмотреть где какие айдишники клеток
        for x in range(WIDTH // TILE_SIZE):
            for y in range(HEIGHT // TILE_SIZE):
                pos = x, y
                print(self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)], end=' ')
            print()

    def get_tile_id(self, pos):
        if pos[0] < WIDTH // TILE_SIZE and pos[1] < HEIGHT // TILE_SIZE:
            return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]
        return 0

    def is_free(self, pos):
        return self.get_tile_id(pos) in self.free_tiles

    def new_step_x(self, start):
        x, y = start
        if self.side == 1:
            if self.is_free((x + 1, y)):
                return (x + 1, y)
            self.side = -1
            return (x, y)
        else:
            if self.is_free((x - 1, y)):
                return (x - 1, y)
            self.side = 1
            return (x, y)

    def new_step_y(self, start):
        x, y = start
        if self.side == 1:
            if self.is_free((x, y + 2)):
                return (x, y + 1)
            self.side = -1
            return (x, y)
        else:
            if self.is_free((x, y)):
                return (x, y - 1)
            self.side = 1
            return (x, y)




class Hero:
    def __init__(self, pos):
        self.x, self.y = pos

    def get_position(self):
        return self.x, self.y

    def set_position(self, pos):
        self.x, self.y = pos

    def render(self, screen):
        global run, anim_count_run, anim_count_stay
        size = TILE_SIZE, TILE_SIZE * 2
        if anim_count_run + 1 >= FPS:
            anim_count_run = 0
        if run:
            screen.blit(pygame.transform.scale(hero_run[anim_count_run // 5], size),
                        (self.x * TILE_SIZE, self.y * TILE_SIZE))
            anim_count_run += 1
        if not run:
            anim_count_run = 0
            screen.blit(pygame.transform.scale(hero_stay[anim_count_stay], size),
                        (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def shoot(self, bullets):
        pass


class Game:
    def __init__(self, map, hero, enemies, flag_enemy):
        self.map = map
        self.hero = hero
        self.flag_enemy = flag_enemy
        if self.flag_enemy == 1:
            self.enemy1 = enemies[0]
        elif self.flag_enemy == 2:
            self.enemy1 = enemies[0]
            self.enemy2 = enemies[1]
        else:
            self.enemy1 = enemies[0]
            self.enemy2 = enemies[1]
            self.enemy3 = enemies[2]

    def render(self, screen):
        self.map.render(screen)
        self.hero.render(screen)
        if self.flag_enemy == 1:
            self.enemy1.render(screen)
        elif self.flag_enemy == 2:
            self.enemy1.render(screen)
            self.enemy2.render(screen)
        else:
            self.enemy1.render(screen)
            self.enemy2.render(screen)
            self.enemy3.render(screen)

    def updata_hero(self, screen):
        global run, anim_count_run
        next_x, next_y = self.hero.get_position()
        speed = 1
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= speed
            run = True
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += speed
            run = True
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += speed
            run = True
        elif pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= speed
            run = True
        else:
            run = False
            anim_count_run = 0
        if self.map.is_free((next_x, next_y + 1)):
            self.hero.set_position((next_x, next_y))

    def move_enemy1(self):
        next_pos = self.map.new_step_x(self.enemy1.get_position())
        self.enemy1.set_position(next_pos)

    def move_enemy2(self):
        next_pos = self.map.new_step_y(self.enemy2.get_position())
        self.enemy2.set_position(next_pos)

    def move_enemy3(self):
        next_pos = self.map.new_step_y(self.enemy3.get_position())
        self.enemy3.set_position(next_pos)


class Enemy:
    def __init__(self, pos):
        self.x, self.y = pos
        self.width, self.heigh = TILE_SIZE * 2, TILE_SIZE * 2
        self.size = self.width, self.heigh

    def get_position(self):
        return self.x, self.y

    def set_position(self, pos):
        self.x, self.y = pos

    def render(self, screen):
        global run_enemy, anim_count_run_enemy
        if anim_count_run_enemy + 1 >= FPS:
            anim_count_run_enemy = 0
        if run:
            screen.blit(pygame.transform.scale(enemy_run[anim_count_run_enemy // 5], self.size),
                        (self.x * TILE_SIZE, self.y * TILE_SIZE))
            anim_count_run_enemy += 1
        if not run:
            anim_count_run_enemy = 0
            screen.blit(pygame.transform.scale(enemy_run[0], self.size),
                        (self.x * TILE_SIZE, self.y * TILE_SIZE))


class Button:
    def __init__(self, rect, image, image2=None, size=pygame.rect.Rect(-WIDTH, -HEIGHT, 10, 10)):
        self.image = image
        self.image2 = image2
        self.rect = rect
        self.size = size
        self.timer = None
        self.size_using = False
        self.sound = load_sound("press.wav")

    def check_pressed(self, pos):
        if (not self.size_using and self.rect.collidepoint(pos)) \
                or (self.size_using and self.size.collidepoint(pos)):
            if self.image2 is not None:
                self.image, self.image2 = self.image2, self.image
            self.timer = 1 if self.image2 is not None else 100
            self.sound.play(maxtime=100)
            return True
        return False

    def draw(self, screen, showing=True):
        if showing:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            self.size_using = False
        else:
            screen.blit(self.image, (self.size.x, self.size.y))
            self.size_using = True

    def update(self):
        if self.timer is not None:
            if self.timer < 15:
                self.timer += 1
                return False
            self.timer = None
            self.image, self.image2 = self.image2, self.image
            return True
