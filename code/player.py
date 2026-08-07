from os.path import join

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            join('images', 'player', '0.png')
        ).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        self.speed = 400
        self.on_ground = False
        self.gravity_index = 1800
        self.jump_speed = 750

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_speed

    def apply_gravity(self, dt):
        self.direction.y += self.gravity_index * dt

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.apply_gravity(dt)
        self.on_ground = False
        self.rect.y += self.direction.y * dt
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                        self.on_ground = True
                        self.direction.y = 0
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0

    def update(self, dt):
        self.input()
        self.move(dt)
