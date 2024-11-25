import streamlit as st
import pandas as pd
import subprocess
import sys

# Function to install a library dynamically
def install_library(library_name):
    try:
        __import__(library_name)
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library_name])
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to install {library_name}. Please install it manually.")
            raise e

# Install required libraries dynamically
try:
    install_library("seaborn")
    install_library("matplotlib")
except Exception as e:
    st.error("An error occurred during library installation.")
    st.error(str(e))

# Import libraries after ensuring they are installed
import seaborn as sns
import matplotlib.pyplot as plt
