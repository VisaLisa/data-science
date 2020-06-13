import streamlit as st
import pandas as pd 
import numpy as np
import pydeck as pdk
import plotly.express as px 
DATA_URL = (
    "../dataset/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Steamlit dashboard that can be used"
" to analyze motor vehicle collisions in NYC🗽💥🚗")

###Translating dataset from csv
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)
original_data = data

### Slider UI feature
st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

###Dropdown feature = st.selectbox; filters the hours on dataset; not map
st.header("How many collisions occur in a given time of day?")
hour = st.slider("Hour to look at", 0 , 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle collision between %i:00 and %i:00" % (hour, (hour + 1) %24))

# coords for initial_view_state
midpoint = (np.average(data['latitude']), np.average(data['longitude']))


st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        'latitude': midpoint[0],
        'longitude': midpoint[1],
        'zoom': 11,
        'pitch': 50,
    },
    layers = [
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/time', 'latitude', 'longitude']],
        get_position = ['longitude', 'latitude'],
        radius = 100,
        extruded = True, # 3d; if taken out, it will show 2d hexagons on the map
        pickable = True,
        elevation_scale = 4,
        elevation_range = [0,1000],
        ),
    ],
))
# charts and histograms
# how many collisions have happened in a 60 minute window [1 hr]
# plot ly - histogram, bar chart
# numpy - calculate the values for the histogram
st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1)%24))
# filtering the data
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]  ###[0] is entry of minutes
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})  ###Filtering data to provide minutes and crashes
fig = px.bar(chart_data, x='minute', y='crashes', hover_data = ['minute', 'crashes'], height=400) ###hover_data allows for the pointer to show the data when hovering
st.write(fig)

st.header("Top 5 dangerous streets by affected type")
select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorist'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])  ### ":5" show TOP 5 values

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])  ### ":5" show TOP 5 values of cyclists

else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])  ### ":5" show TOP 5 values

### Displaying dataset
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
