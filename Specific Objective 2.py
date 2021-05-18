import pandas as pd
from matplotlib import pyplot
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


# Load dataset

path = "C:/Python Projects/Specific Objective 2/D_alata.xlsx"

names = ['Site', 'BTC', 'EPC', 'MTC', 'PSC', 'TTP']

dataset = pd.read_excel(path, names=names)


# Define X, Y

array = dataset.values

X = array[:, 1:5]

Y = array[:, 0]


# Test Size

test_size = 0.20


# Train, Test Splitting for further Stratified Splitting

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size)


# Feature Scaling

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


"""
Spot Check Algorithms
"""

models = []

models.append(('LR', LogisticRegression(C=1.206, penalty='l2')))

models.append(('LDA', LinearDiscriminantAnalysis(solver='svd')))

models.append(('KNN', KNeighborsClassifier(metric='euclidean', n_neighbors=5, weights='uniform')))

models.append(('CART', DecisionTreeClassifier(criterion='entropy', max_depth=4)))

models.append(('NB', GaussianNB(var_smoothing=0.01)))

models.append(('SVM', SVC(C=1, gamma=0.1, kernel='rbf')))


"""
Evaluate each model in turn
"""

results = []

names = []

for name, model in models:

    skf = StratifiedKFold(n_splits=10)

    cv_results = cross_val_score(model, X_train, Y_train, cv=skf, scoring='accuracy')

    results.append(cv_results)

    names.append(name)

    msg = "%s:%f(%f)" % (name, cv_results.mean(), cv_results.std())

    print(msg)


"""
Compare algorithms
"""

fig = pyplot.figure()

fig.suptitle('Algorithm Comparison')

ax = fig.add_subplot(111)

pyplot.boxplot(results)

ax.set_xticklabels(names)

pyplot.show()   # Box and Whisker Plots Comparing Algorithm Performance.


"""
Make predictions on test dataset using the best model
"""

cart = DecisionTreeClassifier()

cart.fit(X_train, Y_train)

predictions = cart.predict(X_test)

print(accuracy_score(Y_test, predictions))

print(confusion_matrix(Y_test, predictions))

print(classification_report(Y_test, predictions))
