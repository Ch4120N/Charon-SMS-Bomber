from colorama import Fore, init
init()

VERSION = "2.1.1"
INPUT_HOME = f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTWHITE_EX}HOME{Fore.CYAN}]-[{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.WHITE} Choose > "
INPUT_BACKMENU = f"\n\n {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTYELLOW_EX}  Press {Fore.CYAN}[{Fore.LIGHTRED_EX}ENTER{Fore.CYAN}]{Fore.LIGHTYELLOW_EX} key to back to main menu ..."
INPUT_EXIT = f"\n\n {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTYELLOW_EX}  Press {Fore.CYAN}[{Fore.LIGHTRED_EX}ENTER{Fore.CYAN}]{Fore.LIGHTYELLOW_EX} key to exit ..."
INPUT_START = f"\n {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.WHITE}  Press {Fore.CYAN}[{Fore.YELLOW}CTRL+C{Fore.CYAN}]{Fore.WHITE} to stop the attacking or {Fore.CYAN}[{Fore.BLUE}ENTER{Fore.CYAN}]{Fore.WHITE} to start it"

PROMPTS = [
    f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTWHITE_EX}  Enter the target phone number (e.g,091234567890): ",
    f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTWHITE_EX}  Enter number of threads (e.g, 10):{Fore.WHITE} ",
    f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTWHITE_EX}  Enter the number of SMS sending rounds for each number {Fore.CYAN}({Fore.LIGHTYELLOW_EX}Max: 20{Fore.CYAN}):{Fore.WHITE} ",
    f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTMAGENTA_EX}INPUT{Fore.CYAN}]{Fore.LIGHTWHITE_EX}  Enter delay time in seconds (e.g., 1.5):{Fore.WHITE} ",
    
]