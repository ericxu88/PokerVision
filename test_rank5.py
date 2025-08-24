import pytest
from cards import parse_card
from hand_rank5 import rank5

def H(*ss):
    """Helper: parse a list of 'Ah','Td',... into [(14,'h'),(10,'d'),...]"""
    return [parse_card(s) for s in ss]

def test_requires_exactly_five_cards():
    with pytest.raises(ValueError):
        rank5(H("Ah","Kh","Qh","Jh"))            # 4 cards
    with pytest.raises(ValueError):
        rank5(H("Ah","Kh","Qh","Jh","Th","9h"))  # 6 cards

def test_straight_flush_and_wheel():
    # K-high straight flush
    sf = rank5(H("9h","Th","Jh","Qh","Kh"))
    assert sf[0] == 8 and sf[1] == 13  # high = King(13)

    # Wheel straight flush A-2-3-4-5 (Ace counts low -> high=5)
    wheel_sf = rank5(H("Ah","2h","3h","4h","5h"))
    assert wheel_sf == (8, 5)

def test_four_of_a_kind():
    r = rank5(H("Ah","Ad","Ac","As","2h"))
    assert r == (7, 14, 2)  # quads Aces, kicker 2

    # kicker comparison
    r1 = rank5(H("9s","9h","9d","9c","As"))
    r2 = rank5(H("9s","9h","9d","9c","Ks"))
    assert r1 > r2

def test_full_house():
    r = rank5(H("Kh","Kd","Kc","2s","2d"))
    assert r == (6, 13, 2)

    # tie-breaker: compare trip rank first, then pair rank
    r1 = rank5(H("Qs","Qh","Qd","9c","9d"))
    r2 = rank5(H("Js","Jh","Jd","As","Ad"))
    assert r1 > r2  # queens full > jacks full

def test_flush_no_straight():
    r = rank5(H("As","Ts","8s","4s","2s"))
    assert r[0] == 5 and r[1:] == (14,10,8,4,2)

    # flush vs flush tie-breakers
    r1 = rank5(H("Ks","9s","8s","6s","2s"))
    r2 = rank5(H("Ks","9s","8s","5s","2s"))
    assert r1 > r2

def test_straight_normal_and_wheel():
    r = rank5(H("Tc","Jh","Qs","Kd","Ah"))
    assert r == (4, 14)  # A-high straight

    wheel = rank5(H("Ad","2s","3h","4c","5d"))
    assert wheel == (4, 5)

def test_three_of_a_kind():
    r = rank5(H("Qh","Qd","Qc","7s","2d"))
    assert r == (3, 12, 7, 2)

    # kicker tie-breakers
    r1 = rank5(H("8h","8d","8c","Ah","9s"))
    r2 = rank5(H("8h","8d","8c","Ah","7s"))
    assert r1 > r2

def test_two_pair_and_tiebreakers():
    r = rank5(H("Jc","Jd","4s","4h","9d"))
    assert r == (2, 11, 4, 9)

    # compare second pair if top pair equal, then kicker
    r1 = rank5(H("Kc","Kd","Qh","Qs","9d"))  # KQ with 9
    r2 = rank5(H("Kc","Kd","Jh","Js","Ah"))  # KJ with A
    assert r1 > r2  # because Q > J even though kicker A > 9

def test_one_pair_and_high_card():
    onep = rank5(H("9c","9d","Ah","Kd","2s"))
    assert onep == (1, 9, 14, 13, 2)

    high = rank5(H("Ah","Kd","9s","5c","3d"))
    assert high == (0, 14, 13, 9, 5, 3)

def test_category_ordering_sanity():
    # SF > Quads > Full > Flush > Straight > Trips > TwoPair > OnePair > High
    sf   = rank5(H("9h","Th","Jh","Qh","Kh"))
    quad = rank5(H("Ah","Ad","Ac","As","2h"))
    full = rank5(H("Kh","Kd","Kc","2s","2d"))
    flsh = rank5(H("As","Ts","8s","4s","2s"))
    strt = rank5(H("9c","Td","Jh","Qs","Kc"))
    tri  = rank5(H("Qh","Qd","Qc","7s","2d"))
    twop = rank5(H("Jc","Jd","4s","4h","9d"))
    onep = rank5(H("9c","9d","Ah","Kd","2s"))
    high = rank5(H("Ah","Kd","9s","5c","3d"))
    assert sf > quad > full > flsh > strt > tri > twop > onep > high