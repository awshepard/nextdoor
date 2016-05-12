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

    logging.info("Tree root at creation:")
    logging.info(mtn)

    #mtn.derive_children()
    start_time = time.time()
    mtn.explore(args.depth)
    total_time = time.time() - start_time

    logging.info("Tree root after exploration:")
    logging.info(mtn)
    logging.info("Time to explore depth %d: %f" % (args.depth, total_time))

    final_state, min_moves = mtn.fetch_min_list()
    logging.info("Moves to minimum state:")
    logging.info(', '.join(str(move) for move in min_moves))
    logging.info("Final state:")
    logging.info(final_state)

    # for child in mtn.children_list:
    #     logging.debug(mtn.children[child])




if __name__ == '__main__':
    main()