# intitialise libraries and packages
import uvicorn
import pandas as pd
from fastapi import FastAPI
from pydantic import create_model
import joblib
import json
from fastapi.middleware.cors import CORSMiddleware

# initialize FastAPI
app = FastAPI()

# add CORS middleware to allow requests from frontend to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load feature names
with open("feature_names.json", "r") as f:
    feature_names = json.load(f)

PredictionFeatures = create_model("PredictionFeatures",
    **{
        feature: (float, ...)
        for feature in feature_names
    }
)

# Global variable to store the loaded model
model = None

# Download the model
def download_model():
    global model
    model = joblib.load('stroke_prediction_model.joblib')

# Download the model immediately when the script runs
download_model()

# API Root endpoint
@app.get("/")
async def index():
    return {"message": "Survival Prediction After Stroke"}

# Prediction endpoint
@app.post("/predict")
async def predict(features: PredictionFeatures):

    # Create input DataFrame for prediction
    input_data = pd.DataFrame([features.model_dump()],columns=feature_names)

    # Predict using the loaded model
    prediction = model.predict(input_data)[0]

    return {
        "Post-stroke Survival (days)": prediction
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)