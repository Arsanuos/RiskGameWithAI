from abc import ABC, abstractmethod

class Heuristic(ABC):


    @abstractmethod
    def make_decision(self, state):
        """
        implement this function to get new state by this heuristic.
        :return: new state after decisions.
        """