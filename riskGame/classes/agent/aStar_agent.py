from riskGame.classes.agent.one_time_agent import OneTimeAgent
from riskGame.classes.evaluations.sigmoidEval import SigmoidEval


class AStar(OneTimeAgent):

    def __init__(self, evaluation_heuristic=SigmoidEval()):
        self.__evaluation_heuristic = evaluation_heuristic
        super(AStar, self).__init__(self.calculate_fn)

    def calculate_fn(self, state):
        gn = state.calculate_gn(self.__initial_state)
        hn = self.__evaluation_heuristic.score(state)
        return gn + hn

