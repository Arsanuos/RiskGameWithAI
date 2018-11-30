from riskGame.classes.state.move import Move
from copy import deepcopy


class Agent:

    def __init__(self, place_bonus_heuristic, move_heuristic, attack_heuristic):
        self._place_bonus_heuristic = place_bonus_heuristic
        self._move_heuristic = move_heuristic
        self._attack_heuristic = attack_heuristic

    # move is None in all agents unless in case of human it will be not None
    def play(self, current_state, move=None):
        print('Start Playing')
        state = deepcopy(current_state)
        if move is None:
            move = Move()
            if self._place_bonus_heuristic is not None:
                move = self._place_bonus_heuristic.make_decision(state, move)
            if self._move_heuristic is not None:
                move = self._move_heuristic.make_decision(state, move)
            if self._attack_heuristic is not None:
                move = self._attack_heuristic.make_decision(state, move)
        move.apply_move()
        state.increase_turn()
        state.increase_player_turn()
        state.set_parent_state(current_state)
        return state


