import pygame
import sys

# initializing the constructor
pygame.init()

# screen resolution
res = (720, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255, 255, 255)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
text = smallfont.render('quit', True, color)

while True:

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.quit()

    # fills the screen with a color
    screen.fill((60, 25, 60))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    # if mouse is hovered on a button it
    # changes to lighter shade
    if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
        pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])

    else:
        pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

    # superimposing the text onto our button
    screen.blit(text, (width / 2 + 50, height / 2))

    # updates the frames of the game
    pygame.display.update()


'''
    def find_path_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * WIDTH for _ in range(HEIGHT)]
        distance[y][x] = 0
        prev = [[None] * WIDTH for _ in range(HEIGHT)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < WIDTH and 0 < next_y < HEIGHT and \
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y
'''
