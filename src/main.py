from toymj.agent import random_agent
from toymj.environment import Environment
from toymj.rule import Rule

import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

def main(n_episodes):
    environment = Environment(Rule(), seed=20200602)
    agent = random_agent(environment.n_actions, seed=20201031)
    for i in range(n_episodes):
        environment.initialize()
        while environment.in_play:
            agent.reward(environment.transition(agent.action(environment.state())))

if __name__ == '__main__':
    main(100)
