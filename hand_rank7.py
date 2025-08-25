# reuses hand_rank5.py but enumerates C(7,5) = 21 possibilities of five-card subsets
# could optimize with a direct 7-card evaluator

from itertools import combinations
from typing import List, Tuple
from hand_rank5 import rank5

Card = Tuple[int, str]

def rank7(cards7: List[Card]) -> tuple:
    #get best 5-card poker hand available from 7 cards

    if len(cards7) != 7:
        raise ValueError("Expected exactly 7 cards")
    
    #check that all cards are distinct
    if len(set(cards7)) != 7:
        raise ValueError("Cards must be distinct")
    
    best = None

    for five in combinations(cards7, 5):
        r = rank5(list(five))
        if best is None or r > best:
            best = r

    return best