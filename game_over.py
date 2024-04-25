import pygame

import conf
import globals
from elements import Button
from states import State


class GameOver(State):
    def __init__(self, message):
        super().__init__()

        # game over
        font = pygame.font.Font('assets/fonts/kenvector_future.ttf', 72)
        font_small = pygame.font.Font('assets/fonts/kenvector_future.ttf', 40)
        font_button = pygame.font.Font('assets/fonts/kenvector_future.ttf', 24)
        self.message = font.render(message, True, conf.WHITE)
        self.score = font_small.render(f"Score: {globals.game_manager.score}", True, conf.WHITE)

        # play again
        self.play_again_btn = Button(pygame.Rect(10, 10, 200, 40), "Play Again", font_button)
        self.gui = pygame.sprite.Group()
        self.gui.add(self.play_again_btn)

        def onclick():
            self.new_state = "GAME"

        self.play_again_btn.on_click(onclick)

    def update(self, dt):
        self.gui.update(dt)

    def draw(self, surface):
        center = self.message.get_rect(center=surface.get_rect().center)
        surface.blit(self.message, center)
        # positioning score centered below game over message
        center = self.score.get_rect(center=(center[0] + self.message.get_rect().width / 2, center[1] + 100))
        surface.blit(self.score, center)
        self.gui.draw(surface)
