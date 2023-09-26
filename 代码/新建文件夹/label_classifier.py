import pickle
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import neighbors
import numpy as np
# 也可以直接采用这个进行计算
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, roc_auc_score, recall_score, precision_score
from sklearn import svm
import csv
import numpy as np

from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn import neighbors
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

'''
输入一个list，其中的每个元素是元组，返回元组中的所有元素
'''


def get_tuple_list(lst):
    all = []
    for i in lst:
        all.append(i[0])
        all.append(i[1])
        all.append(i[2])
    return all


all_data = pickle.load(open('pickle/all_features.pickle', 'rb'))
up_data = pickle.load(open('pickle/up_features.pickle', 'rb'))
down_data = pickle.load(open('pickle/down_features.pickle', 'rb'))
b_data = pickle.load(open('pickle/Block_sequence.pickle', 'rb'))
u0_data = pickle.load(open('pickle/web_sequence.pickle', 'rb'))
for j in range(0,10):
    print(j)
    features = []
    labels = []
    webpages = all_data.keys()

    count = 0  # label的序号
    xx = 0
    for i in range(j, len(webpages), 10):
        webpage = list(webpages)[i]
        numbers = all_data[webpage]
        for number in range(0, 13):
            d = down_data[webpage][number]
            u = up_data[webpage][number]
            a = all_data[webpage][number]
            b = b_data[webpage][number]
            u0 = u0_data[webpage][number]
            if len(u0) <= 80:
                for i in range(0, 80 - len(u0)):
                    u0.append(0)

            ffeatures = get_tuple_list(b) + u0[49:53] + [u[16], u[17], d[17], a[17], u[1], u[15], u[0]]
            # print(ffeatures)
            features.append(ffeatures)
            labels.append(count)
        # xx = xx + 1
        # if xx ==10:
        #     xx = 0
        count += 1
    # print('test---------------------------------')

    knn = neighbors.KNeighborsClassifier(n_neighbors=5)
    dtree = tree.DecisionTreeClassifier(max_depth=None, criterion='gini', min_samples_split=2)
    rf = RandomForestClassifier(max_features=None, n_estimators=100,
                                min_samples_leaf=1, max_depth=None)
    features = np.array(features)
    labels = np.array(labels)
    knn.fit(features, labels)
    dtree.fit(features, labels)
    rf.fit(features, labels)
    # 支持向量机分类器LinearSVC
    SVM = svm.SVC(gamma='scale', C=1.0, decision_function_shape='ovr', kernel='poly', degree=4, max_iter=-1)
    SVM.fit(features, labels)
    # 朴素贝叶斯分类方法模型
    nb = MultinomialNB()
    nb.fit(features, labels)
    # 逻辑回归分类方法模型
    LR = LogisticRegression(solver='liblinear')
    LR.fit(features, labels)

    # test
    features = []
    labels = []
    webpages = all_data.keys()
    count = 0  # label的序号
    # xx = 0
    for i in range(j, len(webpages), 10):
        webpage = list(webpages)[i]
        numbers = all_data[webpage]
        for number in range(13, 16):
            # print(number)
            d = down_data[webpage][number]
            u = up_data[webpage][number]
            a = all_data[webpage][number]
            b = b_data[webpage][number]
            u0 = u0_data[webpage][number]
            if len(u0) <= 80:
                for i in range(0, 80 - len(u0)):
                    u0.append(0)
            ffeatures = get_tuple_list(b) + u0[49:53] + [u[16], u[17], d[17], a[17], u[1], u[15], u[0]]
            # print(ffeatures)
            features.append(ffeatures)
            labels.append(count)
        # xx = xx + 1
        # if xx == 10:
        #     xx = 0
        count += 1
    features = np.array(features)
    labels = np.array(labels)
    pred = rf.predict(features)
    # print(pred)
    # print(labels)
    # print(classification_report(labels, pred))
    print('randomforest accuracy', accuracy_score(labels, pred))
    print('randomforest recall', recall_score(labels, pred, average='macro'))
    print('randomforest precision', precision_score(labels, pred, average='macro'))
    print('randomforest f1', f1_score(labels, pred, average='macro'))

    pred = knn.predict(features)
    # print(pred)
    # print(labels)
    # print(classification_report(labels, pred))
    print('knn', accuracy_score(labels, pred))

    pred = dtree.predict(features)
    # print(pred)
    # print(labels)
    # print(classification_report(labels, pred))
    print('dtree', accuracy_score(labels, pred))

    # pred = SVM.predict(features)
    # print("支持向量机分类")
    # # print(classification_report(labels, pred))
    # print('svm', accuracy_score(labels, pred))
    #
    # # 朴素贝叶斯分类方法模型
    #
    # pred = nb.predict(features)
    # print("朴素贝叶斯分类")
    # # print(classification_report(labels, pred))
    # print('MultinomialNB', accuracy_score(labels, pred))
    #
    # # 逻辑回归分类方法模型
    #
    # pred = LR.predict(features)
    # print("逻辑回归分类")
    # # print(classification_report(labels, pred))
    # print('LR', accuracy_score(labels, pred))
