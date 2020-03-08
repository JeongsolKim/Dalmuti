from card import Card
from player import Player
import random

class Ruler:
    def __init__(self,N,H):
        self.game_done = False
        self.is_first_turn = True
        self.turn = 0
        self.cycle_num = 0
        self.winner = []
        self.total_player_num = N
        self.human_player_num = H
        self.player_list = [] # list of players who play the game.
        self.rest_list = [] # who pass own turn because they do not have possible submission card.
        self.init_card_set = []
        self.recent_card = None

    def init_game(self):
        self.create_players()
        self.make_card_set()
        self.give_card_set()

    def create_players(self):
        for computer in range(self.total_player_num-self.human_player_num):
            self.player_list.append(Player('computer'+str(computer+1)))
        for human in range(self.human_player_num):
            name = input('Please enter the name of player '+str(human+1)+' : ')
            self.player_list.append(Player(name, True))

        # shuffle it.
        random.shuffle(self.player_list)
        print('All players are created.')

    def make_card_set(self):
        for i in range(12):
            for j in range(i+1):
                self.init_card_set.append(Card(i+1,i+1))

        # two Js.
        self.init_card_set.append(Card(13,13))
        self.init_card_set.append(Card(13,13))

        # shuffle it.
        random.shuffle(self.init_card_set)

    def give_card_set(self):
        for i in range(80):
            code = (i+1)%self.total_player_num
            self.player_list[code].card_list.append(self.init_card_set[i])

        print('All cards are given.')

    # Functions for the game.
    def are_you_done(self, player):
        if len(player.card_list) == 0:
            self.winner.append(player.name)
            self.player_list.remove(player)
            return True
        return False

    def next_play(self):
        # initial possible players
        self.possible_player = [player for player in self.player_list if player.limit_level != 3]
        self.now_player = self.possible_player[self.turn]

        if self.recent_card == None:
            self.now_player.limit_level = 1

        if self.now_player.limit_level != 3:  # this person already die.
            if self.now_player.human:
                self.now_player.do_game(self.recent_card)
            else:
                self.now_player.auto_game(self.recent_card)
            self.recent_card = self.now_player.submitted_card

        # update possible players
        self.possible_player = [player for player in self.player_list if player.limit_level != 3]

    def next_cycle(self):
        self.recent_card = None
        self.cycle_num += 1
        self.is_first_turn = True
        for player in self.player_list:
            if player.limit_level == 2:
                self.turn = self.player_list.index(player)
            else: player.limit_level = 2


