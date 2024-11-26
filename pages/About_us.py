import streamlit as st

# Set page title and layout
st.set_page_config(page_title="About Us", layout="centered")

# About Us Page Title
st.title("🤝 About Us")

# Group Photo Section
st.image("app_files/group_photo.jpeg", caption="Our Amazing Go-Auto Team", use_column_width=True)

# Team Details
st.header("Meet the Team")

# Team Member Details
team_members = [
    {
        "name": "Navkirat singh",
        "linkedin": "https://linkedin.com/in/navkirat",
        "role": "Team Lead",
    },
    {
        "name": "Dionathan Dos Santos",
        "linkedin": "https://www.linkedin.com/in/dionathanadiel",
        "role": "Model Developer",
    },
    {
        "name": "Vinit Kataria",
        "linkedin": "https://www.linkedin.com/in/vinit-kataria-46b13b222/",
        "role": "Result Interpreter and presenter",
    },
    {
        "name": "Mayank khera",
        "linkedin": "https://www.linkedin.com/in/mayank-khera-915b12252/",
        "role": "Data gathering and preparation (Scrum Master)",
    },
]

# Create columns for the team members
cols = st.columns(len(team_members))

# Populate each column with member details
for col, member in zip(cols, team_members):
    with col:
        # Embed LinkedIn profile using an iframe
        st.markdown(
            f"""
            <iframe src="{member['linkedin']}" width="300" height="400" frameborder="0"></iframe>
            """,
            unsafe_allow_html=True,
        )
        # Display member name and role
        st.markdown(f"### {member['name']}")
        st.markdown(f"**Role**: {member['role']}")
