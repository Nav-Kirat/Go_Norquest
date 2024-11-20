import streamlit as st

# Set page configuration
st.set_page_config(page_title="Power BI Dashboard", layout="wide")

# App title
st.title("📊 Power BI Dashboard Integration")

# Description
st.write(
    """
    Below is an embedded Power BI dashboard, providing insights into vehicle sales and geographical clusters in Edmonton. 
    """
)

# Power BI Embed Link (replace with your own embed link)
power_bi_embed_url = "https://app.powerbi.com/reportEmbed?reportId=3ffbcd45-fe80-41e1-aa7b-23adba1df52a&autoAuth=true&ctid=2ba011f1-f50a-44f3-a200-db3ea74e29b7%22"

# Embed Power BI using an iframe
st.components.v1.html(
    f"""
    <iframe 
        title="Power BI Dashboard"
        width="100%" 
        height="600" 
        src="{power_bi_embed_url}" 
        frameborder="0" 
        allowFullScreen="true"></iframe>
    """,
    height=600,  # Adjust height as needed
    scrolling=True
)
