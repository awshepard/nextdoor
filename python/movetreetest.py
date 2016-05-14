import logging
from board import Move
from board import MoveTree
from board import MoveTreeNode
from board import Board
from deck import Deck
from deck import Card
import sys
import os
import re
import itertools
import argparse
import logging
import time
from pympler import asizeof
import resource
import random
from SmallTreeNode import SmallTreeNode

parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug', action='store_true', default=False, help='debug mode')
parser.add_argument(
    '--depth', type=int, default=1, help='how deep to search')


global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

def main():


    new_deck = Deck.init_small_deck()
    random.shuffle(new_deck)
    logging.info("new deck:")
    logging.info(new_deck)
    logging.info("Size of a new deck at creation")
    logging.info(asizeof.asizeof(new_deck))

    new_board = Board.init_small_board()

    logging.info("Size of a new board at creation")
    logging.info(asizeof.asizeof(new_board))

    # populate board
    card = new_deck.pop()
    for i in range(0,len(new_deck)):
        new_board.append(new_deck[i])
    logging.info("Size of a new board after adding cards")
    logging.info(asizeof.asizeof(new_board))

    stn = SmallTreeNode(new_deck.pop(1),new_board)
    logging.info("SmallTreeNode:")
    logging.info(stn.to_short_string())
    logging.info("Size of small tree node")
    logging.info(asizeof.asizeof(stn))


    logging.info("start exploring")
    start_time = time.time()
    stn.explore(args.depth)
    total_time = time.time() - start_time
    moves_explored = stn.moves_explored

    logging.info("Tree root after exploration:")
    logging.info(stn.to_short_string())
    # time per node hovers around 0.001152
    logging.info("Time to explore depth %d: %f" % (args.depth, total_time))
    logging.info("Moves evaluated: %d, time per move : %f" % (moves_explored, total_time/float(moves_explored)))

    # final_state, min_moves = mtn.fetch_min_list()
    # #mtn.update_moves()
    # logging.info("Moves to minimum state:")
    # logging.info(', '.join(str(move) for move in min_moves))
    # logging.info("Final state:")
    # logging.info(final_state)





    #
    #
    # board = Board()
    # logging.info("Size of a board at creation")
    # logging.info(asizeof.asizeof(board))
    # deck = Deck()
    # logging.info("Size of a deck at creation")
    # logging.info(asizeof.asizeof(deck))
    # deck.shuffle()
    # logging.info("Size of a deck after shuffle")
    # logging.info(asizeof.asizeof(deck))
    # logging.debug(deck)
    # card = deck.get_card()
    # logging.info("Size of a card")
    # logging.info(asizeof.asizeof(card))
    # while card is not None:
    #     board.add_card(card)
    #     card = deck.get_card()
    # logging.info("Size of a board after adding cards")
    # logging.info(asizeof.asizeof(board))
    # logging.debug(board)
    # available_moves = board.get_available_moves()
    # logging.debug(', '.join(str(move) for move in available_moves))
    #
    #
    # mt = MoveTree()
    # mtn = MoveTreeNode(None, 52, board)
    # mt.root = mtn
    #
    #
    #
    # logging.info("Size of tree before:")
    # logging.info(asizeof.asizeof(mtn))
    #
    # logging.info("Tree root at creation:")
    # logging.info(mtn)
    #
    # #mtn.derive_children()
    # start_time = time.time()
    # mtn.explore(args.depth)
    # total_time = time.time() - start_time
    # moves_explored = mtn.moves_explored
    #
    # logging.info("Tree root after exploration:")
    # logging.info(mtn)
    # # time per node hovers around 0.001152
    # logging.info("Time to explore depth %d: %f" % (args.depth, total_time))
    # logging.info("Moves evaluated: %d, time per move : %f" % (moves_explored, total_time/float(moves_explored)))
    #
    # final_state, min_moves = mtn.fetch_min_list()
    # #mtn.update_moves()
    # logging.info("Moves to minimum state:")
    # logging.info(', '.join(str(move) for move in min_moves))
    # logging.info("Final state:")
    # logging.info(final_state)
    #
    #
    #
    # logging.info("Size of tree after:")
    # logging.info(float(asizeof.asizeof(mtn))/float(pow(2,20)))
    logging.info("Max memory usage:")
    logging.info(float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/float(pow(2,20)))# / float((pow(2,10))))
    # for child in mtn.children_list:
    #     logging.debug(mtn.children[child])







if __name__ == '__main__':
    main()