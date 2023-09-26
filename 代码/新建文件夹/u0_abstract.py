import pickle
import collections
from scapy.all import *
import numpy as np
from dtw import dtw

Block_sequence = {}
total_s = 0
total_e = 0
total_count = 0
total_u_block_number = []
mean_s0_sequence = {}
mean_e0_sequence = {}
mean_u0_sequence = {}
ffilter = 9
'''
将字典按照值排序
'''


def sort_dict(dic):
    return sorted(dic.items(), key=lambda x: x[1], reverse=True)


'''
判断字典的值是否大于3，不大于3的删除
'''


def del_dict(dic):
    for key in list(dic.keys()):
        if dic[key] <= 3:
            dic.pop(key)
    return dic


'''
按照原本字典中的顺序输出dict中键值最大的四个元素，
'''


def get_max_1(dic):
    lst = sorted(dic.items(), key=lambda x: x[1], reverse=True)[:1]
    return [i[0] for i in lst]


'''
输入一个list，如果list长度不足4，则在list后面补0
'''


def get_list_len(lst):
    if len(lst) < 1:
        lst = lst + [(0, 0, 0) for i in range(0, 1 - len(lst))]
    return lst


# 计算Bi=(si,ei,ai) 开始，结束，值
# A={u:c} ， S={u:s} 和 E={u:e}
def cal_u0_abstract(webpage, number, lst):
    A_list = {}
    S_list = {}
    E_list = {}
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            if lst[i] in A_list:
                A_list[lst[i]] = A_list[lst[i]] + 1
            else:
                S_list[lst[i]] = i
                A_list[lst[i]] = 2
        if lst[i] in A_list and (lst[i] != lst[i + 1] or i == len(lst) - 2):
            E_list[lst[i]] = i
    # print(lst)
    # print(A_list)
    # print(S_list)
    # print(E_list)
    # 对A_list排序，然后得到ui，从s和e中得到(si,ei,ui)的三元组。
    A_list = del_dict(A_list)
    # print(lst)
    # print(A_list)
    # print(S_list)
    # print(E_list)

    max_1 = get_max_1(A_list)
    for key in A_list:
        if key in max_1:
            if webpage in Block_sequence:
                if number in Block_sequence[webpage]:
                    Block_sequence[webpage][number].append((S_list[key], E_list[key], key))
                else:
                    Block_sequence[webpage][number] = [(S_list[key], E_list[key], key)]
            else:
                Block_sequence[webpage] = {number: [(S_list[key], E_list[key], key)]}
                # 记住开始的s1的值
    if len(A_list) == 0:
        if webpage in Block_sequence:
            Block_sequence[webpage][number] = []
        else:
            Block_sequence[webpage] = {number: []}
    total_u_block_number.append(len(Block_sequence[webpage][number]))


data = pickle.load(open('pickle/web_sequence.pickle', 'rb'))

webpages = data.keys()
print(webpages)

for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        print(number)
        cal_u0_abstract(webpage, number, data[webpage][number])
for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        Block_sequence[webpage][number] = get_list_len(Block_sequence[webpage][number])

print(total_u_block_number)
print(len(total_u_block_number))
print(collections.Counter(total_u_block_number))
print(Block_sequence)
b = {}
e = {}
for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        print(number,Block_sequence[webpage][number])
        print(Block_sequence[webpage][number][0][0])
        if Block_sequence[webpage][number][0][0] in b:
            b[Block_sequence[webpage][number][0][0]]= b [Block_sequence[webpage][number][0][0]]+1
        else:
            b[Block_sequence[webpage][number][0][0]] = 1
        if Block_sequence[webpage][number][0][1] in e:
            e[Block_sequence[webpage][number][0][1]] = e[Block_sequence[webpage][number][0][1]] + 1
        else:
            e[Block_sequence[webpage][number][0][1]] = 1
print(b)
print(e)
exit(0)
# 求平均的s0
for webpage in webpages:
    numbers = data[webpage]
    total_s0 = 0
    total_u0 = 0
    total_e0 = 0
    for number in numbers:
        total_s0 += Block_sequence[webpage][number][0][0]
        total_e0 += Block_sequence[webpage][number][0][1]
        total_u0 += Block_sequence[webpage][number][0][2]
        if Block_sequence[webpage][number][0][0] != 0 and Block_sequence[webpage][number][0][1] != 0:
            total_s = total_s + Block_sequence[webpage][number][0][0]
            total_e = total_e + Block_sequence[webpage][number][0][1]
            total_count = total_count + 1
        print(webpage, number)
        print(Block_sequence[webpage][number][0][0])
        print(Block_sequence[webpage][number][0][2])

    mean_s0_sequence[webpage] = round(total_s0 / 15)
    mean_e0_sequence[webpage] = round(total_e0 / 15)
    mean_u0_sequence[webpage] = round(total_u0 / 15)
    # print(total_u0 / 15)
    # print(total/15)
    # print(round(total/15))

# 对齐u0序列
'''
输出从x开始的n个数，n可以是负数
'''


def get_num(x, n):
    if n > 0:
        return [i for i in range(x, x + n)]
    else:
        return [i for i in range(x, x + n, -1)]


'''
将整个list向前平移x个位置
'''


