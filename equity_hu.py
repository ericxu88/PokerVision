# 2 player headsup equity calculations
# 1 or 2 unknown cards (turn and river)

#hero_hole and villain_hole

from typing import List, Tuple, Dict
from itertools import combinations
import math

from cards import make_deck, Card
from hand_rank7 import rank7

def _validate_inputs(hero_hole: List[Card], villain_hole: List[Card], board_partial: List[Card]):
    if len(hero_hole) != 2 or len(villain_hole) != 2:
        raise ValueError("Both hero and villain must have exactly 2 hole cards.")
    if len(board_partial) > 5:
        raise ValueError("Board can have at most 5 cards.")
    all_cards = hero_hole + villain_hole + board_partial
    if len(set(all_cards)) != len(all_cards):
        raise ValueError("All cards must be distinct.")
    
def _choose(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)

def enumerate_runouts(hero_hole: List[Card], villain_hole: List[Card], board_partial: List[Card], *, allow_large: bool = False,) -> Dict[str, int]:
    #find how many cards still unknown in the board
    # build remaining deck
    # enumerate runouts for the remaining cards
    # score the runouts
    # return Win/ties/total count (equity is expected share of the pot, and ties are half)
    # equity is (wins + 0.5 * ties) / total
    _validate_inputs(hero_hole, villain_hole, board_partial)

    need = 5 - len(board_partial)
    if need < 0:
        raise ValueError("Board cannot have more than 5 cards.")
    if need > 2 and not allow_large:
        raise ValueError("Cannot enumerate runouts with more than 2 unknown cards.")
    
    used = hero_hole + villain_hole + board_partial
    deck = make_deck(exclude=used)

    #counts
    wins = ties = total = 0

    #enumerate runouts
    for drawn in combinations(deck, need):
        full_board = board_partial + list(drawn)

        hero_best = rank7(hero_hole + full_board)
        villain_best = rank7(villain_hole + full_board)

        if hero_best > villain_best:
            wins += 1
        elif hero_best == villain_best:
            ties += 1
        total += 1

    return {"wins": wins, "ties": ties, "total": total}

def equity_hu_exact(hero_hole: List[Card], villain_hole: List[Card], board_partial: List[Card], *, allow_large: bool = False) -> Dict[str, float]:
    #calculate exact equity for 1v1 poker
    counts = enumerate_runouts(hero_hole, villain_hole, board_partial, allow_large=allow_large)
    
    Wins, Ties, Total = counts["wins"], counts["ties"], counts["total"]

    if Total == 0:
        equity = 0.0
    else: 
        equity = (Wins + 0.5 * Ties) / Total

    return {"equity": equity, "wins": Wins, "ties": Ties, "total": Total}
