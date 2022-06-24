# coding=utf-8
# pacmanState.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to Virginia Casino
#
# Attribution Information: The Pacman AI projects were developed at EUPT University of Zaragoza.
# The class was created by Virginia Casino (780722@unizar.es).

from game import Configuration, Directions, Actions
import copy


class PacmanState(object):
    """
        The state of Pac-Man for search algorithms.
        This class is used to represent a state of the Pac-Man game.
        Each state contains the number of food that it has not been
        eaten, the matrix with the food position and the position
        of the Pac-Man.
    """
    walls = set()

    def __init__(self, numFood, position, direction, food):
        self.numFood = numFood
        self.config = Configuration(position, direction)
        self.food = food

    def __str__(self):
        to_str = "Number of food: " + str(self.numFood) + \
            "\n    Position: " + str(self.config.pos)
        return to_str

    def __eq__(self, other):
        if other is None:
            return False
        return (self.config.pos == other.config.pos) and (self.numFood == other.numFood) and (self.food == other.food)

    def succ(self, action):
        """
            Rellenar con el codigo necesario para generar un nuevo estado a partir del actual
            y una accion proporcionada como parametro. La accion tiene el formato 'East', 'South', 'North'
            or 'West' para indicar la dirección que toma. La funcion debe devolver None si el estado generado
            es invalido segun las especificaciones del problema
        """

        return None

    def next_states(self, state):
        new_states = []

        """
        Rellenar con el codigo necesario para generar la lista de nuevos estados accesibles
        desde el estado actual, aplicando las diferentes acciones posibles. Los estados deben 
        ser validos segun las especificaciones del problema. La lista debe estar formada por 
        pares (nuevo_estado, accion)
        """
        return new_states

    def getNewPosition(self, direction):
        x, y = self.config.pos

        if direction is Directions.NORTH:
            y += 1
        elif direction is Directions.SOUTH:
            y -= 1
        elif direction is Directions.EAST:
            x += 1
        elif direction is Directions.WEST:
            x -= 1
        else:
            print('ERROR')
            return

        return Configuration((x, y), direction)
