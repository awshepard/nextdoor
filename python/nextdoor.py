import sys
import os
import re
import itertools
import argparse
import logging

from deck import Deck
from game import Game


parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug', action='store_true', default=False, help='debug mode')
parser.add_argument(
    '--games', type=int, default=1, help='how many games to play')
parser.add_argument('--turnStrategy', type=str, default='simple',
                    help='what strategy to use when turning over cards')
parser.add_argument('--collapseStrategy', type=str, default='simple',
                    help='what strategy to use when collapsing the board')

global args
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

# check this out for strategy pattern:
# http://stackoverflow.com/questions/963965/how-to-write-strategy-pattern-in-python-differently-than-example-in-wikipedia


def main():
    results = []
    games = []
    for i in range(0, args.games):
        deck = Deck()
        deck.shuffle()
        logging.debug(deck)
        game = Game(deck)
        turns = game.play()
        results.append(turns)
        logging.debug(game.board_to_string())

    logging.info("Total Games = %d" % args.games)
    logging.info("Total Wins = %d" % sum([x for x in results if x == 1]))
    logging.info("Average Piles = {0}".format(
        float(sum(results)) /
        float(len(results))))
    logging.debug("Results: {0}".format(','.join(str(x) for x in results)))


if __name__ == '__main__':
    main()
