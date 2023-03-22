
import logging
import pandas as pd
import os
from joblib import dump

from typing import List

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer
from sklearn.metrics import classification_report
from sklearn.tree import ExtraTreeClassifier


def fill_and_frame(row_data:pd.DataFrame, model_names:List[str])->pd.DataFrame:
    """
    fill the dataframe with NA on the columns that aren't available (as the model impute them automatically)
    and returns a data frame copy with only the rows needed
    """

    import numpy as np

    col_data_set = {*row_data.columns}
    names_set = {*model_names}
    missing_names = names_set.difference(col_data_set)

    for nm in missing_names:
        row_data[nm] = np.NaN        

    return row_data[model_names]

def run(argv = None):

    iris = load_iris(as_frame=True)

    X = iris['data']
    y = iris['target']

    X_train, X_valid, y_train, y_valid = train_test_split(
    X, y, test_size=0.8, random_state=42)

    pipe = Pipeline([
        ('scaler', MinMaxScaler()),
        ('imputer', KNNImputer()),
        ('estimator', ExtraTreeClassifier())
    ],verbose= True)

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_valid)

    if hasattr(pipe['estimator'],'feature_importances_'):
        importances = pipe['estimator'].feature_importances_
        forest_importances = pd.Series(importances, index = X.columns)
        forest_importances.sort_values(inplace=True, ascending= False)
        logging.info(forest_importances)

    logging.info("\n" + classification_report(y_valid, y_pred))

    path_model = os.path.normpath("ml/models/model.joblib")
    dump(pipe, path_model, compress = ('gzip',9))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()