import pytest
from cards import parse_card
from hand_rank7 import rank7

def H(*ss):
    """Helper: parse strings like 'Ah','Td' into card tuples."""
    return [parse_card(s) for s in ss]

def test_requires_exactly_seven_and_no_duplicates():
    # wrong sizes
    with pytest.raises(ValueError):
        rank7(H("Ah","Kh","Qh","Jh","Th","9h"))  # 6 cards
    with pytest.raises(ValueError):
        rank7(H("Ah","Kh","Qh","Jh","Th","9h","8h","7h"))  # 8 cards
    # duplicates
    with pytest.raises(ValueError):
        rank7(H("Ah","Ah","Qh","Jh","Th","9h","8h"))

def test_royal_flush_on_board_is_detected():
    # Board: royal flush in hearts, Hole: irrelevant low cards
    cards = H("Ah","Kh","Qh","Jh","Th","2c","3d")
    r = rank7(cards)
    # Straight flush with high card Ace (14) -> (8, 14)
    assert r[0] == 8 and r[1] == 14

def test_flush_improves_with_hole_over_board():
    # Board has a heart flush A,K,8,4,2; hole adds Qh which should replace 2h
    cards = H("Ah","Kh","8h","4h","2h","Qh","9c")
    r = rank7(cards)
    # Best flush should be A,K,Q,8,4
    assert r[0] == 5 and r[1:] == (14, 13, 12, 8, 4)

def test_trips_on_board_becomes_full_house_with_hole_pair():
    # Board: 9 9 9 5 2; Hole: 5 A  -> Full house 9 over 5
    cards = H("9h","9d","9s","5c","2d","5s","Ah")
    r = rank7(cards)
    assert r[0] == 6 and r[1:] == (9, 5)

def test_straight_uses_hole_card():
    # Board: 5 6 7 8 K (no straight by itself)
    # Hole adds 9 to make a 9-high straight (5-9)
    cards = H("5c","6d","7h","8s","Kc","9d","2h")
    r = rank7(cards)
    assert r[0] == 4 and r[1] == 9

def test_category_ordering_against_another_hand():
    # Hand A: strong flush (should beat two pair)
    handA = H("Ah","Kh","Qh","4h","2h","9c","9d")  # flush hearts A,K,Q,4,2
    # Hand B: at best two pair K and 9 (no flush/straight)
    handB = H("Kd","Ks","9h","9s","3c","2d","5s")
    rA = rank7(handA)
    rB = rank7(handB)
    assert rA[0] == 5          # flush
    assert rB[0] == 2          # two pair
    assert rA > rB