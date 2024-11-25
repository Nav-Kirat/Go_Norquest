import streamlit as st
import pandas as pd

# Path to the HTML file containing the map
html_file_path = "Dealership-map.html"

# Configure the Streamlit page
st.set_page_config(page_title="Dealership and Sales Insights", layout="wide")

# Title for the page
st.title("🚗 Dealerships and Sales Insights in Edmonton")

# Section 1: Map
st.subheader("🗺️ Dealership Locations")
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        map_html = f.read()
    # Embed the HTML map in Streamlit
    st.components.v1.html(map_html, height=600, scrolling=True)
except FileNotFoundError:
    st.error("The HTML file containing the map was not found. Please check the file path.")

# Section 2: Sales Analysis for New Cars
st.markdown("---")
st.header("📊 Sales Insights: New Cars")
st.subheader("Top 10 Regions for New Car Sales (Selected Makes)")

# Load New Cars Dataset
new_cars_path = "new_cars.csv"  # Update with your actual dataset path
new_cars_makes = ['Ford', 'GMC', 'Ram', 'Chevrolet', 'Jeep', 'Nissan']

try:
    df_new = pd.read_csv(new_cars_path)

    # Ensure required columns exist
    required_columns_new = ['region_label', 'make', 'vin']
    if not all(col in df_new.columns for col in required_columns_new):
        st.error(f"The new cars dataset must include the following columns: {', '.join(required_columns_new)}")
    else:
        # Filter dataset by selected makes
        df_new_filtered = df_new[df_new['make'].isin(new_cars_makes)]

        # Calculate sales by region and make
        new_region_make_sales = df_new_filtered.groupby(['region_label', 'make']).agg(
            total_sales=('vin', 'count')
        ).reset_index()

        # Find the top 10 regions by sales
        top_new_regions = (
            new_region_make_sales.groupby('region_label')['total_sales']
            .sum()
            .nlargest(10)
            .index.tolist()
        )

        # Filter data for the top regions
        new_filtered_data = new_region_make_sales[new_region_make_sales['region_label'].isin(top_new_regions)]

        # Streamlit bar chart for new cars
        st.bar_chart(new_filtered_data.pivot(index='region_label', columns='make', values='total_sales').fillna(0))
except FileNotFoundError:
    st.error("The new cars dataset file was not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred while processing new cars data: {e}")

# Section 3: Sales Analysis for Used Cars
st.markdown("---")
st.header("📊 Sales Insights: Used Cars")
st.subheader("Top 10 Regions for Used Car Sales (Selected Makes)")

# Load Used Cars Dataset
used_cars_path = "used_cars.csv"  # Update with your actual dataset path
used_cars_makes = ['Ford', 'Chevrolet', 'Hyundai', 'Honda', 'Toyota', 'Ram']

try:
    df_used = pd.read_csv(used_cars_path)

    # Ensure required columns exist
    required_columns_used = ['region_label', 'make', 'vin']
    if not all(col in df_used.columns for col in required_columns_used):
        st.error(f"The used cars dataset must include the following columns: {', '.join(required_columns_used)}")
    else:
        # Filter dataset by selected makes
        df_used_filtered = df_used[df_used['make'].isin(used_cars_makes)]

        # Calculate sales by region and make
        used_region_make_sales = df_used_filtered.groupby(['region_label', 'make']).agg(
            total_sales=('vin', 'count')
        ).reset_index()

        # Find the top 10 regions by sales
        top_used_regions = (
            used_region_make_sales.groupby('region_label')['total_sales']
            .sum()
            .nlargest(10)
            .index.tolist()
        )

        # Filter data for the top regions
        used_filtered_data = used_region_make_sales[used_region_make_sales['region_label'].isin(top_used_regions)]

        # Streamlit bar chart for used cars
        st.bar_chart(used_filtered_data.pivot(index='region_label', columns='make', values='total_sales').fillna(0))
except FileNotFoundError:
    st.error("The used cars dataset file was not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred while processing used cars data: {e}")
