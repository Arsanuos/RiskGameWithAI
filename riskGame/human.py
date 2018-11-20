from riskGame.player import Player


class Human(Player):

    def __init__(self, name , bonus, captured, state):
        super(Human, self).__int__(name, bonus, captured, state)

    def put_army(self, state):
        pass

    def play(self, state):
        pass
