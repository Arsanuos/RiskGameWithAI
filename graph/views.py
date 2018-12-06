from django.shortcuts import render
from riskGame.classes.parser.parser import Parser
from riskGame.classes.agent.human import Human
from riskGame.classes.agent.one_time_agent import OneTimeAgent
from riskGame.classes.agent.real_time_aStar import RTAStar
import json
from django.http import JsonResponse

prev_state = None
current_state = None
agents = []
all_states = []
parser = Parser()
flag = False

# Create your views here.
def index(request):
    #this is the shape of the request add your logic here based on that.
    dict = request.POST.dict()
    global prev_state, current_state, agents, parser, all_states, flag

    if 'json' in dict:
        data = dict['json']
        type = dict['type']
        dic = json.loads(data)
        if type == "state":
            # dic from frontend for the initial state
            parser.parse_json_to_state(dic)
            initial_state = parser.get_initial_state()
            agents = []
            all_states = []
            flag = False
            agents.append(parser.get_agent(1))
            agents.append(parser.get_agent(2))
            current_state = initial_state
            print('Finished Initialization')
            dic = {'status':'initial'}
            return JsonResponse(dic)
        elif type == "turn":
            if current_state is None:
                exit(-1)
            player_turn = current_state.get_player_turn_number()
            game_end = False
            if isinstance(agents[player_turn], Human):
                # get dic from front end for the move
                move, errors = parser.parse_json_to_move(current_state, dic)
                if move:
                    prev_state = current_state
                    current_state = agents[player_turn].play(current_state, move)
                dic = parser.parse_state_to_json(current_state, errors)
            else:
                # get request to represent get the next turn state
                prev_state = current_state
                if isinstance(agents[player_turn], OneTimeAgent):
                    if len(all_states) == 0 and flag == False:
                        all_states = agents[player_turn].search(current_state)
                        flag = True
                    if flag and len(all_states) == 0:
                        # no change in current state but insert tie
                        current_state = current_state
                        game_end = True
                    else:
                        current_state = all_states.pop(0)
                elif isinstance(agents[player_turn], RTAStar):
                    current_state = agents[player_turn].play(current_state)
                else:
                    if len(all_states) > 0:
                        current_state = all_states.pop(0)
                    else:
                        current_state = agents[player_turn].play(current_state, None)
                dic = parser.parse_state_to_json(current_state, [])

            if current_state.get_winner():
                dic["status"] = "winner"
                dic["winner"] = str(current_state.get_winner().get_name())
            if game_end:
                dic["status"] = "tie"
            print('Finished Playing,, the current state is following:')
            print(dic)
            return JsonResponse(dic)
        else:
            NotImplemented
    return render(request, 'index.html')

    """
        except Exception as e:
        print(str(e))
    """