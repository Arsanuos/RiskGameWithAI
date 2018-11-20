
class Node:

    def __int__(self, player, army):
        self.__player = player
        self.__army = army

    @property
    def set_player(self, player):
        self.__player = player

    @property
    def set_army(self, army):
        self.__army = army

    @property
    def get_player(self):
        return self.__player

    @property
    def get_army(self):
        return self.__army


    


