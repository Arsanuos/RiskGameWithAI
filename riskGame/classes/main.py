from riskGame.classes.parser.parser import Parser
from riskGame.classes.agent.human import Human

#dic from frontend for the initial state
dic = {}
parser = Parser()
parser.parse_json_to_state(dic)
initial_state = parser.get_initial_state()
agents = []
agents.append(parser.get_agent(1))
agents.append(parser.get_agent(2))
prev_state = None
current_state = initial_state

while current_state.get_winner() is None:
    player_turn = current_state.get_player_turn_number()
    if isinstance(agents[player_turn], type(Human)):
        # get dic from front end for the move
        move, errors = parser.parse_json_to_move(current_state, dic)
        if move:
            prev_state = current_state
            current_state = agents[player_turn].play(current_state, move)
        dic = parser.parse_state_to_json(current_state, errors)
    else:
        # get request to represent get the next turn state
        prev_state = current_state
        current_state = agents[player_turn].play(current_state)
        dic = parser.parse_state_to_json(current_state, [])
    # send dic to front end

