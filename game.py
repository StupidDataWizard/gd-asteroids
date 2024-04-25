import random

import pygame
from pygame.math import Vector2

import conf
import globals
from collisions import CollisionManager
from counter import Counter
from enemies import Asteroid, UFO
from hierarchical_sprites import HierarchicalGroup
from living_background import BackgroundGroup
from spaceship import Spaceship
from states import State


class Game(State):
    def __init__(self):
        super().__init__()

        globals.game_manager.score = 0

        x = conf.DISPLAY_WIDTH * .5
        y = conf.DISPLAY_HEIGHT * .6
        self.number_of_asteroids = conf.NUMBER_OF_ASTEROIDS

        self.ship_group = HierarchicalGroup()
        self.spaceship = Spaceship(x, y)
        self.ship_group.add(self.spaceship)
        self.background_group = AsteroidsBackgroundGroup()

        self.asteroids_group = pygame.sprite.Group()
        self.laser_group = pygame.sprite.Group()
        self.ufo_group = pygame.sprite.Group()

        self.score_counter = Counter((40, 10), "assets/fonts/kenvector_future.ttf", 60, conf.WHITE)
        self.score_counter.digits = 1
        self.score_counter.set_value(globals.game_manager.score)

        self.collision_manager = CollisionManager()
        self.collision_manager.add_group(self.asteroids_group, "SHOTS")
        self.collision_manager.add_group(self.spaceship.weapon.active_bullets, "SHOTS")

        self.collision_manager.add_group(self.ufo_group, "SHOTS_AT_UFO")
        self.collision_manager.add_group(self.spaceship.weapon.active_bullets, "SHOTS_AT_UFO")

        self.collision_manager.add_group(self.ship_group, "SHIP")
        self.collision_manager.add_group(self.asteroids_group, "SHIP")

        self.collision_manager.add_group(self.ship_group, "UFO")
        self.collision_manager.add_group(self.ufo_group, 'UFO')

    def process_event(self, event):
        if event.type == CollisionManager.COLLISION_EVENT:
            if event.layer == "SHOTS":
                event.sprite.hit()
                for sprite in event.collisions:  # the bullets
                    sprite.kill()
            if event.layer == "SHIP":
                self.spaceship.hit()
            if event.layer == "UFO":
                # if the UFO hits the spaceship, destroy the it
                self.spaceship.hit()
            if event.layer == "SHOTS_AT_UFO":
                # The player hits the ufo.
                event.sprite.kill()
        elif event.type == Spaceship.DESTROYED:
            self.new_state = "GAME_OVER"
        elif event.type == globals.GameManager.SCORE_CHANGED:
            self.score_counter.set_value(event.score)

    def update(self, dt):
        # UFO
        # Random init once ever 10 seconds if not exists
        if len(self.ufo_group.sprites()) == 0:
            # 60 FPS, one check per frame, should be roughly one UFO per 10 seconds
            if random.randint(0, 600) == 1:
                self.ufo_group.add(UFO())
        self.collision_manager.update(dt)

        self.ship_group.update(dt)

        # if the are noe more asteroids left, regenerate them
        if len(self.asteroids_group) == 0:
            self.number_of_asteroids += 1
            for _ in range(self.number_of_asteroids):
                self.asteroids_group.add(Asteroid())

        self.asteroids_group.update(dt)
        self.laser_group.update(dt)
        self.ufo_group.update(dt)

    def draw(self, surface):
        self.background_group.draw(surface)
        self.ship_group.draw(surface)
        # The drawing of the bullets here is not elegant
        self.spaceship.weapon.active_bullets.draw(surface)
        self.asteroids_group.draw(surface)
        self.ufo_group.draw(surface)
        self.laser_group.draw(surface)
        self.score_counter.draw(surface)


class AsteroidsBackgroundGroup(BackgroundGroup):
    class Star(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            scaling = random.randint(0, 20)
            star_image = pygame.image.load(
                'assets/images/Effects/star' + str(random.randint(1, 3)) + '.png').convert_alpha()

            # Place our random star
            self.image = pygame.transform.scale(star_image, (scaling, scaling))
            self.rect = self.image.get_rect()
            self.position = Vector2(random.randint(0, conf.DISPLAY_WIDTH), random.randint(0, conf.DISPLAY_HEIGHT))
            self.rect.center = self.position

            # Change color of the star randomly
            # In essence, we overlay the star image with a color
            color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            color_image = pygame.Surface(self.image.get_size()).convert_alpha()
            color_image.fill(color)
            self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def __init__(self):
        super().__init__('assets/images/Backgrounds/blue.png', (conf.DISPLAY_WIDTH, conf.DISPLAY_HEIGHT))
        for _ in range(100):
            self.add(AsteroidsBackgroundGroup.Star())
