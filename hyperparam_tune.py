from tune_sklearn import TuneGridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle
from src.clean_data import clean_data


def tune():
    df = clean_data()
    df_ = df[['career_assists', 'career_points', 'career_powerPlayTimeOnIcePerGame',
              'career_shots', 'career_powerPlayTimeOnIce', 'career_powerPlayPoints',
              'assists22', 'career_timeOnIce', 'career_evenTimeOnIce',
              'powerPlayTimeOnIcePerGame22']]

    X = df_
    y = df['Salary_2021-22']

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    param_grid = {
        'n_estimators': range(1, 500, 5),
        'criterion': ['squared_error', 'absolute_error', 'poisson'],
        'max_depth': [None, 100, 200, 500, 1000],
        'min_samples_split': [2, 3, 4, 5],
        'min_samples_leaf': range(1, 10, 2),
        'max_features': ['sqrt', 'log2', None],
        'bootstrap': [True],
        'oob_score': [True, False],
        'ccp_alpha': np.linspace(0, 1, 9)
    }

    tune_search = TuneGridSearchCV(
        RandomForestRegressor(),
        param_grid,
        n_jobs=-1,
        # early_stopping=True,
        scoring='neg_mean_absolute_error',
        verbose=2,
        use_gpu=True
    )

    tune_search.fit(X_train, y_train)

    y_hat = tune_search.predict(X_test)

    pickle_out = open("models/rf_tune_search", "wb")
    pickle.dump(tune_search, pickle_out)
    pickle_out.close()

    print('Mean Absolute Error:', mean_absolute_error(y_test, y_hat))


if __name__ == '__main__':
    tune()
