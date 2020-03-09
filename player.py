import utils

class Player:
    def __init__(self, name, human=False):
        self.name = name
        self.human = human
        self.card_list = []
        self.card_ref = []
        self.submission_history = []
        self.submitted_card = []
        # 1 can submit any combination of cards. 2 should follow the rule. 3 cannot submit any cards.
        self.limit_level = 2

    def submit_card(self, input_card, recent_card):
        if input_card == 'die' or input_card == 'Die' or input_card == 'pass' or  input_card == '-1' :
            self.limit_level = 3
            return True

        # make reference list of card numbers
        if not self.card_ref:
            for c in self.card_list:
                self.card_ref.append(str(c.number))
        print(self.card_ref)

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
            if input_card.number == '13': # actually, this does not have to use if.
                input_card.value = card_num[0]

            input_cards.append(input_card)

        # check limitation.
        if recent_card != None: # always limit_level = 2.
            # number check.
            if len(recent_value) != len(input_cards):
                print('Wrong submit. You should submit the same number of cards to previous submission.')
                return False
            # value check.
            if int(recent_value[0])<=int(input_cards[0].value):
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
        return True

    def do_game(self, recent_card): # for real player.
        print('Player '+self.name +"'s turn.")
        utils.check_card_separation([self])
        player_input = input("Select your cards : ")
        is_submit = self.submit_card(player_input, recent_card)
        while not is_submit:
            utils.check_card_separation([self])
            player_input = input("Select your cards : ")
            is_submit = self.submit_card(player_input, recent_card)

    def auto_game(self,recent_card): # for computers.
        print(self.name + "'s turn.")