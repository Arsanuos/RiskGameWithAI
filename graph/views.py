from django.shortcuts import render
from riskGame.classes.parser.parser import Parser
from riskGame.classes.agent.human import Human
import json
from django.http import JsonResponse

prev_state = None
current_state = None
agents = []
parser = Parser()


# Create your views here.
def index(request):
    #this is the shape of the request add your logic here based on that.
    dict = request.POST.dict()
    global prev_state, current_state, agents, parser

    if 'json' in dict:
        data = dict['json']
        type = dict['type']
        dic = json.loads(data)
        if type == "state":
            # dic from frontend for the initial state
            parser.parse_json_to_state(dic)
            initial_state = parser.get_initial_state()
            agents = []
            agents.append(parser.get_agent(1))
            agents.append(parser.get_agent(2))
            current_state = initial_state
            print('Finished Initialization')
        elif type == "turn":
            if current_state.get_winner() is None:
                player_turn = current_state.get_player_turn_number()
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
                    current_state = agents[player_turn].play(current_state, None)
                    dic = parser.parse_state_to_json(current_state, [])

                print('Finished Playing,, the current state is following:')
                print(dic)
                return JsonResponse(dic)
                # send dic to front end
            else:
                response = {"status":"winner", "winner": "Player " + str(current_state.get_winner().get_name() + 1)}
                return render(response, 'index.html')

    return render(request, 'index.html')

    """
        except Exception as e:
        print(str(e))
    """