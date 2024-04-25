import pygame

FPS = 60
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
COOLDOWN = 100
NUMBER_OF_ASTEROIDS = 5
INITIAL_VOLUME = .5
SPEED_LIMIT = 1000  # pixel / seconds
ACCELERATION = 1000  # pixel / seconds
TURN_SPEED = 180  # degree / seconds
LASER_SPEED = 2000  # pixel / seconds
HYPERSPACE_COOLDOWN = 3000

# Controls
LEFT = pygame.K_a
RIGHT = pygame.K_d
THROTTLE = pygame.K_w
FIRE = pygame.K_SPACE
HYPERSPACE = pygame.K_e

# Music
MUTE = pygame.K_m
VOLUME_UP = pygame.K_PERIOD
VOLUME_DOWN = pygame.K_COMMA
