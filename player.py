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
        card_num = list(input_card.strip().split(' '))

        # input check.
        temp_card = card_num[0]
        for card in card_num:
            if card != temp_card:
                if card == '13' or temp_card == '13':
                    continue
                else:
                    print('Wrong submit. You can submit only the same number.')
                    return False
            temp_card = card

            if card not in self.card_ref:
                print('Wrong submit. Submitted card does not exist in your set.')
                return False

            else:
                if card != '13':
                    if card_num.count(card) > self.card_ref.count(card):
                        print('Wrong submit. Submitted card are too much than you have.')
                        return False

        # check limitation.
        if recent_card != None:
            if self.limit_level == 2:
                # number check.
                if len(recent_card) != len(card_num):
                    print('Wrong submit. You should submit the same number of cards to previous submission.')
                    return False
                # value check.
                if int(recent_card[0])<=int(card_num[0]):
                    print('Wrong submit. You should submit the less value cards than previous submission.')
                    return False

        # real submission.
        for card in card_num:
            i = self.card_ref.index(card)
            self.submission_history.append(self.card_list.pop(i))
            self.card_ref.pop(i)
        self.submitted_card = card_num
        return True

    def do_game(self, recent_card): # for real player.
        print('Player '+self.name +"'s turn.")
        player_input = input("Select your cards : ")
        is_submit = self.submit_card(player_input, recent_card)
        while not is_submit:
            player_input = input("Select your cards : ")
            is_submit = self.submit_card(player_input, recent_card)

    def auto_game(self,recent_card): # for computers.
        print(self.name + "'s turn.")