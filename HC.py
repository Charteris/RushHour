import BFS, time, helper, ASTAR, random
from typing import List
from turtle import Turtle

'''-------------------------------------------------- HILL CLIMBING ALGORITHM -----------------------------------------------------------'''
# Greedy hill-climb
def greedy(initial: str, maxTime: int, vehicles: List[str]) -> {str, str, int, int}:
    # Note: Hill-climbing does not record path
    start = time.time()
    node = initial
    neighbours = []
    evals = []
    steps = 0

    # Evaluate current node
    E = ASTAR.heuristic(node)

    while True:
        # Exceeds time limit
        if (time.time() - start * 1000) >= float(maxTime):
            return "....................................", str(steps) + " steps", (time.time() - start) * 1000, 0

        neighbours.clear()
        evals.clear()
        lowest = True
        # Expand to find neighbours
        for i in range(len(vehicles)):
            for dir in range(2):
                children = BFS.expand(node, vehicles[i], dir)
                # Check if unique neighbour
                for n in children:
                    child = n[0]
                    if child not in neighbours:
                        neighbours.append(child)
                        evals.append(ASTAR.heuristic(neighbours[-1]))

        # Move to next neighbour if it has less obstructions
        for i, n in enumerate(neighbours):
            if evals[i] < E:
                lowest = False
                # Note: This should not break the loop as their may be a shallower neighbour
                node = n
                E = evals[i]

        # If hit a divot / plateau, return node
        if lowest:
            return node, str(steps) + " steps", (time.time() - start) * 1000, steps
        steps += 1

# Random restart hill-climb
def randRestart(initial: str, maxTime: int, vehicles: List[str], explored: List[str], board: Turtle = None) -> {str, str, int, int}:
    # Check initial state
    solution, steps, t, steps = greedy(initial, maxTime, vehicles)
    nodes = steps

    # Proceed to perform greedy search on random states
    start = time.time()
    restarts = 0
    while not BFS.solved(solution) and len(explored) > 0:
        if (time.time() - start) * 1000 >= float(maxTime):
            return "....................................", str(restarts) + " restarts | " + str(steps) + " steps", (time.time() - start) * 1000, 0

        # Randomly selects new initial state
        # THIS LIST OF INITIAL STATES COULD ALSO BE GENERATED THROUGH REPEATED EXPANSION. THE BFS EXPLORED LIST IS MERELY USED FOR EASE SINCE ITS ALREADY GENERATED.
        next = random.choice(explored)
        if board is not None:
            helper.setupVehicles(next, board)
        # Pops randomly selected state from explored list to ensure no doubles are selected
        explored.pop(explored.index(next))
        restarts += 1
        solution, steps, t, steps = greedy(next, maxTime, vehicles)
        nodes += steps

    # Return solution
    return solution, str(restarts) + " restarts | " + str(steps) + " steps", (time.time() - start) * 1000, steps, nodes