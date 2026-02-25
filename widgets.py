from pygame.font import Font
from pygame.sprite import Group, Sprite


class Text(Sprite):
    def __init__(self, group: Group, pos: tuple, text: str, font: Font) -> None:
        self.group = group
        self.font = font
        self.pos = pos
        super().__init__(group)
        self.last_txt = ""
        self.update_text(text)

    def update_text(self, text: str):
        if text == self.last_txt:
            return
        self.image = self.font.render(text, True, "white", "gray5").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)
        self.last_txt = text

    def update(self, text):
        self.update_text(text)
