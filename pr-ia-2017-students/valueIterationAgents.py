# valueIterationAgents.py
# -----------------------
##
import mdp, util
import sys

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp = None, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbabilities(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        if (self.mdp != None):
            self.doValueIteration()

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """

        #"*** YOUR CODE STARTS HERE ***"
        qvalue = 0
        transSP = self.mdp.getTransitionStatesAndProbabilities(state, action)
        
        for x in transSP:
            qvalue = qvalue + (x[1] * (self.mdp.getReward(state, action, x[0])
             + (self.discount * self.values[x[0]])))
        """
          This function is later used in doValueIteration
          and computeActionFromValues
          So we declare it beforehand
        """


        #"*** YOUR CODE FINISHES HERE ***"
        
        return qvalue
    

    def doValueIteration (self):
        # Write value iteration code here

        print "Iterations: ", self.iterations
        print "Discount: ", self.discount
        states = self.mdp.getStates()
        maxDelta = float("-inf")


        #"*** YOUR CODE STARTS HERE ***"
        # Your code should include the implementation of value iteration
        # At the end it should show in the terminal the number of states
        # considered in self.values and
        # the Delta between the last two iterations

        temp = util.Counter() #Don't update the v-values "live"
        maxDeltaState = ""
        
        for it in range(self.iterations): #For the number of iterations
            for state in states: #For all states
                if self.mdp.isTerminal(state): #If state is terminal the reward 
                    temp[state] = 0            # is 0

                else:
                    possibleActions = self.mdp.getPossibleActions(state)
                    ValuesConsidered = [] #Reset Q-values considered
                     
                    for action in possibleActions: #For all possible actions
                        ValuesConsidered.append(self.getQValue(state, action))
                    temp[state] = max(ValuesConsidered)#Take the highest Q-Value

            #Calculate the difference for each iteration 
            maxDeltaState = util.Counter.argMax(temp - self.values)
            maxDelta = temp[maxDeltaState] - self.values[maxDeltaState]

            self.values = temp #Load the temporary value into the V-values
            temp = util.Counter() #Reset the temporary values

        print "Number of states considered: ", len(self.values)
        print "Last Delta between iterations: ", maxDelta

        return self.values

        #"*** YOUR CODE FINISHES HERE ***"
        
    def setMdp( self, mdp):
        """
          Set an mdp.
        """
        self.mdp = mdp
        self.doValueIteration()

    def setDiscount( self, discount):
        """
          Set a discount
        """
        self.discount = discount

    def setIterations( self, iterations):
        """
          Set a number of iterations
        """
        self.iterations = iterations
       
       
    def getValue(self, state):
        """
          Return the value of the state
        """
        return self.values[state]
        


    def showPolicy( self ):

        """
          Print the policy
        """
        
        states = self.mdp.getStates()
        for state in states:
            print "Policy\n", state, self.getPolicy(state)


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """

        #"*** YOUR CODE STARTS HERE ***"

        if self.mdp.isTerminal(state):
            return None

        posActions = self.mdp.getPossibleActions(state)
        allQValues = util.Counter()

        for action in posActions:
            allQValues[action] = self.computeQValueFromValues(state, action)
        return util.Counter.argMax(allQValues)

        #"*** YOUR CODE FINISHES HERE ***"

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getPolicy(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getAction(state)

    
    def getQValue(self, state, action):
        "Returns the Q value."        
        return self.computeQValueFromValues(state, action)

    def getPartialPolicy(self, stateL):
        "Returns the partial policy at the state. Random for unkown states"        
        state,state_names = self.mdp.stateToHigh(stateL)
        if self.mdp.isKnownState(state):
            return self.computeActionFromValues(state)
        else:
            # random action
            return util.random.choice(stateL.getLegalActions()) 

