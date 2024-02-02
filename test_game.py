from run import decide_who_wins, Hand, Result


def test_decide_who_wins():
    """
    Add a test to ensure that the correct result is displaying for each game.
    """
    assert decide_who_wins(Hand.paper, Hand.rock) == Result.player_one_wins
    assert decide_who_wins(Hand.rock, Hand.rock) == Result.draw
    assert decide_who_wins(Hand.scissors, Hand.rock) == Result.player_two_wins
    assert decide_who_wins(Hand.paper, Hand.paper) == Result.draw
    assert decide_who_wins(Hand.rock, Hand.paper) == Result.player_two_wins
    assert decide_who_wins(Hand.scissors, Hand.paper) == Result.player_one_wins
    assert decide_who_wins(Hand.paper, Hand.scissors) == Result.player_two_wins
    assert decide_who_wins(Hand.rock, Hand.scissors) == Result.player_one_wins
    assert decide_who_wins(Hand.scissors, Hand.scissors) == Result.draw
