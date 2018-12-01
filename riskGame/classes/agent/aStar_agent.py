from riskGame.classes.agent.one_time_agent import OneTimeAgent
from riskGame.classes.evaluations.sigmoidEval import SigmoidEval


class AStar(OneTimeAgent):

    def __init__(self, evaluation_heuristic=SigmoidEval()):
        self.__evaluation_heuristic = evaluation_heuristic
        super(AStar, self).__init__()

    def calculate_fn(self, state, initial_state):
        gn = state.calculate_gn(initial_state)
        hn = self.__evaluation_heuristic.score(state)
        return gn + hn

