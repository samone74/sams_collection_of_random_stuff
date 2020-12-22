import pygame
import random

class Number(pygame.sprite.Sprite):
    def __init__(self, x, y, size, bck_color, number_color, number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size / 2, size))
        pygame.Surface.fill(self.image, bck_color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        menu_font_obj = pygame.font.Font(None, int(size * 1.5))
        text = menu_font_obj.render(str(number), True, number_color, bck_color)
        text_rect = text.get_rect()
        self.image.blit(text, text_rect)
        self.number = number
        self.number_color = number_color
        self.bck_color = bck_color
        self.size = size

    def update(self):
        menu_font_obj = pygame.font.Font(None, int(self.size * 1.5))
        text = menu_font_obj.render(str(self.number), True, self.number_color, self.bck_color)
        text_rect = text.get_rect()
        self.image.blit(text, text_rect)

    def change_position_and_number(self, win_width, win_height, snakes):
        self.number = random.randint(1, 9)

        redo = True
        while redo:
            self.rect.left = random.randint(0, win_width - self.size / 2)
            self.rect.top = random.randint(0, win_height - self.size)
            redo = False
            for snake in snakes:
                if self.check_colide(snake):
                    redo = True

    def check_colide(self, snake):
        if pygame.sprite.spritecollide(self, snake.snake_element, False):
            return True
        return False

