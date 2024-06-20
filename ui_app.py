import streamlit as st
import requests
from datetime import date

st.title('Travel Query App')

query = st.text_area('Query')
travel_date = st.date_input('Travel Date', value=date.today())
destination = st.text_input('Destination')
submit_button = st.button('Submit')