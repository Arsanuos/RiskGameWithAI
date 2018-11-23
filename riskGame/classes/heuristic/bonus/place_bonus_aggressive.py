from riskGame.classes.heuristic.heuristic import Heuristic


class PlaceBonusAggressive(Heuristic):

    def make_decision(self, state, move):
        largest_node = None
        max_armies = 0
        for node in self.state.get_current_player().get_hold_nodes():
            if node.get_army() > max_armies:
                largest_node = node
                max_armies = node.get_army()
            # break ties
            elif node.get_army() == max_armies and node.get_node_name() < largest_node.get_node_name():
                largest_node = node
        if largest_node:
            move.set_bonus_hold_node(largest_node)
        return move
