
import logging
import time
import copy
import itertools

class Move:
    types = {
        'nd':'next door',
        'st':'skip two'
    }

    def __init__(self, index, type):
        self.index = index
        self.type = type

    def __str__(self):
        return '%d|%s' % (self.index, self.type)


class Board:

    def __init__(self):
        self.piles = []
        self.piles.append([])
        self.last_index = 0

    @staticmethod
    def init_small_board():
        p = []
        p.append([])
        return p

    @staticmethod
    def get_score_new(b):
        return 0

    # todo
    @staticmethod
    def perform_move_new(move, board):
        return board

    # todo
    @staticmethod
    def get_available_moves_new(board):
        return [board[1],board[2]]

    def __len__(self):
        return len(self.piles) - 1
    def __getitem__(self, item):
        return self.piles[item]

    def add_card(self, card, pile = None):
        if pile is None:
            # add new pile and add card to back
            self.last_index += 1
            self.piles.append([])
            self.piles[self.last_index].insert(0, card)
        else:
            # validate pile we're attempting to add to
            if self.piles[pile][0].suit == card.suit or self.piles[pile][0].rank == card.rank:
                self.piles[pile].insert(0,card)
            else:
                raise Exception("can't put card on pile!")

    def move_pile(self, from_pile, to_pile):
        # validate move
        logging.debug("moving from %d to %d" % (from_pile, to_pile))
        try:
            if (self.piles[from_pile][0].suit == self.piles[to_pile][0].suit) or (
                        self.piles[from_pile][0].rank == self.piles[to_pile][0].rank):
                self.piles[to_pile] = self.piles.pop(from_pile) + self.piles[to_pile]
                self.last_index -= 1
            else:
                raise Exception("can't move piles from (%d) to (%d)" % (from_pile, to_pile) + str(self))
        except IndexError:
            raise Exception(str(self))

    def perform_move(self, move):
        self.move_pile(move.index,
                       (move.index - 1) if move.type=='nd' else (move.index - 3))



    def get_available_moves(self):
        logging.debug("Evaluate possible starting points")
        starting_moves = []
        start_time = time.time()
        for i in xrange(2, self.last_index + 1):
            logging.debug(
                "Looking at pile {0}, card {1}".format(i,
                                                       self.piles[i][0].to_short_string()))
            if i >= 1:
                if (self.piles[i - 1][0].rank == self.piles[i][0].rank or
                            self.piles[i - 1][0].suit == self.piles[i][0].suit):
                    logging.debug("Could do next door move of {0} up to {1}".format(
                        self.piles[i][0].to_short_string(),
                        self.piles[i - 1][0].to_short_string(),
                    ))
                    starting_moves.append(Move(i, 'nd'))
            if i >= 4:
                if (self.piles[i - 3][0].rank == self.piles[i][0].rank or
                            self.piles[i - 3][0].suit == self.piles[i][0].suit):
                    self.debug = logging.debug(
                        "Could do skip two move of {0} up to {1}".format(self.piles[i][0].to_short_string(),
                                                                         self.piles[i - 3][0].to_short_string(), ))
                    starting_moves.append(Move(i, 'st'))
        total_time = time.time() - start_time

        logging.debug("Found %d moves in %f seconds" % (len(starting_moves), total_time))
        return starting_moves

    def get_score(self):
        return len(self.get_available_moves()) * 1.1 ** (52 - len(self.piles))

    def __str__(self):
        to_return = ""
        test = itertools.izip_longest(*self.piles, fillvalue='--')
        t2 = map(list, test)
        for pile in t2:
            to_return += "\n\t"
            for card in pile:
                val = card
                if card != '--':
                    val = card.to_short_string()
                to_return += "|" + val
        return to_return

class MoveTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

class MoveTreeNode:

    def __init__(self, move, min_piles, board, parent = None):
        self.move = move
        self.board = board
        if self.move is not None:
            self.update_board()
        self.min_piles = len(self.board)
        self.children_list = self.derive_child_list()
        self.children = {}
        # if len(self.children_list) > 0:
        #     self.derive_children()
        self.parent = parent
        self.min_child = -1
        self.sub_tree_branch_average = 0
        self.board_score = self.board.get_score()
        self.moves_explored = 0


    def __str__(self):
        return """
            Move: %s
            Min Piles: %d
            Child List: %s
            Min Child: %s
            Board Piles: %d
            Subtree Branch Average: %f
            Board Score: %d
            Board State: %s
            Moves Explore: %d
        """ % (
                self.move, self.min_piles,
                ', '.join(str(child) for child in self.children_list), self.min_child,
                len(self.board), self.sub_tree_branch_average, self.board_score,str(self.board),
                self.moves_explored)


    def derive_child_list(self):
        return self.board.get_available_moves()

    def derive_children(self):
        self.explore(1)

    def update_board(self):
        self.board.perform_move(self.move)

    def update_moves(self):
        self.moves_explored = 0
        for child in self.children_list:
            self.moves_explored += self.children[child].moves_explored

    def has_any_children(self):
        return len(self.children) > 0

    def explore(self, depth = 1):
        self.moves_explored += 1
        #logging.info("my moves explored before children: %d" % self.moves_explored)
        if depth == 0:
            return
        for child in self.children_list:
            child_mtn = MoveTreeNode(child, 52, copy.deepcopy(self.board), self)
            if len(child_mtn.children_list) > 0:
                # depth first here
                min_piles = child_mtn.explore(depth - 1)
                if min_piles < self.min_piles:
                    self.min_piles = len(child_mtn.board)
                    self.min_child = child
            self.children[child] = child_mtn

            # print leaf node?
            if len(child_mtn.children_list) == 0:
                logging.debug("REACHED A LEAF at depth %d" % depth)
                logging.debug(str(child_mtn))
        total_branches = 0
        for child in self.children_list:
            total_branches += len(self.children[child].children_list)
            self.moves_explored += self.children[child].moves_explored
        self.sub_tree_branch_average = float(total_branches) / float(len(self.children))
        #logging.info("my moves explored after children: %d" % self.moves_explored)

            # if len(child_mtn.board) < self.min_piles:
            #     self.min_piles = len(child_mtn.board)
            #     self.min_child = child

    def fetch_min_list(self):
        move_list = []
        mtn = self
        while mtn.min_child != -1 and len(mtn.children_list)>0:
            move_list.append(mtn.min_child)
            mtn = mtn.children[mtn.min_child]
        return (mtn,move_list)