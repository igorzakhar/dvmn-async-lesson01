import asyncio
import curses
import random
import time


TIC_TIMEOUT = 0.1


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        for tic in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for tic in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        for tic in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        for tic in range(3):
            await asyncio.sleep(0)


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

    while True:
        for coro in coroutines:

            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)

        if len(coroutines) == 0:
            break
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
