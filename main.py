from player import Player
from ruler import Ruler
from card import Card
import sys, utils

# Initialize the game.
# 1. Input the number of players.
print('Welcome! This is the Dalmuti game.')
print('Input how many people will do the game(4 ~ 8).')
N = int(input('The total player number is... : ')) # string exception should be made.
while N<4 or 8<N:
    print('Please input between 4 and 8.')
    N = int(input('The player number is... : '))

H = int(input('The human player number is... : '))
while H>N or H<1:
    print('Please input right number. It should be larger than 1 and less or equal than total number.')
    H = int(input('The human player number is... : '))

# 2. Create the ruler.
GameRuler = Ruler(N, H)

# 3. Create Players & Create Cards and give it to each players.
GameRuler.init_game()

# <debug. check what card is given to whom. (cheat!!)>
utils.check_card_separation(GameRuler.player_list)

# <debug. check whether submit works well>
# utils.check_submit(GameRuler, 0)

# 4. Game start.
print('Game start!')
while not GameRuler.game_done:
    utils.shut_down_computers(GameRuler.player_list)

    GameRuler.next_play()
    anyone_fin = GameRuler.are_you_done(GameRuler.now_player)
    if GameRuler.now_player.limit_level == 1: GameRuler.now_player.limit_level = 2

    total_in_action = len(GameRuler.possible_player)
    if total_in_action == 1: # if all players except one have limit level 3.
        GameRuler.next_cycle()
        utils.check_state_level(GameRuler.player_list)
        continue

    if GameRuler.turn + 1 < total_in_action: GameRuler.turn += 1
    else: GameRuler.turn = 0

    if GameRuler.now_player.limit_level == 3:
        if GameRuler.turn != 0:
            GameRuler.turn -= 1

    if len(GameRuler.player_list) == 1:
        GameRuler.game_done = True

    GameRuler.is_first_turn = False
    utils.check_state_level(GameRuler.player_list)

