# -*- coding: utf-8 -*-

import copy

def Permulation(aList: list):
    if len(aList) <= 1:
        return [aList]
    else:
        Rankings = []
        for element in aList:
            tmpList = copy.deepcopy(aList)
            tmpList.remove(element)
            for subList in Permulation(tmpList):
                Rankings.append([element] + subList)
        return Rankings


def main():
    print(Permulation([i for i in range(5, 1)]))


if __name__ == '__main__':
    main()
