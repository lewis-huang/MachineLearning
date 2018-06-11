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



data = {'Barton LLC': 109438.50,
        'Frami, Hills and Schmidt': 103569.59,
        'Fritsch, Russel and Anderson': 112214.71,
        'Jerde-Hilpert': 112591.43,
        'Keeling LLC': 100934.30,
        'Koepp Ltd': 103660.54,
        'Kulas Inc': 137351.96,
        'Trantow-Barrows': 123381.38,
        'White-Trantow': 135841.99,
        'Will LLC': 104437.60}
group_data = list(data.values())
group_names = list(data.keys())
group_mean = mean(group_data)

chart, ax = plt.subplots()

"""

axes.barh(x,y)

x: 代表的是纵轴
y: 代表的是横轴

axes.barh 这里的 barh 可能代表的是 bar horizontal 的意思

所以 x 用来承载维度，而 y 来承载度量

"""
ax.barh(group_names, group_data)
plt.show()






