import itertools

class Suit:
    def __init__(self, ranks, dups):
        self.ranks = ranks
        self.dups = dups

def get_suit(i_suit):
    i, suit = i_suit
    return [(i, j) for j in range(suit.ranks) for k in range(suit.dups)]

def get_suit_uniq(i_suit):
    i, suit = i_suit
    return [(i, j) for j in range(suit.ranks)]

class Rule:

    def __init__(self, suits=[Suit(7, 4)], sets=1):
        self.suits = suits
        self._distinct_tiles = list(itertools.chain.from_iterable(map(get_suit_uniq, enumerate(suits))))
        self._distinct_tiles_index = dict((v, k) for (k, v) in enumerate(self._distinct_tiles))
        self.sets = sets

    def get_pile(self):
        return list(itertools.chain.from_iterable(
                map(get_suit, enumerate(self.suits))))

    def state_to_hand(self, hand):
        return list(itertools.chain.from_iterable(
                itertools.repeat(self._distinct_tiles[i], n)
                for (i, n) in enumerate(hand)))