import time
import sys
list = ['start']
game = ['game-start']
my_5_card_hand = []
round = set()
myset = set()
flop_flag = True
turn_flag = True
river_flag = True


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
    idx_1 = cards.find('R')
    idx_2 = cards.find('R',idx_1+1)
    river_cd = cards[idx_1+1:idx_2]
    my_5_card_hand.append(card_numbers[int(river_cd)])
    return False

def get_turn_card(cards):
    idx_1 = cards.find('T')
    idx_2 = cards.find('T',idx_1+1)
    turn_cd = cards[idx_1+1:idx_2]
    my_5_card_hand.append(card_numbers[int(turn_cd)])
    return False

def get_flop_cards(flop):
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
    hand_decision = open('../pokercasino/botfiles/botToCasino0','wt')
    print('r',file=hand_decision)
    return False

def first_round(my_hand):
    index_1 = my_hand.find('A')
    index_2 = my_hand.find('B')
    first_card = my_hand[index_1+1:index_2]
    second_card = my_hand[index_2+1:]
    my_5_card_hand.append(card_numbers[int(first_card)])
    my_5_card_hand.append(card_numbers[int(second_card)])

    hand_decision = open('../pokercasino/botfiles/botToCasino0','wt')
    print('c',file=hand_decision)

def get_round_num(casinoInfo):
    idx = casinoInfo.find('D')
    round_num = casinoInfo[0:idx]

    if round_num not in round:
        #my_5_card_hand.clear()
        myset.clear()
        round.add(round_num)
        return [True, True, True]
    return [False,False,False]


try:
    while True:

        infile = open('../pokercasino/botfiles/casinoToBot0','rt')
        first_two_cards = open('../pokercasino/botfiles/cardToBot0','rt')
        outfile = open('home.txt','wt')

        for line in infile:
            casinoInfo = str(line.rstrip())
            flop_flag,turn_flag,river_flag = get_round_num(casinoInfo)
            if list[len(list)-1] != casinoInfo:

                print(casinoInfo, file=outfile)
                list.append(casinoInfo)
                myset = set(casinoInfo)

                if 'F' in myset and flop_flag:
                    flop_flag = get_flop_cards(casinoInfo)
                if 'T' in myset and turn_flag:
                    turn_flag = get_turn_card(casinoInfo)
                if 'R' in myset and river_flag:
                    river_flag = get_river_card(casinoInfo)


        outfile.close()

        for liner in first_two_cards:
            if game[len(game)-1] != str(liner.rstrip()):
                game.append(liner.rstrip())
                first_round(str(liner.rstrip()))

        time.sleep(0.05)

except KeyboardInterrupt:
    print('Quitting the program.')
except:
    print('Unexpected error: '+sys.exc_info()[0])

for n in my_5_card_hand:
    print(n)
