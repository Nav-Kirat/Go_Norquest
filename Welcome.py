import streamlit as st


# Set page configuration
st.set_page_config(page_title="Go Auto Sales Analysis")

# Title Section
st.markdown(
    """
    <div style="background-color:#E52525;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">🚗 Go Auto Sales Analysis Dashboard 🚗</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Add some spacing
st.write("\n")

# Introduction Section
st.markdown(
    """
    ### Welcome to the Go Auto Sales Analysis Project!
    
    This project leverages a **dataset compiled by the Business Intelligence Team at Go Auto**, utilizing APIs from the **Canadian Black Book (CBB)**. The dataset includes:
    
    - **Vehicle Listings:** Active and sold vehicles across various dealerships in Edmonton within the last 30 days.
    - **Details:** Each listing provides rich details such as year, make, model, mileage, price, and dealership location.
    
    ---
    ### 🛠️ Project Goal:
    
    The main goal of this project was to:
    
    - Apply **Exploratory Data Analysis (EDA)** techniques.
    - Develop a **Machine Learning Model** for clustering.
    - Use **Power BI Visualizations** to:
        - Analyze geographical clusters in Edmonton.
        - Identify areas with the highest number of sales and total gross sales.
        - Optimize inventory distribution and enhance targeted marketing strategies.

    ---
    ### 🚀 Why This Matters:
    
    By identifying the top-performing geographical regions:
    
    - **Dealerships can target marketing efforts more effectively.**
    - **Inventory distribution can be optimized across Edmonton.**
    - **Operational efficiency** is improved, ultimately leading to increased revenue!
    
    ---
    """
)

# Add a visual element (optional image or icon)
st.markdown(
    """
    <div style="text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/1048/1048312.png" width="300" alt="Car Sales Icon">
    </div>
    """, 
    unsafe_allow_html=True
)

