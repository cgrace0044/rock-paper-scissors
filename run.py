"""
Import libraries needed for game.
"""

from datetime import date
import enum
import random
import os
import time
import warnings

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
LEADERBOARD = GSPREAD_CLIENT.open("rock_paper_scissors").worksheet(
    "leaderboard"
)


class Context:
    """
    Main Game Class. Sets username, the total number of games and the score.
    """

    def __init__(self, username, total_games=5):
        self.username = username
        self.total_games = total_games
        self.current_game = 1
        self.score = 0


class Result(enum.Enum):
    """
    An enum that represents the result of the game.
    There are three possible outcomes:
    Player 1 wins, Player 2 wins or a draw.
    """

    player_one_wins = enum.auto()
    player_two_wins = enum.auto()
    draw = enum.auto()


class Hand(int, enum.Enum):
    """
    Class which defines the three possible hands in the game:
    Paper, Rock or Scissors.
    """

    paper = 1
    rock = 2
    scissors = 3


def is_valid_username(val: str, max_length: int = 15) -> bool:
    """
    Function which validates the username input.
    The username should be greater than 0 characters but less than 15.
    """
    return 0 < len(val) <= max_length


def decide_who_wins(player_one_hand: Hand, player_two_hand: Hand) -> Result:
    """
    This function decides who wins the game.
    Rock crushes scissors.
    Scissors cuts paper.
    Paper covers rock.
    If the computer and the user produce the same hand it is a draw.
    """
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
    """
    Generates a random hand for the computer.
    """
    return random.choice([Hand.paper, Hand.scissors, Hand.rock])


def get_user_choice() -> Hand:
    """
    Allows the user to choose 1. Paper, 2. Rock or 3. Scissors.
    If the user chooses anything other than 1, 2 or 3 a ValueError appears.
    """
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
    """
    This function clears the screen when called.
    """
    os.system("clear")


def main() -> None:
    """
    This is the function for the welcome screen at the beginning of the game.
    It displays the name of the game, asks for a username and greets the user.
    If the username is valid the user is redirected to the main menu.
    """
    print(
        pyfiglet.figlet_format(
            "Rock Paper Scissors", justify="center", width=80
        )
    )
    print(
        Fore.GREEN + Style.BRIGHT + "Can you beat the computer?\n".center(80)
    )

    username = ""
    while True:
        username = (
            input(
                Fore.YELLOW
                + Style.BRIGHT
                + "Please enter your name to begin: "
            )
            .strip()
            .capitalize()
        )
        if not is_valid_username(username):
            print(
                Fore.RED
                + Style.BRIGHT
                + "Username length must be between 1 and 15 characters"
            )
        else:
            break

    context = Context(username)

    print(
        Fore.GREEN
        + Style.BRIGHT
        + f"Hello {context.username}"
        + Style.RESET_ALL
    )
    time.sleep(3)
    clear_screen()
    show_menu(context)


def show_menu(context: Context) -> None:
    """
    This defines the main menu of the game. There are three options:
    1. Play
    2. Instructions
    3. Leaderboard
    Any other selections will trigger a ValueError.
    """
    print("Please choose from the following options:\n")
    menu_option = input(
        f"{Fore.GREEN + Style.BRIGHT}1 - PLAY\n2 - INSTRUCTIONS\n"
        f"3 - LEADERBOARD{Fore.RESET}\n"
    ).strip()
    if menu_option == "1":
        run_game(context)
    elif menu_option == "2":
        show_instructions(context)
    elif menu_option == "3":
        show_leaderboard(context)
    else:
        print("please select 1, 2 or 3")
        time.sleep(2)
        show_menu(context)


def show_instructions(context: Context) -> None:
    """
    This function controls the instructions screen.
    It displays the instructions and provides 2 options:
    1. Play - starts the game.
    2. Quit - brings the user to the gameover screen.
    Any other selections will trigger a ValueError.
    """
    clear_screen()
    rules = """
                  ____________________________________________
                 |                                            |
                 |               Instructions                 |
                 |                                            |
                 |         Play Rock Paper Scissors!          |
                 |                                            |
                 |            Rock beats Scissors             |
                 |           Scissors beats Paper             |
                 |              Paper beats Rock              |
                 |                                            |
                 |        Can you beat the computer?          |
                 |   How many games can you win out of 5?     |
                 |                                            |
                 |   In the case of a draw another round of   | 
                 | the same game is generated until there is  |
                 |             an outright winner.            |
                 |                                            |
                 |        Press 1 to Play or 2 to Quit        |
                 |                                            |
                 |____________________________________________|
    """
    print(rules)
    instructions_option = input(
        f"{Fore.GREEN}1 - PLAY\n2 - QUIT{Fore.RESET}\n"
    ).strip()
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


