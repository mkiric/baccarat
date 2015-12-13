from __future__ import division
import random
import sys
from math import *

def check_winner(player_sum, banker_sum):
	
		if (player_sum > banker_sum):
			return 1
		elif (banker_sum > player_sum):
			return 2
		else:
			return 0

def play_shoe():
	suit = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
	deck = suit + suit + suit + suit
	bdeck = deck + deck + deck + deck + deck + deck
	random.shuffle(bdeck)
	player_win_count = 0
	banker_win_count = 0
	tie_count = 0

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
		#If either the player or the bank have a total of 8 or 9 on the first two cards no further cards are drawn
		#(iow, skip to checking winner)
		if (player_sum < 8 and banker_sum < 8):
			if player_sum <= 5:
				#player draws a third card
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
				elif banker_sum == 3 and not player_third_card == 8:
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
				elif banker_sum == 4 and not (player_third_card == 0 or player_third_card == 1 or player_third_card == 8 or player_third_card == 9):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
				elif banker_sum == 5 and (player_third_card == 4 or player_third_card == 5 or player_third_card == 6 or player_third_card == 7):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
				elif banker_sum == 6 and (player_third_card == 6 or player_third_card == 7):
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
			else:
				#player does not draw a third card
				if banker_sum < 6:
					#bank takes a third card
					banker_sum = (banker_sum + bdeck[idx]) % 10
					idx += 1
				#else:
					#bank does not take a third card, done
		winner = check_winner( player_sum, banker_sum )
		if winner == 1:
			#player wins
			player_win_count += 1
		elif winner == 2:
			banker_win_count += 1
		else:
			tie_count += 1
		#print 'index: ', idx
		bdeck = bdeck[idx:]

	#print 'done'
	#print "Player wins: ", player_win_count
	#print "Banker wins: ", banker_win_count
	#print "Ties: ", tie_count
	return [player_win_count, banker_win_count, tie_count]


no_games = 1000000

#player, banker, tie
running_total = [0, 0, 0]
running_average = [0, 0, 0]

for i in range(1, no_games):
	
	winner_counts = play_shoe()
	total = sum(winner_counts)

	for j in range(0,3):
		running_total[j] = running_total[j] + winner_counts[j]

	#print 'Player: ', (player_win_count / total) * 100, '%'
	#print 'Banker: ', (banker_win_count / total) * 100, '%'
	#print 'Tie: ', (tie_count / total) * 100, '%'
	for j in range(0, 3):
		running_average[j] = (running_total[j] / sum(running_total)) * 100
	
	sys.stdout.write("\033[F") #cursor up one line
	sys.stdout.write("\033[K") #clear current line
	print 'Player: %.2f  --- Banker %.2f --- Tie %.2f' % (running_average[0], running_average[1], running_average[2])	
