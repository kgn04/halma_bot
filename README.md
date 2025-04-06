# Minimax implementation in halma

This project was creating for simulating halma games between two bots using minimax algorithm.
User can observe games with different parameters and collect logs for results analysis.

## What is halma?

https://en.wikipedia.org/wiki/Halma

In this project two player setup is used.

## What is minimax?

https://en.wikipedia.org/wiki/Minimax

## Heuristics used (distance functions)

- [Manhattan](https://en.wikipedia.org/wiki/Taxicab_geometry)
- [Chebyshev](https://en.wikipedia.org/wiki/Chebyshev_distance)
- [Euclidean](https://en.wikipedia.org/wiki/Euclidean_distance)


## Positions

There are [already generated middle game positions](positions).
[pos1.txt](positions/pos1.txt) contains starting position.
User can generate new positions using [positions_generator.py](positions_generator.py).

## User guide

After cloning repository just run
> python halma_bot [options]

    options:
      -h, --help            show this help message and exit
      -v, --verbose         print current board position and rating after each move
      -p POSITION, --position POSITION
                            position id from 'positions' directory (1..101)
      -md MAX_DEPTH, --max-depth MAX_DEPTH
                            max game tree depth
      -l LOGGING, --logging LOGGING
                            name of file to save the logs to
      -rl ROUNDS_LIMIT, --rounds-limit ROUNDS_LIMIT
                            draw after playing that many rounds
      -p1, --prune1         use alpha beta pruning for player 1 moves.
      -d1 {manhattan,chebyshev,euclides}, --distance1 {manhattan,chebyshev,euclides}
                            distance function for heuristics used by player 1.
      -p2, --prune2         use alpha beta pruning for player 2 moves.
      -d2 {manhattan,chebyshev,euclides}, --distance2 {manhattan,chebyshev,euclides}
                            distance function for heuristics used by player 2.

example:
> python halma_bot -md 2 -d1 euclides -d2 euclides -p 99 -l logs/some_log_file.log -v -p1


Also check an [example of game log](research/logs/11-p1.log).

## Research

I compared minimax without and with pruning, and the heuristics. 
Process of generating data, processing, and visualisation is located [here](research/research.ipynb).
(Note that some of the compilation results are long, so it is better to open notebook in environment,
that allows you to hide the cell compilation results.)

All the results are gathered in notebook markdown cells.