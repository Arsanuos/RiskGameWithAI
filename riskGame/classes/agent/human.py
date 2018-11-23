from riskGame.classes.agent.agent import Agent
from riskGame.classes.state.move import Move


class Human(Agent):

    def __init__(self):
        super(Human, self).__init__(None, None, None)

    def play_human(self, state, bonus_hold_node_number=None, move_from_node_number=None, move_to_node_number=None, \
                   moved_armies=None, attacker_node_number=None, attacked_node_number=None, attacked_node_armies=None):

        move = Move()
        if bonus_hold_node_number:
            node = state.get_current_player().get_node_by_name(bonus_hold_node_number)
            move.set_bonus_hold_node(node)

        if move_from_node_number and move_to_node_number and moved_armies > 0:
            from_node = state.get_current_player().get_node_by_name(move_from_node_number)
            to_node = state.get_current_player().get_node_by_name(move_to_node_number)
            move.set_move_from_node(from_node)
            move.set_move_to_node(to_node)
            move.set_moved_armies(moved_armies)

        if attacker_node_number and attacked_node_number and attacked_node_armies > 0:
            attacker_node = state.get_current_player().get_node_by_name(attacker_node_number)
            if attacker_node:
                attacked_node = attacker_node.get_possible_attacked_node_by_name(attacked_node_number)
            else:
                attacked_node = None
            move.set_attacker_node(attacker_node)
            move.set_attacked_node(attacked_node)
            move.set_attacked_node_armies(attacked_node_armies)

        return self.play(state, move)
