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
    top_used_regions = (
        used_region_make_sales.groupby('region_label')['total_sales']
        .sum()
        .nlargest(10)
        .index.tolist()
    )
    used_data_top_regions = used_region_make_sales[used_region_make_sales['region_label'].isin(top_used_regions)]

    # Layout: Side-by-side maps
    col1, col2 = st.columns(2)

    # Embed the new cars map
    with col1:
        st.write("### 🗺️ Dealerships for New Cars (Selected Makes)")
        try:
            with open(html_new_map_path, "r", encoding="utf-8") as f:
                new_map_html = f.read()
            st.components.v1.html(new_map_html, height=600, scrolling=True)
        except FileNotFoundError:
            st.error("The HTML file for the new cars map was not found.")

    # Embed the used cars map
    with col2:
        st.write("### 🗺️ Dealerships for Used Cars (Selected Makes)")
        try:
            with open(html_used_map_path, "r", encoding="utf-8") as f:
                used_map_html = f.read()
            st.components.v1.html(used_map_html, height=600, scrolling=True)
        except FileNotFoundError:
            st.error("The HTML file for the used cars map was not found.")

    # Visualizations
    st.write("## 📊 Sales by Region and Make")

    # Bar chart for new cars
    st.write("### New Cars: Top 10 Regions for Selected Makes")
    st.bar_chart(new_data_top_regions.pivot(index='region_label', columns='make', values='total_sales').fillna(0))

    # Bar chart for used cars
    st.write("### Used Cars: Top 10 Regions for Selected Makes")
    st.bar_chart(used_data_top_regions.pivot(index='region_label', columns='make', values='total_sales').fillna(0))

except FileNotFoundError as e:
    st.error(f"Dataset file not found: {e.filename}")
except Exception as e:
    st.error(f"An error occurred: {e}")
