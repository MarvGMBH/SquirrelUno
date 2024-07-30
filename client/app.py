# ANSI escape codes for colors
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BLUE = "\033[38;5;45m"
LIGHT_PINK = "\033[38;5;218m"
WHITE = "\033[38;5;15m"
MAGENTA = "\033[35m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

def display_creator_message():
    creator_message = (f"{ORANGE}#############################################################{RESET}\n"
                       f"{' '*61}\n"
                       f"{' '*61}\n"
                       f"{' '*10}{LIGHT_BLUE}{BOLD}G{RESET}{LIGHT_PINK}{BOLD}a{RESET}{WHITE}{BOLD}m{RESET}{LIGHT_PINK}{BOLD}e {RESET}{LIGHT_BLUE}{BOLD}m{RESET}{LIGHT_PINK}{BOLD}a{RESET}{WHITE}{BOLD}d{RESET}{LIGHT_PINK}{BOLD}e {RESET}{LIGHT_BLUE}{BOLD}b{RESET}{LIGHT_PINK}{BOLD}y {RESET}{WHITE}{BOLD}C{RESET}{LIGHT_PINK}{BOLD}h{RESET}{LIGHT_PINK}{BOLD}i{RESET}{LIGHT_BLUE}{BOLD}p{RESET}{LIGHT_PINK}{BOLD}p{RESET}{WHITE}{BOLD}e{RESET}{LIGHT_PINK}{BOLD}r{RESET}{LIGHT_BLUE}{BOLD}f{RESET}{LIGHT_PINK}{BOLD}l{RESET}{WHITE}{BOLD}u{RESET}{LIGHT_PINK}{BOLD}f{RESET}{LIGHT_BLUE}{BOLD}f :P{RESET}\n"
                       f"{' '*61}\n"
                       f"{' '*61}\n"
                       f"{ORANGE}#############################################################{RESET}\n")
    print(creator_message)
    input(f"{MAGENTA}Press Enter to continue...{RESET}")