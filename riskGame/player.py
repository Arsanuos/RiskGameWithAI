class Player:

    def __int__(self, name, bouns):
        self.__name = name
        self.__bouns = bouns

    @property
    def set_name(self, name):
        self.__name = name

    @property
    def set_bouns(self, bouns):
        self.__bouns = bouns

    @property
    def get_name(self):
        return self.__name

    @property
    def get_bouns(self):
        return self.__bouns





