import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, font, text_color=pygame.Color(200, 200, 200),
                 background_color=pygame.Color(100, 40, 40)):
        super().__init__()
        self._font = font
        self._text_color = text_color
        self._background_color = background_color
        self._text = text
        self.rect = rect
        self.observers = []
        self._render()

    def _render(self):
        self.rendered_text = self.font.render(self._text, True, self.text_color)
        self.image = pygame.Surface((self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
        x_offset = (self.rect.width - self.rendered_text.get_rect().width) / 2
        y_offset = (self.rect.height - self.rendered_text.get_rect().height) / 2
        pygame.draw.rect(self.image, self.background_color, self.image.get_rect(), border_radius=4)
        self.image.blit(self.rendered_text, (x_offset, y_offset))

    def on_click(self, func):
        self.observers.append(func)

    def update(self, dt):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                print("Button clicked!")
                for func in self.observers:
                    func()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._render()

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value
        self._render()

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = value
        self._render()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._render()