def show_leaderboard(context: Context) -> None:
    """
    This function controls the leaderboard screen.
    It displays the leaderboard from Google Sheets.
    Then it provides two options:
    1. Play - starts the game
    2. Quit - brings the user to the gameover screen
    Any other selections will trigger a ValueError.
    """
    clear_screen()
    for name, score, date in LEADERBOARD.get_all_values()[1:][0:10]:
        print(f"{name} scored {score} on {date}")
    leaderboard_option = input(
        f"{Fore.GREEN}1 - PLAY\n2 - QUIT{Fore.RESET}\n"
    ).strip()
    if leaderboard_option == "1":
        clear_screen()
        run_game(context)
    elif leaderboard_option == "2":
        clear_screen()
        gameover()
    else:
        print("please select 1 or 2")
        time.sleep(2)
        show_leaderboard(context)


def gameover() -> None:
    """
    This function controls the Gameover screen.
    It displays Gameover text from Pyfiglet.
    """
    clear_screen()
    print(pyfiglet.figlet_format("Gameover", justify="center", width=80))


def add_new_entry_leaderboard(context: Context) -> None:
    """
    Add name, score and date to row in leaderboard Google Sheet.
    The leaderboard is sorted from highest score to lowest.
    A future deprecation warning of GSHEET is ignored.
    The warning is ignored as it is not valid for the
    Python version in Heroku or the IDE.
    """
    today = date.today()
    date_format = today.strftime("%d/%m/%Y")
    print(Fore.GREEN + Style.BRIGHT + "Updating leaderboard...\n")
    LEADERBOARD.append_row([context.username, context.score, date_format])
    # supress future deprecation warning for gsheet >= 6.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # now sort by score
        LEADERBOARD.sort((2, "des"))
    print(Fore.GREEN + Style.BRIGHT + "Leaderboard Updated.\n")


def run_game(context: Context) -> None:
    """
    This function controls the flow of the Game.
    1. The get_user_choice function is called to display the user's hand.
    2. The get_random_hand function is called to display the computer's hand.
    3. The 2 functions are within a while loop so that 5 games are played.
    4. The decide_who_wins function is called to decide the result.
    5. The result of each game is printed to the terminal.
    6. Once 5 games have been played the overall winner is printed.
    7. The play_again function is then called which has two options:
        1. Start Again - brings the user back to the Welcome Screen.
        2. Quit - displays the gameover screen.
    """
    clear_screen()
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
                + f"Round {round} - {context.username} has produced: "
                + f"{player_one_hand.name}"
            )
            print(
                Fore.MAGENTA
                + Style.BRIGHT
                + f"Round {round} - Computer has produced: {player_two_hand.name}\n"
            )

            result = decide_who_wins(player_one_hand, player_two_hand)
            if result == Result.draw:
                print(
                    Fore.WHITE
                    + Style.BRIGHT
                    + "Draw! Play game again!"
                    )
                round += 1
                continue

            winner = (
                f"{context.username}"
                if result == Result.player_one_wins
                else "Computer"
            )
            print(f"{Fore.WHITE}=======================================")
            print(
                Fore.WHITE
                + Style.BRIGHT
                + f"This game was won by {winner} in round {round}"
            )
            print(f"{Fore.WHITE}=======================================\n")
            if result == Result.player_one_wins:
                context.score += 1

            game_is_finished = True
            context.current_game += 1

    print(f"\n{Fore.YELLOW}=======================================\n")
    print(
        Fore.YELLOW
        + Style.BRIGHT
        + f"{context.username} has a total score of {context.score} "
        + f"out of {context.total_games}\n"
    )
    print(f"{Fore.YELLOW}=======================================\n")
    add_new_entry_leaderboard(context)

    play_again()


def play_again():
    over_option = input(
        f"{Fore.GREEN}1 - START AGAIN \n2 - QUIT{Fore.RESET}\n"
    ).strip()
    if over_option == "1":
        clear_screen()
        main()
    elif over_option == "2":
        clear_screen()
        gameover()
    else:
        print("please select 1 or 2")
        time.sleep(2)
        play_again()


if __name__ == "__main__":
    main()
