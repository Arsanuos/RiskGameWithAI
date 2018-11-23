from riskGame.classes.heuristic.heuristic import Heuristic


class AttackAggressive(Heuristic):

    # attempts to attack so as to cause the most damage, so we will attack the possible nodes with the largest armies
    def make_decision(self, state, move):
        # attach = (attacker node, attacked node)
        attack = (None, None)
        max_armies = 0
        for node in self.state.get_current_player().get_hold_nodes():
            possible_attacked_nodes = node.get_possible_attacked_nodes()
            for attacked_node in possible_attacked_nodes:
                if attacked_node.get_army() > max_armies:
                    attack = (node, attacked_node)
                    max_armies = attacked_node.get_army()
                # break ties
                elif attacked_node.get_army() == max_armies and attacked_node.get_node_name() < attack[1].get_node_name():
                    attack = (node, attacked_node)
        if attack[0]:
            move.set_attacker_node(attack[0])
            move.set_attacked_node(attack[1])
            move.set_attacked_node_armies(1)
        return move
