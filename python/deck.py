import logging
import random




class Deck:

    def __init__(self):
        self.deck = []
        for i in range(0, 4):
            for j in range(2, 15):
                self.deck.append(Card(j, i))

    def shuffle(self):
        random.shuffle(self.deck)

    @staticmethod
    def populate_byte_array():
        b = bytearray()
        for suit in range(0, 4):
            for rank in range(2, 15):
                b.append(rank<<2 | suit)
        return b

    def shuffle_perfect(self):
        # swap two cards to make suits meet
        temp = self.deck[13]
        self.deck[13] = self.deck[25]
        self.deck[25] = temp

        temp = self.deck[39]
        self.deck[39] = self.deck[51]
        self.deck[51] = temp

    def print_deck(self):
        for card in self.deck:
            logging.debug(card.to_string())

    def get_card(self):
        try:
            return self.deck.pop(0)
        except IndexError:
            return None

    def __str__(self):
        return ','.join(map(str, self.deck))


class SmallCard:
    def __init__(self, rank, suit):
        value = (rank << 2) | suit
        logging.info("rank: %d, suit: %d, value: %d" % (rank, suit, value))
        self.value = value

    def __str__(self):
        return str(self.value)

class SmallDeck:
    def __init__(self):
        self.deck = []
        for i in range(0, 4):
            for j in range(2, 15):
                self.deck.append((j<<2)|i)

class Card:

    rank_long = {
        2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
        7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack',
        12: 'Queen', 13: 'King', 14: 'Ace'
    }
    rank_short = {
        2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
        7: '7', 8: '8', 9: '9', 10: '0', 11: 'J',
        12: 'Q', 13: 'K', 14: 'A'
    }
    suit_long = {0: 'Spades', 1: 'Hearts', 2: 'Diamonds', 3: 'Clubs'}
    suit_short = {0: 's', 1: 'h', 2: 'd', 3: 'c'}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    @staticmethod
    def small_card_to_string(sc):
        rank = sc >> 2
        suit = sc & 0b00000011
        return Card.rank_long[rank] + " of " + Card.suit_long[suit]

    def to_string(self):
        return Card.rank_long[self.rank] + " of " + Card.suit_long[self.suit]

    def to_short_string(self):
        return Card.rank_short[self.rank] + Card.suit_short[self.suit]

    def __str__(self):
        return Card.rank_short[self.rank] + Card.suit_short[self.suit]
