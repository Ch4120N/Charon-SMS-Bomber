from Core.Functions import clear_screen
from colorama import Fore, init
init()



class Banner:
    @staticmethod
    def DefaultBanner():
        clear_screen()
        return f"""{Fore.CYAN}

 ▄████▄   ██░ ██   ██████  ███▄ ▄███▓  ██████  ▄▄▄▄    ▒█████   ███▄ ▄███▓ ▄▄▄▄   ▓█████  ██▀███  
▒██▀ ▀█  ▓██░ ██▒▒██    ▒ ▓██▒▀█▀ ██▒▒██    ▒ ▓█████▄ ▒██▒  ██▒▓██▒▀█▀ ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒
▒▓█    ▄ ▒██▀▀██░░ ▓██▄   ▓██    ▓██░░ ▓██▄   ▒██▒ ▄██▒██░  ██▒▓██    ▓██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒
▒▓▓▄ ▄██▒░▓█ ░██   ▒   ██▒▒██    ▒██   ▒   ██▒▒██░█▀  ▒██   ██░▒██    ▒██ ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  
▒ ▓███▀ ░░▓█▒░██▓▒██████▒▒▒██▒   ░██▒▒██████▒▒░▓█  ▀█▓░ ████▓▒░▒██▒   ░██▒░▓█  ▀█▓░▒████▒░██▓ ▒██▒
░ ░▒ ▒  ░ ▒ ░░▒░▒▒ ▒▓▒ ▒ ░░ ▒░   ░  ░▒ ▒▓▒ ▒ ░░▒▓███▀▒░ ▒░▒░▒░ ░ ▒░   ░  ░░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░
  ░  ▒    ▒ ░▒░ ░░ ░▒  ░ ░░  ░      ░░ ░▒  ░ ░▒░▒   ░   ░ ▒ ▒░ ░  ░      ░▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░
░         ░  ░░ ░░  ░  ░  ░      ░   ░  ░  ░   ░    ░ ░ ░ ░ ▒  ░      ░    ░    ░    ░     ░░   ░ 
░ ░       ░  ░  ░      ░         ░         ░   ░          ░ ░         ░    ░         ░  ░   ░     
░                                                   ░                           ░                 
                                                {Fore.LIGHTYELLOW_EX}Programming By {Fore.LIGHTWHITE_EX}AmirHossein Ghanami {Fore.LIGHTBLUE_EX}[ {Fore.LIGHTRED_EX}Ch4120N {Fore.LIGHTBLUE_EX}]
"""
    
    @staticmethod
    def AttackingBanner():
        clear_screen()
        return f"""{Fore.LIGHTRED_EX}
    ░█▀▀░█░█░█▀▀░█▄█░█▀▀░█▀▄░█▀█░█▄█░█▀▄░█▀▀░█▀▄
    ░█░░░█▀█░▀▀█░█░█░▀▀█░█▀▄░█░█░█░█░█▀▄░█▀▀░█▀▄
    ░▀▀▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀░░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀
              By {Fore.LIGHTWHITE_EX}AmirHossein Ghanami {Fore.LIGHTBLUE_EX}[ {Fore.LIGHTRED_EX}Ch4120N {Fore.LIGHTBLUE_EX}]
"""


class Menu:
    @staticmethod
    def MainMenu():
        return f"""
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}1{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Start
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}2{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Continue {Fore.LIGHTRED_EX}(DISABLED)
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}3{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Help
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}4{Fore.CYAN}]{Fore.LIGHTGREEN_EX} About
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}5{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Exit
"""
    @staticmethod
    def MainMenuContinue():
        return f"""
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}1{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Start
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}2{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Continue
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}3{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Help
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}4{Fore.CYAN}]{Fore.LIGHTGREEN_EX} About
 {Fore.CYAN}[{Fore.LIGHTWHITE_EX}5{Fore.CYAN}]{Fore.LIGHTGREEN_EX} Exit
"""