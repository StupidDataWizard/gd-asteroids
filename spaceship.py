import random

import pygame

import conf
import globals
from animations import Sheet, Animation
from hierarchical_sprites import HierarchicalSprite
from weapon import Weapon, LaserShot


class Spaceship(HierarchicalSprite):
    DESTROYED = pygame.event.custom_type()

    # constructor
    def __init__(self, x=0, y=0):
        super().__init__()
        img = pygame.image.load('assets/images/playerShip1_blue.png')
        self.ship_image = pygame.transform.rotate(img, -90)
        self.image = self.ship_image.copy()
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width / 2) * 0.9
        self.position = pygame.Vector2(x, y)
        self.rect.center = self.position
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 90
        self.acceleration = conf.ACCELERATION
        self._rotate_image()
        self.weapon = Weapon(self, (50, 0), LaserShot, cool_down=200)
        explosion_sheet = Sheet("assets/animations/explosion3.png", 89, 89, 2, 5, border=1, spacing=1,
                                color_key=pygame.Color(111, 109, 81))
        self.explosion_frames = explosion_sheet.get_frames(range(10))
        self.explosion_anim = None
        globals.sound_manager.preload_sfx("assets/sounds/explosion.wav")
        self.speed_limit = conf.SPEED_LIMIT
        self.flame = Flame()
        self.hyperspace_cooldown = conf.HYPERSPACE_COOLDOWN
        self.last_hyperspace_jump = pygame.time.get_ticks()

    def hit(self):
        if self.explosion_anim:
            return
        print("We got hit!")
        self.explosion_anim = Animation(self.explosion_frames, callback=self.destroy, play_once=True)
        self.explosion_anim.rect.center = (0, 0)
        self.sprites.add(self.explosion_anim)
        globals.sound_manager.play_sfx("assets/sounds/explosion.wav")

    def destroy(self, _):
        self.kill()
        event = pygame.event.Event(Spaceship.DESTROYED, ship=self)
        pygame.event.post(event)

    def _rotate_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.ship_image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self, dt):
        self.position += self.velocity * dt
        if self.position.y > conf.DISPLAY_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = conf.DISPLAY_HEIGHT
        if self.position.x > conf.DISPLAY_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = conf.DISPLAY_WIDTH
        self.rect.center = self.position

        key_pressed = pygame.key.get_pressed()
        if key_pressed[conf.THROTTLE]:
            self.velocity += pygame.Vector2(self.acceleration * dt, 0).rotate(-self.rotation)
            # set a speed limit
            if self.velocity.length() > self.speed_limit:
                self.velocity = self.velocity.normalize() * self.speed_limit

            # Play engine sound
            globals.sound_manager.play_sfx('assets/sounds/spaceEngine_000.ogg')
            globals.sound_manager.fadeout_sfx('assets/sounds/spaceEngine_000.ogg')
            self.sprites.add(self.flame)
        else:
            self.flame.kill()

        if key_pressed[conf.LEFT]:
            # rotate left
            self.rotation += conf.TURN_SPEED * dt
            self._rotate_image()
        if key_pressed[conf.RIGHT]:
            # rotate right
            self.rotation -= conf.TURN_SPEED * dt
            self._rotate_image()

        # Hyperspace
        if key_pressed[conf.HYPERSPACE]:
            if self.last_hyperspace_jump + self.hyperspace_cooldown < pygame.time.get_ticks():
                # set random spawn point
                self.position = pygame.Vector2(random.randint(0, conf.DISPLAY_HEIGHT),
                                               random.randint(0, conf.DISPLAY_WIDTH))
                self.last_hyperspace_jump = pygame.time.get_ticks()
        # Laser
        if key_pressed[conf.FIRE]:
            # Shoot
            self.weapon.fire(self.rotation)

        self.weapon.update(dt)
        # Fade out during explosion
        if self.explosion_anim:
            self.image.set_alpha(self.image.get_alpha() * 0.5)


class Flame(HierarchicalSprite):
    image = pygame.image.load("assets/images/Effects/fire00.png")

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotate(Flame.image, 90)
        self.rect = self.image.get_rect()
        self.rect.top -= 8
        self.rect.left -= 77
