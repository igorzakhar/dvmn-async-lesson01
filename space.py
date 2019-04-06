import asyncio
import time
import curses


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        await asyncio.sleep(0)


def main(canvas):
    curses.curs_set(False)
    canvas.border()
    row, column = (5, 20)

    coro = blink(canvas, row, column, symbol='*')

    coro.send(None)
    coro.send(None)
    coro.send(None)
    time.sleep(10)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
