import streamlit as st

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
