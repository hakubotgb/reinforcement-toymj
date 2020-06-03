import numpy
from sklearn.linear_model import SGDRegressor

import itertools

import logging
logger = logging.getLogger(__name__)

def random_agent(rule, gamma=0.966, eps=0.1, seed=None):
    import random
    rng = random.Random(seed)
    return Agent(rule, gamma, eps, rng)

class MultiClassSGDRegressor:

    def __init__(self, n_classes, features, rng):
        self._models = [
                SGDRegressor(random_state=rng.randrange(1<<32))
                for _ in range(n_classes)]
        self.features = features

    def predict1(self, x):
        return self.predict(
                numpy.asarray(self.features.transform(x)).reshape((1, -1)))

    def predict(self, X):
        '''
        X: n_samples * n_features
        return: n_samples * n_classes
        '''
        logger.debug(f'predict({X.shape})')
        return numpy.stack((
                model.predict(X)
                for model in self._models), axis=-1)

    def partial_fit1(self, x, y):
        return self.partial_fit(
                numpy.asarray(self.features.transform(x)).reshape((1, -1)),
                numpy.asarray(y).reshape((1, -1))
                )

    def partial_fit(self, X, Y):
        '''X: n_samples * n_features; y: n_samples * n_classes'''
        logger.debug(f'partial_fit({X.shape}, {Y.shape})')
        for (model, y) in zip(self._models, Y.T):
            model.partial_fit(X, y)

    def fit(self, X, Y):
        logger.debug(f'fit({X.shape}, {Y.shape})')
        for (model, y) in zip(self._models, Y.T):
            model.fit(X, y)

class FeatureExtractor:
    def __init__(self, rule):
        pass

    def transform(self, state):
        return list(itertools.chain.from_iterable([n < s for s in state] for n in range(3)))

class Agent:

    def __init__(self, rule, gamma, eps, rng):
        self.rng = rng
        self.dim_state = rule.dim_state()
        self.n_actions = rule.n_actions()
        self.model = MultiClassSGDRegressor(self.n_actions, FeatureExtractor(rule), self.rng)
        n_random_states = self.n_actions * 2
        self.model.fit(
                numpy.asarray(list(map(self.model.features.transform, rule.random_states(n_random_states, self.rng)))),
                numpy.asarray([[self.rng.random() for _ in range(self.n_actions)] for _ in range(n_random_states)]))
        self._sa = None
        self.gamma = gamma
        self.eps = eps

    def action(self, state):
        if self.rng.random() < self.eps:
            ret = self.rng.randrange(self.n_actions)
        else:
            ret = numpy.argmax(self.model.predict1(state)[0])
        self._sa = (state, ret)
        ret -= 1
        logger.info(f'action: {ret}')
        return ret

    def reward(self, rs):
        logger.info(f'reward: {rs[0]}')
        target = rs[0]
        if rs[1]:
            target += self.gamma * numpy.amax(
                self.model.predict1(rs[1]))
        target_full = self.model.predict1(self._sa[0])
        target_full[0, self._sa[1]] = target
        self.model.partial_fit1(self._sa[0], target_full)
        return rs[0]
