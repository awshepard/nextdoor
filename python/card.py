


# card = byte
# rank = 2 .. 15 (4)
# suit = 0 .. 3  (2)
# moves = 00 - no move, 01 - next door, 10 - skip two (2)
# basic card = rank << 4 | suit << 2
# card in motion = rank << 4 | suit << 2 | move


class Card(object):
    move_long = {
        0: 'none', 1: 'next door', 2: 'skip two'
    }
    move_short = {
        0: '', 1: 'nd', 2: 'skip two'
    }
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

    @staticmethod
    def to_string(card):
        move = card & 0b00000011
        rank = card >> 4
        suit = (card >> 2) & 0b00000011
        to_return = '%s of %s'
        if move > 0 :
            to_return = ('Move %s ' % Card.move_long[move]) + to_return
        return to_return % (Card.rank_long[rank], Card.suit_long[suit])

    @staticmethod
    def to_short_string(card):
        move = card & 0b00000011
        rank = card >> 4
        suit = (card >> 2) & 0b00000011
        to_return = '%s%s' % (Card.rank_short[rank], Card.suit_short[suit])
        if move > 0:
            to_return += '|%s' % Card.move_short[move]
        return to_return

