import sys

import pygame.mixer

from classes import *


background = pygame.transform.scale(
    pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/bg.jpg"), WINDOW_SIZE)

restart_button = Button(
        image=pygame.transform.scale(
            pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/restart_button.png"), (50, 50)),
        rect=pygame.rect.Rect(WIDTH // 2, HEIGHT // 2, 100, 100),
        size=pygame.rect.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.1), 50, 50))
home_button = Button(
        image=pygame.transform.scale(
            pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/home.png"), (50, 50)),
        rect=pygame.rect.Rect(WIDTH - 60, 10, 50, 50))
play_button = Button(
        image=pygame.transform.scale(
            pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/play.png"), (100, 100)),
        rect=pygame.rect.Rect(WIDTH // 2 - 200, HEIGHT // 2, 100, 100),
        size=pygame.rect.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.1), 50, 50))
buttons = [play_button]
buttons2 = [restart_button]
flag = True
flag_enemy = 1

def terminate():
    pygame.quit()
    sys.exit()

def start(screen, waiting=True):
    global flag_enemy
    screen.blit(background, (0, 0))
    pygame.mouse.set_visible(False)
    all_sprites = pygame.sprite.Group()
    start_music(filename="background_menu.mp3")
    cursor_image = pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/cursor.png")
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()
    sprite_cursor = pygame.sprite.Sprite()
    sprite_cursor.image = cursor_image
    sprite_cursor.rect = sprite_cursor.image.get_rect()
    all_sprites.add(sprite_cursor)
    smallfont = pygame.font.SysFont('Corbel', 35)
    smallfont_bold = pygame.font.SysFont('Corbel', 35, bold=True)
    text1 = smallfont.render('Easy', True, COLOR_WHITE)
    text2 = smallfont.render('Medium', True, COLOR_WHITE)
    text3 = smallfont.render('Hard', True, COLOR_WHITE)
    text_main = smallfont_bold.render('Выберите уровень сложности:', True, COLOR_WHITE)
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_pressed(event.pos):
                    waiting = False
                if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 \
                        and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
                    flag_enemy = 1
                if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 \
                        and HEIGHT / 2 + 50 <= mouse[1] <= HEIGHT / 2 + 90:
                    flag_enemy = 2
                if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 \
                        and HEIGHT / 2 + 100 <= mouse[1] <= HEIGHT / 2 + 140:
                    flag_enemy = 3
            if event.type == pygame.MOUSEMOTION:
                sprite_cursor.rect.topleft = event.pos
        screen.blit(background, (0, 0))
        for button in buttons:
            button.draw(screen)
        mouse = pygame.mouse.get_pos()
        #1 button check
        if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2, 240, 40])
        elif flag_enemy == 1:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2, 240, 40])
        else:
            pygame.draw.rect(screen, color_dark, [WIDTH / 2 + 100, HEIGHT / 2, 240, 40])
        #2 button  check
        if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 and HEIGHT / 2 + 50 <= mouse[1] <= HEIGHT / 2 + 90:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2 + 50, 240, 40])
        elif flag_enemy == 2:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2 + 50, 240, 40])
        else:
            pygame.draw.rect(screen, color_dark, [WIDTH / 2 + 100, HEIGHT / 2 + 50, 240, 40])
        # 3 button  check
        if WIDTH / 2 + 100 <= mouse[0] <= WIDTH / 2 + 240 and HEIGHT / 2 + 100 <= mouse[1] <= HEIGHT / 2 + 140:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2 + 100, 240, 40])
        elif flag_enemy == 3:
            pygame.draw.rect(screen, color_light, [WIDTH / 2 + 100, HEIGHT / 2 + 100, 240, 40])
        else:
            pygame.draw.rect(screen, color_dark, [WIDTH / 2 + 100, HEIGHT / 2 + 100, 240, 40])

        screen.blit(text1, (WIDTH / 2 + 150, HEIGHT / 2))
        screen.blit(text2, (WIDTH / 2 + 150, HEIGHT / 2 + 50))
        screen.blit(text3, (WIDTH / 2 + 150, HEIGHT / 2 + 100))
        screen.blit(text_main, (WIDTH / 2 - 30, HEIGHT / 2 - 50))
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()

