#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 12:45:15 2020

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
            print( f"Player Hand : {player_value} {player_hand}") 
            print( f"Dealer Hand : {dealer_value} {dealer_hand} \n") 
            return -1
        known_cards = np.append(known_cards, card)
    
   
    # dealer turn
    while dealer(dealer_hand):
        card, deck = draw_cards(deck, 1)
        dealer_hand = np.append(dealer_hand, card)
        dealer_value = hand_sum(dealer_hand)
        if dealer_value>21:
            print( f"Player Hand : {player_value} {player_hand}") 
            print( f"Dealer Hand : {dealer_value} {dealer_hand} \n") 
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




def five_player_blackjack(players, num_decks=8):
    '''
    Simulates a blackjack game.

    Parameters
    ----------
    players : list
        A list with the agents that will play the game.
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
    
    # deal the cards    
    dealer_hand, deck = draw_cards(deck, 2)
    p1_hand, deck = draw_cards(deck, 2)
    p2_hand, deck = draw_cards(deck, 2)
    p3_hand, deck = draw_cards(deck, 2)
    p4_hand, deck = draw_cards(deck, 2)
    p5_hand, deck = draw_cards(deck, 2)
        
    # create a list of all the cards that we know
    known_cards = np.array([p1_hand, p2_hand, p3_hand, p4_hand, p5_hand]).flatten()
    known_cards = np.append(known_cards, dealer_hand[0])
    
    hands = [p1_hand, p2_hand, p3_hand, p4_hand, p5_hand]
    player_hand = dict(zip(players, hands))

    # player turn
    for player in player_hand:
        while player.play(player_hand[player], known_cards):
            card, deck = draw_cards(deck, 1)
            player_hand[player] = np.append(player_hand[player], card)
            
            player_value = hand_sum(player_hand[player])
            known_cards = np.append(known_cards, card)
    
   
    # dealer turn
    while dealer(dealer_hand):
        card, deck = draw_cards(deck, 1)
        dealer_hand = np.append(dealer_hand, card)
        dealer_value = hand_sum(dealer_hand)
    
    # compute the hand value of each player
    player_value = {}
    for player, hand in player_hand.items():
        player_value[player] = hand_sum(hand)
    
    # hand value of dealer
    dealer_value = hand_sum(dealer_hand)
    
    # check the results for each player
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
            
    
    for idx, player in enumerate(players):
        print( f"Player {idx+1} Hand : {player_value[player]} {player_hand[player]}") 
    print( f"Dealer Hand : {dealer_value} {dealer_hand} \n") 
    
    return results