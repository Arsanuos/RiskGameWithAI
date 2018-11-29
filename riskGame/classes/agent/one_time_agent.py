from riskGame.classes.agent.passive_agent import Passive
from heapq import *


class OneTimeAgent:

    def __init__(self, evaluate_state):
        self.__evaluate_state = evaluate_state
        self.__initial_state = None
        self.__vis = set()

    """
        search for the best next state from initial_state to reach the goal.
        initial_state : initial of the game
    """
    def search(self, initial_state):
        self.__initial_state = initial_state
        self.__initial_state.set_parent_state(None)
        passive_agent = Passive()

        states_heap = []
        self.__vis.add(initial_state)
        child_states = initial_state.expand()
        for child in child_states:
            heappush(states_heap, (self.__evaluate_state(child), child))

        while len(states_heap):
            # break tie by FIFO criteria
            current_explored_state = heappop(states_heap)[1]
            if current_explored_state in self.__vis:
                continue

            if current_explored_state.get_winner():
                end = current_explored_state
                break

            self.__vis.add(current_explored_state)
            astar_turn_state = passive_agent.play(current_explored_state)
            astar_turn_state.set_parent_state(current_explored_state)

            child_states = astar_turn_state.expand()
            for child in child_states:
                heappush(states_heap, (self.__evaluate_state(child), child))

        return end.get_steps_to_root()
