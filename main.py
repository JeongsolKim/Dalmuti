from ruler import Ruler
import utils, os, time

# Initialize the game.
# 1. Input the number of players.
print('Welcome! This is the Dalmuti game.')
while True:
    G = input('How many game cycles do you want to play? ')
    if not G.isdigit():
        print("Input must be numeric.")
    else:
        if int(G) <= 0:
            print('Please input at least one.')
        else:
            break

print('Input how many people will do the game(4 ~ 8).')
while True:
    N = input('The player number is... : ')
    if N not in ['4','5','6','7','8']:
        print('Please input between 4 and 8.')
    else:
        N = int(N)
        break
'''
while True:
    H = input('The human player number is... : ')
    if H not in [str(x+1) for x in range(N)]:
        print('Please input right number. It should be larger than 1 and less or equal than total number.')
    else:
        H = int(H)
        break
'''
# For test,
H = int(input('test. input 0:  '))

# 2. Create the ruler.
GameRuler = Ruler(N, H, speed = 10)

# 3. Create Players & Create Cards and give it to each players.
GameRuler.init_game()

# <debug. check what card is given to whom. (cheat!!)>
# utils.check_card_separation(GameRuler.player_list)

# <debug. check whether submit works well>
# utils.check_submit(GameRuler, 0)

# 4. Game start.
time.sleep(1)
print('Game start!\n')

for Game_cycle in range(int(G)):
    print('Game cycle ['+str(Game_cycle+1)+'/'+G+'].\n')
    # 5. check revolution
    revolution = GameRuler.revolution_check()
    if revolution:
        GameRuler.revolution()

    while not GameRuler.game_done:
        #utils.shut_down_computers(GameRuler.player_list)
        GameRuler.next_play()
        if GameRuler.now_player.limit_level == 1: GameRuler.now_player.limit_level = 2

        # If all players except one have limit level 3.
        # or, if no one left in possible_player list.
        if len(GameRuler.possible_player) <= 1:
            if len(GameRuler.player_list) <= 1:
                GameRuler.game_done = True
            GameRuler.next_cycle()
            # debug
            # utils.check_state_level(GameRuler.player_list)
            continue

        #if len(GameRuler.player_list) == 1:
        #    GameRuler.game_done = True

        # debug
        # utils.check_state_level(GameRuler.player_list)

    print("One Game Done!!")

    # add left player :<.
    if GameRuler.player_list:
        GameRuler.winner.append(GameRuler.player_list[0].name)

    print("Cycle in this game : "+str(GameRuler.cycle_num))
    for winner_num in range(len(GameRuler.winner)):
        if winner_num == 0:
            print('1st winner : ' + GameRuler.winner[winner_num])
        elif winner_num == 1:
            print('2nd winner : ' + GameRuler.winner[winner_num])
        elif winner_num == 2:
            print('3rd winner : ' + GameRuler.winner[winner_num])
        else:
            print(str(winner_num+1)+'th winner: ' + GameRuler.winner[winner_num])

    if Game_cycle + 1 == int(G):
        break

    # ask continue the game?
    next_game = True

    '''
    while True:
        conti = input('Will you continue next game? (y/n) : ')
        if conti.lower() in ['y', 'yes']:
            print('\n')
            conti = True
            break
        elif conti.lower() in ['n', 'no']:
            conti = False
            break
    '''
    # for testm
    conti = True
    if not (next_game and conti): break
    else: GameRuler.prepare_next_game()

print('Thank you for playing.')