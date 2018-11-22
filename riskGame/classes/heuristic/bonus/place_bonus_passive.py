from riskGame.classes.heuristic import Heuristic
from sys import maxsize


class PlaceBonusPassive(Heuristic):

    def make_decision(self, state):
        fewest_army = None
        max_arms = maxsize
        for node in self.state.get_current_player().get_hold_nodes():
            if node.get_army() < max_arms:
                fewest_army = node
                max_arms = node.get_army()

        if fewest_army:
            fewest_army.move_bonus_to_mine()

        return state
