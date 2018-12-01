from riskGame.classes.agent.one_time_agent import OneTimeAgent
from riskGame.classes.evaluations.sigmoidEval import SigmoidEval


class Greedy(OneTimeAgent):

    def __init__(self, evaluation_heuristic=SigmoidEval()):
        self.__evaluation_heuristic = evaluation_heuristic
        super(Greedy, self).__init__()

    def calculate_fn(self, state, inital_state):
        hn = self.__evaluation_heuristic().score(state)
        return hn

