import BFS, time, helper
from typing import List, Tuple
import BFS, time, helper

'''-------------------------------------------------- DFS ALGORITHM --------------------------------------------------'''
# Solves given problem through bread-first search algorithm
def DLS(initial, maxTime, vehicles, depth):
    # Define variables and perform initial state check
    node = helper.Node(initial, "", '')
    if BFS.solved(initial):
        return node.state, "NA", 0, 0
    start = time.time()
    frontier = [node]
    explored = {}

    # Loop until solution or failure is found
    while len(frontier) > 0 and (time.time() - start) * 1000 < float(maxTime):
        node = frontier.pop()  # Gets shallowest node
        explored[node.state] = node.cost

        # Expansion of potential action states
        for i in range(len(vehicles)):
            for dir in range(2):
                children = BFS.expand(node.state, vehicles[i], dir)

                for child in children:
                    # Ensure that it does not exist in current path
                    unique = child[0] not in explored and child[0] not in frontier
                    if child[0] in explored:
                        if node.cost + 1 < explored[child[0]]:
                            unique = True
                            explored[child[0]] = node.cost

                    if unique:
                        seq = node.dir + " " + child[1]
                        if node.dir == '':
                           seq = child[1]

                        # Check if solved
                        if BFS.solved(child[0]):
                            print("Success!")
                            edit = list(seq)
                            edit[-1] = chr(ord(edit[-1]) + 2)
                            seq = ''.join(edit)
                            return child[0], seq, (time.time() - start) * 1000, len(explored) + len(frontier) + 1

                        if node.cost < depth:
                            frontier.append(helper.Node(child[0], node.state, seq, node.cost + 1))

    # Error or exceeded time limit
    return "....................................", "NA", (time.time() - start) * 1000, 0

def main(initial, maxTime, vehicles):
    # Check initial state
    if BFS.solved(initial):
        return initial, "NA", 0, 0, 0
    # Continue performing at higher depth (a depth above 1000 is considered too deep for given problem)
    i = 0
    start = time.time()
    solution, sequence, var, nodes = "....................................", "NA", 0, 0
    while (solution == "...................................." and i < 75) and ((time.time() - start) * 1000 < float(maxTime)):
        i += 1
        solution, sequence, var, nodes = DLS(initial, maxTime, vehicles, i)
    return solution, sequence, (time.time() - start) * 1000, i + 1, nodes

'''-------------------------------------------------- ITERATIVE DEEPENING ALGORITHM --------------------------------------------------'''
# Different attempt to ID without referring to other functions
'''
def main(initial: str, maxTime: int, vehicles: List[Tuple[str, int]]) -> {str, str, int, int}:
    # Check initial state
    if BFS.solved(initial):
        return initial, "NA", 0, 0
    depth = 1
    start = time.time()
    frontier, explored = [helper.Node(initial, "", '')], []
    # Continue expanding frontier and incrementing depth (limit max depth to 1000)
    while depth < 1000 and ((time.time() - start) * 1000 < float(maxTime)):
        # Expand all current parents in frontier
        l = len(frontier)
        while l > 0:
            l -= 1
            node = frontier.pop(0)
            explored.append(node)

            for i in range(len(vehicles)):
                for dir in range(2):
                    children = BFS.expand(node.state, vehicles[i], dir)
                    unique = True

                    for j in range(len(children)):
                        child = children[j][0]
                        # Check if child is valid
                        for n in range(len(explored)):
                            if explored[n].state == child:
                                unique = False
                        for n in range(len(frontier)):
                            if frontier[n].state == child:
                                unique = False

                        # If unique, check if solution and push onto frontier
                        if unique:
                            frontier.append(helper.Node(child, node.state, children[j][1]))

                            # Check if solved
                            if BFS.solved(child):
                                print("Success!")
                                # Determine appropriate action sequence
                                index = len(explored) - 1
                                final = list(children[j][1])
                                final[2] = chr(ord(final[2]) + 2)
                                temp, action = frontier.pop(), ["".join(final)]
                                cost = 1
                                while index != 0:
                                    if temp.parent == explored[index].state:
                                        cost += 1
                                        action.append((explored[index].dir))
                                        temp = explored[index]
                                    index -= 1
                                action.reverse()
                                return child, " ".join(action), (time.time() - start) * 1000, cost

        # Increment depth
        depth += 1

    return "....................................", "NA", (time.time() - start) * 1000, 0'''
