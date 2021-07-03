import pandas as pd
import numpy as np

#Data Preprocessing 
data=pd.read_csv("cancer.csv")
data.drop(["Unnamed: 32"],axis="columns",inplace=True)
data.drop(["id"],axis="columns",inplace=True)
a=pd.get_dummies(data["diagnosis"]) 
cancer=pd.concat([data,a],axis="columns")
cancer.drop(["diagnosis","B"],axis="columns",inplace=True) #Removing Dummy Variable Trap
cancer.rename(columns={"M":"Malignant/Benign"},inplace=True)
y=cancer[["Malignant/Benign"]]
X=cancer.drop(["Malignant/Benign"],axis="columns")


#Classification models
from sklearn.linear_model import LogisticRegression
logreg=LogisticRegression()
X=np.array(X)
y=np.array(y)
logreg.fit(X,y.reshape(-1,)) #Training the Model


from sklearn.externals import joblib
joblib.dump(logreg,"Cancer_model")

#Inorder to load the model use m=joblib.load("filename")




