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