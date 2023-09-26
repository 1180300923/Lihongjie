import pickle
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
# 也可以直接采用这个进行计算
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, roc_auc_score, recall_score, precision_score







#Load boston housing dataset as an example
all_data = pickle.load(open('pickle/all_features.pickle', 'rb'))
up_data = pickle.load(open('pickle/up_features.pickle', 'rb'))
down_data = pickle.load(open('pickle/down_features.pickle', 'rb'))
webpages = all_data.keys()

features = []
labels = []
count = 0  # label的序号
for webpage in webpages:

    numbers = all_data[webpage]
    for number in numbers:
        ffeatures = all_data[webpage][number]+up_data[webpage][number]+down_data[webpage][number]
        print(ffeatures)
        features.append(ffeatures)
        labels.append(count)
    count += 1
label_names = ['allmin','allmax','allmean','allmad','allstd','allvar','allskew','allkurt','allper1',
              'allper2','allper3','allper4','allper5','allper6','allper7','allper8','allper9','alllen',
              'upmin','upmax','upmin','upmad','upstd','upvar','upskew','upkurt','upper1',
              'upper2','upper3','upper4','upper5','upper6','upper7','upper8','upper9','uplen',
              'downmin','downmax','downmean','downmad','downstd','downvar','downskew','downkurt','downper1',
              'downper2','downper3','downper4','downper5','downper6','downper7','downper8','downper9','downlen']

rf = RandomForestRegressor()
rf2 = RandomForestClassifier(max_features=None, n_estimators=10,
                            min_samples_leaf=1, max_depth=None)
rf.fit(features, labels)

print("Features sorted by their score:")
results = sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), label_names),
             reverse=True)
print(type(results))
print(results)
results = results[:10]
plt.barh([i[1] for i in results],[i[0] for i in results])
X = np.arange(10)
Y = [i[0] for i in results]
plt.title("Feature importance")
plt.ylabel("Features")
for x, y in zip(X , Y):
    plt.text(float(y)+0.01,float(x)+0.05,str(y),ha='center',va='bottom' )


plt.show()

features = []
labels = []
count = 0
for webpage in webpages:
    numbers = all_data[webpage]
    for number in range(0,10):
        d = down_data[webpage][number]
        u = up_data[webpage][number]
        a = all_data[webpage][number]
        ffeatures = [u[16], u[17], d[17], a[17], u[1],u[15],u[0]]
        # print(ffeatures)
        features.append(ffeatures)
        labels.append(count)
    count = count + 1
rf2.fit(features,labels)
pred = rf2.predict(features)
print(pred)
print(labels)
print(accuracy_score(labels,pred))

features = []
labels = []
count = 0
for webpage in webpages:
    numbers = all_data[webpage]
    for number in range(10,len(numbers)):
        d = down_data[webpage][number]
        u = up_data[webpage][number]
        a = all_data[webpage][number]
        ffeatures = [u[16], u[17], d[17], a[17], u[1],u[15],u[0]]
        # print(ffeatures)
        features.append(ffeatures)
        labels.append(count)

    count += 1

# 输入真实的样本和对应的标签
pred = rf2.predict(features)
print(pred)
print(labels)
print(accuracy_score(labels,pred))