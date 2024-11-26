import streamlit as st
import pandas as pd
import altair as alt

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

# Section 2: Used vs New Cars Sold in Edmonton Regions
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

# Plotting the bar graph using Altair
st.subheader("🚗 Used vs New Cars Sold in Edmonton Regions")

sales_data_chart = sales_data.copy()
sales_data_chart['region_label'] = sales_data_chart['region_label'].astype(str)  # Ensure string for Altair

chart = alt.Chart(sales_data_chart).mark_bar().encode(
    x=alt.X('region_label:N', title='Region'),
    y=alt.Y('cars_sold:Q', title='Number of Cars Sold'),
    color=alt.Color('car_type:N', title='Car Type', scale=alt.Scale(domain=["Used", "New"], range=["#FF6F61", "#C0392B"])),
    tooltip=['region_label', 'car_type', 'cars_sold']
).properties(
    width=800,
    height=500
)

st.altair_chart(chart, use_container_width=True)

# Section 3: Average Price vs Model Year
# Group by model year and calculate average price
price_by_year = df_combined.groupby("model_year")["price"].mean().reset_index()
price_by_year = price_by_year.sort_values(by="model_year")  # Ensure proper order

# Plotting the line graph using Altair
st.subheader("📈 Average Price vs Model Year")

line_chart = alt.Chart(price_by_year).mark_line(color="#C0392B").encode(
    x=alt.X('model_year:Q', title='Model Year'),
    y=alt.Y('price:Q', title='Average Price'),
    tooltip=['model_year', 'price']
).properties(
    width=800,
    height=500
)

st.altair_chart(line_chart, use_container_width=True)

# Section 4: Top 10 Car Makes
# Group by make and stock_type to calculate the number of cars sold
sales_data_makes = (
    df_combined.groupby(["make", "car_type"])["vin"]
    .count()
    .reset_index(name="cars_sold")
)

# Calculate total cars sold per make
total_sales_per_make = (
    sales_data_makes.groupby("make")["cars_sold"]
    .sum()
    .reset_index(name="total_cars_sold")
)

# Get the top 10 makes by total cars sold
top_10_makes = total_sales_per_make.sort_values(by="total_cars_sold", ascending=False).head(10)["make"]

# Filter the sales data to include only the top 10 makes
top_sales_data = sales_data_makes[sales_data_makes["make"].isin(top_10_makes)]

# Sort the makes by total sales for consistent plotting
top_sales_data["make"] = pd.Categorical(
    top_sales_data["make"], 
    categories=top_10_makes, 
    ordered=True
)

# Plotting the stacked bar chart using Altair
st.subheader("📊 Top 10 Car Makes (Used vs New)")

red_color_scale = alt.Scale(domain=["Used", "New"], range=["#FF6F61", "#C0392B"])

chart = alt.Chart(top_sales_data).mark_bar().encode(
    x=alt.X('make:N', sort=top_10_makes, title='Make'),
    y=alt.Y('cars_sold:Q', title='Number of Cars Sold'),
    color=alt.Color('car_type:N', title='Stock Type', scale=red_color_scale),
    tooltip=['make', 'car_type', 'cars_sold']
).properties(
    width=800,
    height=500
)

st.altair_chart(chart, use_container_width=True)


