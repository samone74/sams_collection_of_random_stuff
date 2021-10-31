from snake import *
from number import *
from pygame.locals import *
import sys


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
    # creating a Display surface and an alpha surface
    snakes = []
    start_size = 10
    snakes.append(Snake(get_color('lime'),  10.0, 10.0, 10, K_LEFT, K_RIGHT, win_width, win_height, start_size))
    number = Number(30, 40, 20, back_ground_color, get_color('red'), 9)
    number.change_position_and_number(win_width, win_height, snakes)
    number_plain = pygame.sprite.RenderPlain(number)
    snakes.append(Snake(get_color('aqua'),  10.0, 300.0, 10, K_a, K_d, win_width, win_height, start_size))
    #   `snakes.append(Snake(get_color('blue'),  10.0, 100.0, 10, K_f, K_g, win_width, win_height, start_size))
    #snakes.append(Snake(get_color('purple'),  10.0, 150.0, 10, K_j, K_k, win_width, win_height, start_size))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                for snake in snakes:
                    snake.turn(event.key)
        display_surf.fill(back_ground_color)
        for snake in snakes:
            snake.update()
            if snake.self_collide() or snake.other_collide(snakes):
                snakes.remove(snake)
                if not snakes:
                    terminate()
                continue
            if snake.collide_number(number):
                number.change_position_and_number(win_width, win_height, snakes)

            snake.all_sprites.draw(display_surf)
        number_plain.update()
        number_plain.draw(display_surf)
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
