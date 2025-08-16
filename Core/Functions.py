import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colorizeInput(prompt:str):
    print(prompt, end='', flush=True)
    ch = input()
    print()
    return ch