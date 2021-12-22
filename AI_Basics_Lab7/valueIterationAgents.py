import util

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):

    def __init__(self, mdp, discount=0.9, iterations=100):
 
        super().__init__()
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here

        for i in range(self.iterations):
            updatedValues = self.values.copy()

            for state in self.mdp.getStates():

                if self.mdp.isTerminal(state):
                    continue

                actions = self.mdp.getPossibleActions(state)
                optimal = max([self.getQValue(state, action) for action in actions])
                updatedValues[state] = optimal

            self.values = updatedValues

    def getValue(self, state):
        
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        

        qval = 0

        for s_prime, T in self.mdp.getTransitionStatesAndProbs(state, action):
            qval += T * (self.mdp.getReward(state, action, s_prime) + self.discount * self.getValue(s_prime))

        return qval

    def computeActionFromValues(self, state):
       

        policy = util.Counter()

        for action in self.mdp.getPossibleActions(state):
            policy[action] = self.getQValue(state, action)

        return policy.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
