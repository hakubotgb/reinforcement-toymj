from toymj.agent import random_agent
from toymj.environment import Environment
from toymj.rule import Rule, Suit

import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

def main(n_episodes):
    rule = Rule(suits=[Suit(3, 3)])
    environment = Environment(rule, seed=20200602)
    agent = random_agent(rule, seed=20201031)
    for i in range(n_episodes):
        total_reward = 0
        environment.initialize()
        while environment.in_play:
            total_reward += agent.reward(environment.transition(agent.action(environment.state())))
        print(total_reward)

if __name__ == '__main__':
    main(100)
