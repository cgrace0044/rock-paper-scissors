import enum
import random
import os
import time

import gspread
from google.oauth2.service_account import Credentials
import pyfiglet
from colorama import Fore, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

class Result(enum.Enum):
    player_one_wins = enum.auto()
    player_two_wins = enum.auto()
    draw = enum.auto()


class Hand(int, enum.Enum):
    paper = 1
    rock = 2
    scissors = 3


def decide_who_wins(player_one_hand: Hand, player_two_hand: Hand) -> Result:
    if player_one_hand == player_two_hand:
        return Result.draw

    elif player_one_hand == Hand.paper:
        if player_two_hand == Hand.rock:
            return Result.player_one_wins
        if player_two_hand == Hand.scissors:
            return Result.player_two_wins
    elif player_one_hand == Hand.rock:
        if player_two_hand == Hand.paper:
            return Result.player_two_wins
        if player_two_hand == Hand.scissors:
            return Result.player_one_wins
    elif player_one_hand == Hand.scissors:
        if player_two_hand == Hand.paper:
            return Result.player_one_wins
        if player_two_hand == Hand.rock:
            return Result.player_two_wins
    else:
        raise ValueError(f"Unknown combination of hands")


def get_random_hand() -> Hand:
    return random.choice([Hand.paper, Hand.scissors, Hand.rock])

def get_user_choice() -> Hand:
    while True:
        user_choice = input(Fore.CYAN + Style.BRIGHT +"Select your play: '1' Paper, '2' Rock, '3' Scissors: ")
        try:
            user_play = Hand(int(user_choice))
            return user_play
        except ValueError:
            print('Please enter "1", "2" or "3"')
            continue


def welcome():
    """
    Display name of game and ask for username.
    Greet the user by their username.
    """
    print(pyfiglet.figlet_format(
            "Rock Paper Scissors", justify="center", width=80))
    print(
            Fore.GREEN + Style.BRIGHT +
            "Can you beat the computer?\n".center(80))
    global username
    username = input(
            Fore.MAGENTA + Style.BRIGHT +
            "Please enter your name to begin: ").strip().capitalize()
    print(
        Fore.GREEN + Style.BRIGHT +
        f"Hello {username}" + Style.RESET_ALL)
    time.sleep(3)
    os.system('clear')
    menu()

def menu():
    print('Please choose from the following options:\n')
    menu_option = input(
        f"{Fore.GREEN}1 - PLAY\n2 - INSTRUCTIONS{Fore.RESET}\n"
        ).strip()
    if menu_option == "1":
        game()
    elif menu_option == "2":
        instructions()
    else:
        print('please select 1 or 2')
        time.sleep(2)
        menu()

def instructions():
    rules = """
                  ____________________________________________ 
               | |                                            | |
               | |               Instructions                 | |
               | |                                            | |
               | |         Play Rock Paper Scissors!          | |
               | |                                            | |
               | |            Rock beats Scissors             | |
               | |           Scissors beats Paper             | |
               | |              Paper beats Rock              | |
               | |                                            | |
               | |        Can you beat the computer?          | |
               | |                                            | |
               | |                                            | |
               | |                                            | |
               | |                                            | |
               | |____________________________________________| |
    """
    print(rules)
    instructions_option = input(
        f"{Fore.GREEN}1 - PLAY\n2 - QUIT{Fore.RESET}\n"
        ).strip()
    if instructions_option == "1":
        os.system('clear')
        game()
    elif instructions_option == "2":
        os.system('clear')
        gameover()
    else:
        print('please select 1 or 2')
        time.sleep(2)
        instructions()

def gameover():
    os.system('clear')
    print(pyfiglet.figlet_format(
            "Gameover", justify="center", width=80))
    time.sleep(3)
    os.system('clear')
    welcome()

def game():
    # while the game is not finished:
    # each opponent produces one of rock, paper or scissors
    # the game logic decides who wins or if its a draw
    game_is_finished = False
    round = 1
    while not game_is_finished:
        player_one_hand = get_user_choice()
        player_two_hand = get_random_hand()

        print(Fore.MAGENTA + Style.BRIGHT + f"Round {round} - {username} has produced: {player_one_hand}")
        print(Fore.MAGENTA + Style.BRIGHT + f"Round {round} - Computer has produced: {player_two_hand}\n")

        result = decide_who_wins(player_one_hand, player_two_hand)
        if result == Result.draw:
            round += 1
            continue

        game_is_finished = True
        winner = f"{username}" if result == Result.player_one_wins else "Computer"
        print(Fore.WHITE + Style.BRIGHT + f"This game was won by {winner} in round {round}\n")

def main():
    
    welcome()
    game()

if __name__ == "__main__":
    main()
