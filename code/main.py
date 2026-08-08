from os.path import join

import pygame
from groups import AllSprites
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import Sprite
from utils import import_folder, import_image


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.load_assetes()
        self.setup()

    def load_assetes(self):
        # graphics
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

    def setup(self):
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))

        for x, y, image in tmx_map.get_layer_by_name('Main').tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=image,
                groups=(self.all_sprites, self.collision_sprites),
            )
        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                surf=image,
                groups=(self.all_sprites),
            )

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    frames=self.player_frames,
                    pos=(obj.x, obj.y),
                    groups=(self.all_sprites),
                    collision_sprites=self.collision_sprites,
                )

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
