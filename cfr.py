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


RANKS = [str(i) for i in range(6, 11)] + ['J', 'Q', 'K', 'A']
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
player_1_raise = False
player_2_raise = False


#while(stacks[0] > 0 and stacks[1] > 0):

random.seed()
random.shuffle(POKER_BOX)

def decision_at_flop_player_1(p2_raise):
    if not p2_raise:
        return 'r'
    else:
        return 'f'

def decision_of_opponent_at_flop(p1_raise):

    return 'r'

def decision_at_turn_player_1(p2_raise):
    if not p2_raise:
        return 'r'
    else:
        return 'f'

def decision_of_opponent_at_turn(p1_raise):

    return 'r'

def decision_at_river_player_1(p2_raise):
    if not p2_raise:
        return 'r'
    else:
        return 'f'

def decision_of_opponent_at_river(p1_raise):

    return 'r'

def best_hand(cards):
            # not efficient but for the sake of readability...
            all_hands = list(itertools.permutations(cards , 5))
            # all_hands = itertools.permutations(cards + self.shared_cards, 5)
            scores = [Hand(hand).get_score() for hand in all_hands]
            return max(scores),Hand(all_hands[scores.index(max(scores))])


stacks[button] -= 2

stacks[(button+1)%2] -= 4
pot += 6


# deal first 2 cards to players ***
player_1 = POKER_BOX[:2]
player_2 = POKER_BOX[2:4]
# player_1 = ['1S','AD']
# player_2 = ['AS','7D']

player_1_two_card = player_1[0][0] + player_1[1][0]
player_2_two_card = player_2[0][0] + player_2[1][0]

# print(player_1)
# print(player_2)
# print(player_1_two_card)
# print(player_2_two_card)


if button_names[button] == 'player_1':
    if player_1_two_card in pre_flop_odds:
        print('player_1 raise')
        pot += 4
        stacks[0] -= 4
    else:
        pot += 2
        stacks[0] -= 2

if button_names[button] == 'player_2':
    if player_2_two_card in pre_flop_odds:
        print('player_2 raise')
        pot += 4
        stacks[1] -= 4
    else:
        pot += 2
        stacks[1] -= 2

if button_names[(button+1)%2] == 'player_1':
    if player_1_two_card in pre_flop_odds:
        print('player_1 raise')
        pot += 4
        stacks[0] -= 4
    else:
        pot += 2
        stacks[0] -= 2

if button_names[(button+1)%2] == 'player_2':
    if player_2_two_card in pre_flop_odds:
        print('player_2 raise')
        pot += 4
        stacks[1] -= 4
    else:
        pot += 2
        stacks[1] -= 2

flop_cards = POKER_BOX[4:7]
# flop cards on table ***
player_1_with_flop = player_1 + flop_cards
player_2_with_flop = player_2 + flop_cards

print(player_1_with_flop)
# print(player_2_with_flop)

cards =  player_1_with_flop

num = Hand(cards).get_score()
print('score is {}'.format(num))

if button_names[button] == 'player_1':
    if decision_at_flop_player_1(player_2_raise) == 'r':
        print('player_1 raise at flop')
        pot += 4
        stacks[0] -= 4
        player_1_raise = True
    elif decision_at_flop_player_1(player_2_raise) == 'c':
        print('player_1 calls')
        player_1_raise = False

    if decision_of_opponent_at_flop(player_1_raise) == 'c':
        print('player_2 calls')
        if player_1_raise:
            pot += 4
            stacks[1] -= 4

    elif decision_of_opponent_at_flop(player_1_raise) == 'r':
        print('player_2 raise at flop')
        if player_1_raise:
            pot += 8
            stacks[1] -= 8
        else:
            pot += 4
            stacks[1] -= 4
            player_2_raise = True

    if player_2_raise:
        if decision_at_flop_player_1(player_2_raise) == 'c':
            pot += 4
            stacks[0] -= 4

        elif decision_at_flop_player_1(player_2_raise) == 'f':
            print('player_1 folds')
            stacks[1] += pot
            print('player_2 wins ${}'.format(pot))

else:
    if decision_of_opponent_at_flop(player_1_raise) == 'r':
        print('player_2 raise at flop')
        pot += 4
        stacks[1] -= 4
        player_2_raise = True
    elif decision_of_opponent_at_flop(player_1_raise) == 'c':
        print('player_2 calls')
        player_2_raise = False

    if decision_at_flop_player_1(player_2_raise) == 'c':
        print('player_1 calls')
        if player_2_raise:
            pot += 4
            stacks[0] -= 4
    elif decision_at_flop_player_1(player_2_raise) == 'r':
        print('player_1 raise at flop')
        if player_2_raise:
            pot += 8
            stacks[0] -= 8
        else:
            pot += 4
            stacks[0] -= 4
        player_1_raise = True

    if player_1_raise:
        if decision_of_opponent_at_flop(player_1_raise) == 'c':
            pot += 4
            stacks[1] -= 4
        elif decision_of_opponent_at_flop(player_1_raise) == 'f':
            print('player_2 folds')
            stacks[0] += pot
            print('player_1 wins ${}'.format(pot))

# Turn cards on table ***
player_1_raise = False
player_2_raise = False
turn_cards = POKER_BOX[7:8]
print(flop_cards)
print(turn_cards)

