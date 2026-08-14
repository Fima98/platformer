from math import sin
from random import choice, randint

import pygame
from timer import Timer


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func=self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()
        self.death_timer.update()


class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += (
            sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
        )

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()


class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.area = rect
        self.speed = randint(160, 200)
        self.direction = choice((1, -1))

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if self.rect.right >= self.area.right:
            self.direction = -1
        elif self.rect.left <= self.area.left:
            self.direction = 1

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        current_frame = self.frames[int(self.frame_index) % len(self.frames)]

        if self.direction == 1:
            self.image = current_frame
        else:
            self.image = pygame.transform.flip(current_frame, True, False)


class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        self.direction = direction
        self.speed = 850
        self.timer = Timer(5000, autostart=True, func=self.kill)

        if self.direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.midright = pos
        else:
            self.rect.midleft = pos

    def update(self, dt):
        self.timer.update()
        self.rect.x += self.direction * self.speed * dt


class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.timer = Timer(100, autostart=True, func=self.kill)
        self.y_offset = pygame.Vector2(0, 8)
        self.facing_right = player.facing_right

        if not self.player.facing_right:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, dt):
        self.timer.update()

        if not self.player.facing_right:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.facing_right != self.player.facing_right:
            self.kill()
