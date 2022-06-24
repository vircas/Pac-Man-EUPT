# coding=utf-8
# game.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu and Virginia Casino.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# Also, it is modified by Virginia Casino (780722@unizar.es)


# game.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu), Dan Klein (klein@cs.berkeley.edu)
# and Virginia Casino (780722@unizar.es).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import traceback
from gameState import GameState


class Agent(object):
    def __init__(self, index=0):
        self.index = index


class Directions(object):
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'


class Configuration(object):
    """
    A Configuration holds the (x,y) coordinate of a character, along with its
    traveling direction.

    The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases
    horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __eq__(self, other):
        if other is None:
            return False
        return self.pos is other.pos and self.direction is other.direction

    def __str__(self):
        return "(x,y)=" + str(self.pos) + ", " + str(self.direction)

    def generateSuccessor(self, vector):
        """
        Generates a new configuration reached by translating the current
        configuration by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.

        Actions are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vectorToDirection(vector)
        if direction == Directions.STOP:
            direction = self.direction  # There is no stop direction
        return Configuration((x + dx, y + dy), direction)


class Grid(object):
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.
    """

    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]:
            raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return sum([x.count(item) for x in self.data])

    def asList(self, key=True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] is key:
                    list.append((x, y))
        return list

    def _cellIndexToPosition(self, index):
        x = index / self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        """
        Fills in data from a bit-level representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height:
                    break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0:
            print('ValueError, must be a positive integer')
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools

####################################
# Parts you shouldn't have to read #
####################################


