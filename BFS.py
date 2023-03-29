import helper, time
from typing import List, Tuple

'''-------------------------------------------------- EXPANSION ALGORITHM --------------------------------------------------'''
# Expands the given parent to the relevant action specific child
# Returns the parent instance if child is not valid for given direction / vehicle
def expand(parent: str, vehicle: Tuple[str, int], dir: int) -> List[List[str]]:
    # Check error case
    if parent is None or len(parent) != 36:
        return []
    # Define variables
    v = vehicle[0]
    isTruck = v >= 'O' and v <= 'R'
    index = parent.find(v)
    # If vehicle does not exist in parent, return
    if index == -1:
        return []
    state = list(parent)
    y = index // 6
    x = index - y*6
    distances = []

    # Attempt to move right or down
    if dir == 0:
        # Check if vertical or horizontal
        if vehicle[1] == 1:  # RIGHT
            while x < 4 - isTruck and parent[y*6 + x + 2 + isTruck] == '.':
                state[y * 6 + x + 2 + isTruck] = v
                state[y * 6 + x] = '.'
                distances.append(["".join(state), v + 'R' + str(len(distances) + 1)])
                x += 1

        elif vehicle[1] == 0:  # DOWN
            while y < 4 - isTruck and parent[(y + 2 + isTruck) * 6 + x] == '.':
                state[(y + 2 + isTruck) * 6 + x] = v
                state[y * 6 + x] = '.'
                distances.append(["".join(state), v + 'D' + str(len(distances) + 1)])
                y += 1
    # Attempt to move left or up
    else:
        # Check if vertical or horizontal
        if vehicle[1] == 1:  # LEFT
            while x > 0 and x < 5 - isTruck and parent[y * 6 + x - 1] == '.':
                state[y * 6 + x - 1] = v
                state[y * 6 + x + 1 + isTruck] = '.'
                distances.append(["".join(state), v + 'L' + str(len(distances) + 1)])
                x -= 1

        elif vehicle[1] == 0:  # UP
            while y > 0 and y < 5 - isTruck and parent[(y - 1) * 6 + x] == '.':
                state[(y - 1) * 6 + x] = v
                state[(y + 1 + isTruck) * 6 + x] = '.'
                distances.append(["".join(state), v + 'U' + str(len(distances) + 1)])
                y -= 1

    # If vehicle cannot move or cannot be found (nothing has been appended to distances)
    if len(distances) == 0:
        return distances

    # Return array of potential distances for given vehicle movement
    distances.reverse()
    return distances

'''-------------------------------------------------- BFS ALGORITHM --------------------------------------------------'''
# Determines if the state is the goal state (if 'x' is located at the end of line 3)
def solved(state: str) -> bool:
    # end of 3rd row at string pos 17
    if len(state) != 36 or state is None:
        return False
    return (state[16] == 'X') and (state[17] == 'X')

# Solves given problem through bread-first search algorithm
def main(initial: str, maxTime: int, vehicles: List[Tuple[str, int]]) -> {str, str, int, int}:
    # Define variables and perform initial state check
    if solved(initial):
        return initial, "NA", 0, 0, 0, []
    node = helper.Node(initial, "", '')
    start = time.time()
    frontier = [node]
    explored = []

    # Loop until solution or failure is found
    while len(frontier) > 0 and (time.time() - start) * 1000 < float(maxTime):
        node = frontier.pop(0) # Gets shallowest node
        explored.append(node.state)

        # Expansion of potential action states
        for i in range(len(vehicles)):
            for dir in range(2):
                children = expand(node.state, vehicles[i], dir)

                for child in children:
                    # If unique, pass to frontier
                    if child[0] not in explored and child[0] not in frontier:
                        seq = node.dir + " " + child[1]
                        if node.dir == '':
                            seq = child[1]

                        # Check if solved
                        if solved(child[0]):
                            print("Success!")
                            edit = list(seq)
                            edit[-1] = chr(ord(edit[-1]) + 2)
                            seq = ''.join(edit)
                            for f in frontier:
                                explored.append(frontier.pop().state)
                            return child[0], seq, (time.time() - start) * 1000, (len(seq) + 1) // 4, len(explored) + 1, explored

                        frontier.append(helper.Node(child[0], node.state, seq))

    # Error or exceeded time limit
    return "....................................", "NA", (time.time() - start) * 1000, 0, 0, []