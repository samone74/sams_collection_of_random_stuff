import pygame


class Snake:
    def __init__(self, color, x_start, y_start, size, key_left, key_right, win_width, win_height, start_size):
        self.color = color
        self.v = 5
        self.vx = self.v
        self.vy = 0
        self.key_left = key_left
        self.key_right = key_right
        self.win_width = win_width
        self.win_height = win_height
        self.size = size
        self.snake_element = []
        self.grow_size = 0

        for i in range(int(start_size * size / self.v)):
            self.snake_element.append(SnakeElement(color, x_start - i * self.v, y_start, size))
        self.all_sprites = pygame.sprite.RenderPlain(self.snake_element)

    def draw(self, display_surf):
        self.all_sprites.draw(display_surf)

    def turn(self, key_pressed):
        if key_pressed == self.key_left:
            # turn left
            if self.vx > 0:
                self.vx = 0
                self.vy = -self.v
            elif self.vx < 0:
                self.vx = 0
                self.vy = self.v
            elif self.vy > 0:
                self.vx = self.v
                self.vy = 0
            elif self.vy < 0:
                self.vx = -self.v
                self.vy = 0
        elif key_pressed == self.key_right:
            # turn right
            if self.vx> 0:
                self.vx = 0
                self.vy = self.v
            elif self.vx < 0:
                self.vx = 0
                self.vy = -self.v
            elif self.vy > 0:
                self.vx = -self.v
                self.vy = 0
            elif self.vy < 0:
                self.vx = self.v
                self.vy = 0

    def update(self):
        old_center = self.snake_element[0].rect.center
        self.snake_element[0].rect.left += self.vx
        self.snake_element[0].rect.top += self.vy
        if self.snake_element[0].rect.left > self.win_width - self.size:
            self.snake_element[0].rect.left = 0
        if self.snake_element[0].rect.left < 0:
            self.snake_element[0].rect.left = self.win_width - self.size
        if self.snake_element[0].rect.top > self.win_height - self.size:
            self.snake_element[0].rect.top = 0
        if self.snake_element[0].rect.top < 0:
            self.snake_element[0].rect.top = self.win_height - self.size

        for i in range(1, len(self.snake_element)):
            cur_center = self.snake_element[i].rect.center
            self.snake_element[i].rect.center = old_center
            old_center = cur_center

        if self.grow_size > 0:
            self.all_sprites.remove(self.snake_element)
            self.snake_element.append(SnakeElement(self.color, old_center[0] - self.size / 2,
                                                   old_center[1] - self.size / 2, self.size))
            self.grow_size -= 1
            self.all_sprites.add(self.snake_element)

    def self_collide(self):
        col_list = pygame.sprite.spritecollide(self.snake_element[0], self.snake_element[5:], False)
        if col_list:
            return True
        return False

    def other_collide(self, other_snakes):
        for other_snake in other_snakes:
            if other_snake == self:
                continue
            col_list = pygame.sprite.spritecollide(self.snake_element[0], other_snake.snake_element, False)
            if col_list:
                return True
        return False

    def collide_number(self, number):
        if pygame.sprite.collide_rect(self.snake_element[0], number):
            self.grow_size += int(number.number * self.size / self.v)
            return True


class SnakeElement(pygame.sprite.Sprite):
    def __init__(self, color, x_start, y_start, size):
        self.color = color
        self.image = pygame.Surface((size, size))
        pygame.Surface.fill(self.image, self.color)
        self.rect = self.image.get_rect()
        self.rect.left = x_start
        self.rect.top = y_start
        self.size = size
        pygame.sprite.Sprite.__init__(self)
