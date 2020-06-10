import streamlit as st

st.write("Hello World")
###SLIDER example
x = st.slider('x')
st.write(x, 'squared is', x * x)