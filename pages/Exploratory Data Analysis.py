import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])

import seaborn as sns

# File paths
html_file_path = "Dealership-map.html"
used_cars_path = "used_cars.csv"
new_cars_path = "new_cars.csv"

# Page Configuration
st.set_page_config(page_title="Dealership EDA", layout="wide")

# Title
st.title("🗺️ Dealerships in Edmonton")

# Embed the HTML map
st.write("### Dealership Map")
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=600, scrolling=True)
except FileNotFoundError:
    st.error("The HTML file containing the map was not found. Please check the file path.")

# Load datasets
@st.cache_data
def load_data():
    used_cars = pd.read_csv(used_cars_path)
    new_cars = pd.read_csv(new_cars_path)
    return used_cars, new_cars

used_cars, new_cars = load_data()

# Dataset Selection
st.sidebar.header("🔍 Filter Data")
data_type = st.sidebar.radio("Select Dataset", options=["Used Cars", "New Cars"], index=0)
if data_type == "Used Cars":
    df = used_cars
else:
    df = new_cars

# Dataset Filters
st.sidebar.write("### Filter Dataset")
make_filter = st.sidebar.multiselect("Filter by Make", options=df['make'].unique())
region_filter = st.sidebar.multiselect("Filter by Region", options=df['region_label'].unique())
price_range = st.sidebar.slider("Filter by Price Range", min_value=int(df['price'].min()), max_value=int(df['price'].max()), value=(int(df['price'].min()), int(df['price'].max())))

# Apply filters
if make_filter:
    df = df[df['make'].isin(make_filter)]
if region_filter:
    df = df[df['region_label'].isin(region_filter)]
df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

# Display Dataset
st.write("### Filtered Dataset")
st.dataframe(df)

# Summary Statistics
st.write("### Summary Statistics")
st.write(df.describe())

# Visualizations
st.write("### Visualizations")

# Price Distribution
st.write("#### Price Distribution")
fig, ax = plt.subplots()
sns.histplot(df['price'], kde=True, ax=ax)
ax.set_title("Price Distribution")
ax.set_xlabel("Price")
st.pyplot(fig)

# Sales by Region
st.write("#### Sales by Region")
region_sales = df.groupby('region_label')['vin'].count().sort_values(ascending=False).reset_index()
region_sales.columns = ['Region', 'Total Sales']

fig, ax = plt.subplots()
sns.barplot(data=region_sales, x='Region', y='Total Sales', ax=ax)
ax.set_title("Sales by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Total Sales")
plt.xticks(rotation=45)
st.pyplot(fig)

# Mileage vs. Price
st.write("#### Mileage vs. Price")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='mileage', y='price', hue='make', ax=ax)
ax.set_title("Mileage vs Price")
ax.set_xlabel("Mileage")
ax.set_ylabel("Price")
st.pyplot(fig)

# Correlation Heatmap
st.write("#### Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include=['float64', 'int64']).corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation Heatmap")
st.pyplot(fig)
