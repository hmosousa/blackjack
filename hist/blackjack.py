#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:47:05 2020

@author: hugosousa
"""

import numpy as np

def draw_cards(deck, n):
    hand = deck[:n]
    deck = deck[n:]
    return hand, deck


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


class BlackJack():
    def __init__(self, num_decks=8, verbose=False):
        self.num_decks = num_decks
        self.cards     = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.deck      = np.array(self.cards * 4 * self.num_decks)
        self.verbose   = verbose
   
    def log(self, text):
        if self.verbose:
            print(text)

    @staticmethod
    def dealer(dealer_hand):
        dealer_value = hand_sum(dealer_hand)
        
        while (dealer_value < 17):
            return True
        return False


    def game(self, agent):
        np.random.shuffle(self.deck)
            
        dealer_hand, deck = draw_cards(self.deck, 2)
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
        while self.dealer(dealer_hand):
            card, deck = draw_cards(deck, 1)
            dealer_hand = np.append(dealer_hand, card)
            dealer_value = hand_sum(dealer_hand)
            if dealer_value>21:
                return 1
        
        player_value = hand_sum(player_hand)
        dealer_value = hand_sum(dealer_hand)
        
        self.log( f"Player Hand : {player_value} {player_hand}") 
        self.log( f"Dealer Hand : {dealer_value} {dealer_hand} \n") 
        
        if player_value>dealer_value:
            return 1
        elif player_value==dealer_value:
            return 0 
        return -1
    
    
class Agent3():
    def __init__(self):
        self.values = np.zeros(21+14)
        self.policy = np.repeat(False,21)
        
    
    def play(self, hand, table_cards): 
        hand = np.array(hand)
        table_cards = np.array(table_cards)
        
        cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
        cards_left = dict(zip(cards,np.repeat(4*8,len(cards))))
        
        for c in table_cards:
            cards_left[c] -= 1
        
        hand_value = hand_sum(hand)
        
        if hand_value == 21: 
            self.values[hand_value] = 5 + self.values[hand_value]
            return False
        
        # compute probabilities        
        probabilities = list(cards_left.values())/sum(cards_left.values())
        
        # policy evaluation
        # if action = True
        rewards = []
        for v in np.arange(hand_value+1, hand_value+14):
            if v == 21:
                rewards.append(10)
            elif v<21:
                rewards.append(1)
            else:
                rewards.append(-10)
        rewards = np.array(rewards)
        
        values = self.values[(hand_value+1):(hand_value+1+13)]
        valueT = np.dot(probabilities.T, rewards + values)  
        
        # if poolicy = False
        valueF = 0.1+self.values[hand_value]
        
        if valueT >= valueF:
            self.values[hand_value] = valueT
            self.policy[hand_value] = True
        else:
            self.values[hand_value] = valueF
            self.policy[hand_value] = False
        
        return self.policy[hand_value]
    
       
        

p1 = Agent3()
p1.play(["2","2"], ["2","3","2","2"])



blackjack = BlackJack(verbose=False)

num_games = 10000
games = []
for _ in range(num_games):
    games.append(blackjack.game(p1))
    

p1.policy
p1.values
games=np.array(games)

sum(games==1)
sum(games==0)
sum(games==-1)

import matplotlib.pyplot as plt
plt.plot(games.cumsum())



