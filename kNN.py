"""
这部分导入 numpy 的库

"""
from numpy import *
import operator

"""
这部分导入 Matplotlib 库，用来作图
"""

import matplotlib
import matplotlib.pyplot as plt

"""

导入 _thread 模块，加载 MatplotLib 画的图
此处应该注意的是, Python多线程的处理方法以及各自的优缺点

"""
import _thread


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances **0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    """
    Python2 中才有的 dict.iteritems() 方法，Python 3中已经用dict.items()取代了
    dict.iteritems() 用于流式计算，类似于PipeLine的数据处理
    目的都是为了取回字典中的所有数据
    """
    # sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        """
        Python 的范围标记[0:3]，意为第一位开始到第三位止，共 3 位，并左开右闭
        """
        returnMat[index,:] = listFromLine[0:3]
        print("The Line is : %s; The ListFromLine is :%s ;" % (line,listFromLine))
        classLabelVector.append( ( listFromLine[-1] ))
        index = index + 1
    return returnMat,classLabelVector

"""
底下定义个多线程渲染 MatPlotLib 做的图。
在主线程中，不加线程来渲染图，在主线程退出的那一瞬间，图还没来得及呈现，主程序退出连带图也一起退出
此图就一矩阵列表形成的图，所以带的参数仅仅是二维矩阵列表即可

经过再三实验，用非主线程来渲染图，是会出现问题的：
Runtime Error: main thread is not in main loop
Tcl_AsyncDelete: async handler deleted by the wrong thread

并且在使用主线程来渲染图的过程中，渲染的速度也比非主线程渲染快
"""

def getPlot(dataMatrix,lock):
    """
    第一次使用 MatPlotLib 对 plot 十分陌生，先从简单的例子做起
    :param dataMatrix:
    :param lock:
    :return:

    chart = plt.figure()
    axis = chart.add_subplot(111)
    axis.scatter(dataMatrix[:, 1], dataMatrix[:, 2])
    for i in dataMatrix[:,1]:
        print (" the value is : %s" % (str(i)))
    chart.show()
    userInfo = input("Please submit your comments:")
    lock.release()

     """
    plt.plot([1,2,3,4])
    plt.ylabel("Some Value")
    plt.show()
    userInfo = input("Please make your comments")
    lock.release()





def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals  -  minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals , (m,1))
    normDataSet = normDataSet / tile(ranges,(m,1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix("datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)

    # shape 都是 NumPy 的函数
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0

    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:] , datingLabels[numTestVecs:m],4)
        if(classifierResult)!=datingLabels[i]:
            errorCount = errorCount + 1.0

    print("The total error rate is :%f " %( errorCount / float(numTestVecs)))





datingDataMat,datingLabels = file2matrix("datingTestSet2.txt")
normDataSet, ranges, minVals = autoNorm(datingDataMat)
datingClassTest()

# datingDataMat
"""
for  label in datingLabels :                   
    print("This label is: %s" %( label ))      
       
"""

"""

用非主线程来渲染图画，是会有运行时错误的

"""

"""
LockList = []
lock = _thread.allocate_lock()
lock.acquire()
LockList.append(lock)
_thread.start_new_thread( getPlot,(datingDataMat,lock))
for locker in LockList:
    while locker.locked():pass
"""

""" 底下这句命令是为了可以让子线程在画图完毕之后，不随主线程退出而退出"""
#exitcheck = input("Press any key to exit!")


## 冰激凌和游戏维度

"""
x = datingDataMat[:,1]
y = datingDataMat[:,2]

"""


## 飞机里程与游戏维度

x = datingDataMat[:,0]
y = datingDataMat[:,1]


"""

底下 area 定义中须知：
1 给某一分类加上系数，使得其分类特性更加清晰。此情景是依据某一分类权重值大小，来决定半径大小，从而提高辨识度
2 使用 [ int(x) for x in List[L] ] 来给列表 List[L]中的每一个元素重新赋值

"""
area =  [ (int(number_string)*3)**2 for number_string in datingLabels ]
color = 15 * [ int(number_string) for number_string in datingLabels ]

plt.scatter(x, y, s =area, alpha=0.5)
plt.show()



