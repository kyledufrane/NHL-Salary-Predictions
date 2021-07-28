# --------------------------------------------------------------
# Data Cleaning library
# --------------------------------------------------------------

# Import libaries needed for functions

import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd
import statsmodels.api as sm
import datetime

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.formula.api import ols
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_regression

##################################################################

# Define the function
def performance(y_true, y_predict):
    """ 
    Calculates and returns the two performance scores between 
    true and predicted values - first R-Squared, then RMSE
    """

    # Calculate the r2 score between 'y_true' and 'y_predict'
    r2 = r2_score(y_true, y_predict)
    # Calculate the root mean squared error between 'y_true' and 'y_predict'
    rmse = np.sqrt(mean_squared_error(y_true, y_predict))
    # Return the score
    return r2, rmse

##################################################################

# feature selection
def select_features(X_train, y_train, X_test, features):
	# configure to select a subset of features
	fs = SelectKBest(score_func=f_regression, k=features)
	# learn relationship from training data
	fs.fit(X_train, y_train)
	# transform train input data
	X_train_fs = pd.DataFrame(fs.transform(X_train))
	# transform test input data
	X_test_fs = pd.DataFrame(fs.transform(X_test))
	return X_train_fs, X_test_fs, fs