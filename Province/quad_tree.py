import sys
import pydot
from collections import OrderedDict
import csv
import operator
import ast

class Point:
    def __init__(self, x = None, y = None, xy = None, value = None):
        if value != None:
            self.x = value
            self.y = value
        elif xy != None:
            self.x = float(xy[0])
            self.y = float(xy[1])
        elif x != None and y != None:
            self.x = float(x)
            self.y = float(y)
        elif x != None and y != None and xy != None and value != None:
            exit(1)
        else:
            self.x = 0
            self.y = 0

    def __add__ (self, target):
        return Point(self.x+target.x, self.y+target.y)

    def __sub__ (self, target):
        return Point(self.x - target.x, self.y - target.y)

    def __str__(self):
        return '({} {})'.format(self.x, self.y)

    def __mul__(self, target):
        return Point(self.x * target, self.y * target)

    def __div__(self, target):
        return Point(self.x/target, self.y/target)

    def getTuple(self):
        return (self.x, self.y)

class Rectangle:

    def __init__(self, btmLeft = Point(0,0), topRight = Point(1,1)):
        self.btmLeft = btmLeft
        self.topRight = topRight
        self.halfWidth = (topRight.x - btmLeft.x)/2
        self.halfHeight = (topRight.y - btmLeft.y)/2
        self.center = Point(x = btmLeft.x + self.halfWidth, y = btmLeft.y + self.halfHeight)

    def isInside(self, point):
        if(point.x < self.btmLeft.x or point.x > self.topRight.x):
            return False
        if(point.y < self.btmLeft.y or point.y > self.topRight.y):
            return False
        return True

    def getWidth(self):
        return self.topRight.x - self.btmLeft.x

    def getHeight(self):
        return self.topRight.y - self.btmLeft.y

