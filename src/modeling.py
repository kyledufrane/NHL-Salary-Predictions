from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

import numpy as np
import pandas as pd
##################################################################


def baseline_modeling_pipeline(X_train, X_test, y_train, y_test, model):
    
    if model == 'randomforest':
        model = RandomForestClassifier()
    elif model == 'extratrees':
        model = ExtraTreesClassifier()
    else:
        model = XGBClassifier()

    # numeric_features = X_train.select_dtypes(
    #     ['int64', 'float64']).columns.tolist()
    # categorical_features = X_train.select_dtypes(
    #     ['object', 'bool']).columns.tolist()

    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[('num', numeric_transformer, X_train),])
                     # ('cat', categorical_transformer, categorical_features)])

    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', model)])

    clf.fit(X_train, y_train)

    y_hat = clf.predict(X_test)

    print(classification_report(y_test, y_hat))

    # try:

    #     onehot_columns = clf.named_steps['preprocessor'] \
    #                             .named_transformers_['cat'] \
    #                             .get_feature_names(input_features=categorical_features)

    #     feature_importance = pd.DataFrame(data=clf.named_steps['classifier'].feature_importances_,
    #                             index=np.array(numeric_features + list(onehot_columns))) \
    #                             .sort_values(0, ascending=False)
    # except:
    #     feature_importance = []

    return clf # , feature_importance
