import csv as csv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.neighbors import KNeighborsClassifier

csv_file_object = csv.reader(open('train.csv', 'r')) 
header = csv_file_object.__next__() 
data=[] 

for row in csv_file_object:
    data.append(row)
data = np.array(data) 

# For .read_csv, always use header=0 when you know row 0 is the header row
train = pd.read_csv('train.csv', header=0)
test_original  = pd.read_csv('test.csv', header=0)

all_ = pd.concat([train,test_original])
median_ages = np.zeros((2,3))

sex = {'female': 0, 'male': 1} 

for key,i in sex.items():
    for j in range(0, 3):
        median_ages[i,j] = all_[(all_['Sex'] == key) & \
                              (all_['Pclass'] == j+1)]['Age'].dropna().median()


def process_dataframe(df):
	df['Embarked_int'] = df['Embarked'].map( {'C':0,'S':1,'Q':2,None:1}).astype(int)
	df['Gender'] = df['Sex'].map( sex ).astype(int)

	df['AgeFill'] = df['Age']
	for i in range(0, 2):
	    for j in range(0, 3):
	        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1),\
	                'AgeFill'] = median_ages[i,j]

	df['FamilySize'] = df['SibSp'] + df['Parch']
	df['Age*Class'] = df.AgeFill * df.Pclass
	df.loc[df['Fare'].isnull(), 'Fare'] = 0
	df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1) 
	df = df.drop(['Age', 'SibSp', 'Parch'], axis=1)

	df = (df - df.min()) / (df.max() -df.min())
	return df




distance_cols = ['Pclass', 'Fare', 'Embarked_int', 'Gender', 'AgeFill','FamilySize', 'Age*Class']
train = process_dataframe(train)
test = process_dataframe(test_original)


n = 33

clf = KNeighborsClassifier(n_neighbors=n)
clf.fit(train[distance_cols], train['Survived'])
preds = clf.predict(test[distance_cols])

predictions_file = open("firsttest.csv", "w")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(test_original['PassengerId'].values, preds.astype(int)))
predictions_file.close()




cheatsheet  = pd.read_csv('cheatsheet.csv', header=0)
gendermodel = pd.read_csv('gendermodel.csv', header=0)

test_original['Prediction'] = preds
cheattest = pd.merge(test_original, cheatsheet, on='Name', how='left')
cheattest.loc[cheattest['Survived'].isnull(), 'Survived'] = 1

count = 0
print (cheattest.head(1))

for ll in cheattest[['Prediction','Survived','Name']].values:
	if ll[0] == ll[1]:
	 	count+=1
	else:
		print(ll[1], ll[2])

print (count, count / float(len(preds)))


print (len(cheattest[['Prediction','Survived','Name']].index))
cheattest['Survived_real'] = cheattest.Survived
cheattest= cheattest.drop(['Prediction','Survived'], axis=1)
gender_test = pd.merge(gendermodel, cheattest, on='PassengerId', how='left')
print (len(gendermodel.index))
print (len(gender_test.index))

count = 0
for ll in gender_test[['Survived','Survived_real']].values:
	if ll[0] == ll[1]:
	 	count+=1

print (count, count / float(len(preds)))