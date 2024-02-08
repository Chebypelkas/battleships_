import pygame as pg
from board import Board, EnemyBoard
import speech_recognition as sr
from constants import *


def main():
    rec = sr.Recognizer()

    pg.init()

    window = DISPLAY
    window.fill('white')
    pg.display.flip()

    board = Board(0, 'blue')
    enemy_board = EnemyBoard(WIDTH_WINDOW/2, 'red')

    board.draw(window)
    enemy_board.draw(window)
    pg.display.flip()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    listen(rec, enemy_board, window)

        board.update()
        enemy_board.update()

        board.draw(window)
        enemy_board.draw(window)

        pg.display.flip()


def listen(rec: sr.Recognizer, board: Board, window: pg.Surface):
    with sr.Microphone() as mic:
        print('начал слушать')
        audio = rec.listen(mic)
        print('закончил слушать')

    try:
        text = latin_to_cyrill(rec.recognize_google(audio, language='ru-RU').lower().replace('-', ''))

        print(text)

        for char in letters:
            for number in range(10):
                if f'{char}{number}' in text:
                    shooting(char, number, board, window)
                    break
            else:
                continue
            break
    except sr.exceptions.UnknownValueError:
        print('UnknownValueError, кажется, что вы ни чего не сказали')


def shooting(char: str, number: int, board: Board, window: pg.Surface):
    pos = f'{char}{number}'
    for ship in board.ships:
        for cell in ship.rects:
            if board.cells[pos].rect.colliderect(cell):
                pg.draw.circle(window, 'red', board.cells[pos].rect.center, 5)
            else:
                pg.draw.circle(window, 'black', board.cells[pos].rect.center, 5)


def latin_to_cyrill(word: str) -> str:
    result = word
    if word == 'опять':
        return 'о5'
    for char in word:
        if char in lat_letters:
            result = result.replace(char, LAT_TO_CYRILL[char])
    return result


if __name__ == '__main__':
    main()
