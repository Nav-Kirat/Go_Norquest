# Project - Go_Norquest

[![Interactive Map](https://github.com/user-attachments/assets/de9ba237-9d42-4852-a3ee-57a0a0ed7e3d)](https://github.com/Nav-Kirat/Go_Norquest/blob/master/app_files/Dealership-map.html)

## Description
Go_Norquest leverages a dataset compiled by the Business Intelligence Team at Go Auto, integrating APIs from the Canadian Black Book (CBB). The dataset includes vehicle listings—both active and sold—across dealerships in Edmonton within the past 30 days. Each listing contains detailed information, including year, make, model, mileage, price, and dealership details like location and listing specifics.

The project's objective is to apply exploratory data analysis (EDA) and machine learning techniques, with a focus on data visualization via Microsoft Power BI, to:
- Identify geographical clusters within Edmonton where vehicles sell most effectively.
- Analyze sales and gross sales by dealership postal codes.
- Provide actionable insights to optimize marketing efforts and inventory distribution.

---

## Data Exploration
- **Dataset Overview**:
  - 145,114 rows and 49 columns.
  - Key metrics include `price`, `mileage`, `days_on_market`, and dealership data.
- **Descriptive Statistics**:
  - Spread analysis for columns like `price` and `mileage`.
- **Initial Data Preview**:
  - Overview of column types and sample data.

---

## Data Cleaning & Processing
1. **Key Columns**: Focused on vehicle listings, dealer information, and attributes.
2. **Missing Values**: Rows with null values were removed to ensure data integrity.
3. **Geographical Data**: Postal codes converted to latitude and longitude using an external API.
4. **Region Categorization**: Data segmented into regions (North, South, East, West, Downtown, and Suburbs) based on postal code prefixes.
5. **Composite Key**: Added a unique identifier for each car listing.
6. **Standardized Dealer Names**: Mapped dealer names to consistent forms using `dealer_id`.

---

## Analysis & Results
### Sales and Stock Metrics
- **Total Sales per Dealer**: Calculated the number of sales per dealership.
- **Gross Sales**: Aggregated revenue for each dealer.
- **Active Inventory**: Counted the active vehicle listings for each dealer.

### Best-Selling Models
- Identified the most popular vehicle models for each dealer.

---

## Clustering Models
Two clustering models were developed to group dealerships by sales metrics and inventory characteristics.

### Model 1: Sales-Based Clustering
Clusters dealerships based on total sales and gross sales, incorporating geographical location.

### Model 2: New vs. Used Car Clustering
Segments dealerships by the ratio of new to used car sales, using K-Means to classify based on inventory composition and revenue.

---

## Price Analysis
- **Price Categories**: Vehicles categorized as `budget`, `mid_range`, and `high_end` based on price.
- **Dealer Insights**: Calculated average prices and category distribution for each dealership to analyze market positioning.

---

## Power BI Dashboard: Dealership Sales and Inventory Analysis

The Power BI dashboard provides an interactive platform for exploring dealership performance and vehicle sales data across Edmonton. It includes:

### Key Features
- **Interactive Dealership Map**:
  - Color-coded by clusters to highlight high-performing areas.
- **Filters**:
  - **Stock Type, Make, and Model**: Refine results.
  - **Vehicle Age**: Adjustable slider for inventory age.
  - **Gross Sales & Total Sales**: Narrow focus to specific sales ranges.
- **Dealership Summary**:
  - **Total Gross Sales**, **Total Cars Sold**, and **Top Models**.
- **Regional Price Trends**:
  - Bar chart showing average vehicle prices by Edmonton regions.

---

## Streamlit Application: Go Auto Dealership Analysis

**[Live Link](https://go-auto.streamlit.app/)**

An interactive Streamlit application complements the Power BI dashboard, offering real-time analysis and tools for dealership managers.

### Key Features
1. **Interactive Map**:
   - Displays dealerships with detailed tooltips (name, stock count, top models).
   - Zoom functionality for granular insights.
2. **Car Sales Region Classifier**:
   - Recommends the best region to sell a car based on price, mileage, make, and drivetrain.
   - Highlights matching dealerships in the selected region.
3. **Dealership Insights**:
   - View inventory and top models for dealerships in a specific region.
4. **Inventory Search**:
   - Filter by make, drivetrain, price range, and mileage.
5. **Dynamic Visualizations**:
   - Uses Pydeck for interactive geographical analysis with real-time tooltips and map styling.

---

## Example Use Case
A dealership manager can use the app to:
1. Determine the best region for selling a specific car based on its attributes.
2. Explore high-performing dealerships in the identified region.
3. Analyze inventory and sales trends to guide marketing and inventory strategies.

---


