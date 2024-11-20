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
power_bi_embed_url = "https://app.powerbi.com/groups/me/reports/724471ab-a1c7-463d-aae5-41937040853e?ctid=2ba011f1-f50a-44f3-a200-db3ea74e29b7&amp;pbi_source=linkShare&amp;bookmarkGuid=8d1990d9-641c-4f7d-afb3-d6814fb76182"

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