def end(screen, event, win=True):
    global flag
    screen.blit(load_image(f'{BACKGROUNDS_DIR}/you_win.jpg', color_key=-1), (WIDTH // 2, HEIGHT // 2))
    screen.blit(background, (0, 0))
    pygame.mouse.set_visible(False)
    all_sprites = pygame.sprite.Group()
    if flag and win:
        start_music(filename="win.mp3")
        pygame.time.delay(3000)
        flag = False
    if flag and not win:
        start_music(filename='failed.mp3')
        pygame.time.delay(3000)
        flag = False
    if not flag:
        start_music(filename='background_mini.mp3')
    cursor_image = pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/cursor.png")
    for button in buttons2:
        button.draw(screen)
    pygame.display.flip()
    sprite_cursor = pygame.sprite.Sprite()
    sprite_cursor.image = cursor_image
    sprite_cursor.rect = sprite_cursor.image.get_rect()
    all_sprites.add(sprite_cursor)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_pressed(event.pos):
                    waiting = False
            if event.type == pygame.MOUSEMOTION:
                sprite_cursor.rect.topleft = event.pos
        screen.blit(background, (0, 0))
        for button in buttons2:
            button.draw(screen)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.check_pressed(event.pos):
                flag = True
                main()
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    map = Map('map.tmx', FREE_TILES, FINISH_TILE)
    hero = Hero((2, 3))
    clock = pygame.time.Clock()
    start_music(filename="background_main.mp3")
    cursor_image = pygame.image.load(f"{DATA_DIR}/{BACKGROUNDS_DIR}/cursor.png")
    sprite_cursor = pygame.sprite.Sprite()
    sprite_cursor.image = cursor_image
    sprite_cursor.rect = sprite_cursor.image.get_rect()
    all_sprites.add(sprite_cursor)
    pygame.mouse.set_visible(False)
    start(screen)
    if flag_enemy == 1:
        enemy1 = Enemy((2, 13))
        game = Game(map, hero, [enemy1], flag_enemy)
    elif flag_enemy == 2:
        enemy1 = Enemy((2, 13))
        enemy2 = Enemy((8, 3))
        game = Game(map, hero, [enemy1, enemy2], flag_enemy)
    elif flag_enemy == 3:
        enemy1 = Enemy((2, 13))
        enemy2 = Enemy((8, 3))
        enemy3 = Enemy((22, 3))
        game = Game(map, hero, [enemy1, enemy2, enemy3], flag_enemy)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.check_pressed(event.pos):
                    start(screen)
            if event.type == pygame.MOUSEMOTION:
                sprite_cursor.rect.topleft = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hero.shoot(bullets)
            if map.get_tile_id(hero.get_position()) == FINISH_TILE:
                end(screen, event)
                pygame.display.flip()
        game.updata_hero(screen)
        if flag_enemy == 1:
            game.move_enemy1()
            if hero.get_position() == enemy1.get_position():
                end(screen, event, win=False)
                pygame.display.flip()
        elif flag_enemy == 2:
            game.move_enemy1()
            game.move_enemy2()
            if hero.get_position() == enemy1.get_position() \
                    or hero.get_position() == enemy2.get_position():
                end(screen, event, win=False)
                pygame.display.flip()
        elif flag_enemy == 3:
            game.move_enemy1()
            game.move_enemy2()
            game.move_enemy3()
            if hero.get_position() == enemy1.get_position() \
                    or hero.get_position() == enemy2.get_position() \
                    or hero.get_position() == enemy3.get_position():
                end(screen, event, win=False)
                pygame.display.flip()
        screen.fill((0, 0, 0))
        game.render(screen)
        home_button.draw(screen)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()