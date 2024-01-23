import gspread
from google.oauth2.service_account import Credentials
import enum
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

# Class for win scenarios
class Result(enum.Enum):
    player_one_wins = enum.auto()
    player_two_wins = enum.auto()
    draw = enum.auto()

# Class for hand scenarios
class Hand(enum.Enum):
    paper = enum.auto()
    rock = enum.auto()
    scissors = enum.auto()

# Decide who wins function
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
        raise ValueError(f"Unknown combination of hands: {player_one_hand} & {play