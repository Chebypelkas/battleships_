from cells import Cell
import pygame as pg


class Ship:
    def __init__(self, cells: list[Cell]):
        self.rects = [cell.rect for cell in cells]

    def update(self):
        pass

    def draw(self, window: pg.Surface):
        for rect in self.rects:
            pg.draw.rect(window, 'black', rect)
