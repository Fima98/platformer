from os.path import join
from random import randint

import pygame
from groups import AllSprites
from player import Player
from pytmx.util_pygame import load_pygame
from settings import *
from sprites import Bee, Bullet, Fire, Sprite, Worm
from timer import Timer
from utils import audio_importer, import_folder, import_image


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
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.load_assetes()
        self.setup()

        self.bee_timer = Timer(
            duration=1000, func=self.create_bee, autostart=True, repeat=True
        )

    def create_bee(self):
        Bee(
            frames=self.bee_frames,
            pos=(self.level_width + WINDOW_WIDTH, randint(0, self.level_height)),
            groups=(self.all_sprites, self.enemy_sprites),
            speed=randint(300, 500),
        )

    def create_bullet(self, pos, direction):
        Bullet(
            self.bullet_surf, pos, direction, (self.all_sprites, self.bullet_sprites)
        )
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].play()

    def load_assetes(self):
        # graphics
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

        self.audio = audio_importer('audio')

    def setup(self):
        tmx_map = load_pygame(join('data', 'maps', 'world.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

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
                    create_bullet=self.create_bullet,
                )
            elif obj.name == 'Worm':
                Worm(
                    frames=self.worm_frames,
                    rect=pygame.FRect(obj.x, obj.y, obj.width, obj.height),
                    groups=(self.all_sprites, self.enemy_sprites),
                )

        self.audio['music'].play(loops=-1)

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(
                bullet, self.enemy_sprites, False, pygame.sprite.collide_mask
            )
            if sprite_collisions:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collisions:
                    sprite.destroy()

        if pygame.sprite.spritecollide(
            self.player, self.enemy_sprites, False, pygame.sprite.collide_mask
        ):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