player_1_cards_at_turn = player_1_with_flop + turn_cards
player_2_cards_at_turn = player_2_with_flop + turn_cards

print('player 1\'s cards at turn {}'.format(player_1_cards_at_turn))
print('player 2\'s cards at turn {}'.format(player_2_cards_at_turn))

# num = best_hand(player_1_cards_at_river)
# print('player_1 has {}'.format(num[0][1]))
# num2 = best_hand(player_2_cards_at_river)
# print('player_2 has {}'.format(num2[0][1]))

        # betting at the river ***

if button_names[button] == 'player_1':
    if decision_at_turn_player_1(player_2_raise) == 'r':
        print('player_1 raise at turn')
        pot += 4
        stacks[0] -= 4
        player_1_raise = True
    elif decision_at_turn_player_1(player_2_raise) == 'c':
        print('player_1 calls at turn')
        player_1_raise = False

    if decision_of_opponent_at_turn(player_1_raise) == 'c':
        print('player_2 calls at turn')
        if player_1_raise:
            pot += 4
            stacks[1] -= 4
    elif decision_of_opponent_at_turn(player_1_raise) == 'r':
        print('player_2 raise at turn')
        if player_1_raise:
            pot += 8
            stacks[1] -= 8
        else:
            pot += 4
            stacks[1] -= 4
        player_2_raise = True

    if player_2_raise:
        if decision_at_turn_player_1(player_2_raise) == 'c':
            pot += 4
            stacks[0] -= 4
        elif decision_at_turn_player_1(player_2_raise) == 'f':
            print('player_1 folds')
            stacks[1] += pot
            print('player_2 wins ${}'.format(pot))

else:
    if decision_of_opponent_at_turn(player_1_raise) == 'r':
        print('player_2 raise at turn')
        pot += 4
        stacks[1] -= 4
        player_2_raise = True
    elif decision_of_opponent_at_turn(player_1_raise) == 'c':
        print('player_2 calls at turn')
        player_2_raise = False

    if decision_at_turn_player_1(player_2_raise) == 'c':
        print('player_1 calls at turn')
        if player_2_raise:
            pot += 4
            stacks[0] -= 4
    elif decision_at_turn_player_1(player_2_raise) == 'r':
        print('player_1 raise at turn')
        if player_2_raise:
            pot += 8
            stacks[0] -= 8
        player_1_raise = True

    if player_1_raise:
        if decision_of_opponent_at_turn(player_1_raise) == 'c':
            pot += 4
            stacks[1] -= 4
        elif decision_of_opponent_at_turn(player_1_raise) == 'f':
            print('player_2 folds')
            stacks[0] += pot
            print('player_1 wins ${}'.format(pot))

player_1_raise = False
player_2_raise = False

river_cards = POKER_BOX[8:9]
print(flop_cards)
print(turn_cards)
print(river_cards)

player_1_cards_at_river = player_1_cards_at_turn + river_cards
player_2_cards_at_river = player_2_cards_at_turn + river_cards
print(player_1_cards_at_river)
print(player_2_cards_at_river)

            # betting at the river ***

if button_names[button] == 'player_1':
    if decision_at_river_player_1(player_2_raise) == 'r':
        print('player_1 raise at river')
        pot += 4
        stacks[0] -= 4
        player_1_raise = True
    elif decision_at_river_player_1(player_2_raise) == 'c':
        print('player_1 calls at river')
        player_1_raise = False

    if decision_of_opponent_at_river(player_1_raise) == 'c':
        print('player_2 calls at river')
        if player_1_raise:
            pot += 4
            stacks[1] -= 4
    elif decision_of_opponent_at_river(player_1_raise) == 'r':
        print('player_2 raise at river')
        if player_1_raise:
            pot += 8
            stacks[1] -= 8
        else:
            pot += 4
            stacks[1] -= 4
        player_2_raise = True

    if player_2_raise:
        if decision_at_river_player_1(player_2_raise) == 'c':
            pot += 4
            stacks[0] -= 4
        elif decision_at_river_player_1(player_2_raise) == 'f':
            print('player_1 folds')
            stacks[1] += pot
            print('player_2 wins ${}'.format(pot))

else:
    if decision_of_opponent_at_river(player_1_raise) == 'r':
        print('player_2 raise at river')
        pot += 4
        stacks[1] -= 4
        player_2_raise = True
    elif decision_of_opponent_at_river(player_1_raise) == 'c':
        print('player_2 calls at river')
        player_2_raise = False

    if decision_at_river_player_1(player_2_raise) == 'c':
        print('player_1 calls at river')
        if player_2_raise:
            pot += 4
            stacks[0] -= 4

    elif decision_at_river_player_1(player_2_raise) == 'r':
        print('player_1 raise at river')
        if player_2_raise:
            pot += 8
            stacks[0] -= 8
        else:
            pot += 4
            stacks[0] -= 4
        player_1_raise = True

    if player_1_raise:
        if decision_of_opponent_at_river(player_1_raise) == 'c':
            pot += 4
            stacks[1] -= 4
        elif decision_of_opponent_at_river(player_1_raise) == 'f':
            print('player_2 folds')
            stacks[0] += pot
            print('player_1 wins ${}'.format(pot))
