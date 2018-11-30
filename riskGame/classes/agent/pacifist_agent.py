from riskGame.classes.agent.agent import Agent
from riskGame.classes.heuristic.bonus.place_bonus_passive import PlaceBonusPassive
from riskGame.classes.heuristic.attack.attack_pacifist import AttackPacifist


class Pacifist(Agent):

    def __init__(self, place_bonus_heuristic=PlaceBonusPassive(), attack_heuristic=AttackPacifist()):
        super(Pacifist, self).__init__(place_bonus_heuristic, None, attack_heuristic)

