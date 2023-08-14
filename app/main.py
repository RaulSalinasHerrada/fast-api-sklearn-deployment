import ml.classifier as clf
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey
# from fastapi import HTTPException
# from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from ml.modelType import ModelType
from ml.training import fill_and_frame
from pandas import DataFrame
import pandas as pd
import auth
import os
import traceback

import joblib 

app = FastAPI(
    title=os.environ.get("API_TITLE", "A default title"),
    description=os.environ.get("API_DESCRIPTION", "A default description"),
    version=os.environ.get("API_VERSION", "0.0.9000"))

@app.on_event('startup')
async def load_model():
    clf.model = joblib.load("./ml/models/model.joblib")
    clf.names = clf.model.feature_names_in_

@app.get('/', tags=['hello_world'])
async def root():
    return {"message": "Hello World"}

@app.get('/api/column_names',tags=['predictions'])
async def get_names(api_key: APIKey = Depends(auth.get_api_key)):
    return {'names': clf.names}

@app.post('/api/predict', tags=['predictions'])
async def get_prediction(
    model_type: ModelType,
    api_key: APIKey = Depends(auth.get_api_key)):
    
    try:
        data_dict = model_type.data
        data_dict = {k: [float(v)] for k,v in data_dict.items()}
        data = DataFrame.from_dict(data_dict, orient = 'columns')
        data = fill_and_frame(data, clf.names)
        prediction = clf.model.predict_proba(data) 
        
        json_pred = pd.DataFrame(prediction).to_dict(orient="records")
        return {"prediction": json_pred}
    
    except Exception as e:
        tb = traceback.format_exc()
        return {
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "traceback": tb}
        

