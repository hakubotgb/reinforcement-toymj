import random
import itertools
import logging
logger = logging.getLogger(__name__)

from toymj.rule import Rule

class Environment:

    def __init__(self, rule: Rule, *, seed=None):
        self.rng = random.Random(seed)
        self.rule = rule
        self.pile = rule.get_pile()

    def initialize(self):
        self.rng.shuffle(self.pile)
        self.p = self.rule.sets * 3 + 2
        self._state = [0 for _ in self.rule._distinct_tiles]
        for i in range(self.p):
            self._state[self.rule._distinct_tiles_index[self.pile[i]]] += 1
        self.in_play = True

    def state(self):
        logger.info(f'state: {self.rule.state_to_hand(self._state)}')
        return self._state

    def transition(self, action):
        if action == -1: # hu
            self.in_play = False
            return 1
        if self._state[action]:
            self._state[action] -= 1
            if self.p == len(self.pile):
                return 0
            self._state[self.rule._distinct_tiles_index[self.pile[self.p]]] += 1
            self.p += 1
            return 0
        self.in_play = False
        return -1

    def n_actions(self):
        return len(self.rule._distinct_tiles)
