import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate

#Data Preprocessing 
data=pd.read_csv("diabetes.csv")
X=data.iloc[:,:8]
y=data[["Outcome"]]


#Model Fitting
from sklearn.linear_model import LogisticRegression
logreg=LogisticRegression()
logreg.fit(X,y)

#Kfold cross validation
cv_results = cross_validate(logreg,X,y, cv=10)
print(cv_results)

#Saving the Model
import joblib
joblib.dump(logreg,"diabetes_model")

