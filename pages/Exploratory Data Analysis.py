import streamlit as st
import pandas as pd

# Path to the HTML file containing the map
html_file_path = "Dealership-map.html"

# Configure the Streamlit page
st.set_page_config(page_title="Dealership-map", layout="wide")

# Title for the page
st.title("🗺️ Dealerships in Edmonton")

# Read and embed the HTML file
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        map_html = f.read()
    
    # Embed the HTML map in Streamlit
    st.components.v1.html(map_html, height=600, scrolling=True)
except FileNotFoundError:
    st.error("The HTML file containing the map was not found. Please check the file path.")

#Plot 1
# Load dataset
file_path = "new_cars.csv"  # Update with your actual dataset path
try:
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ['region_label', 'make', 'vin']
    if not all(col in df.columns for col in required_columns):
        st.error(f"The dataset must include the following columns: {', '.join(required_columns)}")
    else:
        # Calculate sales by region and make
        region_make_sales = df.groupby(['region_label', 'make']).agg(
            total_sales=('vin', 'count')
        ).reset_index()

        # Find the top 10 regions by sales
        top_regions = (
            region_make_sales.groupby('region_label')['total_sales']
            .sum()
            .nlargest(10)
            .index.tolist()
        )

        # Filter data for the top regions
        filtered_data = region_make_sales[region_make_sales['region_label'].isin(top_regions)]

        # Streamlit bar chart
        st.write("### Top 10 Regions for New Car Sales by Most Popular Makes")
        st.bar_chart(filtered_data.pivot(index='region_label', columns='make', values='total_sales').fillna(0))
except FileNotFoundError:
    st.error("The dataset file was not found. Please check the file path.")
except Exception as e:
    st.error(f"An error occurred: {e}")
