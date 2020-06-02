import logging
logger = logging.getLogger(__name__)

def random_agent(n_actions, seed=None):
    import random
    rng = random.Random(seed)
    return Agent(n_actions, rng)

class Agent:

    def __init__(self, n_actions, rng):
        self.rng = rng
        self.n_actions = n_actions

    def action(self, state):
        ret = self.rng.randrange(self.n_actions() + 1) - 1
        logger.info(f'action: {ret}')
        return ret

    def reward(self, r):
        logger.info(f'reward: {r}')
