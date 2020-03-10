import utils, os, random, time

class Player:
    def __init__(self, name, human, speed):
        self.name = name
        self.human = human
        self.card_list = []
        self.card_ref = []
        self.submission_history = []
        self.submitted_card = []
        # 1 can submit any combination of cards. 2 should follow the rule. 3 cannot submit any cards.
        self.limit_level = 2
        self.revolution_probability = 0.5
        self.sudo_thinking_time = speed

    def do_I_want_revolution(self):
        if self.human:
            ans = input('You can make REVOLUTION!!!. Will you? (y/n) : ').lower()
            while ans not in ['y','n','yes','no']:
                ans = input('Wrong input. You can make REVOLUTION!!!. Will you? (y/n) : ').lower()
            if ans in ['y','n','yes','no']:
                return True
            return False

        else:
            if self.revolution_probability > random.uniform(0.0, 1.0):
                print(self.name+' decides to make the revolution!!.')
                return True
            return False

    def submit_card(self, input_card, recent_card):

        #print('input: '+input_card)

        if input_card == 'die' or input_card == 'Die' or input_card == 'pass' or  input_card == '-1' :
            self.limit_level = 3
            return True

        # make reference list of card numbers
        if not self.card_ref:
            for c in self.card_list:
                self.card_ref.append(str(c.number))

        # split input string and sorting.
        for char in input_card.strip().split(' '):
            if char not in [str(x+1) for x in range(13)]:
                print('Wrong submit. Please input only integer value between 1 and 13.')
                return False
        card_num = list(map(int, input_card.strip().split(' '))) # first change to int for sorting.
        card_num = sorted(card_num) # after sorting,
        card_num = list(map(str, card_num)) # change to string list.

        # get value of recent cards
        if recent_card:
            recent_value = [card.value for card in recent_card]
            recent_value = sorted(recent_value)

        # input check using 'card_num'.
        temp_card = card_num[0]
        for card in card_num:
        # 1) Is the input number exist in player's card list.
        #   - number (Is '9' in card list?)
        #   - count (Are three '9's in card list?)
        #   * Of course, this can be made just counting the cards.
        #   * But, I separate them to alert different messages.
            if card not in self.card_ref:
                print('Wrong submit. Submitted card does not exist in your set.')
                return False
            else:
                if card != '13':
                    if card_num.count(card) > self.card_ref.count(card):
                        print('Wrong submit. Submitted card are too much than you have.')
                        return False

        # 2) Are the input numbers the same. (Except '13'. It can be used with any other numbers.)
            if card != temp_card:
                if card == '13' or temp_card == '13':
                    continue
                else:
                    print('Wrong submit. You can submit only one kind of number.')
                    return False

            temp_card = card

        # change input cards num into card classes
        input_cards = []
        for card in card_num:
            input_card_index = self.card_ref.index(card)
            input_card = self.card_list[input_card_index]
            if input_card.number == '13':
                if input_cards:
                    input_card.value = input_cards[0].value

            input_cards.append(input_card)

        # check limitation.
        if recent_card != None: # always limit_level = 2.
            #print('recent: '+str(recent_value[0]+' input: '+str(input_cards[0].value)))
            # number check.
            if len(recent_value) != len(input_cards):
                print('Wrong submit. You should submit the same number of cards to previous submission.')
                return False
            # value check.
            if int(recent_value[0]) <= int(input_cards[0].value):
                print('Wrong submit. You should submit the less value cards than previous submission.')
                return False

        # real submission.
        submit = []
        for input_card in input_cards:
            submit.append(input_card)
            card_index_in_card_list = self.card_ref.index(input_card.number)
            self.submission_history.append(self.card_list.pop(card_index_in_card_list))
            self.card_ref.remove(input_card.number)
        self.submitted_card = submit
        #temp_message = sorted([x.number for x in self.submitted_card])
        return True

    def do_game(self, recent_card): # for real player.
        print('Player '+self.name +"'s turn.")
        if recent_card:
            print('Recent submit : '+' '.join([card.number for card in recent_card])+'.')
        # print cards that now player has.
        utils.check_card_separation([self])
        player_input = input("Select your cards : ")
        is_submit = self.submit_card(player_input, recent_card)
        while not is_submit:
            utils.check_card_separation([self])
            player_input = input("Select your cards : ")
            is_submit = self.submit_card(player_input, recent_card)

        print('\n')

    def auto_game(self,recent_card): # for computers.
        print(self.name + "'s turn.")
        # how to?
        # 1. get possible card set list to submit.
        # 2. Among possible set, choose...
        #   - random one (level 1, easy)
        #   - the first one (level 2, normal)
        #   - calculate probability (level 3, little bit hard)
        if recent_card:
            print('Recent submit : '+' '.join([card.number for card in recent_card])+'.')
        #utils.check_card_separation([self])

        # Thinking time
        time.sleep(self.sudo_thinking_time)
        computer_input = self.computer_method(recent_card)
        is_submit = self.submit_card(computer_input, recent_card)
        while not is_submit:
            computer_input = self.computer_method(recent_card)
            is_submit = self.submit_card(computer_input, recent_card)

        if self.limit_level != 3:
            print(self.name+' submits '+computer_input+'.')
        elif self.limit_level == 3:
            print(self.name + ' pass!')
        print('\n')

    def computer_method(self, recent_card, level = 1):
        if recent_card:
            submit_count = len(recent_card)
            submit_value = int(recent_card[0].value)
        else:
            submit_count = None
            submit_value = 99999

        Jocker = 0
        temp = []
        for card in self.card_list:
            if int(card.number) == 13: Jocker += 1
            if int(card.value) < submit_value: temp.append(card.number)

        unique_temp = list(set(temp))
        possible_set = []
        for value in unique_temp:
            if submit_count:
                if temp.count(value) >= submit_count:
                    possible_set.append([value]*submit_count)
                elif temp.count(value) + Jocker >= submit_count:
                    if unique_temp == ['13']: # if player can submit only Jockers (in case of revolution)
                        continue
                    for j in range(Jocker):
                        possible_set.append([value]*(submit_count-j-1)+[13]*(j+1))
            else:
                possible_set = possible_set + utils.make_combinations([value]*temp.count(value))

        if not possible_set:
            return 'die'

        if level == 1:
            submit = random.choice(possible_set)
            submit = list(map(str,submit))
            return ' '.join(submit)
        return 'die'




