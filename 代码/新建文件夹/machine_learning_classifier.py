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
import time
import joblib
'''
输入一个list，其中的每个元素是元组，返回元组中的所有元素
'''
endtime = 5

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
features = []
labels = []
webpages = all_data.keys()
count = 0  # label的序号
xx = 0
for webpage in list(webpages):
    numbers = all_data[webpage]
    for number in range(0, 12):
        d = down_data[webpage][number]
        u = up_data[webpage][number]
        a = all_data[webpage][number]
        b = b_data[webpage][number]
        u0 = u0_data[webpage][number]
        if len(u0)<=80:
            for i in range(0,80-len(u0)):
                u0.append(0)

        ffeatures = get_tuple_list(b) + u0[49:54] + [u[16], u[17], d[17], a[17], u[1],u[15],u[0]]
        print(ffeatures)
        features.append(ffeatures)
        labels.append(count)
    # xx = xx + 1
    # if xx ==10:
    #     xx = 0
    count += 1
print('test---------------------------------')

knn = neighbors.KNeighborsClassifier(n_neighbors=1)
dtree = tree.DecisionTreeClassifier(max_depth=None, criterion='gini', min_samples_split=2)
rf = RandomForestClassifier(max_features=None, n_estimators=100,
                            min_samples_leaf=1, max_depth=None)
features = np.array(features)
labels = np.array(labels)
start_time = time.time()
knn.fit(features, labels)
end = time.time()
print(end-start_time,'s')
start_time = time.time()
dtree.fit(features, labels)
end = time.time()
print(end-start_time,'s')
start_time = time.time()
rf.fit(features, labels)
end = time.time()
x = endtime+end-start_time-int(end-start_time)
print(x,'s')
# # 支持向量机分类器LinearSVC
# SVM = svm.SVC(gamma='scale', C=1.0, decision_function_shape='ovr', kernel='poly',degree=4,max_iter=-1)
# SVM.fit(features,labels)
# 朴素贝叶斯分类方法模型
start_time = time.time()
nb = MultinomialNB()
nb.fit(features,labels)
end = time.time()
print(end-start_time,'s')
# 逻辑回归分类方法模型
LR = LogisticRegression(solver='liblinear')
LR.fit(features,labels)
joblib.dump(rf, open('pickle/rf.model', 'wb'), protocol=2)
joblib.dump(nb, open('pickle/nb.model', 'wb'), protocol=2)
joblib.dump(knn, open('pickle/knn.model', 'wb'), protocol=2)
joblib.dump(dtree, open('pickle/dtree.model', 'wb'), protocol=2)



# test
test_features = []
test_labels = []
webpages = all_data.keys()
count = 0  # label的序号
# xx = 0
for webpage in list(webpages):
    numbers = all_data[webpage]
    for number in range(12,16):
        # print(number)
        d = down_data[webpage][number]
        u = up_data[webpage][number]
        a = all_data[webpage][number]
        b = b_data[webpage][number]
        u0 = u0_data[webpage][number]
        if len(u0)<=80:
            for i in range(0,80-len(u0)):
                u0.append(0)
        ftest_features = get_tuple_list(b) + u0[49:54] + [u[16], u[17], d[17], a[17], u[1],u[15],u[0]]
        # print(ftest_features)
        test_features.append(ftest_features)
        test_labels.append(count)
    # xx = xx + 1
    # if xx == 10:
    #     xx = 0
    count += 1
test_features = np.array(test_features)
test_labels = np.array(test_labels)

start_time = time.time()
pred = rf.predict(test_features)
end = time.time()
print('randomforest',end-start_time,'s')

# print(pred)
# print(test_labels)
# print(classification_report(test_labels, pred))
print('randomforest accuracy',accuracy_score(test_labels, pred))
print('randomforest recall',recall_score(test_labels,pred,average='macro'))
print('randomforest precision',precision_score(test_labels,pred,average='macro'))
print('randomforest f1',f1_score(test_labels,pred,average='macro'))


start_time = time.time()
pred = knn.predict(test_features)
end = time.time()
print('knn',end-start_time,'s')

# print(pred)
# print(test_labels)
# print(classification_report(test_labels, pred))
print('knn accuracy',accuracy_score(test_labels, pred))
print('knn recall',recall_score(test_labels,pred,average='macro'))
print('knn precision',precision_score(test_labels,pred,average='macro'))
print('knn f1',f1_score(test_labels,pred,average='macro'))

start_time = time.time()
pred = dtree.predict(test_features)
end = time.time()
print('dtree',end-start_time,'s')

# print(pred)
# print(test_labels)
# print(classification_report(test_labels, pred))
print('dtree accuracy',accuracy_score(test_labels, pred))
print('dtree recall',recall_score(test_labels,pred,average='macro'))
print('dtree precision',precision_score(test_labels,pred,average='macro'))
print('dtree f1',f1_score(test_labels,pred,average='macro'))


# pred = SVM.predict(test_features)
# print("支持向量机分类")
# # print(classification_report(test_labels, pred))
# print('svm',accuracy_score(test_labels, pred))

print("朴素贝叶斯分类")
# 朴素贝叶斯分类方法模型
start_time = time.time()
pred = nb.predict(test_features)
end = time.time()
print('NB',end-start_time,'s')


# print(classification_report(test_labels, pred))
print('MultinomialNB accuracy',accuracy_score(test_labels, pred))
print('MultinomialNB recall',recall_score(test_labels,pred,average='macro'))
print('MultinomialNB precision',precision_score(test_labels,pred,average='macro'))
print('MultinomialNB f1',f1_score(test_labels,pred,average='macro'))
# 逻辑回归分类方法模型

pred = LR.predict(test_features)
print("逻辑回归分类")
# print(classification_report(test_labels, pred))
print('LR',accuracy_score(test_labels, pred))