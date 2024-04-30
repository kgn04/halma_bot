from algorithms import minimax, alpha_beta_pruning
from strategies import manhattan_distance, euclidean_distance, chebyshev_distance
from game_tree import PositionNode
from game import play

MAX_DEPTH = 2

with open(f'positions/pos52.txt') as position:
    tree = PositionNode([line[:-1].split(' ') for line in position])
    print(play(
        tree, MAX_DEPTH, alpha_beta_pruning, alpha_beta_pruning,
        chebyshev_distance, manhattan_distance, True
    ))

