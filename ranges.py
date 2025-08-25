from typing import Iterable, List, Tuple, Optional
from cards import RANKS, SUITS, RANK_TO_VAL, VAL_TO_RANK, Card

def _all_pair_combos(v: int) -> List[Tuple[Card, Card]]:
    # v is rank, should be 6 suit combos for pocket pair
    out: List[Tuple[Card, Card]] = []
    suits = list(SUITS)
    for i in range(len(suits)):
        for j in range(i + 1, len(suits)):
            out.append(((v, suits[i]), (v, suits[j])))

    return out # 6 combos

def _all_nonpair_combos(vhi: int, vlo: int, suited_flag: Optional[bool]) -> List[Tuple[Card, Card]]:
    #suited_flag is True for suited only, False for offsuit only, None for both
    out: List[Tuple[Card, Card]] = []
    if suited_flag is None:
        if suited_flag is None:
            out.extend(_all_nonpair_combos(vhi, vlo, True))
            out.extend(_all_nonpair_combos(vhi, vlo, False))
            return out
        if suited_flag:
            for s in SUITS:
                out.append(((vhi, s), (vlo, s)))
            return out
    #offsuit
    for s1 in SUITS:
        for s2 in SUITS:
            if s1 == s2:
                continue
            out.append(((vhi, s1), (vlo, s2)))
    return out

def _expand_token(token: str) -> List[Tuple[str, int, int, Optional[bool]]]:
    # expand single token into list of (kind, vhi, vlo, suited_flag) where kind is either pair or nonpair
    t = token.strip()
    if not t or len(t) < 2:
        return []
    plus = t.endswith("+")
    if plus:
        t = t[:-1]

    suited_flag: Optional[bool] = None
    if t.endswith("s"):
        suited_flag = True
        t = t[:-1]
    elif t.endswith("o"):
        suited_flag = False
        t = t[:-1]
    
    if len(t) != 2:
        return []
    
    r1, r2 = t[0].upper(), t[1].upper()
    if r1 not in RANK_TO_VAL or r2 not in RANK_TO_VAL:
        return []
    
    v1, v2 = RANK_TO_VAL[r1], RANK_TO_VAL[r2]

    if v2 > v1:
        v1, v2 = v2, v1

    if v1 == v2:
        if plus:
            return [("pair", v, 0, None) for v in range(v1, 15)]
        else:
            return [("pair", v1, 0, None)]
    
    if plus:
        lows = list(range(v2, v1))
    else:
        lows = [v2]
    return [("nonpair", v1, lo, suited_flag) for lo in lows]

