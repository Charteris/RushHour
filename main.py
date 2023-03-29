# Rush Hour graphical game
import turtle, sys, getopt, boardSetup, helper
import BFS, ID, ASTAR, HC

# Constant
DEFAULT = "...................................."

# Get command line arguments
try:
    fileName = sys.argv[1]
    maxTime = sys.argv[2]
except getopt.GetoptError:
    print("Please input a filename and the maximum solution time.")
    sys.exit(0)

# Open file and store problem sets starting from line 9
problems, sols = [], []
f = open(fileName, "r")

# Read all problems
for n in range(8):
    f.readline()
for n in range(40):
    problems.append(f.read(36))
    f.read(1) # Handles new lines
for n in range(4):
    f.readline()
for n in range(40):
    for i in range(14):
        f.readline()
    temp = f.readline()
    temp = temp[:-1]
    while len(temp) > 0 and temp[-1] != '.':
        temp = temp + f.readline()[7:]
        temp = temp[:-1]
    sols.append(temp)
f.close()

# Create screen
screen = turtle.Screen()
screen.setup(1200, 750)
screen.bgcolor("#696969") # dim gray
screen.title("Rush Hour")
screen.tracer(0)
menu = boardSetup.menu()
pen = boardSetup.pen(sols[0])
problem = 1

# Draw boards (192x192 6x6 grids spaced in a particular order)
initial = boardSetup.setupBoard(-546, -5, 32, "Initial State", screen)
initial.cars, initial.trucks, initial.target = helper.init(screen)
tests, keys = [], ["Breadth-first", "Iterative Deepening", "A* Algorithm", "Greedy Hill-climb", "Random Restart (solved)", "Random Restart (initial)"]
coords = [(-246, 150), (54, 150), (-246, -160), (54, -160), (354, -160), (354, 150)]
for i, title in enumerate(keys):
    tests.append(boardSetup.setupBoard(coords[i][0], coords[i][1], 32, title, screen))
    tests[i].cars, tests[i].trucks, tests[i].target = helper.init(screen)
    helper.setupVehicles(problems[problem - 1], tests[i])
vehicles = helper.setupVehicles(problems[problem - 1], initial)

'''-------------------------------------------------- MAIN LOOP --------------------------------------------------'''
# Print solution sequence and time taken to the screen accordingly to relative test (0:BFS, 1:ID, 2:A*, 3:HC)
def runFunc(solution: str, sequence: str, timeTaken: int, cost: int, nodes: int, test: int) -> None:
    # Formatting
    x, y = 120, 280
    if test == 1 or test == 3:
        x = 360
    if test == 2 or test == 3:
        y = -300
    # Solution found
    if solution != DEFAULT:
        print("Path cost:", cost, "| " + sequence + " | ~" + str(int(timeTaken)) + "ms elapsed")
        if(cost > 9):
            boardSetup.message(pen, "Refer to console (Large output sequence)", coords[test][0] + 101, coords[test][1] - 131, False, 10)
        else:
            boardSetup.message(pen, sequence, coords[test][0] + 101, coords[test][1] - 131, False, 10)
        boardSetup.message(pen, "Time elapsed: ~" + str(int(timeTaken)) + "ms", coords[test][0] + 101, coords[test][1] - 146, False, 10)
        boardSetup.message(pen, "Path cost: " + str(cost) + " | Nodes traversed: " + str(nodes), coords[test][0] + 101, coords[test][1] - 161, False, 10)
        helper.setupVehicles(solution, tests[test])
    # Solution not found or time exceeds limit
    else:
        boardSetup.message(pen, "Solution not found!", coords[test][0] + 101, coords[test][1] - 131, False, 10)
        boardSetup.message(pen, "Time elapsed: ~" + str(int(timeTaken)) + "ms", coords[test][0] + 101, coords[test][1] - 146, False, 10)
    screen.update()

# Interactive with main menu
def interact(mx: int, my: int) -> None:
    # Quit button
    if helper.checkLocation(mx, my, 400, 360, 160, 60):
        turtle.bye()

    # Run all button
    if helper.checkLocation(mx, my, 220, 360, 160, 60):
        all()

    # Solve button
    if helper.checkLocation(mx, my, 40, 360, 160, 60):
        solve()

    # Arrows
    right(mx, my)
    left(mx, my)

