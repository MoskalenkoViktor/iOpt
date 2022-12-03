import sys

import numpy as np
from depq import DEPQ

from iOpt.problem import Problem
from iOpt.solution import Solution
from iOpt.trial import FunctionValue, Point, Trial

# from bintrees import AVLTree


class SearchDataItem(Trial):
    def __init__(self, y: Point, x: np.double,
                 functionValues: np.ndarray(shape=(1), dtype=FunctionValue) = [FunctionValue()],
                 discreteValueIndex: int = 0):
        super().__init__(point=y, functionValues=functionValues)
        self.point = y
        self.__x = x
        self.__discreteValueIndex = discreteValueIndex
        self.__index: int = -2
        self.__z: np.double = sys.float_info.max
        self.__leftPoint: SearchDataItem = None
        self.__rightPoint: SearchDataItem = None
        self.delta: np.double = -1.0
        self.globalR: np.double = -1.0
        self.localR: np.double = -1.0
        self.iterationNumber: int = -1

    def GetX(self) -> np.double:
        return self.__x

    def GetY(self) -> Point:
        return self.point

    def GetDiscreteValueIndex(self) -> int:
        return self.__discreteValueIndex

    def SetIndex(self, index: int):
        self.__index = index

    def GetIndex(self) -> int:
        return self.__index

    def SetZ(self, z: np.double):
        self.__z = z

    def GetZ(self) -> np.double:
        return self.__z

    def SetLeft(self, point: 'SearchDataItem'):
        self.__leftPoint = point

    def GetLeft(self) -> 'SearchDataItem':
        return self.__leftPoint

    def SetRight(self, point: 'SearchDataItem'):
        self.__rightPoint = point

    def GetRight(self) -> 'SearchDataItem':
        return self.__rightPoint

    def __lt__(self, other):
        return self.GetX() < other.GetX()


class CharacteristicsQueue:
    # __baseQueue: depq = DEPQ(iterable=None, maxlen=None)

    def __init__(self, maxlen: int):
        self.__baseQueue = DEPQ(iterable=None, maxlen=maxlen)

    def Clear(self):
        self.__baseQueue.clear()

    def Insert(self, key: np.double, dataItem: SearchDataItem):
        # приоритет - значение характеристики
        self.__baseQueue.insert(dataItem, key)

    def GetBestItem(self) -> (SearchDataItem, np.double):
        return self.__baseQueue.popfirst()

    def IsEmpty(self):
        return self.__baseQueue.is_empty()

    def GetMaxLen(self) -> int:
        return self.__baseQueue.maxlen

    def GetLen(self) -> int:
        return len(self.__baseQueue)


