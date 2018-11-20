from riskGame.player import Player


class Agent(Player):

    def __init__(self, name , bonus, captured, state, move_heuristic, attack_heuristic):
        super(Agent, self).__int__(name, bonus, captured, state)
        self._move_heuristic = move_heuristic
        self._attack_heuristic = attack_heuristic

    def put_army(self, state):
        pass

    def play(self, state):
        pass
