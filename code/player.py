import pygame
from sprites import AnimatedSprite
from timer import Timer


class Player(AnimatedSprite):
    def __init__(self, frames, pos, groups, collision_sprites):
        super().__init__(frames, pos, groups)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2(0, 0)
        self.speed = 400
        self.on_ground = False
        self.gravity_index = 1800
        self.jump_speed = 750
        self.facing_right = True

        # timer
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        if keys[pygame.K_SPACE]:
            self.jump()

        if pygame.mouse.get_pressed()[0] and not self.shoot_timer:
            print('shoot bullet')
            self.shoot_timer.activate()

    def jump(self):
        if self.on_ground:
            self.direction.y = -self.jump_speed

    def apply_gravity(self, dt):
        self.direction.y += self.gravity_index * dt

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        self.on_ground = False
        self.apply_gravity(dt)
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

    def animate(self, dt):
        if not self.on_ground:
            self.frame_index = 1
        elif self.direction.x != 0:
            self.frame_index += self.animation_speed * dt
        else:
            self.frame_index = 0

        current_frame = self.frames[int(self.frame_index) % len(self.frames)]

        if self.facing_right:
            self.image = current_frame
        else:
            self.image = pygame.transform.flip(current_frame, True, False)

    def update(self, dt):
        self.shoot_timer.update()
        self.input()
        self.move(dt)
        self.animate(dt)
