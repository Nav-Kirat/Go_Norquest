import streamlit as st
import pandas as pd

# Configure the Streamlit page
st.set_page_config(page_title="Car Sales Analysis", layout="wide")

# Title for the page
st.title("🚗 Car Sales Analysis in Edmonton")

# Path to the HTML file containing the map
html_new_map_path = "Dealership-map-new.html"
html_used_map_path = "Dealership-map-used.html"

# Load datasets
new_cars_file_path = "new_cars.csv"
used_cars_file_path = "used_cars.csv"

# Define the makes to focus on
new_car_makes = ['Ford', 'GMC', 'Ram', 'Chevrolet', 'Jeep', 'Nissan']
used_car_makes = ['Ford', 'Chevrolet', 'Hyundai', 'Honda', 'Toyota', 'Ram']

# Load and process the datasets
try:
    df_new = pd.read_csv(new_cars_file_path)
    df_used = pd.read_csv(used_cars_file_path)

    # Validate required columns
    required_columns = ['region_label', 'make', 'vin']
    for df, car_type in [(df_new, "new"), (df_used, "used")]:
        if not all(col in df.columns for col in required_columns):
            st.error(f"The {car_type} cars dataset must include the following columns: {', '.join(required_columns)}")
            st.stop()

    # Filter new and used cars by selected makes
    df_new_filtered = df_new[df_new['make'].isin(new_car_makes)]
    df_used_filtered = df_used[df_used['make'].isin(used_car_makes)]

    # Calculate sales by region and make for new cars
    new_region_make_sales = df_new_filtered.groupby(['region_label', 'make']).agg(
        total_sales=('vin', 'count')
    ).reset_index()

    # Top 10 regions for new cars
    top_new_regions = (
        new_region_make_sales.groupby('region_label')['total_sales']
        .sum()
        .nlargest(10)
        .index.tolist()
    )
    new_data_top_regions = new_region_make_sales[new_region_make_sales['region_label'].isin(top_new_regions)]

    # Calculate sales by region and make for used cars
    used_region_make_sales = df_used_filtered.groupby(['region_label', 'make']).agg(
        total_sales=('vin', 'count')
    ).reset_index()

    # Top 10 regions for used cars
    
