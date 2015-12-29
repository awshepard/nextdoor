from deck import Deck
from deck import Card
import itertools
import logging


class Game:

    def __init__(self, deck, turn_strategy='simple',
                 collapse_strategy='simple'):
        self.deck = deck
        self.board = []
        self.board.append([])
        self.last_index = -1
        self.turn_strategy = turn_strategy
        self.collapse_strategy = collapse_strategy

    def play(self):
        count = 1
        card = self.deck.get_card()
        while card is not None:
            logging.debug("====Card %d====" % count)
            self.turn_simple(card)
            self.collapse_simple()
            count += 1
            card = self.deck.get_card()
        return len(filter(None, self.board))

    def board_to_string(self):
        to_return = ""
        for pile in self.board:
            to_return += "\n"
            for card in pile:
                to_return += " | " + card.to_short_string()
        return to_return

    def turn_simple(self, card):
        # decide where to put this card
        if self.last_index > -1 and (
            self.board[self.last_index][0].rank == card.rank or
            self.board[self.last_index][0].suit == card.suit
        ):
            self.board[self.last_index].insert(0, card)
        elif self.last_index >= 2 and (
            self.board[self.last_index - 2][0].rank == card.rank or
            self.board[self.last_index - 2][0].suit == card.suit
        ):
            self.board[self.last_index - 2].insert(0, card)
        else:
            self.last_index += 1
            self.board.append([])
            self.board[self.last_index].insert(0, card)

    def collapse_simple(self):
        moved_cards = True
        logging.debug("Begin collapse")
        while moved_cards:
            moved_cards = False
            logging.debug("Begin collapse pass")
            logging.debug(self.board_to_string())
            for i in xrange(1, self.last_index + 1):
                # logging.debug(self.board[i][0])
                logging.debug(
                    "Looking at pile {0}, card {1}".format(i,
                                                           self.board[i][0].to_short_string()))
                if i >= 1:
                    if (self.board[i - 1][0].rank == self.board[i][0].rank or
                            self.board[i - 1][0].suit == self.board[i][0].suit):
                        logging.debug("Doing next door move of {0} up to {1}".format(
                            self.board[i][0].to_short_string(),
                            self.board[i - 1][0].to_short_string(),
                        ))
                        self.board[
                            i - 1] = self.board.pop(i) + self.board[i - 1]
                        logging.debug("board after move:")
                        logging.debug(self.board_to_string())
                        self.last_index -= 1
                        moved_cards = True
                        break

                if i >= 3:
                    if (self.board[i - 3][0].rank == self.board[i][0].rank or
                            self.board[i - 3][0].suit == self.board[i][0].suit):
                        logging.debug("Doing skip two move of {0} up to {1}".format(
                            self.board[i][0].to_short_string(),
                            self.board[i - 3][0].to_short_string(),
                        ))
                        self.board[
                            i - 3] = self.board.pop(i) + self.board[i - 3]
                        logging.debug("board after move:")
                        logging.debug(self.board_to_string())
                        self.last_index -= 1
                        moved_cards = True
                        break
