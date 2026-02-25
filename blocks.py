import pygame
from pygame.constants import K_DELETE, KEYDOWN
from pygame.font import Font
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface


class Block(Sprite):
    def __init__(self, group: Group, pos: tuple[int, int]):
        super().__init__(group)
        self.group = group
        self.pos = pos
        self.init_data()
        self.update_image()
        self.update_anchors()

    def init_data(self):
        self.anchors = {
            "top": (0, 0),
            "bottom": (0, 0),
            "left": (0, 0),
            "right": (0, 0),
        }
        self.selected = False
        self.image: Surface
        self.last_image = None

    def update_image(self):
        self.update_rect()

    def update_rect(self):
        if self.last_image != self.image:
            self.rect: Rect = self.image.get_rect()
        self.rect.center = self.pos

        self.last_image = self.image
        self.update_anchors()

    def update_anchors(self):
        self.anchors = {
            "top": self.rect.midtop,
            "bottom": self.rect.midbottom,
            "left": self.rect.midleft,
            "right": self.rect.midright,
        }

    def draw_anchors(self, win, exclude: list = []):
        surf = Surface((12, 12))
        surf.fill("red")
        rect = surf.get_rect()
        for a in self.anchors:
            if a in exclude:
                continue
            rect.center = self.anchors[a]
            win.blit(surf, rect)

    def handle_dragging(self, mouse_motion):
        self.pos = (self.pos[0] + mouse_motion[0], self.pos[1] + mouse_motion[1])
        self.update_rect()

    def while_selected(
        self, mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
    ):
        if key_inputs[K_DELETE]:
            self.group.remove(self)
        pass

    def on_selected(self):
        self.selected = True

    def on_deselected(self):
        self.selected = False

    def update(
        self, mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
    ):
        if mousej_inputs[0]:
            if self.rect.collidepoint(mouse_pos):
                self.on_selected()
            else:
                self.on_deselected()

        if self.selected:
            if mouse_inputs[0]:
                self.handle_dragging(mouse_motion)
            self.while_selected(
                mousej_inputs,
                mouse_inputs,
                mouse_pos,
                mouse_motion,
                key_inputs,
                events,
            )

        if mouse_inputs[1]:
            self.handle_dragging(mouse_motion)


class TextBlock(Block):
    def __init__(self, group: Group, pos: tuple[int, int], font: Font):
        self.font = font
        return super().__init__(group, pos)

    def init_data(self):
        self.text = "TEXT"
        return super().init_data()

    def update_image(self):
        new_txt = ""
        for i in self.text:
            new_txt += f" {i} " if i == "\n" else i

        color = "#403930" if self.selected else "gray15"
        self.image = self.font.render(f" {new_txt} ", True, "white", color).convert()
        return super().update_image()

    def while_selected(
        self, mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
    ):
        for event in events:
            if event.type == KEYDOWN:
                self.text = "" if self.text == "TEXT" else self.text
                name = pygame.key.name(event.key)

                if name == "backspace":
                    self.text = self.text[: len(self.text) - 1]
                    self.update_image()
                elif name == "return":
                    self.text += "\n"
                    self.update_image()
                elif name == "space":
                    self.text += " "
                    self.update_image()
                if len(name) > 1:
                    continue

                self.text += name
                self.update_image()
        return super().while_selected(
            mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
        )

    def on_selected(self):
        super().on_selected()
        self.update_image()

    def on_deselected(self):
        super().on_deselected()
        self.update_image()


class ImageBlock(Block):
    def __init__(self, group: Group, pos: tuple[int, int], fp: str):
        self.fp = fp
        super().__init__(group, pos)

    def init_data(self):
        self.scaling = False
        self.max_size = 160
        self.original: Surface
        return super().init_data()

    def update(
        self, mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
    ):
        if mousej_inputs[0]:
            rx, ry = self.rect.bottomright
            mx, my = mouse_pos
            distance_sq = (rx - mx) ** 2 + (ry - my) ** 2
            if distance_sq < 100:
                self.selected = False
                self.scaling = True
        elif mouse_inputs[0]:
            if self.scaling:
                self.max_size += mouse_motion[0] + mouse_motion[1]
                self.max_size = max(20, min(self.max_size, 500))
                self.update_preview()
        elif self.scaling:
            self.update_image()
            self.scaling = False

        return super().update(
            mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
        )

    def load_original(self):
        if self.original is None:
            self.original = pygame.image.load(self.fp).convert_alpha()

    def update_preview(self):
        self.load_original()

        ow, oh = self.original.get_size()
        mw, mh = self.max_size, self.max_size

        scale = min(mw / ow, mh / oh)
        new_size = (int(ow * scale), int(oh * scale))

        self.image = pygame.transform.scale(self.original, new_size)
        self.update_rect()

    def update_image(self):
        self.load_original()

        ow, oh = self.original.get_size()
        mw, mh = self.max_size, self.max_size

        scale = min(mw / ow, mh / oh)
        new_size = (int(ow * scale), int(oh * scale))

        self.image = pygame.transform.smoothscale(self.original, new_size)
        super().update_image()
