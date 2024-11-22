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
).reset_index()

scaler_used_cars = MinMaxScaler()
X_used = agg_data_used[['avg_price', 'avg_mileage']]
X_used_scaled = scaler_used_cars.fit_transform(X_used)
X_used_scaled[:, 1] *= 1.5

kmeans_used_cars = KMeans(n_clusters=6, random_state=42)
agg_data_used['cluster'] = kmeans_used_cars.fit_predict(X_used_scaled)

# Preprocess New Cars Data
new_cars = df_new
agg_data_new = new_cars.groupby('region_label').agg(
    avg_price=('price', 'mean'),
    avg_mileage=('mileage', 'mean'),
    total_sales=('vin', 'count'),
).reset_index()

scaler_new_cars = MinMaxScaler()
X_new = agg_data_new[['avg_price', 'avg_mileage']]
X_new_scaled = scaler_new_cars.fit_transform(X_new)
X_new_scaled[:, 1] *= 1.5

kmeans_new_cars = KMeans(n_clusters=6, random_state=42)
agg_data_new['cluster'] = kmeans_new_cars.fit_predict(X_new_scaled)

# Function to Predict Best Regions for Used Cars
def predict_used_car_region(price, mileage, drivetrain, make=None):
    # Filter original dataset by make if specified
    filtered_data = df_used if make is None else df_used[df_used['make'] == make]
    
    # Aggregate filtered data by region
    agg_data = filtered_data.groupby('region_label').agg(
        avg_price=('price', 'mean'),
        avg_mileage=('mileage', 'mean'),
        total_sales=('vin', 'count')
    ).reset_index()
    
    # Scale and cluster the aggregated data
    car_features = np.array([[price, mileage]])
    car_features_scaled = scaler_used_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_used_cars.predict(car_features_scaled)[0]
    
    # Get best regions from aggregated data
    best_regions = agg_data[agg_data['cluster'] == predicted_cluster]
    return best_regions[['region_label', 'avg_price', 'avg_mileage', 'total_sales']]


# Function to Predict Best Regions for New Cars
def predict_new_car_region(price, mileage, drivetrain, make=None):
    # Filter original dataset by make if specified
    filtered_data = df_new if make is None else df_new[df_new['make'] == make]
    
    # Aggregate filtered data by region
    agg_data = filtered_data.groupby('region_label').agg(
        avg_price=('price', 'mean'),
        avg_mileage=('mileage', 'mean'),
        total_sales=('vin', 'count')
    ).reset_index()
    
    # Scale and cluster the aggregated data
    car_features = np.array([[price, mileage]])
    car_features_scaled = scaler_new_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_new_cars.predict(car_features_scaled)[0]
    
    # Get best regions from aggregated data
    best_regions = agg_data[agg_data['cluster'] == predicted_cluster]
    return best_regions[['region_label', 'avg_price', 'avg_mileage', 'total_sales']]


# Function to Find Most Selling Car in a Region
def find_most_selling_car(region_label, df):
    region_cars = df[df['region_label'] == region_label]
    most_selling = region_cars.groupby('model').agg(
        total_sales=('vin', 'count'),
        avg_price=('price', 'mean'),
        avg_mileage=('mileage', 'mean')
    ).reset_index().sort_values(by='total_sales', ascending=False)
    if not most_selling.empty:
        return most_selling.iloc[0]
    else:
        return None

# Streamlit App
st.title("🚗 Car Sales Region Predictor")

# Sidebar for Advanced Options
st.sidebar.title("⚙️ Advanced Options")
enable_summary = st.sidebar.checkbox("Show Prediction Summary", value=True)

# Dropdown for Car Makes
car_makes = sorted([
    'Acura', 'Honda', 'Chrysler', 'Dodge', 'Jeep', 'Ram', 'Ford', 'Chevrolet', 'Pontiac', 'Buick',
    'Cadillac', 'Saturn', 'GMC', 'Lincoln', 'Mercury', 'Nissan', 'Volkswagen', 'Mazda', 'Suzuki',
    'Toyota', 'Lexus', 'Fiat', 'Kia', 'Hyundai', 'BMW', 'Infiniti', 'Mitsubishi', 'Mercedes-Benz',
    'Subaru', 'Hummer', 'Tesla', 'Rivian', 'Volvo', 'Scion', 'Genesis', 'Polestar', 'Jaguar',
    'Land Rover', 'Audi', 'Fisker', 'Smart', 'Mini', 'Porsche', 'Maserati', 'Alfa Romeo'
])

# Create Form
st.write("### Enter Car Details")
car_type = st.radio("What type of car are you selling?", options=["Used", "New"], index=0)
car_price = st.slider("Car Price ($)", min_value=5000, max_value=100000, value=30000, step=500)

# Optional Dropdown for Car Make
car_make = st.selectbox("Car Make (Optional)", options=["None"] + car_makes)

# Drivetrain Input
car_drivetrain = st.selectbox("Select Drivetrain", options=['FWD', 'RWD', 'AWD', '4WD'])

# Mileage Input
car_mileage = st.slider("Car Mileage (miles)", min_value=0, max_value=200000, value=50000, step=5000)

# Submit Button
submitted = st.button("🔮 Predict Best Region")

# Handle Predictions
if submitted:
    if car_type == "Used":
        best_regions = predict_used_car_region(car_price, car_mileage, car_drivetrain, make=car_make)
        st.write("### Best Regions for Selling a Used Car")
        dataset = df_used
    else:
        best_regions = predict_new_car_region(car_price, car_mileage, car_drivetrain, make=car_make)
        st.write("### Best Regions for Selling a New Car")
        dataset = df_new

    # Display Best Regions
    st.dataframe(best_regions)

    # Find and Display Most Selling Car for Each Region
    st.write("### Most Selling Cars in Recommended Regions")
    for region in best_regions['region_label']:
        most_selling = find_most_selling_car(region, dataset)
        if most_selling is not None:
            st.write(f"**Region:** {region}")
            st.write(f"**Most Selling Car Model:** {most_selling['model']}")
            st.write(f"**Total Sales:** {most_selling['total_sales']}")
            st.write(f"**Average Price:** ${most_selling['avg_price']:.2f}")
            st.write(f"**Average Mileage:** {most_selling['avg_mileage']:.2f} miles")
            st.write("---")
        else:
            st.write(f"No data available for region: {region}")
