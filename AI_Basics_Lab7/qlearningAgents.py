from learningAgents import ReinforcementAgent

import random, util

class QLearningAgent(ReinforcementAgent):

    def __init__(self, **args):
        ReinforcementAgent.__init__(self, **args)

        self.values  = util.Counter()

    def getQValue(self, state, action):

        return self.values[(state,action)]




    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        Qval = float('-inf')

        for action in self.getLegalActions(state):
            Qval  = max(self.getQValue(state, action), Qval)

        if Qval == float('-inf'):
            return 0.0
        else : return Qval


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        if len(self.getLegalActions(state)) is 0:
            return None

        val = self.computeValueFromQValues(state)
        actions = []

        for action in self.getLegalActions(state):
            if val is self.getQValue(state, action):
                actions.append(action)

        return random.choice(actions)


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"

        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(state)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        self.values[(state, action)] = (1-self.alpha) * self.values[(state,action)] + self.alpha * (reward + self.discount*self.computeValueFromQValues(nextState))


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)

