from fastapi import FastAPI
from pydantic import BaseModel,Field
import joblib
import pandas as pd 
from pathlib import Path
''' BaseModel is the blueprint for creating structured, self‑validating data objects in Python,
 and it’s what powers FastAPI’s request/response validation'''


# create the FastAPI appication
app=FastAPI()

pipeline=joblib.load(Path(__file__).resolve().parent.parent / "random_forest_model.joblib")

class DeliveryRequest(BaseModel):
	customer_state:str
	total_price:float=Field(ge=0)
	total_freight:float=Field(ge=0)
	product_category_name_english:str|None=Field(default=None)
	payment_value:float=Field(ge=0)
	purchase_month:int = Field(ge=1,le=12)

class PredictionResponse(BaseModel):
	predicted_delivery_days:float=Field(ge=0)

@app.post('/predict',response_model=PredictionResponse)
def predict (request:DeliveryRequest):
	features=pd.DataFrame([request.model_dump()])

	prediction=pipeline.predict(features)[0]

	return {'predicted_delivery_days':float(prediction)}



# uvicorn main:app --reload 








'''



class DeliveryRequest(BaseModel):
    distance: float = Field(gt=0)
    product_weight: float = Field(ge=0)


class PredictionResponse(BaseModel):
    predicted_delivery_days: float


@app.post("/predict", response_model=PredictionResponse)
def predict(request: DeliveryRequest):
    features = pd.DataFrame([request.model_dump()])

    prediction = pipeline.predict(features)[0]

    return {
        "predicted_delivery_days": float(prediction)
    }'''