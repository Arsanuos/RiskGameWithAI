from riskGame.classes.agent.agent import Agent
from riskGame.classes.heuristic.bonus.place_bonus_passive import PlaceBonusPassive


class Passive(Agent):

    def __init__(self, place_bonus_heuristic=PlaceBonusPassive):
        super(Passive, self).__init__(place_bonus_heuristic, None, None)

    def play(self, current_state, move=None):
        super(Passive, self).play(current_state, move)