class Actions(object):
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST: (1, 0),
                   Directions.WEST: (-1, 0),
                   Directions.STOP: (0, 0)}
    _directionsAsList = _directions.items()

    TOLERANCE = .001

    def vectorToDirection(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP
    vectorToDirection = staticmethod(vectorToDirection)

    def directionToVector(direction, speed=1.0):
        dx, dy = Actions._directions[direction]
        return dx * speed, dy * speed
    directionToVector = staticmethod(directionToVector)

    def getPossibleActions(config, walls):
        possible = []
        x, y = config.pos
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE:
            return [config.direction]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                possible.append(dir)

        return possible
    getPossibleActions = staticmethod(getPossibleActions)


class Game(object):
    """
    The Game manages the control flow, soliciting actions from agents.
    """

    def __init__(self, agents, display, rules, startingIndex=0):
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.startingIndex = startingIndex
        self.gameOver = False

    def _agentCrash(self, agentIndex):
        """Helper method for handling agent crashes"""
        traceback.print_exc()
        self.gameOver = True
        self.agentCrashed = True
        self.rules.agentCrash(self, agentIndex)

    def run(self, steps):
        """
        Main control loop for game play.
        """
        keyboardAgent = False
        self.display.initialize(self.state.data)

        # inform learning agents of the game start
        for i in range(len(self.agents)):
            agent = self.agents[i]

            if str(agent).__contains__("KeyboardAgent"):
                keyboardAgent = True
            if not agent:
                # this is a null agent, meaning it failed to load the other team wins
                print("Agent %d failed to load" % i)
                self._agentCrash(i)
                return
            if "registerInitialState" in dir(agent):
                agent.registerInitialState(self.state.deepCopy())

        agentIndex = self.startingIndex
        numAgents = len(self.agents)

        index = 0
        while not self.gameOver:
            # for step in steps:
            if index > (len(steps) - 1):
                self.gameOver = True
                print('No more steps!')
                return

            # Fetch the next agent
            agent = self.agents[agentIndex]
            # Generate an observation of the state
            observation = self.state.deepCopy()

            # Solicit an action
            if agentIndex == 0 and (not keyboardAgent):
                action = steps[index]
                index += 1
            else:
                action = agent.getAction(observation)

            # Execute the action
            self.state = self.executeAction(agentIndex, action)
            # Change the display
            self.display.update(self.state.data)
            # Allow for game specific conditions (winning, losing, etc.)
            self.rules.process(self.state, self)
            # Next agent
            agentIndex = (agentIndex + 1) % numAgents

        self.display.finish()

    def executeAction(self, agentIndex, action):
        state = self.state.deepCopy()

        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0:  # Pacman is moving
            state.data._eaten = [False for i in range(state.getNumAgents())]
            PacmanRules.applyAction(state, action)
        else:  # A ghost is moving
            GhostRules.applyAction(state, action, agentIndex)

        # Time passes
        if agentIndex != 0:
            GhostRules.decrementTimer(state.data.agentStates[agentIndex])

        # Resolve multi-agent effects
        GhostRules.checkDeath(state, agentIndex)

        # Book keeping
        state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange

        return state


############################################################################
#                         RULES OF THE PACMAN GAME                         #
#                                                                          #
# You shouldn't need to look through the code in this section of the file. #
############################################################################


SCARED_TIME = 40  # Moves ghosts are scared
COLLISION_TOLERANCE = 0.7  # How close ghosts must be to Pacman to kill
TIME_PENALTY = 1  # Number of points lost each round


class ClassicGameRules(object):
    """
    These game rules manage the control flow of a game, deciding when
    and how the game starts and ends.
    """

    def newGame(self, layout, pacmanAgent, ghostAgents, display):
        agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
        initState = GameState()
        initState.initialize(layout, len(ghostAgents))
        game = Game(agents, display, self)
        game.state = initState
        return game

    def process(self, state, game):
        if state.isWin():
            self.win(state, game)
        if state.isLose():
            self.lose(state, game)

    @staticmethod
    def win(state, game):
        print("Pacman emerges victorious! Score: %d" % state.data.score)
        game.gameOver = True

    @staticmethod
    def lose(state, game):
        print("Pacman died! Score: %d" % state.data.score)
        game.gameOver = True

    @staticmethod
    def agentCrash(agentIndex):
        if agentIndex == 0:
            print("Pacman crashed")
        else:
            print("A ghost crashed")


class PacmanRules(object):
    """
    These functions govern how pacman interacts with his environment under
    the classic game rules.
    """
    PACMAN_SPEED = 1

    def applyAction(state, action):
        """
        Edits the state to reflect the results of the action.
        """
        legal = Actions.getPossibleActions(state.getPacmanState().configuration, state.data.layout.walls)
        if action not in legal:
            print("Illegal action " + str(action))

        pacmanState = state.data.agentStates[0]

        # Update Configuration
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.configuration = pacmanState.configuration.generateSuccessor(vector)

        # Eat
        next = pacmanState.configuration.pos
        nearest = nearestPoint(next)
        manhattanDistance = abs(nearest[0] - next[0]) + abs(nearest[1] - next[1])
        if manhattanDistance <= 0.5:
            # Remove food
            PacmanRules.consume(nearest, state)
    applyAction = staticmethod(applyAction)

    def consume(position, state):
        x, y = position
        # Eat food
        if state.data.food[x][y]:
            state.data.scoreChange += 10
            state.data.food = state.data.food.copy()
            state.data.food[x][y] = False
            state.data._foodEaten = position
            numFood = state.getNumFood()
            if numFood == 0 and not state.data._lose:
                state.data._win = True
        # Eat capsule
        if position in state.getCapsules():
            state.data.capsules.remove(position)
            state.data._capsuleEaten = position
            # Reset all ghosts' scared timers
            for index in range(1, len(state.data.agentStates)):
                state.data.agentStates[index].scaredTimer = SCARED_TIME
    consume = staticmethod(consume)

class GhostRules(object):
    """
    These functions dictate how ghosts interact with their environment.
    """
    GHOST_SPEED = 1.0

    def applyAction(state, action, ghostIndex):
        conf = state.getGhostState(ghostIndex).configuration
        legal = Actions.getPossibleActions(conf, state.data.layout.walls)
        if action not in legal:
            print("Illegal ghost action " + str(action))

        ghostState = state.data.agentStates[ghostIndex]
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector)
    applyAction = staticmethod(applyAction)

    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint(ghostState.configuration.pos)
        ghostState.scaredTimer = max(0, timer - 1)
    decrementTimer = staticmethod(decrementTimer)

    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0:  # Pacman just moved; Anyone can kill him
            for index in range(1, len(state.data.agentStates)):
                ghostState = state.data.agentStates[index]
                ghostPosition = ghostState.configuration.pos
                if GhostRules.canKill(pacmanPosition, ghostPosition):
                    GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.data.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.pos
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)
    checkDeath = staticmethod(checkDeath)

    def collide(state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            GhostRules.placeGhost(state)
            ghostState.scaredTimer = 0
            # Added for first-person
            state.data._eaten[agentIndex] = True
        else:
            if not state.data._win:
                state.data._lose = True
    collide = staticmethod(collide)

    def canKill(pacmanPosition, ghostPosition):
        manhattanDistance = abs(ghostPosition[0] - pacmanPosition[0]) + abs(ghostPosition[1] - pacmanPosition[1])
        return manhattanDistance <= COLLISION_TOLERANCE
    canKill = staticmethod(canKill)

    def placeGhost(ghostState):
        ghostState.configuration = ghostState.start
    placeGhost = staticmethod(placeGhost)


def nearestPoint(pos):
    """
    Finds the nearest grid point to a position (discretizes).
    """
    (current_row, current_col) = pos

    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)
    return grid_row, grid_col
