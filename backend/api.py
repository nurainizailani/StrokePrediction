# intitialise libraries and packages
import pandas as pd
from fastapi import FastAPI
from pydantic import create_model
import joblib
import json
from fastapi.middleware.cors import CORSMiddleware
import os

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

model_folder_path = os.path.join(os.getcwd(), os.path.join("backend","model"))

# load feature names
with open(os.path.join(model_folder_path,"feature_names.json"), "r") as f:
    feature_names = json.load(f)

PredictionFeatures = create_model("PredictionFeatures",
    **{
        feature: (float, ...)
        for feature in feature_names
    }
)

# load summary of dataset
with open(r'C:\Users\nurai\OneDrive\Documents\GitHub\StrokePrediction\backend\summary_dict.json', "r") as f:
    summary_dict = json.load(f)

# Global variable to store the loaded model
model = None

# Download the model
def download_model():
    global model
    model = joblib.load(os.path.join(model_folder_path,"stroke_prediction_model.joblib"))

# Download the model immediately when the script runs
download_model()

# API Root endpoint
@app.get("/trial-info")
async def trial_info():
    return summary_dict

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
        "Post-stroke Survival (days)": int(prediction)
    }
