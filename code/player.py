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
