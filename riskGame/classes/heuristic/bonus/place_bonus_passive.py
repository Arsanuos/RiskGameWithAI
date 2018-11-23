from riskGame.classes.heuristic.heuristic import Heuristic
from sys import maxsize


class PlaceBonusPassive(Heuristic):

    def make_decision(self, state, move):
        fewest_node = None
        min_armies = maxsize
        for node in self.state.get_current_player().get_hold_nodes():
            if node.get_army() < min_armies:
                fewest_node = node
                min_armies = node.get_army()
            # break ties
            elif node.get_army() == min_armies and node.get_node_name() < fewest_node.get_node_name():
                fewest_node = node
        if fewest_node:
            move.set_bonus_hold_node(fewest_node)
        return move
