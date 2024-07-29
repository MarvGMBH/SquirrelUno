import curses
import time

def main(stdscr):
    # Turn off cursor blinking
    curses.curs_set(0)

    # Get initial screen height and width
    height, width = stdscr.getmaxyx()

    # Initial position and direction
    x = width // 2
    y = height // 2
    direction = 1

    while True:
        # Get current screen height and width
        height, width = stdscr.getmaxyx()

        # Clear the screen
        stdscr.clear()

        # Create a simple box
        for i in range(height):
            for j in range(width):
                if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                    try:
                        stdscr.addch(i, j, '#')
                    except curses.error:
                        pass

        # Update position
        x += direction
        if x >= width - 1 or x <= 0:
            direction = -direction

        # Add moving text
        text = "Moving Text"
        text_x = x - len(text) // 2
        if text_x < 0:
            text_x = 0
        if text_x + len(text) >= width:
            text_x = width - len(text) - 1
        try:
            stdscr.addstr(y, text_x, text)
        except curses.error:
            pass

        # Refresh the screen to show content
        stdscr.refresh()

        # Delay to control speed
        time.sleep(0.1)

        # Handle key press to exit
        key = stdscr.getch()
        if key == ord('q'):
            break

curses.wrapper(main)
