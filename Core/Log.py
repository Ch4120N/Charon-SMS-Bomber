from datetime import datetime
from colorama import Fore, init
init(True)

class Logs:
    # def __init__(self) -> None:
    @staticmethod
    def gettime():
        return str(datetime.now().strftime("%H:%M:%S"))
    # def __init__(self):
    #     
    # self.
    @staticmethod
    def success(text:str):
        return f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTGREEN_EX}SUCCESS{Fore.LIGHTBLUE_EX}]{Fore.LIGHTGREEN_EX}  {text}"
    
    @staticmethod
    def failed(text:str):
        return f" {Fore.LIGHTBLUE_EX}[{Fore.LIGHTYELLOW_EX}{Fore.LIGHTYELLOW_EX}{Logs.gettime()}{Fore.LIGHTBLUE_EX}] [{Fore.LIGHTRED_EX}FAILED{Fore.LIGHTBLUE_EX}]{Fore.LIGHTRED_EX}  {text}"
    
    @staticmethod
    def error(text):
        return f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTRED_EX}ERROR{Fore.CYAN}]{Fore.LIGHTRED_EX}  {text}"
    @staticmethod
    def warning(text):
        return f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.YELLOW}WARNING{Fore.CYAN}]{Fore.YELLOW}  {text}"
    
    @staticmethod
    def generalMessage(text):
        return ("      " + text)
    
    @staticmethod
    def fetchMessage(text):
        return f" {Fore.CYAN}[{Fore.LIGHTGREEN_EX}ChSMSBomber{Fore.LIGHTBLUE_EX}@{Fore.LIGHTCYAN_EX}FETCH{Fore.CYAN}]{Fore.LIGHTWHITE_EX}  {text}"