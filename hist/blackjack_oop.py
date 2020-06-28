#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 00:13:58 2020

@author: hugosousa
"""

import numpy as np


def draw_cards(deck, n):
    '''
    Draws n cards from deck. 
    
    Output:
        hand: the n cards that were draw.
        deck: what remains of the deck after the draw.
    '''
    hand = deck[:n]
    deck = deck[n:]
    return hand, deck


def hand_sum(hand):
    '''
    Computes the value of an blackjack hand.
    If the hand has an ace it will return the highes value of the hand.
    
    Parameters
    ----------
    hand : list
        A blackjack hand.

    Returns
    -------
    total : int
        The value of hand in a blackjack game.

    '''
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


def dealer(dealer_hand):
    '''
    This mimics the dealer behaviour in a blackjack game.

    Parameters
    ----------
    dealer_hand : list
        The cards that the dealer has.

    Returns
    -------
    bool
        If the dealer Hits or Stops the game.

    '''
    dealer_value = hand_sum(dealer_hand)
    
    while (dealer_value < 17):
        return True
    return False


def blackjack(agent, num_decks=8):
    '''
    Simulates a blackjack game.

    Parameters
    ----------
    agent : Class
        The agent that will take the decisions.
    num_decks : int,
        The number of decks that we want to play. 
        The default is 8.

    Returns
    -------
    int
        Returns if the agent won, lost or tied.
            won: 1
            lost: -1
            tied: 0
    '''
    
    cards     = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    deck      = np.array(cards * 4 * num_decks)
    
    np.random.shuffle(deck)
        
    dealer_hand, deck = draw_cards(deck, 2)
    player_hand, deck = draw_cards(deck, 2)
    
    known_cards = np.append(player_hand, dealer_hand[0])
    
    ####
    player_value = hand_sum(player_hand)
    dealer_value = hand_sum(dealer_hand)
    
    # player turn
    while agent.play(player_hand, known_cards):
        card, deck = draw_cards(deck, 1)
        player_hand = np.append(player_hand, card)
        player_value = hand_sum(player_hand)
        if player_value>21:
            return -1
        known_cards = np.append(known_cards, card)
    
   
    # dealer turn
    while dealer(dealer_hand):
        card, deck = draw_cards(deck, 1)
        dealer_hand = np.append(dealer_hand, card)
        dealer_value = hand_sum(dealer_hand)
        if dealer_value>21:
            return 1
    
    player_value = hand_sum(player_hand)
    dealer_value = hand_sum(dealer_hand)
    
    print( f"Player Hand : {player_value} {player_hand}") 
    print( f"Dealer Hand : {dealer_value} {dealer_hand} \n") 
    
    if player_value>dealer_value:
        return 1
    elif player_value==dealer_value:
        return 0 
    return -1


  
class Q_Agent():
    def __init__(self, num_decks=8):
        self.num_decks = num_decks
        self.values = np.zeros(21+14)
        self.policy = np.repeat(False,21)
        self.cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
        
    @staticmethod
    def generate_rewards(hand_value):
        rewards = []
        for v in np.arange(hand_value+1, hand_value+14):
            if v == 21:
                rewards.append(10)
            elif v<21:
                rewards.append(3)
            else:
                rewards.append(-10)
        rewards = np.array(rewards)
        return rewards
    
    def policy_evaluation(self, probabilities):
        delta = 1e-3
    
        while True:
            old_values = self.values.copy()
            for s in range(21):
                pol = self.policy[s]
                if pol:
                    rewards = self.generate_rewards(s)
                    val = self.values[(s+1):(s+1+13)]
                    self.values[s] = np.dot(probabilities.T, rewards + 0.9*val)
                else:
                    self.values[s] = 0.1 + 0.9 * self.values[s]
            if max(abs(old_values-self.values)) < delta:
                break
            
    
    def policy_improvement(self, probabilities):
        while True:
            old_policy = self.policy.copy()
            for s in range(21):
                rewards = self.generate_rewards(s+1)
                val = self.values[(s+1):(s+1+13)]
                
                cand = [0.1 + 0.9 * self.values[s],
                        np.dot(probabilities.T, rewards + 0.9*val)]
                
    
                self.policy[s] = cand.index(max(cand))
            if all(old_policy == self.policy):
                break
  
    
    def play(self, hand, table_cards):                 
        card_count = np.repeat(4*self.num_decks, len(self.cards))
        cards_left = dict(zip(self.cards, card_count))       
        for c in table_cards:
            cards_left[c] -= 1
        
        # compute probabilities        
        probabilities = list(cards_left.values())/sum(cards_left.values())
        
        # policy iteration
        self.policy_evaluation(probabilities)
        self.policy_improvement(probabilities)
        
        hand_value = hand_sum(hand)
        
        return self.policy[hand_value-1]
    

p1 = Q_Agent()
p1.play(["6","3"], ["2","3","2","2"])



blackjack(p1)

num_games = 1000
games = []
for _ in range(num_games):
    games.append(blackjack(p1))
    

p1.policy
p1.values
games=np.array(games)

sum(games==1)
sum(games==0)
sum(games==-1)

import matplotlib.pyplot as plt
plt.plot(games.cumsum())