import pickle
import pandas as pd
import scipy.stats as st
import numpy as np
up_features = {}    # 负数
down_features = {}  # 正数
all_features = {}   # 全部流
'''
计算十八维特征 
最小值（min）、
最大值（max）、平均值（mean）
、中值绝对偏差（mad）、标准偏差（std）、
方差（var）、偏斜（skew）、峰度（kurt）、
百分位数（从10%到90） %) (per1 -per9 ) 
和系列中的元素数 (len )
'''
def cal_features(lst):
    lengths = np.array(lst)
    x = pd.Series(lengths)
    x.skew()
    x.kurtosis()
    sort_lengths = np.sort(lengths)
    min_len = min(lst)
    max_len = max(lst)
    mean_len = lengths.mean()
    mad_len = x.mad()
    std_len = np.std(lengths)
    var_len = np.var(lengths)
    skew_len = st.skew(lengths, bias=False)
    kurt_len = st.kurtosis(lengths, bias=False)
    per10_len = np.percentile(sort_lengths, 10)
    per20_len = np.percentile(sort_lengths, 20)
    per30_len = np.percentile(sort_lengths, 30)
    per40_len = np.percentile(sort_lengths, 40)
    per50_len = np.percentile(sort_lengths, 50)
    per60_len = np.percentile(sort_lengths, 60)
    per70_len = np.percentile(sort_lengths, 70)
    per80_len = np.percentile(sort_lengths, 80)
    per90_len = np.percentile(sort_lengths, 90)
    len_len = len(lst)
    return [min_len,max_len,mean_len,mad_len,std_len,
            var_len,skew_len,kurt_len,per10_len,per20_len,per30_len,per40_len,per50_len,per60_len,per70_len,per80_len,per90_len,len_len]

'''
将一个list中的正数分为一个list，负数分为一个list
'''
def get_pos_neg(lst):
    pos=[]
    neg=[]
    for i in lst:
        if i>0:
            pos.append(i)
        else:
            neg.append(i*-1)
    return pos,neg

'''
将一个list的负数变成正数
'''
def neg2pos(lst):
    return [i if i>0 else -i for i in lst]

data = pickle.load(open('pickle/total_length_sequence.pickle', 'rb'))

webpages = data.keys()
print(webpages)
for webpage in webpages:
    numbers = data[webpage]
    for number in numbers:
        length_list = data[webpage][number]
        pos,neg = get_pos_neg(length_list)
        length_list = neg2pos(length_list)

        print('length',length_list)
        print('pos',pos)
        print('neg',neg)
        neg = cal_features(neg)
        pos = cal_features(pos)
        length_list = cal_features(length_list)
        print('length', length_list)
        print('pos', pos)
        print('neg', neg)
        if webpage not in up_features:
            up_features[webpage] = {number: neg}
        else:
            up_features[webpage][number] = neg
        if webpage not in down_features:
            down_features[webpage] = {number: pos}
        else:
            down_features[webpage][number] = pos
        if webpage not in all_features:
            all_features[webpage] = {number: length_list}
        else:
            all_features[webpage][number] = length_list
        pickle.dump(up_features, open('pickle/up_features.pickle', 'wb'), protocol=2)
        pickle.dump(down_features, open('pickle/down_features.pickle', 'wb'), protocol=2)
        pickle.dump(all_features, open('pickle/all_features.pickle', 'wb'), protocol=2)
