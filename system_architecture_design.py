from abc import ABC, abstractmethod
from typing import List
import numpy as np

#Вопросы:
#1. Нужна структура данных для хранения поисковой информации типа дерева
#2. Нужна сруктура данных для очереди интервалов
#3. Подумать о визуализации (параметры и методы представления)

from enum import Enum

class FunctionType(Enum):
    OBJECTIV = 1
    CONSTRAINT = 2

class Point:
    def __init__(self,
                 floatVariables: np.ndarray(shape = (1), dtype = np.double),
                 discreteVariables: np.ndarray(shape = (1), dtype = str),
                ):
        self.floatVariables = floatVariables
        self.discreteVariables = discreteVariables

class FunctionValue:
    def __init__(self,
                 type: FunctionType = FunctionType.OBJECTIV,
                 functionID: str = ""
                ):
        self.type = type
        self.functionID = functionID
        self.value: np.double = 0.0

class SolutionValue(FunctionValue):
    def __init__(self,
                 calculationsNumber: int = -1,
                 holderConstantsEstimations: np.double = -1.0
                ):
        self.calculationsNumber = calculationsNumber
        self.holderConstantsEstimations = holderConstantsEstimations

class TrialPoint(Point):
    def __init__(self,
                 point: Point,
                 functionValues: np.ndarray(shape = (1), dtype = FunctionValue)
                ):
        self.point = point
        self.functionValues = functionValues


class Problem(ABC):
    """Base class for optimization problems"""

    def __init__(self):
        self.numberOfVariables: int = 0
        self.numberOfObjectives: int = 0
        self.numberOfConstraints: int = 0

        self.variableNames: np.ndarray(shape = (1), dtype = str) = []

        self.lowerBound: np.ndarray(shape = (1), dtype = np.double) = []
        self.upperBound: np.ndarray(shape = (1), dtype = np.double) = []

        self.knownOptimum: np.ndarray(shape = (1), dtype = TrialPoint) = []

    @abstractmethod
    def calculate(self, point: Point, functionValue: FunctionValue) -> FunctionValue:
        """
        Compute selected function at given point.
        For any new problem that inherits from :class:`Problem`, this method should be replaced.
        :return: Calculated function value."""
        pass


class SolverParameters:
    def __init__(self,
                 eps: np.double = 0.01,
                 r: np.double = 2.0,
                 itersLimit: int = 20000,
                 evolventDensity: int = 12,
                 epsR: np.double = 0.001,
                 refineSolution: bool = False,
                 startPoint: Point = []
                ):
        """
        :param eps:method tolerance. Less value -- better search precision, less probability of early stop.
        :param r: reliability parameter. Higher value of r -- slower convergence, higher chance to cache the global minima.
        :param itersLimit: max number of iterations.
        :param evolventDensity:density of evolvent. By default density is 2^-12 on hybercube [0,1]^N,
               which means that maximum search accuracyis 2^-12.
               If search hypercube is large the density can be increased accordingly to achieve better accuracy.
        :param epsR: parameter which prevents method from paying too much attention to constraints. Greater values of
               this parameter speed up convergence, but global minima can be lost.
        :param refineSolution: if true, the final solution will be refined with the HookJeves method.
        """
        self.eps = eps
        self.r = r
        self.itersLimit = itersLimit
        self.evolventDensity = evolventDensity
        self.epsR = epsR
        self.refineSolution = refineSolution
        self.startPoint = startPoint

class Solution:
    def __init__(self,
                 numberOfVariables: int,
                 numberOfObjectives: int,
                 numberOfConstraints: int,
                 variableNames: List[str],

                 lowerBound: np.ndarray(shape = (1), dtype = np.double),
                 upperBound: np.ndarray(shape = (1), dtype = np.double),

                 bestTrials: np.ndarray(shape = (1), dtype = TrialPoint),

                 numberOfGlobalTrials: int,
                 numberOfLocalTrials: int,
                 solvingTime: np.double,

                 solutionAccuracy: np.double
                ):
        self.numberOfVariables = numberOfVariables
        self.numberOfObjectives = numberOfObjectives
        self.numberOfConstraints = numberOfConstraints
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.variableNames = variableNames

        self.bestTrials = bestTrials

        self.numberOfGlobalTrials = numberOfGlobalTrials
        self.numberOfLocalTrials = numberOfLocalTrials
        self.solvingTime = solvingTime
        self.solvingTime = solutionAccuracy

class Solver:
    def __init__(self,
                 problem: Problem,
                 parameters: SolverParameters = SolverParameters()
                ):
        """

        :param problem: Optimization problem
        :param parameters: Parameters for solving the problem
        """
        self.problem = problem
        self.parameters = parameters

    def solve(self) -> Solution:
        """
        Retrieve a solution with check of the stop conditions
        :return: Solution for the optimization problem
        """

    def performeGlobalIteration(self, number: int = 1):
        """
        :param number: The number of iterations of the global search performed
        """

    def performeLocalIteration(self, number: int = 1):
        """
        :param number: The number of iterations of the local search performed
        """

    def getResults(self) -> Solution:
        """
        :return: Return current solution for the optimization problem
        """
    def saveProgress(self, fileName: str):
        """
        :return:
        """

    def loadProgress(self, fileName: str):
        """
        :return:
        """
