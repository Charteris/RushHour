# Helper functions for ease and to reduce clutter in main
import turtle, boardSetup
from typing import List, Tuple

# Initialise vehicle arrays
def init(screen: turtle.Screen) -> Tuple[List[turtle.Turtle], List[turtle.Turtle], turtle.Turtle]:
    # Implement vehicle sprites and create vehicles
    cars, trucks = [], []
    for i in range(11):
        # Vehicles initially inactive until board is drawn
        string = 'Car' + chr(ord('A') + i) + '.gif'
        screen.register_shape(string)
        screen.register_shape('S' + string)
        cars.append(boardSetup.vehicle(string))
        cars[len(cars) - 1].active = 0
        cars[len(cars) - 1].dir = 0

    for i in range(4):
        string = 'Truck' + chr(ord('O') + i) + '.gif'
        screen.register_shape(string)
        screen.register_shape('S' + string)
        trucks.append(boardSetup.vehicle(string))
        trucks[len(trucks) - 1].active = 0
        trucks[len(trucks) - 1].dir = 0

    screen.register_shape('CarX.gif')
    screen.register_shape('SCarX.gif')
    target = boardSetup.vehicle('CarX.gif')
    target.active = 1
    target.dir = 0
    return (cars, trucks, target)

# Specification for class node which holds current state, parent state, and action sequence
class Node:
    def __init__(self, state: str, parent: str, dir: int, cost: int = 0, h: int = 0) -> None:
        self.state = state
        self.parent = parent
        self.dir = dir
        self.cost = cost
        self.f = cost + h
    # Overload <
    def __lt__(self, other):
        return self.f < other.f
    # Overload ==
    def __eq__(self, other: str) -> bool:
        return self.state == other

# Place vehicles from board coords
def moveVehicle(vehicle: str, x: int, y: int, scale: int, shape: str, dir: int) -> None:
    # Set position and direction (shape), as well as setting as active
    vehicle.setposition(scale / 2 + x, scale*3 + y - scale / 2)
    vehicle.shape(shape)
    vehicle.showturtle()
    vehicle.dir = dir # 0 is vertical, 1 is horizontal
    vehicle.active = 1

# Cycles through the given 'map' (problem)
def setupVehicles(map: str, board: turtle.Turtle) -> List[Tuple[str, int]]:
    c, t = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'], ['O', 'P', 'Q', 'R']
    if len(map) != 36:
        return None
    for y in range(6):
        for x in range(6):
            char = map[y*6 + x]

            n = 0
            while n < len(c):
                if char == c[n]: # Cars
                    if y < 5 and map[(y+1)*6 + x] == c[n]: # Vertical check
                        moveVehicle(board.cars[ord(c[n]) - 65], board.x + x*board.scale, board.y - y*board.scale - board.scale / 2, board.scale, 'SCar' + c[n] + '.gif', 0)
                    elif x < 5 and map[y*6 + x + 1] == c[n]: # Horizontal check
                        moveVehicle(board.cars[ord(c[n]) - 65], board.x + x*board.scale + board.scale / 2, board.y - y*board.scale, board.scale,'Car' + c[n] + '.gif', 1)
                    c.pop(n)
                else:
                    n += 1

            n = 0
            while n < len(t):
                if char == t[n]: # Trucks
                    if y < 4 and map[(y + 1) * 6 + x] == t[n]:  # Vertical check
                        moveVehicle(board.trucks[ord(t[n]) - ord('O')], board.x + x*board.scale, board.y - y*board.scale - board.scale, board.scale, 'STruck' + t[n] + '.gif', 0)
                    elif x < 4 and map[y * 6 + x + 1] == t[n]:  # Horizontal check
                        moveVehicle(board.trucks[ord(t[n]) - ord('O')], board.x + x*board.scale + board.scale, board.y - y*board.scale, board.scale, 'Truck' + t[n] + '.gif', 1)
                    t.pop(n)
                else:
                    n += 1

            if char == 'X': # Target vehicle
                if y < 5 and map[(y + 1) * 6 + x] == 'X':  # Vertical check
                    moveVehicle(board.target, board.x + x*board.scale, board.y - y*board.scale - board.scale / 2, board.scale, 'SCarX.gif', 0)
                elif x < 5 and map[y * 6 + x + 1] == 'X':  # Horizontal check
                    moveVehicle(board.target, board.x + x*board.scale + board.scale / 2, board.y - y*board.scale, board.scale, 'CarX.gif', 1)
                    x += 1
    for i in range(len(c)):
        board.cars[ord(c[i]) - ord('A')].hideturtle()
        board.cars[ord(c[i]) - ord('A')].active = 0
    for i in range(len(t)):
        board.trucks[ord(t[i]) - ord('O')].hideturtle()
        board.trucks[ord(t[i]) - ord('O')].active = 0

    # Finds the total number of vehicles used
    vehicles = []
    for i in range(len(board.cars)):
        if board.cars[i].active:
            vehicles.append( (chr(ord('A') + i), board.cars[i].dir) )
    for i in range(len(board.trucks)):
        if board.trucks[i].active:
            vehicles.append( (chr(ord('O') + i), board.trucks[i].dir) )
    vehicles.append( ('X', board.target.dir) )
    return vehicles

# Returns whether the mouse is in a designated position
def checkLocation(tx: int, ty: int, rx: int, ry: int, width: int, height: int) -> bool:
	if tx > rx and ty < ry and tx < rx + width and ty > ry - height:
		return True
	return False