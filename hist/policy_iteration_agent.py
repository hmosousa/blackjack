#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:37:27 2020

@author: hugosousa
"""

import numpy as np

def hand_sum(hand):
    total = 0
    total_ace = 0
    for card in hand:
        if card == "A":
            total_ace+=1
        elif card.isnumeric():
            total+=int(card)
        else:
            total+=10
    total += total_ace
    if total_ace > 0:
        if total+10 <= 21:
            total += 10        
    return total


def generate_rewards(hand_value):
    rewards = []
    for v in np.arange(hand_value+1, hand_value+14):
        if v == 21:
            rewards.append(10)
        elif v<21:
            rewards.append(1)
        else:
            rewards.append(-10)
    rewards = np.array(rewards)
    return rewards


def policy_evaluation(values, policy, probabilities):
    delta = 1e-3

    while True:
        old_values = values.copy()
        for s in range(21):
            pol = policy[s]
            if pol:
                rewards = generate_rewards(s)
                val = values[(s+1):(s+1+13)]
                values[s] = np.dot(probabilities.T, rewards + 0.8*val)
            else:
                values[s] = 0.1 + 0.8 * values[s]
        if max(abs(old_values-values)) < delta:
            break
        
    return values

    
def policy_improvement(values, policy, probabilities):
    while True:
        old_policy = policy.copy()
        for s in range(21):
            rewards = generate_rewards(s+1)
            val = values[(s+1):(s+1+13)]
            
            cand = [0.1 + 0.8 * values[s],
                    np.dot(probabilities.T, rewards + 0.8*val)]
            

            policy[s] = cand.index(max(cand))
        if all(old_policy==policy):
            break
    return policy




values = np.zeros(21+14)
policy = np.repeat(False,21)
        
    
hand = ["A","K"]#np.array(hand)
table_cards = ["2","3","A","K"]#np.array(table_cards)
        
cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
cards_left = dict(zip(cards, np.repeat(4*8,len(cards))))
        
for c in table_cards:
    cards_left[c] -= 1




# compute probabilities        
probabilities = list(cards_left.values())/sum(cards_left.values())

# policy iteration
values = policy_evaluation(values, policy, probabilities)

policy = policy_improvement(values, policy, probabilities)


hand_value = hand_sum(hand)
policy[hand_value-1]

       
