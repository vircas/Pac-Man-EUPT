# coding=utf-8
# search.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Virginia Casino
#
# Attribution Information: The Pacman AI projects were developed at EUPT University of Zaragoza.
# The class was created by Virginia Casino (780722@unizar.es).
from datastructures import *
import math


class Node(object):
    """
    This class is used to represent nodes of the search tree.  Each
    node contains a state representation, a reference to the node's
    parent node, a string that describes the action that generated
    the node's state from the parent state, the path cost g from
    the start node to this node, and the estimated path cost h
    from this node to the goal node.
    """

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if other:
            return (self.state.config.pos == other.state.config.pos) and \
                   (self.state.numFood == other.state.numFood) and \
                   (self.state.food == other.state.food)
        else:
            return False

    def expand(self):
        successors = []
        for (newState, action) in self.state.next_states(self.state):
            newNode = Node(newState, self, action)
            successors.append(newNode)
        return successors


# ----------------------------------------------------------------------


def uninformed_search(initial_state, goal_state, frontier):
    """
        Parameters:
            initial_state: search initial state (PacmanState class object)
            goal_state: initial search state (PacmanState class object)
            frontier: data structure to contain the states of the border (class object
               contained in the DataStructures module)
    """

    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0

    """
        Rellenar con el codigo necesario para realizar una busqueda no informada
        siguiendo el pseudocodigo de los apuntes (Graph-Search)
        La funcion debe devolver una tupla con 3 variables:
            1. Nodo del grafo con el estado objetivo (None si no se ha alcanzado el objetivo)
            2. Numero de nodos expandidos (expanded)
            3. Numero de nodos generados (generated)
    """

    return (None, expanded, generated)

# ----------------------------------------------------------------------
# Test functions for uninformed search


def breadth_first(initial_state, goal_state):
    frontier = None  # Indicar estructura de datos adecuada para breadth_first
    return uninformed_search(initial_state, goal_state, frontier)


def depth_first(initial_state, goal_state):
    frontier = None  # Indicar estructura de datos adecuada para depth_first
    return uninformed_search(initial_state, goal_state, frontier)


def uniform_cost(initial_state, goal_state):
    frontier = None  # Indicar estructura de datos adecuada para uniform_cost
    return uninformed_search(initial_state, goal_state, frontier)


# ----------------------------------------------------------------------

def informed_search(initial_state, goal_state, frontier, heuristic):
    """
        Parameters:
            initial_state: search initial state (PacmanState class object)
            goal_state: initial search state (PacmanState class object)
            frontier: data structure to contain the states of the border (class object
               contained in the DataStructures module)
            heuristic: heuristic function used to guide the search process. The
               function receives two parameters (current state and target state) and returns
               an estimate of cost between both states
    """
    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0

    """
        Rellenar con el codigo necesario para realizar una busqueda no informada
        siguiendo el pseudocodigo de los apuntes (Graph-Search), modificada para
        actualizar el valor heuristico (h) de los nodos
        La funcion debe devolver una tupla con 3 variables:
            1. Nodo del grafo con el estado objetivo (None si no se ha alcanzado el objetivo)
            2. Numero de nodos expandidos (expanded)
            3. Numero de nodos generados (generated)
    """

    return (None, expanded, generated)


# ----------------------------------------------------------------------
# Test functions for informed search


def greedy(initial_state, goal_state, heuristic):
    frontier = None # Indicar estructura de datos adecuada para greedy
    return informed_search(initial_state, goal_state, frontier, heuristic)


def a_star(initial_state, goal_state, heuristic):
    frontier = None # Indicar estructura de datos adecuada para A*
    return informed_search(initial_state, goal_state, frontier, heuristic)

# ---------------------------------------------------------------------
# Heuristic functions


def h1(current_state, goal_state):
    return 0

# ---------------------------------------------------------------------


def show_solution(node, expanded, generated):
    path = []
    index = 1
    while node is not None:
        path.insert(0, node)
        node = node.parent
    if path:
        print("Solution took %d steps" % (len(path)))
        for pathSelection in path:
            print(str(index) + ") " + str(pathSelection.state) + "\n    Action: " + str(pathSelection.action))
            index += 1
    print("Nodes expanded:  %d" % expanded)
    print("Nodes generated: %d\n" % generated)
