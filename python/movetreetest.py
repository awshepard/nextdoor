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

parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug', action='store_true', default=False, help='debug mode')
parser.add_argument(
    '--depth', type=int, default=1, help='how deep to search')


global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

def main():
    board = Board()
    deck = Deck()
    deck.shuffle()
    logging.debug(deck)
    card = deck.get_card()
    while card is not None:
        board.add_card(card)
        card = deck.get_card()
    logging.debug(board)
    available_moves = board.get_available_moves()
    logging.debug(', '.join(str(move) for move in available_moves))


    mt = MoveTree()
    mtn = MoveTreeNode(None, 52, board)
    mt.root = mtn

    # typical size in old version was ~32K

    logging.info("Size of tree before:")
    logging.info(asizeof.asizeof(mtn))

    logging.info("Tree root at creation:")
    logging.info(mtn)

    #mtn.derive_children()
    start_time = time.time()
    mtn.explore(args.depth)
    total_time = time.time() - start_time
    moves_explored = mtn.moves_explored

    logging.info("Tree root after exploration:")
    logging.info(mtn)
    # time per node hovers around 0.001152
    logging.info("Time to explore depth %d: %f" % (args.depth, total_time))
    logging.info("Moves evaluated: %d, time per move : %f" % (moves_explored, total_time/float(moves_explored)))

    final_state, min_moves = mtn.fetch_min_list()
    #mtn.update_moves()
    logging.info("Moves to minimum state:")
    logging.info(', '.join(str(move) for move in min_moves))
    logging.info("Final state:")
    logging.info(final_state)

    #old values typically ranged from:
    # depth 1
    # 1 MB for tree size
    # 10 MB for totally memory usage
    # depth 2
    # 20-45 MB for tree size
    # 40-85 MB for totally memory usage
    # depth 3
    # 700 MB-1GB for tree size
    # 1.3-2.0 GB for totally memory usage
    # depth 4
    # consumed 14+GB ram

    logging.info("Size of tree after:")
    logging.info(float(asizeof.asizeof(mtn))/float(pow(2,20)))
    logging.info("Max memory usage:")
    logging.info(float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/float(pow(2,20)))# / float((pow(2,10))))
    # for child in mtn.children_list:
    #     logging.debug(mtn.children[child])




if __name__ == '__main__':
    main()