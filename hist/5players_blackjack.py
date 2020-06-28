#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 18:17:32 2020

@author: hugosousa

"""

import numpy as np
import json

def agent2(player_hand, dealer_hand, cards_table, prob_th=0.27):
    '''
    player_hand = np.array(["A","10"])
    dealer_hand = np.array(["3"])
    player(["A","10"], ["2","3"])
    '''
    player_value = hand_sum(player_hand)
    
    cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
    cards_left = dict(zip(cards,np.repeat(4*8,len(cards))))
    cards_value = json.load(open("card_value.json"))
    
    value_left = 21 - player_value
    
    num_fav = 0
    for k,v in cards_left.items():
        if cards_value[k] <= value_left:
            num_fav += v
    num_pos = 4*8*len(cards)
    
    prob = num_fav/num_pos
    #print(prob)
    if prob >= prob_th:
        return True
    
    return False


class Agent3():
    def __init__(self):
        self.values = np.zeros(21+13)
        self.policy = np.repeat(False,21)
        

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
        
    def play(self, hand, table_cards): 
        hand = np.array(hand)
        table_cards = np.array(table_cards)
        
        cards = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K'])
        cards_left = dict(zip(cards,np.repeat(4*8,len(cards))))
        cards_value = json.load(open("card_value.json"))

        
        for c in table_cards:
            cards_left[c] -= 1
        
        hand_value = hand_sum(hand)
        value_left = 21 - hand_value
        
        if value_left == 0: 
            self.values[hand_value] = 5+VALUES[hand_value]
            return False
        
        # compute probabilities        
        probabilities = list(cards_left.values())/sum(cards_left.values())
        
        # policy evaluation
        # if action = True
        rewards = np.append(np.ones(value_left-1), 5)  
        rewards = np.append(rewards, np.repeat(-10, 13-value_left))
        
        values = VALUES[(hand_value+1):(hand_value+1+13)]
        valueT = np.dot(probabilities.T, rewards + values)  
        
        # if poolicy = False
        valueF = 0.1+VALUES[hand_value]
        
        if valueT >= valueF:
            self.values[hand_value] = valueT
            self.policy[hand_value] = True
        else:
            self.values[hand_value] = valueF
            self.policy[hand_value] = False
        
        return self.policy[hand_value]
    

p1 = Agent3()
p2 = Agent3()
p3 = Agent3()
p4 = Agent3()
p5 = Agent3()



player.play(['8', '5'], ['8', '5', '4', '3', '9', '9', '2', '9', 'K', '6', '3'])

players = [p1,p2,p3,p4,p5]


#five player game
def game():
    #define deck
    deck = np.array(['A','2','3','4','5','6','7','8','9','10','J','Q','K']*4*8) # playing with 8 decks
    np.random.shuffle(deck)
        
    dealer_hand, deck = draw_cards(2,deck)
    hand1, deck = draw_cards(2,deck)
    hand2, deck = draw_cards(2,deck)
    hand3, deck = draw_cards(2,deck)
    hand4, deck = draw_cards(2,deck)
    hand5, deck = draw_cards(2,deck)
    
    #players = {"p1":p1_hand,"p2":p2_hand, "p3":p3_hand, "p4":p4_hand,"p5":p5_hand}
    
    known_cards = np.array(list(players.values())).flatten()
    known_cards = np.append(known_cards, dealer_hand[0])
    

    # players turn
    for player in players:
        while p1(, dealer_hand[0], known_cards, prob):
            card, deck = draw_cards(1,deck)
            players[player] = np.append(players[player], card)
            known_cards = np.append(known_cards, card)
            player_value = hand_sum(players[player])
            
        
    # dealer turn
    while dealer(dealer_hand):
        card, deck = draw_cards(1,deck)
        dealer_hand = np.append(dealer_hand, card)
        dealer_value = hand_sum(dealer_hand)
    

    dealer_value = hand_sum(dealer_hand)
    
    player_value = {}
    for player, hand in players.items():
        player_value[player] = hand_sum(hand)
        
    results = {}
    for player, value in player_value.items():
        if (dealer_value <=21) & (value <=21) & (dealer_value<value):    
            results[player] = 1
        elif (value <=21) & (dealer_value>21):
            results[player] = 1
        elif (dealer_value <=21) & (value <=21) & (dealer_value==value):
            results[player] = 0
        else:
            results[player] = -1
        
    return results

num_games = 10000
games = []
for _ in range(num_games):
    games.append(game())
    
data = pd.DataFrame(games)

data.sum()
(data == 1).sum() / num_games * 100


'''
p1    -904
p2    -782
p3   -1000
p4    -869
p5    -985
'''



(data == 1).sum() / num_games * 100
