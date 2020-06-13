import streamlit as st

st.write("Hello World")
st.markdown ('## Myfirst streamlit dashboard')

###SLIDER example
x = st.slider('x')
st.write(x, 'squared is', x * x)
