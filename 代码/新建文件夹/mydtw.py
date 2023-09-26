
import numpy as np
from dtw import dtw
import pickle
from scapy.all import *
data = pickle.load(open('pickle/web_sequence.pickle', 'rb'))
manhattan_distance = lambda x, y: np.abs(x - y)

def draw_line(dict):
    count = 0
    plt.cla
    plt.xlabel('')
    plt.ylabel('')
    for tem in dict:

        print(tem,count)
        for num in dict[tem]:
            plt.plot(dict[tem][num],marker='o', markersize=1)
        count = count + 1
        plt.show()


webpages = data.keys()
print(webpages)
for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        print(number)
        x = np.array(data[webpage][number]).reshape(-1,1)
        total = 0
        for number2 in numbers:
            y = np.array(data[webpage][number2]).reshape(-1, 1)
            d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
            # print(d)
            total += d
        # print(total)
        if total>=8000000:
            print('!!!',number,total)
            if number != 0:
                data[webpage][number] = data[webpage][number-1]
            else:
                data[webpage][number] = data[webpage][number+1]
draw_line(data)
# x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# print(x)
# y = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# print(y)
# d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
# print(d)
