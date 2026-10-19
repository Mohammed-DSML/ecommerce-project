import joblib
import pandas as pd

rf_model=joblib.load('week7_8_model/random_forest_model.joblib')
print("Random Forest model loaded successfully!")

# Select one example from your test set
X_new= pd.read_csv(
    "week7_8_model/test_order.csv"
)
prediction=rf_model.predict(X_new)
print(f"Predicted delivery time: {prediction[0]:.2f} days")