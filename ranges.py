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

def parse_range_tokens(range_list: List[str]) -> List[str]:
    # validate and normalize list of tokens
    out: List[str] = []
    seen = set()
    for token in range_list:
        token = token.strip()
        if not token or token in seen:
            continue
        if _expand_token(token):
            out.append(token)
            seen.add(token)
        else:
            raise ValueError(f"Invalid token '{token}' in range")
    return out

def range_to_combos(range_list: List[str], exclude: Iterable[Card] = ()) -> List[Tuple[Card, Card]]:
    # convert range tokens to list of card pairs
    # exclude is for excluding cards on the table
    exclude_set = set(exclude)
    out: List[Tuple[Card, Card]] = []
    for token in parse_range_tokens(range_list):
        specs = _expand_token(token)
        for kind, vhi, vlo, suited_flag in specs:
            if kind == "pair":
                combos = _all_pair_combos(vhi)
            elif kind == "nonpair":
                combos = _all_nonpair_combos(vhi, vlo, suited_flag)
            else:
                raise ValueError(f"Unknown kind '{kind}' in token '{token}'")
            
            for c1, c2 in combos:
                if c1 in exclude_set or c2 in exclude_set:
                    continue
                #normalize order for dedup
                if (c2[0] > c1[0]) or (c2[0] == c1[0] and c2[1] > c1[1]):
                    combo = (c2, c1)
                else:
                    combo = (c1, c2)
                combos.append(combo)

    seen = set()
    unique: List[Tuple[Card, Card]] = []
    for combo in combos:
        if combo not in seen: 
            seen.add(combo)
            unique.append(combo)
    return unique