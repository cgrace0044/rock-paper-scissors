from datetime import date
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
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("rock_paper_scissors")


class Context:
    """Game context"""

    def __init__(self, username, total_games=5):
        self.username = username
        self.total_games = total_games
        self.current_game = 1
        self.score = 0


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
        raise ValueError("Unknown combination of hands")


def get_random_hand() -> Hand:
    return random.choice([Hand.paper, Hand.scissors, Hand.rock])


def get_user_choice() -> Hand:
    while True:
        user_choice = input(
            Fore.CYAN
            + Style.BRIGHT
            + "Select your play: '1' Paper, '2' Rock, '3' Scissors: "
        )
        try:
            user_play = Hand(int(user_choice))
            return user_play
        except ValueError:
            print('Please enter "1", "2" or "3"')
            continue


def clear_screen() -> None:
    os.system("clear")


def main() -> None:
    """
    Display name of game and ask for username.
    Greet the user by their username.
    """
    print(pyfiglet.figlet_format("Rock Paper Scissors", justify="center", width=80))
    print(Fore.GREEN + Style.BRIGHT + "Can you beat the computer?\n".center(80))
    username = (
        input(Fore.MAGENTA + Style.BRIGHT + "Please enter your name to begin: ")
        .strip()
        .capitalize()
    )
    context = Context(username)

    print(Fore.GREEN + Style.BRIGHT + f"Hello {context.username}" + Style.RESET_ALL)
    time.sleep(3)
    clear_screen()
    show_menu(context)


def show_menu(context: Context) -> None:
    print("Please choose from the following options:\n")
    menu_option = input(f"{Fore.GREEN}1 - PLAY\n2 - INSTRUCTIONS{Fore.RESET}\n").strip()
    if menu_option == "1":
        run_game(context)
    elif menu_option == "2":
        show_instructions(context)
    else:
        print("please select 1 or 2")
        time.sleep(2)
        show_menu(context)


def show_instructions(context: Context) -> None:
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
    instructions_option = input(f"{Fore.GREEN}1 - PLAY\n2 - QUIT{Fore.RESET}\n").strip()
    if instructions_option == "1":
        clear_screen()
        run_game(context)
    elif instructions_option == "2":
        clear_screen()
        gameover()
    else:
        print("please select 1 or 2")
        time.sleep(2)
        show_instructions(context)


def gameover() -> None:
    clear_screen()
    print(pyfiglet.figlet_format("Gameover", justify="center", width=80))


def add_new_entry_leaderboard(context: Context) -> None:
    """
    Add name, score and date to row in leaderboard Google Sheet.
    """
    leaderboard = SHEET.worksheet("leaderboard")
    today = date.today()
    date_format = today.strftime("%d/%m/%Y")
    print("Updating leaderboard...\n")
    leaderboard.append_row([context.username, context.score, date_format])
    print(Fore.GREEN + Style.BRIGHT + "Leaderboard Updated.\n")


def run_game(context: Context) -> None:
    # while the game is not finished:
    # each opponent produces one of rock, paper or scissors
    # the game logic decides who wins or if its a draw
    while context.current_game < context.total_games + 1:
        game_is_finished = False
        round = 1
        while not game_is_finished:
            print(Fore.GREEN + Style.BRIGHT + f"Game {context.current_game}")

            player_one_hand = get_user_choice()
            player_two_hand = get_random_hand()

            print(
                Fore.MAGENTA
                + Style.BRIGHT
                + f"Round {round} - {context.username} has produced: {player_one_hand}"
            )
            print(
                Fore.MAGENTA
                + Style.BRIGHT
                + f"Round {round} - Computer has produced: {player_two_hand}\n"
            )

            result = decide_who_wins(player_one_hand, player_two_hand)
            if result == Result.draw:
                round += 1
                continue

            winner = (
                f"{context.username}"
                if result == Result.player_one_wins
                else "Computer"
            )
            print(
                Fore.WHITE
                + Style.BRIGHT
                + f"This game was won by {winner} in round {round}\n"
            )
            if result == Result.player_one_wins:
                context.score += 1

            game_is_finished = True
            context.current_game += 1

    print(
        f"{context.username} has a total score of {context.score} out of {context.total_games}"
    )
    add_new_entry_leaderboard(context)


if __name__ == "__main__":
    main()
