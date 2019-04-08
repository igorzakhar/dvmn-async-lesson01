import asyncio
import itertools


async def animation_frames(canvas, start_row, start_column, frames):
    frames_cycle = itertools.cycle(frames)

    while True:
        current_frame = next(frames_cycle)

        frame_size_y, frame_size_x = get_frame_size(current_frame)
        frame_pos_x = round(start_column) - round(frame_size_x / 2)
        frame_pos_y = round(start_row) - round(frame_size_y / 2)

        draw_frame(canvas, frame_pos_y, frame_pos_x, current_frame)
        canvas.refresh()

        for tic in range(3):
            await asyncio.sleep(0)

        draw_frame(
            canvas,
            frame_pos_y,
            frame_pos_x,
            current_frame,
            negative=True
        )


def draw_frame(canvas, start_row, start_column, text, negative=False):
    """Draw multiline text fragment on canvas. Erase text instead of drawing
    if negative=True is specified."""

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            # Check that current position it is not in a lower
            # right corner of the window.

            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/urses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


def get_frame_size(text):
    """Calculate size of multiline text fragment. Returns pair (rows number,
    colums number)"""

    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns
