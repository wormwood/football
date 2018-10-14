import Fixtures
import FootballClf
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

fixs = Fixtures.Fixtures()
fixs.fix_load('vwCSV_2.csv', True)

fixs.df['FTG_3']=fixs.df.FTHG_3 - fixs.df.FTAG_3
fixs.df['FTG_5']=fixs.df.FTHG_5 - fixs.df.FTAG_5

fixs.clean()
cols_for_prediction=['ExpectedResult', 'FTG_3', 'FTG_5']
X=fixs.df[cols_for_prediction].values
y=fixs.df['HomeTeamResult'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

clf =  RandomForestClassifier(max_depth=10, n_estimators=2000, min_samples_leaf=10, random_state=0)
clf.fit(X_train, y_train)

y_pred = clf.fit(X_train, y_train).predict(X_test)
rep=classification_report(y_test, y_pred)
print (rep)

c=FootballClf.FootballClf()
c.save(clf, 'small clf', 1, 'a test of the new system', 'f_clf_dev', cols_for_prediction)
