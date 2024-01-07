import pygame
import pygame as pg
from board import Board
from constants import *


def main():
    pg.init()
    window = DISPLAY
    window.fill('white')
    pg.display.flip()
    board = Board()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        board.update()
        board.draw(window)
        pg.display.flip()


if __name__ == '__main__':
    main()
