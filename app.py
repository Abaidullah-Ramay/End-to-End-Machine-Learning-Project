import os
import uvicorn
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mlProject.pipeline.prediction import PredictionPipeline

app = FastAPI(title="Wine Quality Prediction API", version="1.0")

# Allow the Streamlit frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for strict input validation
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wine Quality Prediction API. Go to /docs for the interactive UI."}

@app.get("/train")
def train_model():
    """Triggers the ML pipeline to retrain the model."""
    try:
        os.system("python main.py")
        return {"message": "Training successful!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
def predict(features: WineFeatures):
    """Takes wine features and returns the predicted quality."""
    try:
        # Convert the Pydantic model into a 2D numpy array (1, 11) for the ML model
        data = np.array([[
            features.fixed_acidity, features.volatile_acidity, features.citric_acid,
            features.residual_sugar, features.chlorides, features.free_sulfur_dioxide,
            features.total_sulfur_dioxide, features.density, features.pH,
            features.sulphates, features.alcohol
        ]])
        
        obj = PredictionPipeline()
        prediction = obj.predict(data)
        
        return {"prediction": float(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Running on port 8080 to match the instructor's original Docker setup
    uvicorn.run(app, host="0.0.0.0", port=8080)