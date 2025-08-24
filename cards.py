# card and deck utils
#   - card is tuple (rank, suit)
#   - rank has values {2,... 14} where 14 = ace
#   - suit is {s, h, d, c} for spades, hearts, diamonds, clubs

from typing import List, Tuple, Iterable, Sequence, Optional
import random

# mappings
RANKS = "23456789TJQKA"
SUITS = "shdc"

RANK_TO_VAL = {r: i + 2 for i, r in enumerate(RANKS)}
VAL_TO_RANK = {v: r for r, v in RANK_TO_VAL.items()}

Card = Tuple[int, str]  # (rank, suit)

#parsing card strings into tuple
def parse_card(card_str: str) -> Card:
    if not isinstance(card_str, str):
        raise ValueError(f"Expected string, got {type(card_str).__name__}")
    if len(card_str) != 2:
        raise ValueError(f"Bad card '{card_str}': must be 2 chars")
    r, su = card_str[0].upper(), card_str[1].lower()
    if r not in RANK_TO_VAL:
        raise ValueError(f"Bad rank in '{card_str}'")
    if su not in SUITS:
        raise ValueError(f"Bad suit in '{card_str}'")
    return (RANK_TO_VAL[r], su)

#format tuple back to string
def card_str(card: Card) -> str:
    v, su = card
    if v not in VAL_TO_RANK or su not in SUITS:
        raise ValueError(f"Bad card {card}")
    return f"{VAL_TO_RANK[v]}{su}"

#create deck
def make_deck(exclude: Iterable[Card] = ()) -> List[Card]:
    #exclude is for excluding cards on the table
    excl = set(exclude)
    deck: List[Card] = []
    for v in range(2, 15):
        for su in SUITS:
            card = (v, su)
            if card not in excl:
                deck.append(card)
    return deck

#draw n distinct cards without replacement and returning drawn cards and remaining deck
def deal(deck: Sequence[Card], n: int, *, rng: Optional[random.Random] = None) -> Tuple[List[Card], List[Card]]:
    if n < 0 or n > len(deck):
        raise ValueError(f"Cannot deal {n} cards from deck of size {len(deck)}")
    if rng is None:
        idxs = sorted(random.sample(range(len(deck)), n))
    else:
        idxs = sorted(rng.sample(range(len(deck)), n))

    drawn = [deck[i] for i in idxs]
    remaining = [deck[i] for i in range(len(deck)) if i not in set(idxs)]
    return drawn, remaining

def shuffle_deck(*, rng: Optional[random.Random] = None) -> List[Card]:
    deck = make_deck()
    if rng is None:
        random.shuffle(deck)
    else:
        rng.shuffle(deck)
    return deck

def all_card_strings() -> List[str]:
    return [f"{VAL_TO_RANK[v]}{su}" for v in range(2, 15) for su in SUITS]
