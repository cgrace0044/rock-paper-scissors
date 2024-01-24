import gspread
from google.oauth2.service_account import Credentials
import enum
import random
import os
import time
import pyfiglet
import colorama
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


class Hand(enum.Enum):
    paper = enum.auto()
    rock = enum.auto()
    scissors = enum.auto()


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

def get_user_choice():
    input_valid = False
    user_play = ''
    while input_valid is False:
        user_choice = input("Select your play: '1' Rock, '2' Scissors, '3' Paper : ")
        if user_choice in ['1', '2', '3']: 
            input_valid = True
            if user_choice == '1':
                user_play = Hand.rock
            if user_choice == '2':
                user_play = Hand.scissors
            if user_choice == '3':
                user_play = Hand.paper
        else:
            print('Please enter "1", "2" or "3"')
    return user_play


def welcome():
    print(pyfiglet.figlet_format(
            "Rock Paper Scissors", justify="center", width=80))
    print(
            Fore.GREEN + Style.BRIGHT +
            "Can you beat the computer?\n".center(80))
    username = input(
            Fore.MAGENTA + Style.BRIGHT +
            "Please enter your name to begin.\n").strip().capitalize()
    print(
        Fore.GREEN + Style.BRIGHT +
        "Hello " + username + Style.RESET_ALL)
    time.sleep(3)
    os.system('clear')
    menu()

def menu():
    """
    play game or view instructions screen
    """
    print('Please choose from the following options:\n')
    user_option = input(
        f"{Fore.CYAN}P - PLAY\nI - INSTRUCTIONS{Fore.RESET}\n"
        ).strip().lower()

    if user_option == "p":
            main()

    elif user_option == "i":
        #  Credit: https://www.asciiart.eu/art-and-design/borders
        intro_message = """
             __| |____________________________________________| |__
            (__   ____________________________________________   __)
               | |                                            | |
               | |               How to Play                  | |
               | |                                            | |
               | |    Play Rock, Paper, Scissors against      | |
               | |               the computer.                | |
               | |                                            | |
               | | Press 1 for rock, 2 for Scissors and 3 for | |
               | |                  paper.                    | |
               | |                                            | |
               | |            Rock beats Scissors             | |
               | |            Scissors beats Paper            | |
               | |              Paper beats Rock              | |
               | |                                            | |
               | |         Can you beat the computer?         | |
             __| |____________________________________________| |__
            (__   ____________________________________________   __)
               | |                                            | |
            """
        print(intro_message)
    else:
            print(Fore.RED + "Not a valid option\n")
            self.menu()

def main():
    # while the game is not finished:
    # each opponent produces one of rock, paper or scissors
    # the game logic decides who wins or if its a draw
    welcome()
    game_is_finished = False
    round = 1
    while not game_is_finished:
        player_one_hand = get_user_choice()
        player_two_hand = get_random_hand()

        print(f"Round {round} - Player one has produced: {player_one_hand}")
        print(f"Round {round} - Player two has produced: {player_two_hand}")

        result = decide_who_wins(player_one_hand, player_two_hand)
        if result == Result.draw:
            round += 1
            continue
        print(f'result : {result}')
        game_is_finished = True
        winner = "player1" if result.player_one_wins else "player2"
        print(f"This game was won by {winner} in round {round}")


if __name__ == "__main__":
    main()