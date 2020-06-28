#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 12:46:40 2020

@author: hugosousa
"""

from blackjack import *
from agents import Q_Agent

import matplotlib.pyplot as plt

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


plt.plot(games.cumsum())
plt.show()


# five player game

p1 = Q_Agent()
p2 = Q_Agent()
p3 = Q_Agent()
p4 = Q_Agent()
p5 = Q_Agent()

players = [p1, p2, p3, p4, p5]

num_games = 1000
games = []
for _ in range(num_games):
    games.append(five_player_blackjack(players))


rp1 = np.array([game[p1] for game in games])
rp2 = np.array([game[p2] for game in games])
rp3 = np.array([game[p3] for game in games])
rp4 = np.array([game[p4] for game in games])
rp5 = np.array([game[p5] for game in games])

fig, ax = plt.subplots()
ax.plot(rp1.cumsum(), label='p1')
ax.plot(rp2.cumsum(), label='p2')
ax.plot(rp3.cumsum(), label='p3')
ax.plot(rp4.cumsum(), label='p4')
ax.plot(rp5.cumsum(), label='p5')
ax.legend()
plt.show()

print(p1.policy[11:])
print(p2.policy[11:])
print(p3.policy[11:])
print(p4.policy[11:])
print(p5.policy[11:])

sum(rp1 + rp2+rp3+rp4+rp5)
    