#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 11:56:16 2020

@author: hugosousa
"""

import numpy as np
from blackjack import hand_sum


class Q_Agent():
    def __init__(self, num_decks=8):
        self.num_decks = num_decks
        self.values = np.zeros(21+14)
        self.policy = np.repeat(True, 21)
        self.cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
        
    @staticmethod
    def generate_rewards(hand_value):
        rewards = []
        for v in np.arange(hand_value+1, hand_value+14):
            if v == 21:
                rewards.append(3)
            elif v<21:
                rewards.append(3)
            else:
                rewards.append(-1)
        rewards = np.array(rewards)
        return rewards
    
    def policy_evaluation(self, probabilities):
        delta = 1e-3
    
        while True:
            old_values = self.values.copy()
            for s in range(12,21):
                pol = self.policy[s]
                if pol:
                    rewards = self.generate_rewards(s)
                    val = self.values[(s+1):(s+1+13)]
                    self.values[s] = np.dot(probabilities.T, rewards + 0.9*val)
                else:
                    self.values[s] = 0.9 * self.values[s]
            if max(abs(old_values-self.values)) < delta:
                break
            
    
    def policy_improvement(self, probabilities):
        while True:
            old_policy = self.policy.copy()
            for s in range(12,21):
                rewards = self.generate_rewards(s+1)
                val = self.values[(s+1):(s+1+13)]
                
                cand = [0.9 * self.values[s],
                        np.dot(probabilities.T, rewards + 0.9*val)]
                
    
                self.policy[s] = cand.index(max(cand))
            if all(old_policy == self.policy):
                break
  
    
    def play(self, hand, table_cards):    
        
        hand_value = hand_sum(hand)
        if hand_value >= 21:
            return False
        elif hand_value <= 11:
            return True
                 
        card_count = np.repeat(4*self.num_decks, len(self.cards))
        cards_left = dict(zip(self.cards, card_count))       
        for c in table_cards:
            cards_left[c] -= 1
        
        # compute probabilities        
        probabilities = list(cards_left.values())/sum(cards_left.values())
        
        # policy iteration
        self.policy_evaluation(probabilities)
        self.policy_improvement(probabilities)
        

        return self.policy[hand_value-1]