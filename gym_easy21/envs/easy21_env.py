import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_easy21.engine.easy21_engine import Engine, Player
import numpy as np
class Easy21Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False):
        self.verbose = verbose
        # Observation Space
        # Dealer's first card [1, 10] and player's sum [1, 21]
        self.observation_space = spaces.Tuple((
            spaces.Box(low=1, high=10, shape=(1,), dtype = np.uint8),
            spaces.Box(low=1, high=21, shape=(1,), dtype = np.uint8)
        ))

        # Action Space
        #   0 = Hit
        #   1 = Stick
        self.action_space = spaces.Discrete(2)  
        self.env = Engine(n=1)
        self.reset()
    
    def observe(self):
        dealer_card = self.env.dealer.cards[0]['val']
        player_total = self.env.players[0].total
        return (dealer_card, player_total)
    
    def step(self, action):
        rew = 0
        if self.done:
            if verbose:
                print('Game already over.\nPlease call reset() before performing any action')
            return self.observe(), self.reward, self.done, {'actions':{0:'hit', 1:'stick'}} 
        
        if self.stick:
            if verbose:
                print('Player has stuck and cannot make any move till the dealer is bust')
            return self.observe(), self.reward, self.done, {'actions':{0:'hit', 1:'stick'}} 
        
        if action==0:
            #Hit
            self.env.hit(0)
            if self.env.players[0].bust:
                self.reward = -1
                self.done = True
            return self.observe(), self.reward, self.done, {'actions':{0:'hit', 1:'stick'}} 
        
        elif action==1:
            #Stick
            self.stick = True
            self.dealer_action()
            return self.observe(), self.reward, self.done, {'actions':{0:'hit', 1:'stick'}} 
        else:
            raise ValueError('Action has to be any of (0 - Hit or 1 - Stay)')
    
    def reset(self):
        self.reward = 0
        self.env.reset()
        self.done = False
        self.stick = False
    
    def render(self, mode='human', close=False):
        self.env.show_state()

    def dealer_action(self):
        dealer = self.env.dealer
        player = self.env.players[0]
        while not dealer.bust:
            if dealer.total>=17:
                if verbose:
                    print('Dealer is sticking with %d'%(dealer.total))
                self.done = True
                if dealer.total>player.total:
                    #Lose
                    if verbose:
                        print('Player lost')
                    self.reward = -1
                elif dealer.total ==player.total:
                    #Draw
                    if verbose:
                        print('Draw')
                    self.reward = 0
                else:
                    #Win
                    if verbose:
                        print('Player won')
                    self.reward = 1
                break
            else:
                #Hit
                self.env.hit(-1)
        #Reward if dealer goes bust 
        self.reward = 1