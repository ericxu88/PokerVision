import pytest
from cards import parse_card, VAL_TO_RANK, card_str
from ranges import parse_range_tokens, range_to_combos

def C(*ss):
    return [parse_card(s) for s in ss]

def test_token_validation_and_normalization():
    ok = parse_range_tokens(["22", "TT+", "AQ", "AQs", "AQo", "A9s+", "KTs+", "AQ+"])
    assert ok == ["22","TT+","AQ","AQs","AQo","A9s+","KTs+","AQ+"]

    # bad tokens
    with pytest.raises(ValueError):
        parse_range_tokens(["10h"])   # we require "T" not "10"
    with pytest.raises(ValueError):
        parse_range_tokens(["AQQ"])   # malformed
    with pytest.raises(ValueError):
        parse_range_tokens(["A2x"])   # bad suit flag

def test_combo_counts_no_blockers():
    # pairs
    assert len(range_to_combos(["AA"])) == 6
    # suited / offsuit / both
    assert len(range_to_combos(["AQs"])) == 4
    assert len(range_to_combos(["AQo"])) == 12
    assert len(range_to_combos(["AQ"])) == 16
    # plus ranges
    assert len(range_to_combos(["22+"])) == 13 * 6   # 13 pocket pairs * 6 = 78
    assert len(range_to_combos(["A9s+"])) == 5 * 4   # A9s,ATs,AJs,AQs,AKs → 5 * 4 = 20
    assert len(range_to_combos(["KTs+"])) == 3 * 4   # KTs,KJs,KQs → 3 * 4 = 12
    assert len(range_to_combos(["AQ+"])) == (4+12) + (4+12)  # AQ + AK (both s/o) = 32

def test_dedup_overlapping_tokens():
    # "AQ" already includes AQs, so "AQ" + "AQs" should still yield 16 not 20
    assert len(range_to_combos(["AQ","AQs"])) == 16

def test_blockers_remove_specific_combos():
    # AQs has 4 combos: AsQs, AhQh, AdQd, AcQc
    # Excluding As and Qh leaves AdQd and AcQc (2 combos)
    excl = C("As","Qh")
    combos = range_to_combos(["AQs"], exclude=excl)
    assert len(combos) == 2
    # ensure the remaining combos are the suited diamonds and clubs
    as_strs = set(
    card_str((r1, s1)) + card_str((r2, s2))
    for ((r1, s1), (r2, s2)) in combos
    )
    assert "AdQd" in as_strs and "AcQc" in as_strs