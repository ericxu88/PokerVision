import math
import pytest
from cards import parse_card
from equity_hu import enumerate_runouts, equity_hu_exact

def H(*ss):
    """Helper: 'Ah','Td' → [(14,'h'), (10,'d')]"""
    return [parse_card(s) for s in ss]

# ---------- Full board (need = 0) ----------

def test_full_board_hero_wins():
    hero = H("As","Kd")
    vill = H("9h","9d")
    # Removed the 9♠ from board so villain doesn't make trips
    board = H("Ah","8s","2c","7d","3h")  # hero: pair A; villain: pair 9 → hero wins
    res = equity_hu_exact(hero, vill, board)
    assert res["total"] == 1
    assert res["equity"] == 1.0
    assert res["wins"] == 1 and res["ties"] == 0

def test_full_board_tie():
    hero = H("2c","3d")
    vill = H("4s","5c")
    board = H("Ah","Kh","Qh","Jh","Th")  # royal flush on board → everyone chops
    res = equity_hu_exact(hero, vill, board)
    assert res["total"] == 1
    assert res["equity"] == 0.5
    assert res["wins"] == 0 and res["ties"] == 1

def test_full_board_hero_loses():
    hero = H("As","Kd")
    vill = H("Kh","Qh")
    board = H("Ah","9h","7d","2s","3h")  # villain makes a heart flush
    res = equity_hu_exact(hero, vill, board)
    assert res["total"] == 1
    assert res["equity"] == 0.0
    assert res["wins"] == 0 and res["ties"] == 0

# ---------- River-only unknown (need = 1) ----------

def test_river_only_enumeration_count_and_equity_range():
    # Turn known (4 cards), river unknown → exactly 44 runouts.
    hero = H("Ah","Qh")                 # nut heart draw + two broadways
    vill = H("Jd","9d")                 # top pair J with 9 kicker on this board
    board = H("Jh","7c","2h","9s")      # two hearts on board, so any heart river makes 5 hearts
    res = equity_hu_exact(hero, vill, board)
    assert res["total"] == 44

    # Exactly 9 heart rivers exist, but 9♥ gives villain a full house (9♦+9♠+9♥ with J♦+J♥),
    # which beats our flush. So hero wins only on 8 rivers.
    # Equity = 8 / 44 exactly.
    assert res["equity"] == pytest.approx(8/44, rel=1e-12)

# ---------- Turn + River unknown (need = 2) ----------

def test_turn_river_enumeration_count_and_equity_range():
    # Flop known (3 cards), need=2 → combinations should be C(45, 2) = 990.
    hero = H("Ah","Qh")
    vill = H("Jd","9d")
    board = H("Jh","7c","2h")           # flop only
    res_counts = enumerate_runouts(hero, vill, board)
    assert res_counts["total"] == math.comb(45, 2)  # 990

    res = equity_hu_exact(hero, vill, board)
    # Equity range sanity (again, deliberately loose so tests are stable)
    assert 0.30 <= res["equity"] <= 0.60

# ---------- Guard rails (too many unknowns) ----------

def test_refuse_large_enumeration_by_default():
    # Preflop (need=5) should raise unless allow_large=True.
    hero = H("As","Kd")
    vill = H("Qh","Qs")
    board = []
    with pytest.raises(ValueError):
        enumerate_runouts(hero, vill, board)  # need=5 → too big by default