class SearchData:
    # очереди характеристик
    # _RGlobalQueue: CharacteristicsQueue = CharacteristicsQueue(None)
    # упорядоченное множество всех испытаний по X
    # __allTrials: AVLTree = AVLTree()
    # _allTrials: List = []
    # __firstDataItem:

    # solution: Solution = None

    def __init__(self, problem: Problem, maxlen: int = None):
        self.solution = Solution(problem)
        self._allTrials = []
        self._RGlobalQueue = CharacteristicsQueue(maxlen)
        self.__firstDataItem: SearchDataItem = None

    def ClearQueue(self):
        self._RGlobalQueue.Clear()

    # вставка точки если знает правую точку
    # в качестве интервала используем [i-1, i]
    # если rightDataItem == None то его необходимо найти по дереву _allTrials
    def InsertDataItem(self, newDataItem: SearchDataItem,
                       rightDataItem: SearchDataItem = None):
        flag = True
        if rightDataItem is None:
            rightDataItem = self.FindDataItemByOneDimensionalPoint(newDataItem.GetX())
            flag = False

        newDataItem.SetLeft(rightDataItem.GetLeft())
        rightDataItem.SetLeft(newDataItem)
        newDataItem.SetRight(rightDataItem)
        newDataItem.GetLeft().SetRight(newDataItem)

        self._allTrials.append(newDataItem)

        self._RGlobalQueue.Insert(newDataItem.globalR, newDataItem)
        if flag:
            self._RGlobalQueue.Insert(rightDataItem.globalR, rightDataItem)

    def InsertFirstDataItem(self, leftDataItem: SearchDataItem,
                            rightDataItem: SearchDataItem):
        leftDataItem.SetRight(rightDataItem)
        rightDataItem.SetLeft(leftDataItem)

        self._allTrials.append(leftDataItem)
        self._allTrials.append(rightDataItem)

        self.__firstDataItem = leftDataItem

    # поиск покрывающего интервала
    # возвращает правую точку
    def FindDataItemByOneDimensionalPoint(self, x: np.double) -> SearchDataItem:
        # итерируемся по rightPoint от минимального элемента
        for item in self:
            if item.GetX() > x:
                return item
        return None

    def GetDataItemWithMaxGlobalR(self) -> SearchDataItem:
        if self._RGlobalQueue.IsEmpty():
            self.RefillQueue()
        return self._RGlobalQueue.GetBestItem()[0]

    # Перезаполнение очереди (при ее опустошении или при смене оценки константы Липшица)
    def RefillQueue(self):
        self._RGlobalQueue.Clear()
        for itr in self:
            self._RGlobalQueue.Insert(itr.globalR, itr)

    # Возвращает текущее число интервалов в дереве
    def GetCount(self) -> int:
        return len(self._allTrials)

    def GetLastItem(self) -> SearchDataItem:
        try:
            return self._allTrials[-1]
        except BaseException:
            print("GetLastItem: List is empty")

    def SaveProgress(self, fileName: str):
        """
        :return:
        """

    def LoadProgress(self, fileName: str):
        """
        :return:
        """

    def __iter__(self):
        # вернуть самую левую точку из дерева (ниже код проверить!)
        # return self._allTrials.min_item()[1]
        self.curIter = self.__firstDataItem
        if self.curIter is None:
            raise StopIteration
        else:
            return self

    def __next__(self):
        if self.curIter is None:
            raise StopIteration
        else:
            tmp = self.curIter
            self.curIter = self.curIter.GetRight()
            return tmp


class SearchDataDualQueue(SearchData):
    # __RLocalQueue: CharacteristicsQueue = CharacteristicsQueue(None)

    def __init__(self, problem: Problem, maxlen: int = None):
        super().__init__(problem, maxlen)
        self.__RLocalQueue = CharacteristicsQueue(maxlen)

    def ClearQueue(self):
        self._RGlobalQueue.Clear()
        self.__RLocalQueue.Clear()

    def InsertDataItem(self, newDataItem: SearchDataItem,
                       rightDataItem: SearchDataItem = None):
        flag = True
        if rightDataItem is None:
            rightDataItem = self.FindDataItemByOneDimensionalPoint(newDataItem.GetX())
            flag = False

        newDataItem.SetLeft(rightDataItem.GetLeft())
        rightDataItem.SetLeft(newDataItem)
        newDataItem.SetRight(rightDataItem)
        newDataItem.GetLeft().SetRight(newDataItem)

        self._allTrials.append(newDataItem)

        self._RGlobalQueue.Insert(newDataItem.globalR, newDataItem)
        self.__RLocalQueue.Insert(newDataItem.localR, newDataItem)
        if flag:
            self._RGlobalQueue.Insert(rightDataItem.globalR, rightDataItem)
            self.__RLocalQueue.Insert(rightDataItem.localR, rightDataItem)

    def GetDataItemWithMaxGlobalR(self) -> SearchDataItem:
        if self._RGlobalQueue.IsEmpty():
            self.RefillQueue()
        bestItem = self._RGlobalQueue.GetBestItem()
        while bestItem[1] != bestItem[0].globalR:
            if self._RGlobalQueue.IsEmpty():
                self.RefillQueue()
            bestItem = self._RGlobalQueue.GetBestItem()
        return bestItem[0]

    def GetDataItemWithMaxLocalR(self) -> SearchDataItem:
        if self.__RLocalQueue.IsEmpty():
            self.RefillQueue()
        bestItem = self.__RLocalQueue.GetBestItem()
        while bestItem[1] != bestItem[0].localR:
            if self.__RLocalQueue.IsEmpty():
                self.RefillQueue()
            bestItem = self.__RLocalQueue.GetBestItem()
        return bestItem[0]

    def RefillQueue(self):
        self.ClearQueue()
        for itr in self:
            self._RGlobalQueue.Insert(itr.globalR, itr)
            self.__RLocalQueue.Insert(itr.localR, itr)