uid = 0
class QuadTree:
    # True : Ouput only leaf grid
    # False : Output both parent and leaf grid
    OPTIMIZE_GRID_OUTPUT = True
    boxCsvWriter = None
    treeCsvWriter = None

    def __init__(self, level = 0, rect = Rectangle(), parent = None, value = 'NULL', maxLevel = None, uid_in = None):
        self.level = level
        self.rect = rect
        self.childs =[]
        self.parent = parent
        self.value = value
        self.maxLevel = maxLevel
        if(uid_in == None):
            global uid
            self.uid = uid
            uid += 1
        else:
            self.uid = uid_in

    def createSubQTree(self):
        if(self.level >= self.maxLevel or len(self.childs) != 0):
            return

        else:
            # Quater 1
            self.childs.append(
                QuadTree(
                    level = self.level+1
                    , rect = Rectangle(
                        btmLeft = self.rect.center
                        , topRight = self.rect.topRight)
                    , parent = self
                    , maxLevel = self.maxLevel
            ))
            # Quater 2
            self.childs.append(
                QuadTree(
                    level = self.level+1
                    , rect = Rectangle(
                        btmLeft = Point(x = self.rect.btmLeft.x, y = self.rect.center.y)
                        , topRight = Point(x = self.rect.center.x, y = self.rect.topRight.y))
                    , parent = self
                    , maxLevel = self.maxLevel
            ))
            # Quater 3
            self.childs.append(
                QuadTree(
                    level = self.level+1
                    , rect = Rectangle(
                        btmLeft = self.rect.btmLeft
                        , topRight = self.rect.center)
                    , parent = self
                    , maxLevel = self.maxLevel
            ))
            # Quater 4
            self.childs.append(
                QuadTree(
                    level = self.level+1
                    , rect = Rectangle(
                        btmLeft = Point(x = self.rect.center.x, y = self.rect.btmLeft.y)
                        , topRight = Point(x = self.rect.topRight.x, y = self.rect.center.y))
                    , parent = self
                    , maxLevel = self.maxLevel
            ))

    def Span(self):
        'Span tree to maximum depth(level)'
        self.createSubQTree()
        for child in self.childs:
            child.Span()

    def SetValue(self, point, value):
        if(self.rect.isInside(point)):
            if(len(self.childs) == 0):
                self.value = value
            else:
                for child in self.childs:
                    child.SetValue(point, value)

    def AddDictValue(self, point, value):
        'Recommend only use dict with key being number'
        if(self.rect.isInside(point)):
            if(len(self.childs) == 0):
                if isinstance(self.value, dict):
                    self.value.update(value)
                    self.value = dict(OrderedDict(sorted(
                        self.value.items()
                        , reverse = True
                        , key = operator.itemgetter(0)
                        )))

                    # Remove item which have same value but lower key
                    valueList =  list(set([x for x in self.value.values() if self.value.values().count(x) > 1]))

                    for v in valueList:
                        keyList = []
                        for pair in self.value.items():
                            if pair[1] == v:
                                keyList.append(pair[0])

                        keyList = sorted(keyList)
                        del keyList[-1]
                        for key in keyList:
                            del self.value[key]

                else:
                    self.value = value
            else:
                for child in self.childs:
                    child.AddDictValue(point, value)

    def findValue(self, point):
        if(self.rect.isInside(point)):
            if(len(self.childs) == 0):
                # May change to value later
                return self.value
            else:
                for qTree in self.childs:
                    if(qTree.rect.isInside(point)):
                        return qTree.findValue(point)
        else:
            return 'NULL'

    def PrintTreeValue(self):
        for i in range(self.level):
            sys.stdout.write('\t')
        print self.value
        for child in self.childs:
            child.PrintTreeValue()

    def PrintTreeUID(self):
        for i in range(self.level):
            sys.stdout.write('\t')
        print self.uid
        for child in self.childs:
            child.PrintTreeUID()

    def resetLevel(self):
        if(self.parent == None):
            self.level = 0

        for child in self.childs:
            child.level = self.level + 1
            child.resetLevel()

    def resetUID(self):
        # Check if root node
        global uid
        if(self.parent == None):
            uid = 0
        self.uid = uid
        uid += 1
        for child in self.childs:
            child.resetUID()

    def GroupChilds(self):
        if(len(self.childs) == 0):
            return

        # Optimize all child node
        for child in self.childs:
            if(len(child.childs) != 0):
                child.OptimizeTree()

        # return if one of child still have childs
        for child in self.childs:
            if(len(child.childs) != 0):
                return

        # Check equal of all childs
        for i in range(1, len(self.childs)):
            if(self.childs[0].value != self.childs[i].value):
                return

        # Group all child node
        self.value = self.childs[0].value
        for child in self.childs:
            child.parent = None
        self.childs = []

    def OptimizeTree(self):
        self.GroupChilds()
        self.resetLevel()
        self.resetUID()

    def ConstructPolyLine(self):
        polyline = 'LINESTRING('
        polyline += str(self.rect.topRight.x)+' '+str(self.rect.topRight.y)
        polyline += ', '+str(self.rect.btmLeft.x)+' '+str(self.rect.topRight.y)
        polyline += ', '+str(self.rect.btmLeft.x)+' '+str(self.rect.btmLeft.y)
        polyline += ', '+str(self.rect.topRight.x)+' '+str(self.rect.btmLeft.y)
        polyline += ', '+str(self.rect.topRight.x)+' '+str(self.rect.topRight.y)
        polyline += ')'
        return polyline

    def WriteBoxCSVStart(self, csvFileName, optimizeGridOutput = True):
        QuadTree.boxCsvWriter = csv.writer(open(csvFileName, 'wb'), delimiter = ';')
        QuadTree.boxCsvWriter.writerow(['uid', 'polyline', 'isLeafNode', 'value'])
        QuadTree.OPTIMIZE_GRID_OUTPUT = optimizeGridOutput
        self.__WriteBoxCSV()

    def __WriteBoxCSV(self):
        if(QuadTree.OPTIMIZE_GRID_OUTPUT and len(self.childs) != 0):
            pass
        else:
            QuadTree.boxCsvWriter.writerow(
                [ self.uid
                , self.ConstructPolyLine()
                , len(self.childs) == 0
                , self.value]
            )

        for child in self.childs:
            child.__WriteBoxCSV()

    def exportTreeStructStart(self, csvFileName, mode = 'wb'):
        QuadTree.treeCsvWriter = csv.writer(open(csvFileName, mode), delimiter = ' ')
        self.__exportTreeStruct_Node()
        self.__exportTreeStruct_Edge()

    def __exportTreeStruct_Node(self):
        'uid, Rect:[(btmX, btmY), (topX, topY)], value, level, isLeafNode'
        QuadTree.treeCsvWriter.writerow([
            'node'
            , self.uid
            , self.rect.btmLeft.x, self.rect.btmLeft.y
            , self.rect.topRight.x, self.rect.topRight.y
            , self.value
            , self.level
            , len(self.childs) == 0
        ])
        for child in self.childs:
            child.__exportTreeStruct_Node()

    def __exportTreeStruct_Edge(self):
        'parent_uid, child_uid'
        for child in self.childs:
            QuadTree.treeCsvWriter.writerow(['edge', self.uid, child.uid])

        for child in self.childs:
            child.__exportTreeStruct_Edge()


def strDictReader(value):
    if value == 'NULL':
        return value

    d = ast.literal_eval(value)
    return OrderedDict(sorted(d.items(), reverse= True)).items()

class QuadTreeImporter:
    def __init__ (self, csvFile, isDict = False):
        self.isDict = isDict
        self.ImportTree(csvFile)

    def ImportTree(self, csvFile):
        'uid, Rect:[(btmX, btmY), (topX, topY)], value'
        self.treeCsvReader = csv.reader(open(csvFile, 'rb'), delimiter = ' ')
        self.nodes = []
        self.totalNode = 0
        self.totalEdge = 0

        for row in self.treeCsvReader:
            if(row[0] == 'total_node'):
                self.totalNode = int(row[1])

            elif(row[0] == 'node'):
                value = row[6]
                if self.isDict:
                    value = strDictReader(value)
                self.nodes.append(
                    QuadTree(
                        uid_in = int(row[1])
                        , rect = Rectangle(
                            btmLeft = Point(float(row[2]), float(row[3]))
                            , topRight = Point(float(row[4]), float(row[5]))
                        )
                        , value = value
                    )
                )

            elif(row[0] == 'edge'):
                self.nodes[int(row[1])].childs.append(self.nodes[int(row[2])])
                self.nodes[int(row[2])].parent = self.nodes[int(row[1])]
                self.totalEdge += 1

        self.rootNode = self.nodes[0]
        self.rootNode.OptimizeTree()
