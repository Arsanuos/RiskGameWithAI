from riskGame.classes.agent.passive_agent import Passive
from heapq import *
from abc import ABC, abstractmethod


class OneTimeAgent(ABC):

    def __init__(self):
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

        end = None
        states_heap = []
        self.__vis.add(self.__initial_state)
        child_states = self.__initial_state.expand()
        for child in child_states:
            heappush(states_heap, (self.calculate_fn(child, self.__initial_state), child))

        while len(states_heap):
            # break tie by FIFO criteria
            current_explored_state = heappop(states_heap)[1]
            if current_explored_state in self.__vis:
                continue

            if current_explored_state.get_winner():
                print('Finished Agent, Found Winner')
                end = current_explored_state
                break

            # DEBUG
            print('poping a state and expand more')
            current_explored_state.print_state()

            self.__vis.add(current_explored_state)
            astar_turn_state = passive_agent.play(current_explored_state)
            astar_turn_state.set_parent_state(current_explored_state)

            child_states = astar_turn_state.expand()
            for child in child_states:
                heappush(states_heap, (self.calculate_fn(child, self.__initial_state), child))

        return end.get_steps_to_root()

    @abstractmethod
    def calculate_fn(self, state, inital_state):
        pass

