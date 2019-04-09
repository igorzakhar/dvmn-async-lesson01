import asyncio
import curses
import random
import time

from fire_animation import fire
from animation import animation_frames


TIC_TIMEOUT = 0.1


def load_frame_from_file(filename):
    with open(filename, 'r') as fd:
        return fd.read()


async def go_to_sleep(seconds):
    iteration_count = int(seconds * 10)
    for _ in range(iteration_count):
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol='*'):
    offset = random.randint(0, 3)
    while True:
        if offset == 0:
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await go_to_sleep(2)
            offset += 1

        if offset == 1:
            canvas.addstr(row, column, symbol)
            await go_to_sleep(0.3)
            offset += 1

        if offset == 2:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await go_to_sleep(0.5)
            offset += 1

        if offset == 3:
            canvas.addstr(row, column, symbol)
            await go_to_sleep(0.3)
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

    rocket_frame_1 = load_frame_from_file(
        'anim_frames/rocket/rocket_frame_1.txt'
    )
    rocket_frame_2 = load_frame_from_file(
        'anim_frames/rocket/rocket_frame_2.txt'
    )

    rocket_frames = (rocket_frame_1, rocket_frame_2)

    start_rocket_row = height / 2
    coro_rocket_anim = animation_frames(
        canvas,
        start_rocket_row,
        start_col,
        rocket_frames
    )
    coroutines.append(coro_rocket_anim)

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
