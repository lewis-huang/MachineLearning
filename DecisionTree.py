from math import log
import operator


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet :
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

"""

the following code is used to test whether calcShannonEnt works - 

dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
labels = ['no surfacing','flippers']

entr = calcShannonEnt(dataSet)
print ("the dataset has following entropy :%f" % (entr))

"""

def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet :
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)

    return retDataSet


"""

这部分代码用来测试 splitDataSet 函数是否能够正常运行

dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
retDataSet = splitDataSet(dataSet,0,1)
print(retDataSet)

retDataSet = splitDataSet(dataSet,1,1)
print(retDataSet)


这里涉及到列表的操作：且看 splitDataSet 中的两行：

 reducedFeatVec = featVec[:axis]
 reducedFeatVec.extend(featVec[axis+1:])
 
 featVec[:axis] 是截取列表 featVec 在 axis 之前的元素，且不含 axis 位置上的元素
 featVec[axis + 1:] 是截取列表 featVec 在 axis 之后的元素，且不含 axis 位置上的元素
 
 另：
 列表的声明： []
 元组的声明：()
 字典的声明： {}

"""

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [ example[i] for example in dataSet  ]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals :
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

"""

这部分代码用来测试 chooseBestFeatureToSplit 是否运行正常

dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
bestFeature = chooseBestFeatureToSplit(dataSet)
print(bestFeature)


"""

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] +=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True )
    return sortedClassCount[0][0]


"""

同样用来测试上面函数的可行性

classList = ["20","30","50","60","30"]
classSorted = majorityCnt(classList)
print (classSorted)

"""

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1 :
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals :
        subLables = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLables)
    return myTree



dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
labels = ['no surfacing','flippers']
decisionTree  = createTree(dataSet,labels)
print(decisionTree)