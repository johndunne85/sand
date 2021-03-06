import time
import sys
import deepLearning
import numpy as np
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

list = ['']
game = ['']
my_5_card_hand = []
round = set()
myset = set()
flag_list = [True, True, True]

model = deepLearning.Network(10, 10, [128,128,64])
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)



torch.save(model.state_dict(), 'checkpoint.pth')

state_dict = torch.load('checkpoint.pth')

model = deepLearning.Network(10, 10, [128,128,64])
# This will throw an error because the tensor sizes are wrong!
model.load_state_dict(state_dict)

checkpoint = {'input_size': 10,
              'output_size': 10,
              'hidden_layers': [each.out_features for each in model.hidden_layers],
              'state_dict': model.state_dict()}

torch.save(checkpoint, 'checkpoint.pth')

def load_checkpoint(filepath):
    checkpoint = torch.load(filepath)
    model = deepLearning.Network(checkpoint['input_size'],
                             checkpoint['output_size'],
                             checkpoint['hidden_layers'])
    model.load_state_dict(checkpoint['state_dict'])

    return model

model = load_checkpoint('checkpoint.pth')
#print(model)

card_numbers = [
    '6h', '6c', '6s', '6d',
	'7h', '7c', '7s', '7d',
	'8h', '8c', '8s', '8d',
	'9h', '9c', '9s', '9d',
	'Th', 'Tc', 'Ts', 'Td',
	'Jh', 'Jc', 'Js', 'Jd',
	'Qh', 'Qc', 'Qs', 'Qd',
	'Kh', 'Kc', 'Ks', 'Kd',
	'Ah', 'Ac', 'As', 'Ad']

def get_river_card(cards):
    flag_list[2] = False
    idx_1 = cards.find('R')
    idx_2 = cards.find('R',idx_1+1)
    river_cd = cards[idx_1+1:idx_2]
    my_5_card_hand.append(card_numbers[int(river_cd)])

def get_turn_card(cards):
    flag_list[1] = False
    idx_1 = cards.find('T')
    idx_2 = cards.find('T',idx_1+1)
    turn_cd = cards[idx_1+1:idx_2]
    my_5_card_hand.append(card_numbers[int(turn_cd)])

def get_flop_cards(flop):
    flag_list[0] = False
    idx_1 = flop.find('F')
    idx_2 = flop.find('F',idx_1+1)
    idx_3 = flop.find('F',idx_2+1)
    idx_4 = flop.find('F',idx_3+1)
    flop_cd1 = flop[idx_1+1:idx_2]
    flop_cd2 = flop[idx_2+1:idx_3]
    flop_cd3 = flop[idx_3+1:idx_4]
    my_5_card_hand.append(card_numbers[int(flop_cd1)])
    my_5_card_hand.append(card_numbers[int(flop_cd2)])
    my_5_card_hand.append(card_numbers[int(flop_cd3)])
    x = torch.FloatTensor([[0.71,-0.48,0.03,-0.65,0.99,-0.65,-0.14,-0.65,0.03,-0.82]])
    with torch.no_grad():
        logits = model.forward(x)
    ps = F.softmax(logits, dim=1)
    if ps[0][1] > ps[0][2]:
        call = 'c'
    else:
        call = 'r'

    hand_decision = open('../pokercasino/botfiles/botToCasino0','wt')
    print(call,file=hand_decision)

def first_round(my_hand):
    index_1 = my_hand.find('A')
    index_2 = my_hand.find('B')
    first_card = my_hand[index_1+1:index_2]
    second_card = my_hand[index_2+1:]
    my_5_card_hand.append(card_numbers[int(first_card)])
    my_5_card_hand.append(card_numbers[int(second_card)])

    hand_decision = open('../pokercasino/botfiles/botToCasino0','wt')
    print('c',file=hand_decision)

def make_flop_bet(my_5_cards):
    outfile = open('home.txt','wt')
    hand = '-'.join(my_5_cards)

    print(hand,file=outfile)
    outfile.close()

def get_round_num(casinoInfo):
    idx = casinoInfo.find('D')
    round_num = casinoInfo[0:idx]

    if round_num not in round:
        my_5_card_hand.clear()
        myset.clear()
        round.add(round_num)
        flag_list[0]= True
        flag_list[1]= True
        flag_list[2]= True

try:
    while True:

        infile = open('../pokercasino/botfiles/casinoToBot0','rt')
        first_two_cards = open('../pokercasino/botfiles/cardToBot0','rt')


        for liner in first_two_cards:
            if game[len(game)-1] != str(liner.rstrip()):
                get_round_num(str(liner.rstrip()))
                game.append(liner.rstrip())
                first_round(str(liner.rstrip()))

        for line in infile:
            casinoInfo = str(line.rstrip())
            get_round_num(casinoInfo)
            if len(list[len(list)-1]) != len(casinoInfo):

                list.append(casinoInfo)
                myset = set(casinoInfo)

                if 'F' in myset and flag_list[0]:
                    flag_flop = get_flop_cards(casinoInfo)
                    make_flop_bet(my_5_card_hand)

                if 'T' in myset and flag_list[1]:
                    flag_turn = get_turn_card(casinoInfo)
                if 'R' in myset and flag_list[2]:
                    flag_river = get_river_card(casinoInfo)

except KeyboardInterrupt:
    print('Quitting the program.')
except:
    print('Unexpected error: '+sys.exc_info()[0])


for n in my_5_card_hand:
    print(n)
