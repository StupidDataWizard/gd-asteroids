import pygame

import conf

# We need to initialize before we import the remaining classes
# as we use pygame code in class variables
pygame.init()
screen = pygame.display.set_mode((conf.DISPLAY_WIDTH, conf.DISPLAY_HEIGHT))

import globals
from game import Game
from game_over import GameOver

clock = pygame.time.Clock()
pygame.display.set_caption('Asteroids')

# Sound Manager
globals.sound_manager.set_music('assets/sounds/scifi.ogg')

# State machine
globals.current_state = Game()


def process_events():
    # We use the pressed key dict here
    # to allow keeping a key pressed for 
    # quicker volume change
    key_pressed = pygame.key.get_pressed()
    if key_pressed[conf.VOLUME_UP]:
        globals.sound_manager.raise_volume()

    if key_pressed[conf.VOLUME_DOWN]:
        globals.sound_manager.lower_volume()

    for event in pygame.event.get():
        # We process all event globally FIRST!
        if event.type == pygame.QUIT:
            globals.game_manager.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == conf.MUTE:
                globals.sound_manager.toggle_mute()
        # All events are now handed down
        # to the current state for further
        # processing.
        globals.current_state.process_event(event)


# Game loop
dt = 0
while globals.game_manager.running:
    process_events()
    globals.current_state.update(dt)
    globals.current_state.draw(screen)
    pygame.display.flip()
    next_state = globals.current_state.next_state()
    if next_state == "GAME":
        globals.current_state = Game()
    elif next_state == "GAME_OVER":
        globals.current_state = GameOver("Game Over")

    dt = clock.tick(conf.FPS) / 1000

pygame.quit()
