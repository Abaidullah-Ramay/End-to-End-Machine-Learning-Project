FROM python:3.10-slim-buster

# Update package lists and install AWS CLI and dependencies
RUN apt update -y && apt install awscli -y
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose both ports (8080 for FastAPI, 8501 for Streamlit)
EXPOSE 8080
EXPOSE 8501

# Run both the FastAPI backend and Streamlit frontend simultaneously
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8080 & streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]