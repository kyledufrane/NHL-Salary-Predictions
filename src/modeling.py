from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
##################################################################


def baseline_modeling_pipeline(X,y, model):
    if model == 'randomforest':
        model = RandomForestRegressor()
    elif model == 'extratrees':
        model = ExtraTreesRegressor()
    elif model == 'linearregression':
        model = LinearRegression()
    else:
        model = XGBRegressor()

    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42)

    numeric_features = X_train.select_dtypes(
        ['int64', 'float64']).columns.tolist()
    categorical_features = X_train.select_dtypes(
        ['object', 'bool']).columns.tolist()

    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[('num', numeric_transformer, numeric_features),
                      ('cat', categorical_transformer, categorical_features)])

    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', model)])

    clf.fit(X_train, y_train)

    y_hat = clf.predict(X_test)

    print('R2 test:', r2_score(y_test, y_hat))
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_hat)))

    try:

        onehot_columns = clf.named_steps['preprocessor'] \
                                .named_transformers_['cat'] \
                                .get_feature_names(input_features=categorical_features)

        feature_importance = pd.DataFrame(data=clf.named_steps['classifier'].feature_importances_,
                                index=np.array(numeric_features + list(onehot_columns))) \
                                .sort_values(0, ascending=False)
    except:
        feature_importance = []

    return clf, feature_importance
