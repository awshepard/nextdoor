from card import Card
from board import Board
import copy

class SmallTreeNode():

    def __init__(self, move, board, parent=None):
        self.move = move
        self.board = board
        if self.move is not None:
            # self.update_board()
            pass
        self.min_piles = len(self.board)
        self.children_list = self.derive_children_list()
        self.children = {}
        self.parent = parent
        self.sub_tree_branch_average = 0
        self.board_score = self.get_board_score()
        self.moves_explored = 0

    def update_board(self):
        self.board = Board.perform_move(self.move, self.board)

    def get_board_score(self):
        return Board.get_score_new(self.board)

    def derive_children_list(self):
        return Board.get_available_moves_new(self.board)

    def explore(self, depth=1):
        self.moves_explored += 1
        if (depth == 0):
            return
        for child in self.children_list:
            # for each child, create a node, then recursively explore those
            child_stn = SmallTreeNode(child,copy.deepcopy(self.board), self)
            if len(child_stn.children_list) > 0:
                min_piles = child_stn.explore(depth-1)
                if min_piles < self.min_piles:
                    self.min_piles = len(child_stn.board)
                    self.min_child = child
            # add the child to the children list
            self.children[child] = child_stn

        # calculate branch factor and moves
        total_branches = 0
        for child in self.children_list:
            total_branches += len(self.children[child].children_list)
            self.moves_explored += self.children[child].moves_explored
        self.sub_tree_branch_average = float(total_branches) / float(len(self.children))

    def __str__(self):
        return """
        | Move: %s |
        """ % (
            Card.to_short_string(self.move)
        )

    def to_short_string(self):
        return """
        | %s |
        """ % (
            Card.to_short_string(self.move)
        )