def move_list(lst, x):
    if x > 0:
        # print(lst[x:])
        return lst[x:] + get_num(lst[-1] + 10, x)
    if x < 0:
        # print(lst[:x])
        return get_num(-2 + x, -x) + lst[:x]
    if x == 0:
        return lst


'''
将整个list的值减去x
'''


def add_list(lst, x):
    for i in range(len(lst)):
        lst[i] = lst[i] - x
    return lst


def draw_line(dict):
    count = 0
    plt.cla
    plt.xlabel('')
    plt.ylabel('')
    for tem in dict:
        print(tem, count)
        for num in dict[tem]:
            plt.plot(dict[tem][num], marker='o', markersize=1)
        count = count + 1
        plt.show()


# 去掉异常流
manhattan_distance = lambda x, y: np.abs(x - y)
for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        print(number)
        x = np.array(data[webpage][number]).reshape(-1, 1)
        total = 0
        for number2 in numbers:
            y = np.array(data[webpage][number2]).reshape(-1, 1)
            d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
            # print(d)
            total += d
        print(total)
        if total >= 800000:
            print('!!!', number, total)
            if number != ffilter:
                data[webpage][number] = list(data[webpage][ffilter])
            else:
                data[webpage][number] = list(data[webpage][ffilter - 1])
print(mean_s0_sequence)
print(mean_e0_sequence)
print(mean_u0_sequence)
print(Block_sequence)
# draw_line(data)

# # 左右对齐
# for webpage in webpages:
#     numbers = range(0, 10)
#     total = 0
#     for number in numbers:
#         data[webpage][number] = move_list(data[webpage][number],
#                                           Block_sequence[webpage][number][0][0] - mean_s0_sequence[webpage])
#
# # 去掉异常流
# manhattan_distance = lambda x, y: np.abs(x - y)
# for webpage in webpages:
#     print(webpage)
#     numbers = data[webpage]
#     for number in numbers:
#         print(number)
#         x = np.array(data[webpage][number]).reshape(-1, 1)
#         total = 0
#         for number2 in numbers:
#             y = np.array(data[webpage][number2]).reshape(-1, 1)
#             d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
#             # print(d)
#             total += d
#         # print(total)
#         if total >= 8000000:
#             print('!!!', number, total)
#             if number != 0:
#                 data[webpage][number] = list(data[webpage][number - 1])
#             else:
#                 data[webpage][number] = list(data[webpage][number + 1])
# print(Block_sequence)
# draw_line(data)
# # 再求一次块序列
# print("upupupupup\n\n\n\n\n")
# Block_sequence = {}
# for webpage in webpages:
#     numbers = data[webpage]
#     for number in numbers:
#         cal_u0_abstract(webpage, number, data[webpage][number])
# for webpage in webpages:
#     numbers = data[webpage]
#     for number in numbers:
#         Block_sequence[webpage][number] = get_list_len(Block_sequence[webpage][number])
# # 求平均的u0值
# for webpage in webpages:
#     numbers = range(0, 10)
#     total_u0 = 0
#     for number in numbers:
#         total_u0 += Block_sequence[webpage][number][0][2]
#         print(webpage, number)
#         print(Block_sequence[webpage][number][0][2])
#     mean_u0_sequence[webpage] = round(total_u0 / 15)
#     print(total_u0 / 15)
#
# # 上下对齐
# for webpage in webpages:
#     numbers = range(0, 10)
#     total = 0
#     for number in numbers:
#         print(data[webpage][number])
#         print(Block_sequence[webpage][number][0][2], mean_u0_sequence[webpage])
#         # data[webpage][number] = move_list(data[webpage][number], Block_sequence[webpage][number][0][
#         # 0]-mean_s0_sequence[webpage])
#         data[webpage][number] = add_list(data[webpage][number],
#                                          Block_sequence[webpage][number][0][2] - mean_u0_sequence[webpage])
#         print(data[webpage][number])
#
# # 去掉异常流
# manhattan_distance = lambda x, y: np.abs(x - y)
# for webpage in webpages:
#     print(webpage)
#     numbers = data[webpage]
#     for number in numbers:
#         print(number)
#         x = np.array(data[webpage][number]).reshape(-1, 1)
#         total = 0
#         for number2 in numbers:
#             y = np.array(data[webpage][number2]).reshape(-1, 1)
#             d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
#             # print(d)
#             total += d
#         # print(total)
#         if total >= 8000000:
#             print('!!!', number, total)
#             if number != 0:
#                 data[webpage][number] = list(data[webpage][number - 1])
#             else:
#                 data[webpage][number] = list(data[webpage][number + 1])

# 再求一次块序列

Block_sequence = {}
for webpage in webpages:
    numbers = data[webpage]
    for number in numbers:
        cal_u0_abstract(webpage, number, data[webpage][number])

print(Block_sequence)
for webpage in webpages:
    print(webpage)
    numbers = data[webpage]
    for number in numbers:
        Block_sequence[webpage][number] = get_list_len(Block_sequence[webpage][number])

pickle.dump(data, open('pickle/web_sequence.pickle', 'wb'), protocol=2)
print(Block_sequence)
pickle.dump(Block_sequence, open('pickle/BLock_sequence.pickle', 'wb'), protocol=2)
print(sum(mean_s0_sequence.values()) / len(mean_s0_sequence))
print(sum(mean_e0_sequence.values()) / len(mean_e0_sequence))
print(total_s/total_count)
print(total_e/total_count)
