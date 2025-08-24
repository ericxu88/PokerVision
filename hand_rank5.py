# hand category 
# 0 to 8, high card to straight flush (royal flush is the best straight flush)

from typing import List, Tuple

Card = Tuple[int, str]

#straight detection
def _straight_high(sorted_unique_vals_asc: List[int]) -> int | None:
    if len(sorted_unique_vals_asc) < 5:
        return None
    
    seq = sorted_unique_vals_asc
    if 14 in seq and 1 not in seq:
        seq = [1] + seq
    
    run = 1
    best_high = None
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1] + 1:
            run += 1
            if run >= 5:
                best_high = seq[i]
        elif seq[i] != seq[i - 1]:
            run = 1
    return best_high

# evaluate 5-card hand
def rank5(cards5: List[Card]) -> tuple:
    if len(cards5) != 5:
        raise ValueError("Expected exactly 5 cards")
    
    vals = [v for v, _ in cards5]
    suits = [s for _, s in cards5]
    vals_sorted_desc = sorted(vals, reverse=True)
    vals_unique_desc = sorted(set(vals), reverse=True)
    vals_unique_asc = list(reversed(vals_unique_desc))

    from collections import Counter
    counts = Counter(vals)
    by_count = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    is_flush = len(set(suits)) == 1

    #straight?
    s_high = _straight_high(vals_unique_asc)

    #straight flush
    if is_flush and s_high is not None: 
        return (8, s_high)
    
    #4 of a kind
    if by_count[0][1] == 4:
        quad = by_count[0][0]
        kicker = max([v for v in vals_unique_desc if v != quad])
        return (7, quad, kicker)
    
    # full house
    trips = [v for v, c in by_count if c == 3]
    pairs = [v for v, c in by_count if c == 2]
    if trips and pairs:
        return (6, trips[0], pairs[0])
    
    # flush
    if is_flush:
        return (5, *vals_sorted_desc)
    
    # straight
    if s_high is not None:
        return (4, s_high)
    
    # 3 of a kind
    if by_count[0][1] == 3:
        t = by_count[0][0]
        kickers = [v for v in vals_unique_desc if v != t][:2]
        return (3, t, *kickers)
    
    # 2 pair
    pairs_only =  [v for v, c in by_count if c == 2]
    if len(pairs_only) == 2:
        p1, p2 = sorted(pairs_only, reverse=True)
        kicker = [v for v in vals_unique_desc if v not in (p1, p2)][0]
        return (2, p1, p2, kicker)
    
    # one pair
    if len(pairs_only) == 1:
        p = pairs_only[0]
        kickers = [v for v in vals_unique_desc if v != p][:3]
        return (1, p, *kickers)
    
    # high card 
    return (0, *vals_sorted_desc)
    
