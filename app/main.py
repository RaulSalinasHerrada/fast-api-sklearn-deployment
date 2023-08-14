import pandas as pd
import auth
import os
import traceback
import joblib 

import ml.classifier as clf
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
from ml.schemas import DataSchema, ErrorSchema, PredictSchema, NamesSchema
from ml.ml_utils import fill_and_frame
from typing import List

app = FastAPI(
    title=os.environ.get("API_TITLE", "A local default title"),
    description=os.environ.get("API_DESCRIPTION", "A local default description"),
    version=os.environ.get("API_VERSION", "0.0.9001"))

@app.on_event('startup')
async def load_model():
    clf.model = joblib.load("./ml/models/model.joblib")
    clf.names = clf.model.feature_names_in_

@app.get('/', tags=['hello_world'])
async def root():
    return {"message": "Hello World"}

@app.get('/api/column_names',tags=['predictions'])
async def get_names(api_key: APIKey = Depends(auth.get_api_key)):
    return NamesSchema(names=clf.names)

@app.post('/api/predict', tags=['predictions'])
async def get_prediction(
    model_type: DataSchema,
    api_key: APIKey = Depends(auth.get_api_key)):
    
    try:
        data_dict = model_type.data
        data_format = dict()
        
        for k,v in data_dict.items():
            if isinstance(v, float | int):
                data_format[k] = [v]
            elif isinstance(v, List):
                data_format[k] = v
        
        data = pd.DataFrame.from_dict(data_format, orient = 'columns')
        data = fill_and_frame(data, clf.names)
        prediction = clf.model.predict_proba(data) 
        
        json_pred = pd.DataFrame(prediction).to_dict(orient="records")
        return PredictSchema(prediction=json_pred)
    
    except Exception as e:
        err_type = type(e).__name__
        err_msg = str(e)
        tb = traceback.format_exc()
        return ErrorSchema(
            error_type=err_type,
            error_msg= err_msg,
            traceback=tb)
        