# Solve current problem for all algorithms (3s delay inbetween)
def solve() -> None:
    # Solve for BFS
    solution, sequence, timeTaken, cost, nodes, explored = BFS.main(problems[problem - 1], maxTime, vehicles)
    runFunc(solution, sequence, timeTaken, cost, nodes, 0)

    # Solve for ID
    solution, sequence, timeTaken, cost, nodes = ID.main(problems[problem - 1], maxTime, vehicles)
    runFunc(solution, sequence, timeTaken, cost, nodes, 1)

    # Solve for A*
    solution, sequence, timeTaken, cost, nodes = ASTAR.main(problems[problem - 1], maxTime, vehicles)
    runFunc(solution, sequence, timeTaken, cost, nodes, 2)

    # Solve for Hill-climbing (greedy, random restart, and randomised)
    solution, sequence, timeTaken, cost = HC.greedy(problems[problem - 1], maxTime, vehicles)
    runFunc(solution, sequence, timeTaken, cost, cost, 3)

    # Solve for Random Restart Hill-climbing
    solution, sequence, timeTaken, cost, nodes = HC.randRestart(problems[problem - 1], maxTime, vehicles, explored, tests[5])
    runFunc(solution, sequence, timeTaken, cost, nodes, 4)
    print("solved!")

# Prints problem solutions to an output file
def printOut(file, p: int, solution: str, sequence: str, nodes: int, timeTaken: float, cost: int, type: str) -> float:
    file.write("[" + type + " | Problem: " + str(p // 5 + 1) + "] := ")
    # Prints path cost, difference to actual path cost, nodes traversed, time taken and sequence to achieve goal state from initial state
    # Alternatively prints steps taken for both hill-climbing algorithms and number of restarts for random restarts
    if solution != "....................................":
        dif = cost - (len(sols[p//5]) - 8)//4
        file.write("Path cost (depth - 1): " + str(cost) + " | Difference: " + str(dif) + " | Nodes: " + str(nodes) + " | ~" + str(int(timeTaken)) + "ms elapsed | " + sequence + "\n")
    # Prints out failure (found to only be printed if the algorithm exceeds the time limit)
    else:
        file.write("FAILED!\n")
    p += 1
    screen.update()
    return p

# Solve all problems and save to file (WILL TAKE TIME - PLEASE BE PATIENT)
def all() -> None:
    try:
        file = open("out.txt", "w")
    except IOError:
        print("Failed to open file!")
    global vehicles
    n = 0
    for p in problems:
        file.write("--------------------------------------------------------------------------------------------- Problem: " + str(n//5 + 1) + "\n")
        vehicles = helper.setupVehicles(p, initial)
        boardSetup.updatePen(pen, -448, 310, n//5 + 1, sols[n//5])
        screen.update()
        print(p)
        # Solve for BFS
        solution, sequence, timeTaken, cost, nodes, explored = BFS.main(p, maxTime, vehicles)
        n = printOut(file, n, solution, sequence, nodes, timeTaken, cost, "BFS")
        # Solve for ID
        solution, sequence, timeTaken, cost, nodes = ID.main(p, maxTime, vehicles)
        n = printOut(file, n, solution, sequence, nodes, timeTaken, cost, "ID ")
        # Solve for A*
        solution, sequence, timeTaken, cost, nodes = ASTAR.main(p, maxTime, vehicles)
        n = printOut(file, n, solution, sequence, nodes, timeTaken, cost, "A* ")
        # Solve for Greedy Hill-climbing
        solution, sequence, timeTaken, cost = HC.greedy(p, maxTime, vehicles)
        n = printOut(file, n, solution, sequence, cost, timeTaken, cost, "GHC")
        # Solve for Random Restart Hill-climbing
        solution, sequence, timeTaken, cost, nodes = HC.randRestart(p, maxTime, vehicles, explored)
        n = printOut(file, n, solution, sequence, nodes, timeTaken, cost, "RHC")
        # Setup board for next lot of vehicles
    right()
    file.close()
    print("finished!")

# Move to next problem
def right(mx: int = 0, my: int = 0) -> None:
    global problem, vehicles
    if (mx == 0 and my == 0) or helper.checkLocation(mx, my, -400, 350, 50, 50):
        problem += 1
        if problem > 40:
            problem = 1
        vehicles = helper.setupVehicles(problems[problem - 1], initial)
        boardSetup.updatePen(pen, -448, 310, problem, sols[problem - 1])
        for board in tests:
            helper.setupVehicles(problems[problem - 1], board)

# Revert to prev. problem
def left(mx: int = 0, my: int = 0) -> None:
    global problem, vehicles
    if (mx == 0 and my == 0) or helper.checkLocation(mx, my, -550, 350, 50, 50):
        problem -= 1
        if problem < 1:
            problem = 40
        vehicles = helper.setupVehicles(problems[problem - 1], initial)
        boardSetup.updatePen(pen, -448, 310, problem, sols[problem - 1])
        for board in tests:
            helper.setupVehicles(problems[problem - 1], board)

# Set interrupts for key presses
screen.listen()
screen.onkeypress(turtle.bye, "q")
screen.onkeypress(right, "Right")
screen.onkeypress(left, "Left")
screen.onkeypress(solve, "s")
screen.onkeypress(all, "r")
screen.onclick(interact)

# Main loop
while True:
    screen.update()