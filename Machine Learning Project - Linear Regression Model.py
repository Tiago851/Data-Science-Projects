"""
This script collects all my answers to the questions regarding the first Machine Learning project 
from the Udemy course - 2022 Python for Machine Learning & Data Science Masterclass

It takes a dataset that was already cleaned and prepared during the course, and the objective is to
to create a Linear Regression Model, train it on the data with the optimal parameters using a grid 
search, and then evaluate the model's capabilities on a test set.

The csv file is also available here in Github in the same folder as this script.

"""

#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Main dataframe
df = pd.read_csv('AMES_Final_DF.csv')

#The label we are trying to predict is the SalePrice column. Separate out the data into X features and y labels

X = df.drop('SalePrice', axis = 1)
y = df['SalePrice']

#Use scikit-learn to split up X and y into a training set and test set. Since we will later be using a Grid Search strategy, 
#set your test proportion to 10%. 
#To get the same data split as the solutions notebook, you can specify random_state = 101

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = 0.10, 
                                                    random_state = 101)


#The dataset features has a variety of scales and units. For optimal regression performance, scale the X features. 
#Take carefuly note of what to use for .fit() vs what to use for .transform()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#We will use an Elastic Net model. Create an instance of default ElasticNet model with scikit-learn

from sklearn.linear_model import ElasticNet

base_elastic_net_model = ElasticNet()

#The Elastic Net model has two main parameters, alpha and the L1 ratio. 
#Create a dictionary parameter grid of values for the ElasticNet. 

param_grid = {'alpha': [0.1,1,5,10,50,100], 'l1_ratio': [0.1,0.5,0.7,0.99,1]}

#Using scikit-learn create a GridSearchCV object and run a grid search for the best parameters 
#for your model based on your scaled training data.

from sklearn.model_selection import GridSearchCV

grid_model = GridSearchCV(estimator = base_elastic_net_model, param_grid = param_grid,
                         scoring = 'neg_mean_squared_error', cv = 5, verbose = 1)

grid_model.fit(X_train, y_train)

#Display the best combination of parameters for your model
#This is pretty in line with the solutions file where alpha = 100 and l1_ratio = 1

grid_model.best_params_

#Evaluate your model's performance on the unseen 10% scaled test set. 

y_pred = grid_model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error

MAE = mean_absolute_error(y_test, y_pred)
RMSE = mean_squared_error(y_test, y_pred)

#My model had a MAE of 14195 vs 14149 from the solutions. My RMSE was 20558 vs 20532 solutions
print('MAE: '+str(int(MAE))+', RMSE: '+str(int(RMSE**0.5)))