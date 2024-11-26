import subprocess
import sys

try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import random

# Load datasets
df_used = pd.read_csv("used_cars.csv")
df_new = pd.read_csv("new_cars.csv")

# Preprocess Used Cars Data
used_cars = df_used
agg_data_used = used_cars.groupby("region_label").agg(
    avg_price=("price", "mean"),
    avg_mileage=("mileage", "mean"),
    total_sales=("vin", "count"),
).reset_index()

scaler_used_cars = MinMaxScaler()
X_used = agg_data_used[["avg_price", "avg_mileage"]]
X_used_scaled = scaler_used_cars.fit_transform(X_used)
X_used_scaled[:, 1] *= 1.5

kmeans_used_cars = KMeans(n_clusters=6, random_state=42)
agg_data_used["cluster"] = kmeans_used_cars.fit_predict(X_used_scaled)

# Preprocess New Cars Data
new_cars = df_new
agg_data_new = new_cars.groupby(["region_label", "drivetrain_from_vin"]).agg(
    avg_price=("price", "mean"),
    total_sales=("vin", "count"),
).reset_index()

encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
drivetrain_encoded = encoder.fit_transform(agg_data_new[["drivetrain_from_vin"]])
encoded_drivetrain_columns = encoder.get_feature_names_out(["drivetrain_from_vin"])
drivetrain_encoded_df = pd.DataFrame(drivetrain_encoded, columns=encoded_drivetrain_columns)

agg_data_new = pd.concat([agg_data_new, drivetrain_encoded_df], axis=1)
scaler_new_cars = MinMaxScaler()
X_new = agg_data_new[["avg_price"] + list(encoded_drivetrain_columns)]
X_new_scaled = scaler_new_cars.fit_transform(X_new)

kmeans_new_cars = KMeans(n_clusters=6, random_state=42)
agg_data_new["cluster"] = kmeans_new_cars.fit_predict(X_new_scaled)

# Define Prediction Functions
def predict_used_car_region(price, mileage, drivetrain, make=None):
    car_features = np.array([[price, mileage]])
    car_features_scaled = scaler_used_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5
    predicted_cluster = kmeans_used_cars.predict(car_features_scaled)[0]
    best_regions = agg_data_used[agg_data_used["cluster"] == predicted_cluster]
    return best_regions[["region_label", "total_sales"]]

def predict_new_car_region(price, mileage, drivetrain, make=None):
    car_features = np.array([[price, mileage]])
    car_features_scaled = scaler_used_cars.transform(car_features)
    car_features_scaled[:, 1] *= 1.5  # Apply the same weighting as used for training

    # Predict the cluster for the input car
    predicted_cluster = kmeans_used_cars.predict(car_features_scaled)[0]

    # Find the regions in the predicted cluster
    best_regions = agg_data_used[agg_data_used["cluster"] == predicted_cluster]

    return best_regions[["region_label", "total_sales"]]

# Function to get dealerships for a region with the selected car
# Function to get dealerships for a region with the selected car
def get_dealerships_with_car(region_label, df, make, price, mileage):
    # Filter dealerships in the given region
    region_dealerships = df[df["region_label"] == region_label]
    # Further filter dealerships based on the car's details
    filtered_dealerships = region_dealerships[
        (region_dealerships["make"] == make) &
        (region_dealerships["price"] <= price + 5000) &  # Add a price range tolerance
        (region_dealerships["price"] >= price - 5000) &
        (region_dealerships["mileage"] <= mileage + 10000) &  # Add a mileage range tolerance
        (region_dealerships["mileage"] >= mileage - 10000)
    ]
    # Add a count column for the number of cars at each dealership
    dealership_counts = filtered_dealerships.groupby("dealer_name").size().reset_index(name="car_count")
    filtered_dealerships = pd.merge(filtered_dealerships, dealership_counts, on="dealer_name")
    return filtered_dealerships[["Latitude", "Longitude", "dealer_name", "car_count"]]

