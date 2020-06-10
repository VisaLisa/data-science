### Used 'Build your first app' link: https://youtu.be/VtrFjkSGgKM  
### Create an app to explore a dataset of Uber ride pickups in New York City. 
### You’ll learn about caching, drawing charts, plotting data on a map, and how to use interactive widgets.
### See https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py for the original code

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

DATE_TIME = "date/time"
DATA_URL = (
    "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

st.title("Uber Pickups in New York City")
st.markdown(
"""
This is a demo of a Streamlit app that shows the Uber pickups
geographical distribution in New York City. Use the slider
to pick a specific hour and look at how the charts change.
[See source code](https://github.com/streamlit/demo-uber-nyc-pickups/blob/master/app.py)
""")

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)  ##full dataset

### Looking at all Uber pick up at noon
hour = st.slider('hour',0,23,10)
data = data[data[DATE_TIME].dt.hour == hour]

### Geo mapping
'## Geo Data at %sh' % hour
### use 'st.map(data)' if you want plot-point map instead
### Below is map UI 
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

### Raw data
if st.checkbox('Show Raw Data'):
    '## Raw Data at %sh' % hour, data

