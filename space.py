import asyncio
import curses
import time


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
    row = 5
    coroutines = [blink(canvas, row, column) for column in range(20, 45, 5)]

    while True:
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                coroutines.remove(coro)
        if len(coroutines) == 0:
            break

        time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
