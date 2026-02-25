import streamlit as st
import requests

st.set_page_config(page_title="Wine Quality Predictor", layout="centered")

st.title("🍷 Red Wine Quality Predictor")
st.write("Enter the physicochemical properties of the wine below to predict its quality score.")

# The URL where our FastAPI backend is running
API_URL = "http://localhost:8080/predict"

# Create a clean UI using columns
col1, col2 = st.columns(2)

with col1:
    fixed_acidity = st.number_input("Fixed Acidity", value=7.4, step=0.1)
    volatile_acidity = st.number_input("Volatile Acidity", value=0.70, step=0.01)
    citric_acid = st.number_input("Citric Acid", value=0.00, step=0.01)
    residual_sugar = st.number_input("Residual Sugar", value=1.9, step=0.1)
    chlorides = st.number_input("Chlorides", value=0.076, step=0.001, format="%.3f")
    free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", value=11.0, step=1.0)

with col2:
    total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", value=34.0, step=1.0)
    density = st.number_input("Density", value=0.9978, step=0.0001, format="%.4f")
    pH = st.number_input("pH", value=3.51, step=0.01)
    sulphates = st.number_input("Sulphates", value=0.56, step=0.01)
    alcohol = st.number_input("Alcohol", value=9.4, step=0.1)

# Prediction Button
if st.button("Predict Quality", use_container_width=True):
    # Package the inputs into a dictionary that matches our FastAPI Pydantic model
    payload = {
        "fixed_acidity": fixed_acidity,
        "volatile_acidity": volatile_acidity,
        "citric_acid": citric_acid,
        "residual_sugar": residual_sugar,
        "chlorides": chlorides,
        "free_sulfur_dioxide": free_sulfur_dioxide,
        "total_sulfur_dioxide": total_sulfur_dioxide,
        "density": density,
        "pH": pH,
        "sulphates": sulphates,
        "alcohol": alcohol
    }
    
    try:
        with st.spinner("Analyzing wine properties..."):
            # Send the POST request to the FastAPI backend
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            
            # Extract the prediction from the JSON response
            result = response.json()
            prediction = result.get("prediction")
            
            st.success(f"### Predicted Wine Quality Score: {prediction:.2f}")
            
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to the backend. Is your FastAPI server running on port 8080?")
    except Exception as e:
        st.error(f"An error occurred: {e}")