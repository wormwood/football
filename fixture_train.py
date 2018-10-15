from FixturesOdds import FixturesOdds
import FootballClf
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
import numpy as np


n_estimators = [int(x) for x in np.linspace(start=10, stop=100, num=10)]
max_features = ['auto', 'sqrt']
criterion = ['gini']
min_samples_split=[2,5,10]
param_grid = [{'n_estimators' : n_estimators, 'max_features' : max_features, 'criterion' : criterion, 
                      'min_samples_split' : min_samples_split}]

fo=FixturesOdds()
fo.fix_load('vwCSV_3','vwCSV_3.csv', False)
fo.do_calcs()
fo.clean()

clf =  RandomForestClassifier(max_depth=10, n_estimators=2000, min_samples_leaf=10, random_state=0)
X,y=fo.X(),fo.y()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

gs=GridSearchCV(clf, param_grid, cv=5, scoring='recall_weighted')
gs.fit(X_train, y_train)

y_pred = gs.best_estimator_.fit(X_train, y_train).predict(X_test)
print(classification_report(y_test, y_pred))

c=FootballClf.FootballClf()
c.save(gs.best_estimator_, 'betting clf', 1, 'using odds to predict', 'odds_clf_dev', ['ExpectedResult', 'FTG_3', 'FTG_5', 'HomeOdds', 'DrawOdds', 'AwayOdds'])
