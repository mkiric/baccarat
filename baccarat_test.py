from __future__ import division
import random
import sys, getopt
from math import *

global game_type
game_type="standard"
global TIE
TIE= 0
global PLAYER_WIN
PLAYER_WIN = 1
global BANKER_WIN
BANKER_WIN = 2
global PANDA
PANDA = 3
global DRAGON
DRAGON = 4
no_games = 1000000

def usage():
	print "Usage: python baccarat_test.py [-t|--type EZ|standard (default)] [-g|--games <# games> (1M default)]. "


#opts = getopt.getopt(sys.argv[1:], "t:", ["type="])
try:
	opts, args = getopt.getopt(sys.argv[1:], "g:t:", ["type=", "games="])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)

for o, a in opts:
	if o in ("-t", "--type"):
		if (a.lower() == "ez" or a.lower() == "standard"):
			game_type = a.lower()
			print "Playing " + a + " style baccarat"
		else:
			print "Unrecognized game type. Only 'EZ' and 'standard' are supported"
	elif o in ("-g", "--games"):
		no_games = int(a)
	else:
		assert False, "unhandled option"

def check_winner(player_sum, banker_sum, player_cards, banker_cards):
	
		if (player_sum > banker_sum):
			if (game_type == "ez" and player_cards == 3 and player_sum == 8):
				return PANDA
			return PLAYER_WIN
		elif (banker_sum > player_sum):
			if (game_type == "ez" and banker_cards == 3 and banker_sum == 7):
				return DRAGON
			return BANKER_WIN
		else:
			return TIE

def play_shoe():
	suit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
	deck = suit + suit + suit + suit
	bdeck = deck + deck + deck + deck + deck + deck
	random.shuffle(bdeck)
	random.shuffle(bdeck)
	player_win_count = 0
	banker_win_count = 0
	tie_count = 0
	panda_count = 0
	dragon_count = 0

	#shuffled and ready to go
	#discard the first bdeck[0] number of cards
	card_limit = 24
	bdeck = bdeck[bdeck[0]+1:]
	while len(bdeck) > card_limit:
		player = bdeck[0:1]
		banker = bdeck[2:3]
		idx = 4
		player_sum = sum(player) % 10;
		banker_sum = sum(banker) % 10;
		banker_cards = 2
		player_cards = 2
		#If either the player or the bank have a total of 8 or 9 on the first two cards no further cards are drawn
		#(iow, skip to checking winner)
		if (player_sum < 8 and banker_sum < 8):
			if player_sum <= 5:
				#player draws a third card
				player_cards += 1
				player_third_card = bdeck[idx]
				player_sum = (player_sum + player_third_card) % 10
			
				idx += 1
				#If the player does take a third card then the Bank's third-card-rule below will determine if the bank takes a third card.
				#If the bank's total is 2 or less then bank draws a card, regardless of what the players third card is.
				#If the banks total is 3 then the bank draws a third card unless the players third card was an 8.
				#If the banks total is 4 then the bank draws a third card unless the players third card was a 0, 1, 8, or 9.
				#If the banks total is 5 then the bank draws a third card if the players third card was 4, 5, 6, or 7.
				#If the banks total is 6 then the bank draws a third card if the players third card was a 6 or 7.
				#If the banks total is 7 then the bank stands.
				if banker_sum <= 2:
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
				elif banker_sum == 3 and not player_third_card == 8:
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
				elif banker_sum == 4 and not (player_third_card == 0 or player_third_card == 1 or player_third_card == 8 or player_third_card == 9):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
				elif banker_sum == 5 and (player_third_card == 4 or player_third_card == 5 or player_third_card == 6 or player_third_card == 7):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
				elif banker_sum == 6 and (player_third_card == 6 or player_third_card == 7):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
			else:
				#player does not draw a third card
				if banker_sum < 6:
					#bank takes a third card
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
					banker_cards += 1
				#else:
					#bank does not take a third card, done
		winner = check_winner( player_sum, banker_sum, player_cards, banker_cards )
		if (winner == PLAYER_WIN or winner == PANDA):
			#player wins
			player_win_count += 1
			if (winner == PANDA):
				panda_count += 1
		elif winner == BANKER_WIN:
			banker_win_count += 1
		elif winner == DRAGON:
			dragon_count += 1
			#there might be a nuance here I'm missing...
			#betting on banker will tie, but betting on player will lose
			#however, the the tie count cannot increase because tie would mean player ties too.. hmm...
		else:
			tie_count += 1
		#print 'index: ', idx
		bdeck = bdeck[idx:]

	#print 'done'
	#print "Player wins: ", player_win_count
	#print "Banker wins: ", banker_win_count
	#print "Ties: ", tie_count
	return [player_win_count, banker_win_count, tie_count, panda_count, dragon_count]



#player, banker, tie
running_total = [0, 0, 0]
running_average = [0, 0, 0]

dragon_total = 0
dragon_average = 0
panda_total = 0
panda_average = 0

for i in range(1, no_games):
	
	winner_counts = play_shoe()
	total = sum(winner_counts)

	for j in range(0,3):
		running_total[j] = running_total[j] + winner_counts[j]

	for j in range(0, 3):
		running_average[j] = (running_total[j] / sum(running_total)) * 100

	panda_total += winner_counts[3]
	dragon_total += winner_counts[4]
	panda_average = panda_total / i;
	dragon_average = dragon_total / i;
	
	sys.stdout.write("\033[F") #cursor up one line
	sys.stdout.write("\033[K") #clear current line
	print 'Progress %.2f --- Player: %.2f --- Banker %.2f --- Tie %.2f -- Pandas per game %.2f -- Dragons per game %.2f' % ((i / no_games)*100, running_average[0], running_average[1], running_average[2], panda_average, dragon_average)	
