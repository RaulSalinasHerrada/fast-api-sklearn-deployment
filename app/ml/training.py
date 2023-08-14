
import logging
import os
import pandas as pd
from joblib import dump


from sklearn.datasets import load_breast_cancer as load_dataset
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.preprocessing import MinMaxScaler as Scaler
from sklearn.impute import IterativeImputer as Imputer
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier as Estimator
from ml_utils import snake_case



def run(argv = None):
    
    test_size = 0.8

    X,y  = load_dataset(return_X_y=True, as_frame=True)
    
    X.columns = [snake_case(x) for x in X.columns]

    X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=test_size, random_state=42)
    
    X_valid
    
    # 3 stage pipeline: Scaling, Imputing values, Estimating
    pipe = Pipeline([
        ('scaler', Scaler()),
        ('imputer', Imputer()),
        ('estimator', Estimator(class_weight="balanced", random_state=122))
    ],verbose= True)

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_valid)
    
    if hasattr(pipe['estimator'],'feature_importances_'):
        importances = pipe['estimator'].feature_importances_
        forest_importances = pd.Series(importances, index = X.columns)
        forest_importances.sort_values(inplace=True, ascending= False)
        logging.info(forest_importances)

    logging.info("\n" + classification_report(y_valid, y_pred))

    path_model = os.path.normpath("./ml/models/model.joblib")
    dump(pipe, path_model, compress = ('gzip',9))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()