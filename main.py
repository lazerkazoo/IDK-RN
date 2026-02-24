from tkinter.filedialog import askopenfilename

import pygame
from pygame.constants import FULLSCREEN, K_LSHIFT, QUIT
from pygame.display import set_mode
from pygame.font import Font
from pygame.sprite import Group
from pygame.time import Clock

from blocks import ImageBlock, TextBlock

pygame.init()

win = set_mode((0, 0), FULLSCREEN, vsync=1)

clock = Clock()

width, height = pygame.display.get_window_size()

# fonts
font = Font(size=64)
font32 = Font(size=32)
font96 = Font(size=96)

# groups
buttons = Group()
labels = Group()

blocks = Group()

# connections
sel1, sel2 = None, None
lines = []
LINE_WIDTH = 5

# other
last_mouse_pos = (0, 0)


def run():
    global last_mouse_pos, mouse_pos, sel1, sel2, lines

    mousej_inputs = pygame.mouse.get_just_pressed()
    mouser_inputs = pygame.mouse.get_just_released()
    mouse_inputs = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_motion = (mouse_pos[0] - last_mouse_pos[0], mouse_pos[1] - last_mouse_pos[1])
    key_inputs = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            quit()

    if mousej_inputs[2]:
        if key_inputs[K_LSHIFT]:
            pygame.display.set_mode((100, 100))
            pygame.display.iconify()
            fp = askopenfilename(
                filetypes=[
                    ("Image File", ["*.png", "*.jpg", "*.webp"]),
                    ("Vector File", "*.svg"),
                ]
            )
            if fp:
                dog = ImageBlock(blocks, mouse_pos, fp)
                dog.fp = fp
            set_mode((0, 0), FULLSCREEN, vsync=1)
        else:
            TextBlock(blocks, mouse_pos, font)

    if mousej_inputs[0]:
        break_line = True
        for block in blocks:
            for a in block.anchors:
                ax, ay = block.anchors[a]
                mx, my = mouse_pos

                distance = ((ax - mx) ** 2 + (ay - my) ** 2) ** 0.5
                if distance < 15:
                    break_line = False
                    if sel1 is None:
                        sel1 = (block, a)
                    elif sel1 != (block, a) and sel2 is None:
                        sel2 = (block, a)

                    if sel1 is not None and sel2 is not None:
                        lines.append((sel1, sel2))
                        sel1, sel2 = None, None
        if break_line:
            sel1 = None
            sel2 = None

    blocks.update(
        mousej_inputs,
        mouser_inputs,
        mouse_inputs,
        mouse_pos,
        mouse_motion,
        key_inputs,
        events,
    )

    last_mouse_pos = mouse_pos


def draw():
    win.fill("gray10")

    if sel1 is not None and sel2 is None:
        for b in blocks:
            b.draw_anchors(win, sel1[1])
        pygame.draw.aaline(
            win, "white", sel1[0].anchors[sel1[1]], mouse_pos, LINE_WIDTH
        )

    for line in lines:
        b1, a1 = line[0]
        b2, a2 = line[1]
        if not b1 in blocks or not b2 in blocks:
            lines.remove(line)
            continue

        pygame.draw.aaline(win, "white", b1.anchors[a1], b2.anchors[a2], LINE_WIDTH)

    buttons.draw(win)
    labels.draw(win)
    blocks.draw(win)

    win.blit(font32.render(str(round(clock.get_fps())), False, "white"), (16, 16))


def main():
    while True:
        run()
        draw()

        pygame.display.flip()
        clock.tick()


if __name__ == "__main__":
    main()
