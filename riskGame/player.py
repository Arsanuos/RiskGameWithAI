from abc import ABC, abstractmethod


class Player(ABC):

    def __int__(self, name, bonus, captured, state):
        self._name = name
        self._bonus = bonus
        self._captured = captured
        if bonus > 0:
            self.put_army(state)



    @abstractmethod
    def play(self, state):
        """
        implement this function to get new state
        :return: new state after decisions.
        """

    @abstractmethod
    def put_army(self, state):
        """
        Changes the state by putting the army onto the game map
        :param state: the current state of map
        :return: new state after putting the army.
        """

    @property
    def set_name(self, name):
        self._name = name

    @property
    def set_bonus(self, bonus):
        self._bonus = bonus

    @property
    def get_name(self):
        return self._name

    @property
    def get_bouns(self):
        return self._bonus

    def capture_region(self, region):
        self._captured.add(region)

    def lose_region(self, region):
        self._captured.remove(region)





