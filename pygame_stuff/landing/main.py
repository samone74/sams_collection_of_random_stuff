import pygame
from pygame.locals import *
import sys
from lander import Lander


def main():
    back_ground_color = get_color('white')
    win_width = 600  # width of the program's window, in pixels
    win_height = 600  # height in pixels
    fps = 25  # number of frames per second
    pygame.init()
    display_surf = pygame.display.set_mode((win_width, win_height))
    pygame.mouse.set_visible(False)
    # making a clock
    fps_clock = pygame.time.Clock()

    # adding objects
    lander = Lander(get_color('black'), 10, 10, 10)
    sprite_render_plain = pygame.sprite.RenderPlain(lander)
    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT:
                    lander.move(1)
                if event.key == K_RIGHT:
                    lander.move(2)
                if event.key == K_UP:
                    lander.move(3)
                if event.key == K_DOWN:
                    lander.move(4)

        display_surf.fill(back_ground_color)
        sprite_render_plain.update()
        sprite_render_plain.draw(display_surf)
        pygame.display.update()
        fps_clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()


def get_color(color_name):
    color_dict = {
        'aqua': (0, 255, 255),
        'black': (0, 0, 0),
        'blue': (0, 0, 255),
        'fuchsia': (255, 0, 255),
        'gray': (128, 128, 128),
        'green': (0, 128, 0),
        'lime': (0, 255, 0),
        'maroon': (128, 0, 0),
        'navy blue': (0, 0, 128),
        'olive': (128, 128, 0),
        'purple': (128, 0, 128),
        'red': (255, 0, 0),
        'silver': (192, 192, 192),
        'teal': (0, 128, 128),
        'white': (255, 255, 255, 0),
        'yellow': (255, 255, 0),
        'pink': (255, 150, 160),
        'gold': (255, 165, 0),
        'brown': (210, 105, 30)}
    return color_dict[color_name.lower()]


if __name__ == '__main__':
    main()
