from riskGame.agent import Agent
from sys import maxsize


class Passive(Agent):

    def __init__(self, name, bonus, state):
        super(Passive, self).__init__(name, bonus, state, None, None)

    def put_army(self, state):

        fewest_army = None
        max_arms = maxsize
        for region in self._captured:
            if region.get_army() < max_arms:
                fewest_army = region
                max_arms = region.get_army()

        if fewest_army:
            fewest_army.set_army(max_arms + self._bonus)

        return state

    def play(self, state):
        return state
