import pygame as pg


WIDTH_WINDOW = 600
HEIGHT_WINDOW = 600
DISPLAY = pg.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
FPS = 60
CELL_MAP = {}
letters = 'абвгдежзик'
for x in range(10):
    for y in range(10):
        CELL_MAP[x, y] = f'{letters[x] + str(y + 1)}'  # быстрое создание словаря
