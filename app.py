import streamlit as st
import pandas as pd 
import numpy as np 
DATA_URL = (
    "./data-science/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Steamlit dashboard that can be used"
" to analyze motor vehicle collisions in NYC")