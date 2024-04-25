import pygame
import conf

import globals


class Weapon():
    def __init__(self, sprite, position, bullet_class, cool_down=50):
        super().__init__()
        self.sprite = sprite
        # Relative position with respect to sprite.rect.center
        self._position = pygame.Vector2(position)
        self.last_fire = 0
        self.cool_down = cool_down  # ms
        self.bullet_class = bullet_class
        self.active_bullets = pygame.sprite.Group()

    def update(self, dt):
        self.active_bullets.update(dt)

    def draw(self, surface):
        self.active_bullets.draw(surface)

    @property
    def global_position(self):
        pos = self._position.rotate(-self.sprite.rotation)
        return self.sprite.rect.center + pos

    def fire(self, direction):
        """
        direction is global direction of the shot
        """
        if self.last_fire + self.cool_down > pygame.time.get_ticks():
            return
        bullet = self.bullet_class(self, direction)
        self.active_bullets.add(bullet)
        self.last_fire = pygame.time.get_ticks()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, weapon, direction):
        super().__init__()
        self.weapon = weapon
        self.direction = direction


class LaserShot(Bullet):
    laser_image = pygame.image.load("assets/images/Lasers/laserRed01.png").convert_alpha()
    laser_image_rotated = pygame.transform.rotate(laser_image, -90)
    shooting_area = pygame.Rect(0, 0, conf.DISPLAY_WIDTH, conf.DISPLAY_HEIGHT)
    sound = "assets/sounds/sfx_laser1.ogg"

    def __init__(self, weapon, direction):
        globals.sound_manager.play_sfx(LaserShot.sound)
        super().__init__(weapon, direction)
        self.image = pygame.transform.rotate(LaserShot.laser_image_rotated, direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.weapon.global_position
        self.radius = 3
        # Question: do we have to take the speed of the ship into account?
        self.velocity = pygame.Vector2(1, 0) * conf.LASER_SPEED  # speed: pixel / second
        self.velocity.rotate_ip(-direction)
        self.damage = 1

    def update(self, dt):
        self.rect.center += self.velocity * dt
        if not LaserShot.shooting_area.colliderect(self.rect):
            self.kill()
