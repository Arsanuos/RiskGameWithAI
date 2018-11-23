from riskGame.classes.state.move import Move


class Agent:

    def __init__(self, place_bonus_heuristic, move_heuristic, attack_heuristic):
        self._place_bonus_heuristic = place_bonus_heuristic
        self._move_heuristic = move_heuristic
        self._attack_heuristic = attack_heuristic

    # move is None in all agents unless in case of human it will be not None
    def play(self, state, move=None):
        if move is None:
            move = Move()
            if self._place_bonus_heuristic is not None:
                move = self._place_bonus_heuristic(state, move)
            if self._move_heuristic is not None:
                move = self._move_heuristic(state, move)
            if self._attach_heuristic is not None:
                move = self._attach_heuristic(state, move)
        move.apply()
        return state


