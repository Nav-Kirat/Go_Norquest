import sys
import os
import streamlit as st

st.write(f"Python Executable: {sys.executable}")
st.write(f"Python Version: {sys.version}")
st.write(f"Environment PATH: {os.environ['PATH']}")
