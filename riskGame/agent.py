from abc import ABC, abstractmethod

class Agent(ABC):

    def __init__(self, state):
        self.__state = state


    @abstractmethod
    def play(self):
        """
        implement this function to get new state
        :return: new state after decisions.
        """