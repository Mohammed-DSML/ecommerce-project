
# 1. Use Python 3.12 as the base environment
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies file
COPY requirements.txt .

# 4. Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the API code
COPY api/ ./api/

# 6. Copy the trained ML model
COPY random_forest_model.joblib .

# 7. Start the FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
