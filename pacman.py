# coding=utf-8
# pacman.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu and Virginia Casino.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay,
# Pieter Abbeel (pabbeel@cs.berkeley.edu) and Virginia Casino (780722@unizar.es)


"""
Pacman.py holds the logic for the classic pacman game along with the main
code to run a game.  This file is divided into three sections:

  (i)  Your interface to the pacman world:
          Pacman is a complex environment.  You probably don't want to
          read through all of the code we wrote to make the game runs
          correctly.  This section contains the parts of the code
          that you will need to understand in order to complete the
          project.  There is also some code in game.py that you should
          understand.

  (ii)  The hidden secrets of pacman:
          This section contains all of the logic code that the pacman
          environment uses to decide who can move where, who dies when
          things collide, etc.  You shouldn't need to read this section
          of code, but you can if you want.

  (iii) Framework to start a game:
          The final section contains the code for reading the command
          you use to set up the game, then starting up a new game, along with
          linking in all the external parts (agent functions, graphics).
          Check this section out to see all the options available to you.

To play your first game, type 'python pacman.py' from the command line.
The keys are 'a', 's', 'd', and 'w' to move (or arrow keys).  Have fun!
"""

import __main__
import sys
from graphics import graphicsDisplay, layout as layoutlib
from game import Directions, ClassicGameRules
from pacmanState import PacmanState
from search import *


def loadAgent(agent):
    """
        Get agent object specified.
    """
    moduleName = 'agents.py'
    try:
        module = __import__(moduleName[:-3])
    except ImportError:
        print('The modulename ' + moduleName + ' is not specified in the Project.')
        return

    if agent in dir(module):
        return getattr(module, agent)
    print('The agent ' + agent + ' is not specified in any *Agents.py.')


def getLayout(layoutDesign):
    """
        Get layout design specified.
    """
    layout = layoutlib.getLayout(layoutDesign)
    if layout is None:
        print("The layout cannot be found")
        sys.exit(-1)
    return layout


def runGames(pacmanAgent, zoom, frameTime, numGames, steps):
    """
        Executes the game with interface.
    """
    layout = layoutlib.getLayout(LAYOUT)
    # PACMAN
    pacmanType = loadAgent(pacmanAgent)
    pacman = pacmanType()

    # GHOST
    ghostType = loadAgent('GhostAgent')
    # Si se desea que no aparezcan fantasmas para poder ver la actuación del Pac-Man entero
    # cambiar layout.numGhosts por 0
    ghosts = [ghostType(i + 1) for i in range(layout.numGhosts)]

    # DISPLAY
    display = graphicsDisplay.PacmanGraphics(zoom, frameTime)
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules()
    games = []

    for i in range(numGames):
        game = rules.newGame(layout, pacman, ghosts, display)
        game.run(steps)
        games.append(game)

    # RESULTADOS
    scores = [game.state.getScore() for game in games]
    wins = [game.state.isWin() for game in games]
    winRate = wins.count(True) / float(len(wins))
    winStr = (str(([['Loss', 'Win'][int(w)] for w in wins])).
              replace("[", "").replace("]", "").replace("'", ""))

    print('Average Score: ' + str(sum(scores) / float(len(scores))))
    print('Scores:        ' + str(scores).replace("[", "").replace("]", ""))
    print('Win Rate:      ' + str(wins.count(True)) + "/" +
          str(len(wins)) + " (" + str(winRate) + ")")
    print ('Record:       ' + winStr)

    return games


if __name__ == '__main__':

    # LAYOUT #############################################################
    # Se puede seleccionar el tipo de laberinto de diseño que se desea utilizar, estos están disponibles en
    #  la carpeta de layout
    LAYOUT = 'testClassic3'
    layout = getLayout(LAYOUT)

    # PACMAN #############################################################
    # Si se desea emplear los algoritmos de búsquedas hay que poner 'IntelligentAgent'
    PACMAN_AGENT = 'KeyboardAgent'

    # DISPLAY ############################################################
    ZOOM = 1
    FRAME_TIME = 0.1

    NUM_GAMES = 1

    # SEARCH #############################################################
    steps = []
    PacmanState.walls = layout.walls
    food = layout.food.data

    init_state = PacmanState(layout.totalFood, layout.agentPositions[0][1], Directions.STOP, food)
    goal_state = PacmanState(0, layout.agentPositions[0][1], Directions.STOP, food)

    # Breadth First Search algorithm ----------------------------------------
    solution_bf, expanded, generated = breadth_first(init_state, goal_state)
    if solution_bf is not None:
        print("Breadth_first found a solution...")
        show_solution(solution_bf, expanded, generated)

        solution = solution_bf
        while solution is not None:
            if solution.action is not None:
                steps.insert(0, solution.action)
            solution = solution.parent

        runGames(PACMAN_AGENT, ZOOM, FRAME_TIME, NUM_GAMES, steps)
    else:
        print("Breadth_first failed...")

    # Depth First Search algorithm ----------------------------------------
    solution_bf, expanded, generated = depth_first(init_state, goal_state)
    if solution_bf is not None:
        print("Depth_first found a solution...")
        show_solution(solution_bf, expanded, generated)

        solution = solution_bf
        while solution is not None:
            if solution.action is not None:
                steps.insert(0, solution.action)
            solution = solution.parent

        runGames(PACMAN_AGENT, ZOOM, FRAME_TIME, NUM_GAMES, steps)
    else:
        print("Depth_first failed...")

    # Uniform Cost Search algorithm ----------------------------------------
    solution_bf, expanded, generated = uniform_cost(init_state, goal_state)
    if solution_bf is not None:
        print("Uniform-cost found a solution...")
        show_solution(solution_bf, expanded, generated)

        solution = solution_bf
        while solution is not None:
            if solution.action is not None:
                steps.insert(0, solution.action)
            solution = solution.parent

        runGames(PACMAN_AGENT, ZOOM, FRAME_TIME, NUM_GAMES, steps)
    else:
        print("Uniform-cost failed...")

    # Greedy Search algorithm ----------------------------------------
    solution_bf, expanded, generated = greedy(init_state, goal_state, h1)
    if solution_bf is not None:
        print("Greedy found a solution...")
        show_solution(solution_bf, expanded, generated)

        solution = solution_bf
        while solution is not None:
            if solution.action is not None:
                steps.insert(0, solution.action)
            solution = solution.parent

        runGames(PACMAN_AGENT, ZOOM, FRAME_TIME, NUM_GAMES, steps)
    else:
        print("Greedy failed...")

    # A* Search algorithm ----------------------------------------
    solution_bf, expanded, generated = a_star(init_state, goal_state, h1)
    if solution_bf is not None:
        print("A_star found a solution...")
        show_solution(solution_bf, expanded, generated)

        solution = solution_bf
        while solution is not None:
            if solution.action is not None:
                steps.insert(0, solution.action)
            solution = solution.parent

        runGames(PACMAN_AGENT, ZOOM, FRAME_TIME, NUM_GAMES, steps)
    else:
        print("A_star failed...")