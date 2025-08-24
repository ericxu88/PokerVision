#tests should check
# - parse
# - format
# - deck size and uniqueness
# - excludes
# - deal() draws without replacement and is reproducible with rng seed
# - input validation errors

import pytest
from cards import (parse_card, card_str, make_deck, deal, shuffle_deck, all_card_strings, RANKS, SUITS)

def test_parse_roundtrip_all_52():
    for s in all_card_strings():
        c = parse_card(s)
        s2 = card_str(c)
        assert s2 == s

def test_bad_parse_inputs():
    bad = ["", "A", "10h", "1h", "Ahh", "AX", "ZZ", " Qs", "As "]
    for b in bad:
        with pytest.raises(ValueError):
            parse_card(b)

def test_make_deck_basics():
    d = make_deck()
    assert len(d) == 52
    # uniqueness
    assert len(set(d)) == 52
    # contains expected sample cards
    assert parse_card("2s") in d
    assert parse_card("Ad") in d

def test_make_deck_excludes():
    excl = [parse_card("Ah"), parse_card("Td"), parse_card("7s")]
    d = make_deck(exclude=excl)
    assert len(d) == 52 - len(excl)
    for e in excl:
        assert e not in d

def test_deal_without_replacement_and_sizes():
    d = make_deck()
    drawn, rem = deal(d, 5)
    assert len(drawn) == 5
    assert len(rem) == 47
    # no overlap
    assert set(drawn).isdisjoint(set(rem))
    # union equals original (since it was a pure split)
    assert set(drawn) | set(rem) == set(d)

def test_deal_is_reproducible_with_seeded_rng():
    d = make_deck()
    rng1 = __import__("random").Random(42)
    rng2 = __import__("random").Random(42)
    drawn1, rem1 = deal(d, 7, rng=rng1)
    drawn2, rem2 = deal(d, 7, rng=rng2)
    assert drawn1 == drawn2
    assert rem1 == rem2

def test_shuffle_deck_reproducible():
    rng1 = __import__("random").Random(123)
    rng2 = __import__("random").Random(123)
    d1 = shuffle_deck(rng=rng1)
    d2 = shuffle_deck(rng=rng2)
    assert d1 == d2
    # ensure it's actually shuffled vs. the canonical make_deck order
    assert d1 != make_deck()

def test_deal_raises_on_overdraw():
    d = make_deck()
    with pytest.raises(ValueError):
        deal(d, 53)