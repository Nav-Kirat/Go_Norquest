import subprocess
import sys

try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Load datasets
df_used = pd.read_csv('used_cars.csv')
df_new = pd.read_csv('new_cars.csv')

# Preprocess Used Cars Data
used_cars = df_used
agg_data_used = used_cars.groupby('region_label').agg(
    avg_price=('price', 'mean'),
    avg_mileage=('mileage', 'mean'),
    total_sales=('vin', 'count'),
    avg_days_on_market=('days_on_market', 'mean')
).reset_index()

scaler_used_cars = MinMaxScaler()
X_used = agg_data_used[['avg_price', 'avg_mileage', 'avg_days_on_market']]
X_used_scaled = scaler_used_cars.fit_transform(X_used)
X_used_scaled[:, 1] *= 1.5

kmeans_used_cars = KMeans(n_clusters=6, random_state=42)
agg_data_used['cluster'] = kmeans_used_cars.fit_predict(X_used_scaled)

# Preprocess New Cars Data
new_cars = df_new
agg_data_new = new_cars.groupby(['region_label', 'drivetrain_from_vin']).agg(
    avg_price=('price', 'mean'),
    total_sales=('vin', 'count'),
    avg_days_on_market=('days_on_market', 'mean')
).reset_index()

encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
drivetrain_encoded = encoder.fit_transform(agg_data_new[['drivetrain_from_vin']])
encoded_drivetrain_columns = encoder.get_feature_names_out(['drivetrain_from_vin'])
drivetrain_encoded_df = pd.DataFrame(drivetrain_encoded, columns=encoded_drivetrain_columns)

agg_data_new = pd.concat([agg_data_new, drivetrain_encoded_df], axis=1)
scaler_new_cars = MinMaxScaler()
X_new = agg_data_new[['avg_price', 'avg_days_on_market'] + list(encoded_drivetrain_columns)]
X_new_scaled = scaler_new_cars.fit_transform(X_new)
X_new_scaled[:, 1] *= 1.5

kmeans_new_cars = KMeans(n_clusters=6, random_state=42)
agg_data_new['cluster'] = kmeans_new_cars.fit_predict(X_new_scaled)

# Define Prediction Functions
def predict_used_car_region(price, mileage, drivetrain, car_make=None):
    car_features = np.array([[price, mileage]])
    car_features_scaled = scaler_used_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_used_cars.predict(car_features_scaled)[0]
    best_regions = agg_data_used[agg_data_used['cluster'] == predicted_cluster]
    if car_make:
        st.write(f"Car Make: {car_make} factored in for insights.")
    return best_regions[['region_label', 'avg_price', 'avg_mileage', 'total_sales']]

def predict_new_car_region(price, mileage, drivetrain, car_make=None):
    drivetrain_encoded_input = encoder.transform([[drivetrain]])
    car_features = np.concatenate([[price, mileage], drivetrain_encoded_input[0]])
    car_features_scaled = scaler_new_cars.transform([car_features])
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_new_cars.predict(car_features_scaled)[0]
    best_regions = agg_data_new[agg_data_new['cluster'] == predicted_cluster]
    if car_make:
        st.write(f"Car Make: {car_make} factored in for insights.")
    return best_regions[['region_label', 'avg_price', 'total_sales']]

# Streamlit App
st.title("🚗 Car Sales Region Predictor")

# Sidebar for additional settings
st.sidebar.title("⚙️ Advanced Options")
enable_summary = st.sidebar.checkbox("Show Prediction Summary", value=True)

# Create Form
st.write("### Enter Car Details")
car_type = st.radio("What type of car are you selling?", options=["Used", "New"], index=0)
car_price = st.slider("Car Price ($)", min_value=5000, max_value=100000, value=30000, step=500)

# Drivetrain input
car_drivetrain = st.selectbox("Select Drivetrain", options=encoder.categories_[0])

# Mileage input
car_mileage = st.slider("Car Mileage (miles)", min_value=0, max_value=200000, value=50000, step=5000)

# Optional Car Make input
car_make = st.text_input("Car Make (Optional)", placeholder="Enter car make, e.g., Toyota, Ford")

# Submit Button
submitted = st.button("🔮 Predict Best Region")

# Handle Predictions
if submitted:
    if car_type == "Used":
        best_regions = predict_used_car_region(car_price, car_mileage, car_drivetrain, car_make)
        st.write("### Best Regions for Selling a Used Car")
    else:
        best_regions = predict_new_car_region(car_price, car_mileage, car_drivetrain, car_make)
        st.write("### Best Regions for Selling a New Car")

    # Display DataFrame
    st.dataframe(best_regions)

    # Optional Summary
    if enable_summary:
        total_sales = best_regions['total_sales'].sum()
        st.write(f"📊 Total Sales in Recommended Regions: **{total_sales}**")
