import streamlit as st
html_file_path = "Dealership-map.html"

# Read the HTML file
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        map_html = f.read()
    
    # Embed the HTML in Streamlit
    st.components.v1.html(map_html, height=600, scrolling=True)
except FileNotFoundError:
    st.error("The HTML file containing the map was not found. Please check the file path.")
