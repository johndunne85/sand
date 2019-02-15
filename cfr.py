import random
from poker_rules import POKER_BOX, Hand, Card
import numpy as np
import pandas as pd
import itertools
import copy
from collections import Counter

def determine_value(x):
    try:
        return int(x)
    except ValueError:
        return {
            'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }.get(x)

pre_flop_odds = {'AA':'r','AK':'r','AQ':'r','AJ':'r','KK':'r','KQ':'r','KJ':'r','QK':'r','JK':'r','QJ':'r'\
                ,'KA':'r','QA':'r','JA':'r','11':'r','99':'r','88':'r','77':'r','66':'r','JJ':'r','JQ':'r'}


RANKS = [str(i) for i in range(5, 11)] + ['J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']
POKER_BOX = [r+s for r,s in itertools.product(RANKS, SUITS)]
random.seed()
random.shuffle(POKER_BOX)

ACTIONS = ['r', 'c', 'f']  # RAISE or CALL/CHECK or FOLD
turn_card = [0]
river_card = [0]
button = 0
#          0    1
stacks = [100, 100]
button_names = ['player_1','player_2']
pot = 0
small_blind = 1
big_blind = 2

#while(stacks[0] > 0 and stacks[1] > 0):

random.seed()
random.shuffle(POKER_BOX)

stacks[button] -= 1

stacks[(button+1)%2] -= 2
pot += 3

player_1 = POKER_BOX[:2]
player_2 = POKER_BOX[2:4]
# player_1 = ['1S','AD']
# player_2 = ['AS','7D']

player_1_two_card = player_1[0][0] + player_1[1][0]
player_2_two_card = player_2[0][0] + player_2[1][0]

print(player_1)
print(player_2)
print(player_1_two_card)
print(player_2_two_card)


if button_names[button] == 'player_1':
    if player_1_two_card in pre_flop_odds:
        print('player_1 raise')
        pot += 2
        stacks[0] -= 2
    else:
        pot += 1
        stacks[0] -= 1

if button_names[button] == 'player_2':
    if player_2_two_card in pre_flop_odds:
        print('player_2 raise')
        pot += 2
        stacks[1] -= 2
    else:
        pot += 1
        stacks[1] -= 1

if button_names[(button+1)%2] == 'player_1':
    if player_1_two_card in pre_flop_odds:
        print('player_1 raise')
        pot += 2
        stacks[0] -= 2
    else:
        pot += 1
        stacks[0] -= 1

if button_names[(button+1)%2] == 'player_2':
    if player_2_two_card in pre_flop_odds:
        print('player_2 raise')
        pot += 2
        stacks[1] -= 2
    else:
        pot += 1
        stacks[1] -= 1

flop_cards = POKER_BOX[4:7]

player_1_with_flop = player_1 + flop_cards
player_2_with_flop = player_2 + flop_cards

print(player_1_with_flop)
print(player_2_with_flop)



cards =  ['5D','6H','7H','8H','9H']
print(cards)
num = Hand(cards).get_score()
print('score is {}'.format(num))
