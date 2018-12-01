import math


class SigmoidEval:

    """
    this class is implemented based on this paper
    http://www.ke.tu-darmstadt.de/lehre/arbeiten/diplom/2005/Wolf_Michael.pdf?fbclid=IwAR1-fM62HsO0DCnwST0JlZqoXwNHMOKHwlRNqdojbuyZVPNzGBBW3gYN9g4
    """

    def __init__(self):
        self.__state = None

    def score(self, state):
        """
        weight are manually tuned.
        score = w1 * armies feature + w2 * best_enemy_feature + w3 * distance_to_frontier_feature + w4 * enemy_army_bonus_feature +
                w5 * hinterland_feature + w6 * occupied_nodes_feature + w7 * bonus_feature
        we can prove that sigmoid(score) * number of enemy nodes is admissible heuristic.
        :return: score
        """
        self.__state = state
        self.__armies = {}
        for player in self.__state.get_players():
            self.__armies[player.get_name()] = sum([node.get_army() for node in player.get_hold_nodes()])

        w = [8, 7, 9, 3, 1, 10, 7]
        score = w[0] * self.armies_feature() + w[1] * self.best_enemy_feature() + w[2] * self.distance_to_frontier_feature() + \
                w[3] * self.enemy_army_bonus_feature() + w[4] * self.hinterland_feature() + w[5] * self.occupied_nodes_feature() \
                + w[6] * self.bonus_feature()

        sigmoid = 1/(1+math.exp(-1 * score))
        return sigmoid * (self.__state.get_number_nodes() - len(self.__state.get_current_player().get_hold_nodes()))

    def get_total_armies(self):
        return sum(self.__armies.values())

    def get_armies_of(self, player):
        return self.__armies[player.get_name()]

    def armies_feature(self):
        """
        The Armies Feature returns the number of armies of the actual player (AP) in relation
        to the total number of armies on the gameboard.
        :return:
        """
        total_armies = self.get_total_armies()
        cur_player_army = self.__armies[self.__state.get_current_player().get_name()]
        return cur_player_army/total_armies

    def best_enemy_feature(self):
        """
        get the best army of the other players.
        :return:
        """
        v = -100
        for player in self.__state.get_players():
            if player.get_name() != self.__state.get_current_player().get_name():
               for node in player.get_hold_nodes():
                    v = max(v, node.get_army())
        return -1 * v

    def get_min_distance_from_border(self, border_nodes, all_nodes, nodes_len):
        q = []
        for node in border_nodes:
            q.append(node)
        vis = set()
        l = [0] * nodes_len
        d = 0
        while len(q):
            s = len(q)
            node = q.pop(0)
            d += 1
            while s:
                s -= 1
                if int(node.get_node_name()) not in vis:
                    vis.add(int(node.get_node_name()))
                    l[int(node.get_node_name())] = d + 1
                    for child in node.get_neighbours():
                        if child in all_nodes:
                            q.append(child)
        return l

    def distance_to_frontier_feature(self):
        """
        The Distance to Frontier Feature returns a measurement of the army distribution
        throughout the actual player’s territories. Armies positioned far away from territories
        occupied by enemy players result in a lower feature value than armies positioned on
        border territories.
        :return:
        """
        number_nodes = max([int(n.get_node_name()) for p in self.__state.get_players() for n in p.get_hold_nodes()]) + 1

        distances = self.get_min_distance_from_border(self.__state.get_current_player().get_border_nodes(), \
                                                      self.__state.get_current_player().get_hold_nodes(),\
                                                      number_nodes)
        current_armies = self.get_armies_of(self.__state.get_current_player())
        t = 0
        for node in self.__state.get_current_player().get_hold_nodes():
            t += node.get_army() * distances[int(node.get_node_name())]
        return current_armies / t

    def enemy_army_bonus_feature(self):
        """
        The Enemy Estimated Reinforcement Feature returns the negative estimation of the
        total number of armies the enemy players will be able to reinforce in the course of the
        next game round
        :return:
        """
        b = 0
        for i, player in enumerate(self.__state.get_players()):
            if i != self.__state.get_player_turn_number():
                b += player.get_bonus()
        return -1 * b

    def hinterland_feature(self):
        """
        The Hinterland Feature returns the percentage of the territories of the actual player
        (AP) which are hinterland territories
        :return:
        """
        return len(self.__state.get_current_player().get_hold_nodes()) - len(self.__state.get_current_player().get_border_nodes()) /self.__state.get_number_nodes()

    def occupied_nodes_feature(self):
        """
        The Occupied Territories Feature returns the number of territories which are occupied
        by the actual player in relation to the total number of territories on the map
        :return:
        """
        return len(self.__state.get_current_player().get_hold_nodes())/self.__state.get_number_nodes()

    def bonus_feature(self):
        """
        The Own Estimated Reinforcement Feature returns the expectation of the total number
        of armies the actual player.
        :return:
        """
        return self.__state.get_current_player().get_bonus()



