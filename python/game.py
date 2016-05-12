from deck import Deck
from deck import Card
from board import Move
from board import Board
import itertools
import logging
import time
import copy


class Game:

    def __init__(self, deck, turn_strategy='simple',
                 collapse_strategy='simple'):
        self.deck = deck
        self.board = Board()
        self.last_index = -1 #self.board.last_index
        self.turn_strategy = turn_strategy
        self.collapse_strategy = collapse_strategy
        self.board_history = []

    def play(self):
        count = 1
        card = self.deck.get_card()
        while card is not None:
            logging.debug("====Card %d : %s====" % (count, card))
            self.turn_simple(card)
            self.collapse_simple()
            logging.debug(self.board)
            self.board_history.append({'card':card,'board':copy.deepcopy(self.board)})
            count += 1
            card = self.deck.get_card()
        return len(filter(None, self.board))

    def board_to_string(self):
        return str(self.board)

    def turn_simple(self, card):
        # decide where to put this card
        # if self.last_index > -1 and (
        #     self.board[self.last_index][0].rank == card.rank or
        #     self.board[self.last_index][0].suit == card.suit
        # ):
        #     self.board.add_card(card, self.last_index)
        #     #self.board[self.last_index].insert(0, card)
        # elif self.last_index >= 2 and (
        #     self.board[self.last_index - 2][0].rank == card.rank or
        #     self.board[self.last_index - 2][0].suit == card.suit
        # ):
        #     self.board.add_card(card, self.last_index - 2)
        #     #self.board[self.last_index - 2].insert(0, card)
        # else:
            self.board.add_card(card)
            self.last_index = self.board.last_index
            # self.last_index += 1
            # self.board.append([])
            # self.board[self.last_index].insert(0, card)

    def turn_dad(self, card):
        # I used to play "next door" very time, but my current approach
        # is to skip two unless "next door" is the same value.  Not sure
        # why I follow that rule, but the results seem marginally better
        # than skipping two every time.

        # decide where to put this card
        if self.last_index > -1 and (
            self.board[self.last_index][0].rank == card.rank
        ):
            self.board[self.last_index].insert(0, card)
        elif self.last_index >= 2 and (
            self.board[self.last_index - 2][0].suit == card.suit
        ):
            self.board[self.last_index - 2].insert(0, card)
        elif self.last_index > -1 and (
            self.board[self.last_index][0].suit == card.suit
        ):
            self.board[self.last_index].insert(0, card)
        else:
            self.last_index += 1
            self.board.append([])
            self.board[self.last_index].insert(0, card)

    def collapse_simple(self):
        moved_cards = True
        logging.debug("Begin collapse")
        available_moves = self.board.get_available_moves()
        while len(available_moves)>0:
            #moved_cards = False
            logging.debug("Begin collapse pass")
            logging.debug(self.board_to_string())

            move = available_moves[-1]
            self.board.perform_move(move)
            self.last_index = self.board.last_index
            available_moves = self.board.get_available_moves()

            # for i in xrange(1, self.last_index + 1):
            #     # logging.debug(self.board[i][0])
            #     logging.debug(
            #         "Looking at pile {0}, card {1}".format(i,
            #                                                self.board[i][0].to_short_string()))
            #     if i >= 1:
            #         if (self.board[i - 1][0].rank == self.board[i][0].rank or
            #                 self.board[i - 1][0].suit == self.board[i][0].suit):
            #             logging.debug("Doing next door move of {0} up to {1}".format(
            #                 self.board[i][0].to_short_string(),
            #                 self.board[i - 1][0].to_short_string(),
            #             ))
            #             self.board[
            #                 i - 1] = self.board.pop(i) + self.board[i - 1]
            #             logging.debug("board after move:")
            #             logging.debug(self.board_to_string())
            #             self.last_index -= 1
            #             moved_cards = True
            #             break
            #
            #     if i >= 3:
            #         if (self.board[i - 3][0].rank == self.board[i][0].rank or
            #                 self.board[i - 3][0].suit == self.board[i][0].suit):
            #             logging.debug("Doing skip two move of {0} up to {1}".format(
            #                 self.board[i][0].to_short_string(),
            #                 self.board[i - 3][0].to_short_string(),
            #             ))
            #             self.board[
            #                 i - 3] = self.board.pop(i) + self.board[i - 3]
            #             logging.debug("board after move:")
            #             logging.debug(self.board_to_string())
            #             self.last_index -= 1
            #             moved_cards = True
            #             break

    def collapse_search(self):
        logging.debug("Begin collapse search")

        logging.debug("Evaluate possible starting points")
        starting_moves = []
        start_time = time.time()
        for i in xrange(1,self.last_index + 1):
            logging.debug(
                "Looking at pile {0}, card {1}".format(i,
                                                       self.board[i][0].to_short_string()))
            if i >= 1:
                if (self.board[i - 1][0].rank == self.board[i][0].rank or
                            self.board[i - 1][0].suit == self.board[i][0].suit):
                    logging.debug("Could do next door move of {0} up to {1}".format(
                        self.board[i][0].to_short_string(),
                        self.board[i - 1][0].to_short_string(),
                    ))
                    starting_moves.append({'ix':i, 'mv': Move.type['nd']})
            if i >= 3:
                if (self.board[i - 3][0].rank == self.board[i][0].rank or
                            self.board[i - 3][0].suit == self.board[i][0].suit):
                    logging.debug("Could do skip two move of {0} up to {1}".format(
                        self.board[i][0].to_short_string(),
                        self.board[i - 3][0].to_short_string(),
                    ))
                    starting_moves.append({'ix':i, 'mv': Move.type['st']})
        total_time = time.time() - start_time

        logging.debug("Found %d moves in %f seconds" % (len(starting_moves), total_time))

        best_piles = len(self.board)
        logging.debug("Evaluating each starting position for fewest piles")

    def recursive_collapse(self, board):

        logging.debug("Check available moves")
        starting_moves = []
        start_time = time.time()
        for i in xrange(1, len(board) + 1):
            logging.debug(
                "Looking at pile {0}, card {1}".format(i,
                                                       board[i][0].to_short_string()))
            if i >= 1:
                if (board[i - 1][0].rank == board[i][0].rank or
                            board[i - 1][0].suit == board[i][0].suit):
                    logging.debug("Could do next door move of {0} up to {1}".format(
                        board[i][0].to_short_string(),
                        board[i - 1][0].to_short_string(),
                    ))
                    starting_moves.append({'ix': i, 'mv': Move.type['nd']})
            if i >= 3:
                if (board[i - 3][0].rank == board[i][0].rank or
                            board[i - 3][0].suit == board[i][0].suit):
                    logging.debug("Could do skip two move of {0} up to {1}".format(
                        board[i][0].to_short_string(),
                        board[i - 3][0].to_short_string(),
                    ))
                    starting_moves.append({'ix': i, 'mv': Move.type['st']})
        total_time = time.time() - start_time

        logging.debug("Found %d moves in %f seconds" % (len(starting_moves), total_time))
        if len(starting_moves) == 0:
            # no moves left, return number of piles down this path
            return len(board)
        else:
            # moves left. perform move, then recurse
            return 1
