import pygame
from pygame.constants import FULLSCREEN, QUIT
from pygame.display import set_mode
from pygame.font import Font
from pygame.sprite import Group
from pygame.time import Clock

from blocks import Block, TextBlock

pygame.init()

win = set_mode((0, 0), FULLSCREEN, vsync=1)

clock = Clock()

# fonts
font = Font(size=64)
font32 = Font(size=32)
font96 = Font(size=96)

# groups
buttons = Group()
labels = Group()

blocks = Group()


last_mouse_pos = (0, 0)


def run():
    global last_mouse_pos

    mousej_inputs = pygame.mouse.get_just_pressed()
    mouse_inputs = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_motion = (mouse_pos[0] - last_mouse_pos[0], mouse_pos[1] - last_mouse_pos[1])
    key_inputs = pygame.key.get_pressed()
    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            quit()

    if mousej_inputs[2]:
        TextBlock(blocks, mouse_pos, font)

    blocks.update(
        mousej_inputs, mouse_inputs, mouse_pos, mouse_motion, key_inputs, events
    )

    last_mouse_pos = mouse_pos


def draw():
    win.fill("gray10")

    for block in blocks:
        block.draw_anchors(win)

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
