import asyncio
import curses
import random
import time

from fire_animation import fire


TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):
    offset = random.randint(0, 3)
    while True:
        if offset == 0:
            canvas.addstr(row, column, symbol, curses.A_DIM)

            for tic in range(20):
                await asyncio.sleep(0)
            offset += 1

        if offset == 1:
            canvas.addstr(row, column, symbol)

            for tic in range(3):
                await asyncio.sleep(0)
            offset += 1

        if offset == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)

            for tic in range(5):
                await asyncio.sleep(0)
            offset += 1

        if offset == 3:
            canvas.addstr(row, column, symbol)

            for tic in range(3):
                await asyncio.sleep(0)
            offset = 0


def stars_generator(height, width, number=50):
    for star in range(number):
        y_pos = random.randint(1, height - 2)
        x_pos = random.randint(1, width - 2)
        symbol = random.choice(['+', '*', '.', ':'])
        yield y_pos, x_pos, symbol


def main(canvas):
    curses.curs_set(False)
    canvas.border()
    height, width = canvas.getmaxyx()

    coroutines = [
        blink(canvas, row, column, symbol)
        for row, column, symbol in stars_generator(height, width)
    ]

    start_row = height - 2
    start_col = width / 2
    coro_shot = fire(canvas, start_row, start_col)
    coroutines.append(coro_shot)

    while True:
        canvas.refresh()
        index = 0
        while index < len(coroutines):
            coro = coroutines[index]
            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)
            index += 1

        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
