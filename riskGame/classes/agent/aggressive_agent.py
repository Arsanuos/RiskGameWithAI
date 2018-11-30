from riskGame.classes.agent.agent import Agent
from riskGame.classes.heuristic.bonus.place_bonus_aggressive import PlaceBonusAggressive
from riskGame.classes.heuristic.attack.attack_aggressive import AttackAggressive


class Aggressive(Agent):

    def __init__(self, place_bonus_heuristic=PlaceBonusAggressive(), attack_heuristic=AttackAggressive()):
        super(Aggressive, self).__init__(place_bonus_heuristic, None, attack_heuristic)

