import numpy as np
import pandas as pd

#Data Preprocessing 
data=pd.read_csv("diabetes.csv")
X=data.iloc[:,:8].values
y=data[["Outcome"]].values

#Model Fitting
from sklearn.linear_model import LogisticRegression
logreg=LogisticRegression()
logreg.fit(X,y.reshape(-1,))
ans=logreg.predict([[6,148,72,35,0,33.6,2.333,50]])


#Saving the Model
from sklearn.externals import joblib
joblib.dump(logreg,"diabetes_model")

