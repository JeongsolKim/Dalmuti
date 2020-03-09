import itertools

def check_card_separation(player_list):
    for p in player_list:
        temp = []
        for c in p.card_list:
            temp.append(int(c.number))
        temp = sorted(temp)
        temp = list(map(str,temp))
        print('Cards of '+p.name+' are :')
        print(' '.join(temp))

def check_state_level(player_list):
    statement = ''
    for p in player_list:
        statement = statement + str(p.name)+'_'+str(p.limit_level)+'_'+str(len(p.card_list))+', '
    print('State of players (name_limit level_card num): ')
    print(statement)

def check_submit(ruler, player_num):
    print('\n')
    print('Submission Test.')
    player = ruler.player_list[player_num]
    print('Selected player number : '+str(player_num))
    print('Player list before submit test :')
    print(ruler.player_list)
    print('Card list of the selected player before submit test :')
    print(player.card_list)
    print('\n')
    for i in range(3):
        test = input('Test input: ')
        player.submit_card(test, None)
    print('Result of function "are tou end?" :')
    print(ruler.are_you_end(player))
    print('Player list after submit test :')
    print(ruler.player_list)
    print('Card list of the selected player after submit test :')
    print(player.card_list)
    print('Submitted card :')
    print(player.submission_history)

def shut_down_computers(player_list):
    for p in player_list:
        if not p.human:
            p.limit_level = 3

def make_combinations(target_list):
    output = []
    for i in range(len(target_list)):
        output = output + list(map(list,(set(itertools.combinations(target_list, i+1)))))
    return output