# Generate unique colors for each dealership
def assign_colors(dealerships):
    colors = {}
    for dealer in dealerships["dealer_name"].unique():
        colors[dealer] = [random.randint(0, 255) for _ in range(3)]  # Random RGB color
    dealerships["color"] = dealerships["dealer_name"].map(colors)
    return dealerships, colors

# Streamlit App
st.title("🚗 Car Sales Region Classifier and Dealership Locator")

# Dropdown for Car Makes
car_makes = sorted([
    "Acura", "Honda", "Chrysler", "Dodge", "Jeep", "Ram", "Ford", "Chevrolet", "Pontiac", "Buick",
    "Cadillac", "Saturn", "GMC", "Lincoln", "Mercury", "Nissan", "Volkswagen", "Mazda", "Suzuki",
    "Toyota", "Lexus", "Fiat", "Kia", "Hyundai", "BMW", "Infiniti", "Mitsubishi", "Mercedes-Benz",
    "Subaru", "Hummer", "Tesla", "Rivian", "Volvo", "Scion", "Genesis", "Polestar", "Jaguar",
    "Land Rover", "Audi", "Fisker", "Smart", "Mini", "Porsche", "Maserati", "Alfa Romeo"
])

# Create Form
st.write("### Enter Car Details")
car_type = st.radio("What type of car are you considering?", options=["Used", "New"], index=0)
car_price = st.slider("Car Price ($)", min_value=5000, max_value=100000, value=30000, step=500)

# Optional dropdown for car make
car_make = st.selectbox("Car Make (Optional)", options=["None"] + car_makes)

# Optional Drivetrain input
car_drivetrain = st.selectbox("Select Drivetrain (Optional)", options=["None"] + list(encoder.categories_[0]))

# Mileage input
car_mileage = st.slider("Car Mileage (miles)", min_value=0, max_value=200000, value=50000, step=5000)

# Submit Button
submitted = st.button("🔮 Classify and Locate Dealerships")

# Handle Predictions
# Pydeck map with car count in tooltips
if submitted:
    if car_type == "Used":
        best_regions = predict_used_car_region(car_price, car_mileage, car_drivetrain, make=car_make)
        st.write("### Best Regions for Used Car")
    else:
        best_regions = predict_new_car_region(car_price, car_mileage, car_drivetrain, make=car_make)
        st.write("### Best Regions for New Car")
    st.dataframe(best_regions)
    if not best_regions.empty:
        selected_region = best_regions.iloc[0]["region_label"]
        st.write(f"### Dealerships in {selected_region} with the Selected Car")

        if car_make == "None":
            st.write("No car selected.")
        else:
            if car_type == "Used":
                dealerships = get_dealerships_with_car(selected_region, df_used, car_make, car_price, car_mileage)
            else:
                dealerships = get_dealerships_with_car(selected_region, df_new, car_make, car_price, car_mileage)

            if not dealerships.empty:
                # Assign colors to dealerships
                dealerships, color_map = assign_colors(dealerships)

                # Pydeck map with colored markers and car count in tooltips
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=dealerships,
                    get_position="[Longitude, Latitude]",
                    get_fill_color="[color[0], color[1], color[2], 160]",
                    get_radius=300,  # Adjust radius
                    pickable=True,
                )

                view_state = pdk.ViewState(
                    latitude=dealerships["Latitude"].mean(),
                    longitude=dealerships["Longitude"].mean(),
                    zoom=10,
                )

                # Include car count in tooltips
                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style="mapbox://styles/mapbox/light-v10",
                    tooltip={"html": "<b>{dealer_name}</b><br>Cars available: {car_count}", "style": {"color": "white"}},
                )

                st.pydeck_chart(r)

                # Display dealership details in a table
                st.write("### Dealership Details (Color-Coded)")
                dealership_table = dealerships[["dealer_name", "car_count", "Latitude", "Longitude"]]
                st.write(dealership_table)
            else:
                st.write("No dealerships found in the selected region with the specified car.")
