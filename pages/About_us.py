import streamlit as st

# Set page title and layout
st.set_page_config(page_title="About Us", layout="centered")

# About Us Page Title
st.title("🤝 About Us")

# Group Photo Section
st.image("group_photo.jpg", caption="Our Amazing Go-Auto Team", use_column_width=True)

# Team Details
st.header("Meet the Team")

# Team Member Details
team_members = [
    {
        "name": "Alice Johnson",
        "linkedin": "https://www.linkedin.com/in/alice-johnson",
        "role": "Team Lead - Machine Learning Specialist",
    },
    {
        "name": "Bob Smith",
        "linkedin": "https://www.linkedin.com/in/bob-smith",
        "role": "Data Analyst - Visualization Expert",
    },
    {
        "name": "Cathy Brown",
        "linkedin": "https://www.linkedin.com/in/cathy-brown",
        "role": "Data Engineer - Backend Developer",
    },
    {
        "name": "David Lee",
        "linkedin": "https://www.linkedin.com/in/david-lee",
        "role": "Project Manager - Communication Specialist",
    },
]

# Display LinkedIn Profiles and Roles
for member in team_members:
    # LinkedIn Profile
    st.markdown(
        f"### [{member['name']}]({member['linkedin']})",
        unsafe_allow_html=True,
    )
    # Team Role
    st.markdown(f"**Role**: {member['role']}")
    st.write("---")
