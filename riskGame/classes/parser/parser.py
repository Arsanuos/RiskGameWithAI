from riskGame.classes.state.node import Node
from riskGame.classes.state.player import Player as Ply
from riskGame.classes.state.partition import Partition
from riskGame.classes.state.state import State
from riskGame.classes.state.state import Move

from riskGame.classes.agent.human import Human
from riskGame.classes.agent.passive_agent import Passive
from riskGame.classes.agent.aggressive_agent import Aggressive
from riskGame.classes.agent.pacifist_agent import Pacifist
from riskGame.classes.agent.aStar_agent import AStar
from riskGame.classes.agent.greedy_agent import Greedy
from riskGame.classes.agent.real_time_aStar import RTAStar


class Parser:

    def __init__(self):
        self.__initial_state = None
        self.__agent1 = None
        self.__agent2 = None
        self.__error_messages = []

    def parse_json_to_state(self, dic):
        print(dic)
        temp = []
        player1 = Ply('Player 1', temp)
        player2 = Ply('Player 2', temp)
        all_nodes = {}
        all_partitions = []

        # Parsing Nodes
        nodes = dic['nodes']
        player1_nodes = []
        player2_nodes = []
        for node in nodes:
            new_node = Node(node_name=int(node['id']), hold_player=None, army=int(node['title']), \
                            neighbours=None, partition=None)
            if node['player'] == 'Player 1':
                new_node.set_hold_player(player1)
                player1_nodes.append(new_node)
            else:
                new_node.set_hold_player(player2)
                player2_nodes.append(new_node)
            all_nodes[new_node.get_node_name()] = new_node

        player1.set_hold_nodes(player1_nodes)
        player2.set_hold_nodes(player2_nodes)

        # Parsing Partitions
        partitions = dic['partitions']
        partition_id = 0
        for partition in partitions:
            new_partition = Partition(partition_id, None, int(partition[0]))
            partition_nodes = []
            for idx in range(1, len(partition)):
                node_id = partition[idx]
                partition_nodes.append(all_nodes[int(node_id)])
                all_nodes[int(node_id)].set_partition(new_partition)
            new_partition.set_nodes(partition_nodes)
            partitions[partition_id] = new_partition
            partition_id += 1
            all_partitions.append(new_partition)

        # Parsing Edges
        edges = dic['edges']
        neighbours = {}
        for node in all_nodes.values():
            neighbours[node.get_node_name()] = []
        for edge in edges:
            node1_id = int(edge['source']['id'])
            node2_id = int(edge['target']['id'])
            neighbours[node1_id].append(all_nodes[node2_id])
            neighbours[node2_id].append(all_nodes[node1_id])
        for node in all_nodes.values():
            node.set_neighbours(neighbours[node.get_node_name()])

        state = State(len(all_nodes), all_partitions, [player1, player2], 0)
        algorithms = {'Human':Human(), 'Passive':Passive(), 'Aggressive':Aggressive(), 'Nearly Passive':Pacifist(), \
                      'A *':AStar(), 'Greedy':Greedy(), 'RTA *':RTAStar()}

        self.__initial_state = state
        self.__agent1 = algorithms[dic['p1']]
        self.__agent2 = algorithms[dic['p2']]

    def get_initial_state(self):
        return self.__initial_state

    def get_agent(self, agent_index):
        if agent_index == 1:
            return self.__agent1
        return self.__agent2

    def parse_json_to_move(self, current_state, dic):
        print(dic)
        bonus_node = int(dic['bonusNode']['id'])
        attacker_node = dic['attackerNode']['id']
        attacked_node = dic['attackedNode']['id']
        attacked_node_armies = int(dic['attackedNodeArmies'])
        move_from_node = dic['movedFromNode']['id']
        move_to_node = dic['movedToNode']['id']
        moved_armies = int(dic['movedArmies'])
        self.__error_messages = []
        bonus_node = self.validate_bonus(current_state, bonus_node)
        move_from_node, move_to_node, moved_armies = self.validate_move(current_state, move_from_node, move_to_node, moved_armies)
        attacker_node, attacked_node, attacked_node_armies = self.validate_attack(current_state, attacker_node, attacked_node, attacked_node_armies)
        if len(self.__error_messages) > 0:
            return None, self.__error_messages
        else:
            move = Move()
            move.set_bonus_hold_node(bonus_node)
            move.set_move_from_node(move_from_node)
            move.set_move_to_node(move_to_node)
            move.set_moved_armies(moved_armies)
            move.set_attacker_node(attacker_node)
            move.set_attacked_node(attacked_node)
            move.set_attacked_node_armies(attacked_node_armies)
            return move, self.__error_messages

    def validate_bonus(self, current_state, bonus_node):
        if bonus_node == -1:
            return None
        node = current_state.get_current_player().get_node_by_name(bonus_node)
        if node is None:
            self.__error_messages.append("The bonus node with id = {} doesn't belong to the current player".format(bonus_node))
        else:
            return node

    def validate_attack(self, current_state, attacker_node, attacked_node, attacked_armies):
        if attacker_node == 'null' or attacked_node == 'null':
            if not (attacker_node == 'null' and attacked_node == 'null' and attacked_armies == -1):
                self.__error_messages.append("Invalid attack try")
            return None
        attacker_node = current_state.get_current_player().get_node_by_name(int(attacker_node))
        attacked_node = current_state.get_next_player().get_node_by_name(int(attacked_node))
        if (attacker_node is None) or (attacked_node is None) or (attacked_armies <= 0):
            self.__error_messages.append("Invalid attack nodes or attacked armies")
            return None
        if attacker_node.can_attack(attacked_node, attacked_armies):
            return attacker_node, attacked_node, attacked_armies
        else:
            self.__error_messages.append("Can't do the attack, Invalid attack Condition")
            return None

    def validate_move(self, current_state, move_from_node, move_to_node, moved_armies):
        if move_from_node == 'null' or move_to_node == 'null':
            if not (move_from_node == 'null' and move_to_node == 'null' and moved_armies == -1):
                self.__error_messages.append("Invalid move try")
            return None
        move_from_node = current_state.get_current_player().get_node_by_name(int(move_from_node))
        move_to_node = current_state.get_current_player().get_node_by_name(int(move_to_node))
        if (move_from_node is None) or (move_to_node is None) or (moved_armies <= 0):
            self.__error_messages.append("Invalid move nodes or moved armies")
            return None
        if move_from_node.can_move_to_another_node(moved_armies, move_to_node):
            return move_from_node, move_to_node, moved_armies
        else:
            self.__error_messages.append("Can't do the move, Invalid move Condition")
            return None

    def parse_state_to_json(self, state, error_messages):
        dic = {}
        # Parsing status and errors
        if len(error_messages) == 0:
            dic['status'] = 'valid'
        else:
            dic['status'] = 'invalid'
            for error in error_messages:
                dic['error'].append(error)

        # Parsing State to player turn (1 or 2)
        dic['player'] = state.get_player_turn_number() + 1

        # Parsing State to player bonus
        dic['bonus'] = state.get_current_player().get_bonus()

        for player in state.get_players():
            nodes = player.get_hold_nodes()
            for node in nodes:
                node_dic = {}
                node_dic['id'] = node.get_node_name()
                node_dic['x'] = node.get_position()[0]
                node_dic['y'] = node.get_position()[1]
                node_dic['title'] = node.get_army()
                node_dic['Player'] = player.get_name()
                dic['nodes'].append(node_dic)
        return dic


"""
status = valid
'nodes': {id, x, y, title = army, Player = Player 1, 2}
player:
bonus:
messages
"""

"""
'nodes': {id, x, y, title = army, Player = Player 1, 2}
'partitions': [{}, {}, ]
'edges': 1->2 == 1 <->2 []
 p1
 p2
== == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == ==
move ?

"""

