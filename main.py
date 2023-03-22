import ml.classifier as clf
from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKey

from ml.modelType import ModelType
from pandas import DataFrame
import auth

from joblib import load

app = FastAPI(
    title="TITLE OF YOUR API",
    description="DESCRIPTION OF YOUR API",
    version="0.0.9000")

@app.on_event('startup')
async def load_model():

    clf.model = load("ml/models/model.joblib")
    clf.names = clf.model.feature_names_in_

@app.get('/', tags=['hello'])
async def root():
    return {"message": "Hello World"}


@app.post('/api/predict', tags=['predictions'])
async def get_prediction(model_type: ModelType, api_key: APIKey = Depends(auth.get_api_key)):
    data_dict = dict(model_type)['data']
    data = DataFrame(data_dict, index=[0])
    prediction = clf.model.predict(data)[0] 
    return {"prediction": prediction}
