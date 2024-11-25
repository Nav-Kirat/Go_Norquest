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

import pandas as pd
import streamlit as st

# Load datasets
df_used = pd.read_csv("used_cars.csv")
df_new = pd.read_csv("new_cars.csv")

# Add a 'car_type' column to distinguish between used and new cars
df_used["car_type"] = "Used"
df_new["car_type"] = "New"

# Combine the datasets
df_combined = pd.concat([df_used, df_new], ignore_index=True)

# Group by region_label and car_type to calculate the number of cars sold
sales_data = df_combined.groupby(["region_label", "car_type"]).size().reset_index(name="cars_sold")

# Pivot the data for easier plotting
sales_pivot = sales_data.pivot(index="region_label", columns="car_type", values="cars_sold").fillna(0)

# Plotting the bar graph using Streamlit
st.title("🚗 Used vs New Cars Sold in Edmonton Regions")
st.bar_chart(sales_pivot)

# Display raw data for reference
st.write("### Combined Sales Data by Region and Car Type")
st.write(sales_data)
