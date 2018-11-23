from riskGame.classes.heuristic.heuristic import Heuristic


class PlaceBonusAI(Heuristic):

    def make_decision(self, states, move):

        sorted_states = []

        for state in states:
            bonus_node = state.get_bonus_node
            val = bonus_node.max_loss_attack()
            sorted_states.append((bonus_node, val))

        sorted(sorted_states, key=lambda x: x[1])
        move.set_bonus_hold_node(sorted_states[0][0])
        return move
