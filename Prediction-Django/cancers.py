import pandas as pd
import numpy as np
from sklearn.model_selection import cross_validate

#Data Preprocessing 
data=pd.read_csv("cancer.csv")

data.drop(["Unnamed: 32"],axis="columns",inplace=True)
data.drop(["id"],axis="columns",inplace=True)

#Converting the Categorical Variables
a=pd.get_dummies(data["diagnosis"])

#Concatinating the categorical data columns to the dataset 
cancer=pd.concat([data,a],axis="columns")

#Removing Dummy Variable Trap and duplicate Diagnosis column
cancer.drop(["diagnosis","B"],axis="columns",inplace=True) 

cancer.rename(columns={"M":"Malignant/Benign"},inplace=True)

#get the dependnt column
y=cancer[["Malignant/Benign"]]

#Independent column
X=cancer.drop(["Malignant/Benign"],axis="columns")

#READY TO TRAIN AND PREDICT
#Classification models
from sklearn.linear_model import LogisticRegression
logreg=LogisticRegression()
logreg.fit(X,y)

#K fold cross validation
cv_results = cross_validate(logreg,X,y,cv=10)
print(cv_results)


import joblib
joblib.dump(logreg,"Cancer_model")

#Inorder to load the model use m=joblib.load("filename")




