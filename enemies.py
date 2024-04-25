import random

import pygame

import conf
import globals


class Asteroid(pygame.sprite.Sprite):
    # constructor
    def __init__(self, parent=None):
        super().__init__()

        meteor_colors = ['Brown', 'Grey']
        self.sizes = ['small', 'med', 'big']

        self.rotation = random.randint(0, 360)

        if parent:
            self.meteor_color = parent.meteor_color
            self.size = parent.size
            self.number = 3 - parent.number
            self.position = pygame.Vector2(parent.position)
            self.velocity = pygame.Vector2(parent.velocity)
        else:
            self.meteor_color = meteor_colors[random.randint(0, 1)]
            self.size = random.randrange(len(self.sizes))
            self.number = random.randint(1, 2)
            self.position = pygame.Vector2(random.randint(0, 400), random.randint(0, 200))
            self.velocity = pygame.Vector2(1, 0).rotate(self.rotation)

        self.original_images = []
        for s in range(len(self.sizes)):
            img_file = f'assets/images/Meteors/meteor{self.meteor_color}_{self.sizes[s]}{self.number}.png'
            img = pygame.image.load(img_file)
            # img = pygame.transform.scale(img, (50,50))
            self.original_images.append(img)

        self.image = self.original_images[self.size]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self._rotate_image()

    def _rotate_image(self):
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_images[self.size], self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.radius = (self.rect.width / 2) * 0.9

    def update(self, dt):
        self.position += self.velocity
        if self.position.y > conf.DISPLAY_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = conf.DISPLAY_HEIGHT
        if self.position.x > conf.DISPLAY_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = conf.DISPLAY_WIDTH
        self.rect.center = self.position

        self.rotation += 20 * dt
        self._rotate_image()

    def hit(self):
        if self.size == 0:
            print('Asteroid destroyed')
            self.kill()
            globals.game_manager.score += 100
            return
        else:
            globals.game_manager.score += (100 - (self.size * 35))
            self.size -= 1
            child = Asteroid(self)
            child.velocity.rotate_ip(random.randint(-60, -30))
            self.velocity.rotate_ip(random.randint(30, 60))
            for group in self.groups():
                group.add(child)


class UFO(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()

        self.image = pygame.image.load('assets/images/ufoBlue.png')
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(random.randint(0, conf.DISPLAY_WIDTH), random.randint(0, conf.DISPLAY_HEIGHT))
        self.rect.center = self.position
        self.radius = (self.rect.width / 2) * 0.9
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = random.randint(0, 360)
        self.acceleration = random.randint(10, 20) * .1

    def update(self, dt):
        self.position += self.velocity
        if self.position.y > conf.DISPLAY_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = conf.DISPLAY_HEIGHT
        if self.position.x > conf.DISPLAY_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = conf.DISPLAY_WIDTH
        self.rect.center = self.position

        self.velocity += pygame.Vector2(dt, 0).rotate(-self.rotation)  # acceleration removed
        self.rotation += 10 * dt

    def __del__(self):
        self.kill()
        print('UFO destroyed')

