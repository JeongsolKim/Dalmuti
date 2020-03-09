from ruler import Ruler
import utils

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
# utils.check_card_separation(GameRuler.player_list)

# <debug. check whether submit works well>
# utils.check_submit(GameRuler, 0)

# 4. Game start.
print('Game start!')
while not GameRuler.game_done:
    #utils.shut_down_computers(GameRuler.player_list)

    GameRuler.next_play()
    if GameRuler.now_player.limit_level == 1: GameRuler.now_player.limit_level = 2

    # If all players except one have limit level 3.
    # or, if no one left in possible_player list.
    if len(GameRuler.possible_player) <= 1:
        GameRuler.next_cycle()
        # debug
        # utils.check_state_level(GameRuler.player_list)
        continue

    if len(GameRuler.player_list) == 1:
        GameRuler.game_done = True

    # debug
    # utils.check_state_level(GameRuler.player_list)

print("Game Done!!")
print("Total cycle: "+str(GameRuler.cycle_num))
for winner_num in range(len(GameRuler.winner)):
    if winner_num == 0:
        print('1st winner: ' + GameRuler.winner[winner_num])
    elif winner_num == 1:
        print('2nd winner: ' + GameRuler.winner[winner_num])
    elif winner_num == 2:
        print('3rd winner: ' + GameRuler.winner[winner_num])
    else:
        print(str(winner_num+1)+'th winner: ' + GameRuler.winner[winner_num])

