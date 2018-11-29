from riskGame.classes.heuristic.heuristic import Heuristic
from sys import maxsize


class RTAStar(Heuristic):

    def __init__(self):
        self.__hash_table = {}

    def dfs(self, curr_state, distance_from_root, limit):
        if limit == 0:
            # end of limit
            return curr_state.get_heuristic_cost() + distance_from_root

        child_states = curr_state.expand()
        min_cost = maxsize
        for child in child_states:
            if child.isGoal():
                return distance_from_root
            child_cost = self.dfs(child, distance_from_root + 1, limit - 1)
            min_cost = min(min_cost, child_cost)

        return min_cost

    def make_decision(self, state, move):
        # Plan phase
        limit = 3
        child_states = state.expand()
        min_cost = maxsize
        second_min_cost = -1
        next_state = None
        for child in child_states:
            child_cost = 0

            if child in self.__hash_table:
                child_cost = self.__hash_table[child]
            else:
                child_cost = self.dfs(child, 1, limit)

            if child_cost < min_cost:
                second_min_cost = min_cost
                min_cost = child_cost
                next_state = child

        # Execute phase
        self.__hash_table[state] = second_min_cost
        return next_state
