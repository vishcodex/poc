import streamlit as st
import requests
from datetime import date

st.title('Travel Query App')

query = st.text_input("Query")
travel_date = st.date_input("Travel Date", value=date.today())
destination = st.text_input("Destination")
query_type = st.selectbox("Query Type", ["general", "hotels", "places", "attractions"])
submit_button = st.button("Submit")

if submit_button:
    response = requests.post(
        "http://127.0.0.1:8000/process_query/",
        json={
            "query": query,
            "travel_date": travel_date.isoformat(),
            "destination": destination,
            "query_type": query_type
        }
    )
    if response.status_code == 200:
        st.write(response.json()["response"])
    else:
        st.write("Error:", response.status_code)
