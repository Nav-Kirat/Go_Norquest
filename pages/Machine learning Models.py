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
def predict_used_car_region(price, mileage, days_on_market):
    car_features = np.array([[price, mileage, days_on_market]])
    car_features_scaled = scaler_used_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_used_cars.predict(car_features_scaled)[0]
    best_regions = agg_data_used[agg_data_used['cluster'] == predicted_cluster]
    return best_regions[['region_label', 'avg_price', 'avg_mileage', 'avg_days_on_market', 'total_sales']]

def predict_new_car_region(price, days_on_market, drivetrain):
    drivetrain_encoded_input = encoder.transform([[drivetrain]])
    car_features = np.concatenate([[price, days_on_market], drivetrain_encoded_input[0]])
    car_features_scaled = scaler_new_cars.transform([car_features])
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_new_cars.predict(car_features_scaled)[0]
    best_regions = agg_data_new[agg_data_new['cluster'] == predicted_cluster]
    return best_regions[['region_label', 'avg_price', 'avg_days_on_market', 'total_sales']]

# Streamlit App
st.title("🚗 Car Sales Region Predictor")

# Sidebar for advanced options
st.sidebar.title("🚀 Advanced Options")
st.sidebar.write("Customize your predictions with additional features.")
enable_chart = st.sidebar.checkbox("Show visual representation", value=True)
enable_summary = st.sidebar.checkbox("Show summary of predictions", value=True)

# Create Multi-Step Form
st.write("### Step 1: Select Car Type and Details")
car_type = st.radio("What type of car do you want to sell?", options=["Used", "New"], index=0)

st.write("### Step 2: Provide Car Details")
car_price = st.slider("Set the car price ($)", min_value=5000, max_value=100000, value=30000, step=1000)

if car_type == "Used":
    car_mileage = st.slider("Set the car mileage (miles)", min_value=0, max_value=200000, value=50000, step=5000)
    car_days_on_market = st.number_input("Expected days on market", min_value=0, value=30, step=1)
else:
    car_drivetrain = st.selectbox("Select the drivetrain", options=encoder.categories_[0])
    car_days_on_market = st.number_input("Expected days on market", min_value=0, value=30, step=1)

# Submit button
submitted = st.button("🔮 Predict Best Region")

# Handle Predictions
if submitted:
    st.write("### Results")
    if car_type == "Used":
        best_regions = predict_used_car_region(car_price, car_mileage, car_days_on_market)
        st.write("#### Best Regions for Selling a Used Car")
    else:
        best_regions = predict_new_car_region(car_price, car_days_on_market, car_drivetrain)
        st.write("#### Best Regions for Selling a New Car")
    
    st.dataframe(best_regions)

    # Optional visual representation
    if enable_chart:
        st.write("#### Visual Representation of Predictions")
        st.bar_chart(best_regions[['region_label', 'avg_price']].set_index('region_label'))

    # Optional summary
    if enable_summary:
        total_sales = best_regions['total_sales'].sum()
        st.write(f"📈 Total Sales in Recommended Regions: **{total_sales}**")
