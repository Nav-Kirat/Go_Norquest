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

#Section 2

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
st.subheader("🚗 Used vs New Cars Sold in Edmonton Regions")
st.bar_chart(sales_pivot)



#Section 3

# Group by model year and calculate average price
price_by_year = df_combined.groupby("model_year")["price"].mean().reset_index()
price_by_year = price_by_year.sort_values(by="model_year")  # Ensure proper order

# Plotting the line graph using Streamlit
st.subheader("📈 Average Price vs Model Year")
st.line_chart(data=price_by_year, x="model_year", y="price")

# Section 4

# Group by make and stock type to calculate the number of cars sold
top_sold_cars = (
    df_combined.groupby(["make", "stock_type"])["vin"]
    .count()
    .reset_index(name="cars_sold")
    .sort_values(by="cars_sold", ascending=False)
)

# Get the top 10 most sold cars
top_10_sold_cars = top_sold_cars.head(10)

# Plotting the bar chart using Streamlit
st.subheader("📊 Top 10 Sold Cars by Popular Makes and Stock Type")
st.bar_chart(data=top_10_sold_cars, x="make", y="cars_sold")
