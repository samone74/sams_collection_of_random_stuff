# class with the lander the user is controlling
import pygame


class Lander(pygame.sprite.Sprite):
    def __init__(self, color, size, x_start, y_start):
        self.rect = None
        self.v = 1
        self.v_y = 0
        self.brake = 0
        self.g = 1

        self.color = color
        self.image = pygame.Surface((size, size))
        pygame.Surface.fill(self.image, self.color)
        self.rect = self.image.get_rect()
        self.rect.left = x_start
        self.rect.top = y_start
        self.size = size
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        self.rect.top += self.v
        self.rect.left += self.v_y
        self.v += self.g - self.brake

    def move(self,direction):
        if direction == 1:
            self.v_y = -1
        if direction == 2:
            self.v_y = 1
        if direction == 3:
            self.brake += 1
        if direction == 4:
            self.brake -= 1
