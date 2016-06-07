import sys
import pydot
import csv

class Point:
    def __init__(self, x = 0, y = 0, xy = None):
        if(xy == None):
            self.x = float(x)
            self.y = float(y)
        else:
            self.x = float(xy.x)
            self.y = float(xy.y)

    def __add__ (self, target):
        return Point(self.x+target.x, self.y+target.y)

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

uid = 0
class QuadTree:
    # True : Ouput only leaf grid
    # False : Output both parent and leaf grid
    OPTIMIZE_GRID_OUTPUT = True
    boxCsvWriter = None
    treeCsvWriter = None

    def __init__(self, level = 0, rect = Rectangle(), parent = None, value = 'NULL', maxLevel = None):
        self.level = level
        self.rect = rect
        self.childs =[]
        self.parent = parent
        self.value = value
        self.maxLevel = maxLevel
        global uid
        self.uid = uid
        uid += 1

    def createSubQTree(self):
        if(self.level == self.maxLevel or len(self.childs) != 0):
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
            return None

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

    def OptimizeTree(self):
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
        return

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
            child.WriteBoxCSV()

    def resetUID(self):
        # Check if root node
        global uid
        if(self.parent == None):
            uid = 0
        self.uid = uid
        uid += 1
        for child in self.childs:
            child.resetUID()

    def exportTreeStructStart(self, csvFileName):
        QuadTree.treeCsvWriter = csv.writer(open(csvFileName, 'wb'), delimiter = ' ')
        QuadTree.treeCsvWriter.writerow([uid])
        self.__exportTreeStruct_Node()
        self.__exportTreeStruct_Edge()

    def __exportTreeStruct_Node(self):
        QuadTree.treeCsvWriter.writerow([
            self.uid
            , self.rect.topRight.x, self.rect.topRight.y
            , self.rect.btmLeft.x, self.rect.btmLeft.y
            , self.value
        ])
        for child in self.childs:
            child.__exportTreeStruct_Node()

    def __exportTreeStruct_Edge(self):
        for child in self.childs:
            QuadTree.treeCsvWriter.writerow([self.uid, child.uid])

        for child in self.childs:
            child.__exportTreeStruct_Edge()
