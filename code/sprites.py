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


class Bee(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

    def update(self, dt):
        self.animate(dt)


class Worm(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)

    def update(self, dt):
        self.animate(dt)


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
