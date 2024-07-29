import curses
import time

class Console:
    def __init__(self):
        self.buffer = {}
        self.prev_buffer = {}
        self.running = False
        self.width = 0
        self.height = 0
        self.ui_fields = []

    def start(self):
        curses.wrapper(self.main)

    def main(self, stdscr):
        self.stdscr = stdscr
        self.running = True

        # Initialize curses settings
        curses.curs_set(0)  # Turn off cursor
        stdscr.nodelay(True)  # Non-blocking input
        stdscr.clear()  # Clear screen

        self.height, self.width = stdscr.getmaxyx()

        self.setup()

        while self.running:
            self.handle_input()
            self.on_update()
            self.draw()
            time.sleep(0.1)  # Control the update rate

    def setup(self):
        pass

    def register_ui_field(self, field):
        self.ui_fields.append(field)

    def handle_input(self):
        key = self.stdscr.getch()
        if key != -1:
            for field in self.ui_fields:
                if isinstance(field, InputField):
                    field.handle_key_press(key)
            self.on_key_press(key)
        if key == ord('q'):
            self.stop()

    def draw(self):
        updated = self.buffer != self.prev_buffer
        for field in self.ui_fields:
            if field.updated:
                field.draw()
                field.updated = False
                updated = True

        if updated:
            self.stdscr.clear()
            for (y, x), (char, attr) in self.buffer.items():
                try:
                    self.stdscr.addch(y, x, char, attr)
                except curses.error:
                    pass
            self.stdscr.refresh()
            self.prev_buffer = self.buffer.copy()

    def set_text(self, y, x, text, attr=curses.A_NORMAL):
        for i, char in enumerate(text):
            self.buffer[(y, x + i)] = (char, attr)

    def clear_text(self, y, x, length):
        for i in range(length):
            self.buffer.pop((y, x + i), None)

    def stop(self):
        self.running = False

    def on_update(self):
        pass

    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass

    def on_resize(self, new_height, new_width):
        pass

    def check_collision(self, y, x, text):
        for i, char in enumerate(text):
            if (y, x + i) in self.buffer:
                return True
        return False


class InputField:
    def __init__(self, console, y, x, prompt, max_length):
        self.console = console
        self.y = y
        self.x = x
        self.prompt = prompt
        self.max_length = max_length
        self.text = ""
        self.active = True
        self.updated = True  # Flag to track changes

    def draw(self):
        text = self.prompt + self.text
        text += "_" * (self.max_length - len(self.text))
        self.console.set_text(self.y, self.x, text)

    def handle_key_press(self, key):
        if not self.active:
            return

        if key in range(32, 127):  # Printable ASCII characters
            if len(self.text) < self.max_length:
                self.text += chr(key)
        elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            self.text = self.text[:-1]
        elif key == curses.KEY_ENTER or key == 10 or key == 13:  # Enter key
            self.on_text_enter(self.text)
            self.text = ""  # Clear text after enter

        display_text = self.text.ljust(self.max_length)
        self.console.set_text(self.y, self.x + len(self.prompt), display_text)
        self.updated = True

    def on_text_enter(self, text):
        pass
