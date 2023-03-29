import BFS, time, helper
from typing import List, Tuple
from queue import PriorityQueue

'''-------------------------------------------------- A* ALGORITHM -----------------------------------------------------------'''
# Proposed heuristic determined by the number of obstructions starting from target vehicle
def heuristic(state: str) -> int:
    # Add more accuracy to heuristic
    if BFS.solved(state):
        return 0
    # Define initial buffer
    obstructions = 0
    index = state.find('X') + 2
    while index <= 17:
        if state[index] != '.':
            obstructions += 1
        index += 1
    # Return number of obstructions as heuristic value
    return obstructions + 1

# A* algorithm
def main(initial: str, maxTime: int, vehicles: List[Tuple[str, int]]) -> {str, str, int, int}:
    # Define variables and perform initial state check
    if BFS.solved(initial):
        return initial, "NA", 0, 0
    node = helper.Node(initial, "", '', 0, heuristic(initial))
    start = time.time()
    frontier = PriorityQueue()
    frontier.put(node)
    explored = {}

    # Loop until solution or failure is found
    while not frontier.empty() and (time.time() - start) * 1000 < float(maxTime):
        node = frontier.get() # Gets shallowest node
        explored[node.state] = node.cost

        # Check if solved (before expansions such that it allows ALL past children to be passed)
        if BFS.solved(node.state):
            print("Success!")
            edit = list(node.dir)
            edit[-1] = chr(ord(edit[-1]) + 2)
            seq = ''.join(edit)
            return node.state, seq, (time.time() - start) * 1000, (len(seq) + 1) // 4, len(explored) + len(frontier.queue) + 1

        # Expansion of potential action states
        for i in range(len(vehicles)):
            for dir in range(2):
                children = BFS.expand(node.state, vehicles[i], dir)

                for child in children:
                    h = heuristic(child[0])
                    # If unique and heuristic is consistent, pass to frontier
                    unique = child[0] not in explored and child[0] not in frontier.queue
                    if child[0] in explored and node.cost + 1 < explored[child[0]]:
                        unique = True
                        explored[child[0]] = node.cost + 1
                    if child[0] in frontier.queue:
                        for n, ref in enumerate(frontier.queue):
                            if node.state == ref.state:
                                unique = True
                                frontier.queue[n] = node

                    if unique:
                        seq = node.dir + " " + child[1]
                        if node.dir == '':
                            seq = child[1]

                        frontier.put(helper.Node(child[0], node.state, seq, node.cost + 1, h))

    # Error or exceeded time limit
    return "....................................", "NA", (time.time() - start) * 1000, 0, 0