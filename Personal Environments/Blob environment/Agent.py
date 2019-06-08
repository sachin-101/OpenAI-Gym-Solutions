from collections import defaultdict
import sys
import numpy as np 
import pickle

class Agent:

    def __init__(self, env, alpha, gamma=1.0, eps_start=1.0, eps_decay=0.9999, eps_min=0.05):
        self.env = env
        self.eps_start = eps_start
        self.gamma = gamma
        self.alpha = alpha
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.nA = env.ACTION_SPACE

    def action_from_eps_greedy_policy(self, state, Q, epsilon, nA):
        '''
            Chooses action with max Q-value with a probability of 1-epsilon (Exploitation)
            or any other action with probability = epsilon/(nA-1) for each.
            
            sum of probabilities = (nA-1) * epsilon/(nA-1) + 1*(1-epsilon) = 1
        '''
        max_ = np.argmax(Q[state])
        prob = self.get_prob(nA, epsilon, max_)
        action = np.random.choice(np.arange(nA), p=prob)
        return action

    def get_prob(self, nA, epsilon, max_):
        '''
            returns probability distribution
            with max index probability = 1-epsilon
            and rest indices set to probability = epsilon
        '''
        prob = np.ones(nA)*epsilon/(nA-1)
        prob[max_] = 1 - epsilon
        return prob
    

    def interact(self, num_episodes):
        '''
            interact with the environment and learn
        '''
        Q = defaultdict( lambda: np.zeros(self.nA))
        epsilon = self.eps_start
        eps_decay = self.eps_decay  #decay rate of epsilon
        eps_min = self.eps_min       #min epsilon value, not allowing to go very low, to maintain exploration
        # loop over episodes
        for i_episode in range(1, num_episodes+1):
            # monitor progress
            if i_episode % 100 == 0:
                print("\rEpisode {}/{}".format(i_episode, num_episodes), end="")
                sys.stdout.flush() 
            #calculating epsilon
            epsilon = max(epsilon*eps_decay, eps_min)
            #observing state s0 and taking action
            state_prev = self.env.reset()
            action_prev = self.action_from_eps_greedy_policy(state_prev, Q, epsilon, self.nA)
            #loop over SARSA
            while True:
                state, reward, done = self.env.step(action_prev)
                Q[state_prev][action_prev] += self.alpha*(reward + self.gamma*np.max(Q[state]) - Q[state_prev][action_prev])
                if done:
                    break
                #update state and action
                state_prev = state
                action_prev = self.action_from_eps_greedy_policy(state, Q, epsilon, self.nA)

        self.Q = Q
        self.policy = self.get_Policy(Q)

    def get_Policy(self, Q):
        '''
            returns optimal policy using the Q-table
        '''
        policy = defaultdict(lambda: 0)
        for state, action in Q.items():
            policy[state] = np.argmax(action)
        return policy
    
    def take_action(self,state):
        '''
            take action as per policy
        '''
        return self.policy[state]

    def set_policy(self, directory):
        '''
            To be used while importing experience from colab
        '''
        with open(directory, 'rb') as f:
            policy_new = pickle.load(f)
        self.policy = defaultdict(lambda:0, policy_new)  #saved as defaultdict
        print('policy Loaded')        

    def save(self,i):
        try:
            policy = dict(agent.policy)
            with open(f'policy{i}.pickle','wb') as f:
                pickle.dump(policy, f)
        except :
            print('not saved')