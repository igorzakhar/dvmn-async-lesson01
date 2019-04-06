import time
import curses


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    row, column = (5, 20)
    symbol = '*'
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        time.sleep(2)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        time.sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        time.sleep(0.5)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        time.sleep(0.3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
