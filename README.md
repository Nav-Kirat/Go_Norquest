
# Project - Go_Norquest

## Description
This project leverages a dataset compiled by the Business Intelligence Team at Go Auto, utilizing APIs from the Canadian Black Book (CBB). The dataset includes vehicle listings—both active and sold—across various dealerships in Edmonton within the last 30 days. Detailed information about each vehicle is provided, including year, make, model, mileage, price, and dealership information such as location and listing specifics. 

The goal of this Project was to apply exploratory data analysis (EDA) and develop a machine learning model with data visualization using Microsoft’s PowerBI to Analyze and identify geographical clusters within Edmonton where vehicles sell the best, based on the number of sales and total gross sales by dealership postal codes. This will allow dealerships to target marketing efforts more effectively and optimize inventory distribution across different regions of the city. 

## Data Exploration
- **Dataset Shape**: The dataset contains 145,114 rows and 49 columns.
- **Basic Stats**: Descriptive statistics are generated to understand the spread of the data for key columns such as `price`, `mileage`, and `days_on_market`.
- **Data Preview**: The initial rows of the dataset provide an overview of column types and content.

## Data Cleaning & Processing
1. **Selecting Key Columns**: The analysis focuses on key columns related to listings, dealer information, and vehicle attributes.
2. **Handling Missing Values**: Rows with null values were dropped to ensure data consistency.
3. **Converting Postal code to Lat/Lon coordinated**: Postal codes from the dataset were converted into latitude and longitude using a external API. This was crucial for the creation of map.
5. **Region Labeling**: The dataset is categorized into regions (North, South, East, West, Downtown, and Greater Edmonton Suburbs) based on postal code prefixes.
6. **Composite key**: A new feature composite key was created in Dataframe. The purpose of the Composite key was to create a column was can be unique for each car lisiting in datset.
7. **Standardizing Dealer Names**: Dealer names are mapped to standardized forms based on `dealer_id`.

## Analysis & Results
### Sales and Stock Metrics
1. **Total Sales per Dealer**: Each dealership’s total number of sales is calculated.
2. **Gross Sales Calculation**: The sum of sales revenue (`price`) for each dealer is computed and saved for further analysis.
3. **Active Stock Count**: Count of active vehicle listings per dealer.

### Model-Specific Sales
- **Best Selling Model**: Identifies the most popular vehicle model for each dealer based on sales counts.

## Clustering Models
Two clustering models were applied to group dealerships based on sales metrics and location for easier segmentation and analysis in Power BI.

### Model 1: Sales-Based Clustering
Using total sales and gross sales metrics, this model clusters dealerships based on their sales performance and regional location.

### Model 2: New vs Used Car Clustering
This model segments dealers by their inventory and revenue from new and used car sales, using K-Means to classify dealerships based on their sales mix.

## Price Analysis
1. **Price Categories**: Vehicles are segmented into `budget`, `mid_range`, and `high_end` categories based on the `price` column.
2. **Price Sensitivity Analysis**: For each dealer, the average vehicle price and counts for each price category are calculated, enabling analysis of dealership positioning within the market.
