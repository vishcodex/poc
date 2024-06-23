import streamlit as st
import requests
from datetime import date

# Function to display results in a prettier format
def display_results(response_data):
    if 'error' in response_data:
        st.error(response_data['error'])
    else:
        st.success("Query Successful!")
        if isinstance(response_data, dict):
            for key, value in response_data.items():
                st.write(f"**{key.capitalize()}**: {value}")
        elif isinstance(response_data, list):
            for item in response_data:
                st.write(item)

# Navigation Bar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "About Me"])

# Home Page
if selection == "Home":
    st.title("Travel Query App")
    st.markdown("""
        Welcome to the Travel Query App! Here you can find information on hotels, places, and attractions.
        Simply fill out the form below and get started!
    """)

    # Input fields for the user query
    query = st.text_input("Query", "Where to travel?")
    travel_date = st.date_input("Travel Date", value=date.today())
    destination = st.text_input("Destination", "India")
    query_type = st.selectbox("Query Type", ["general", "hotels", "places", "attractions"])
    submit_button = st.button("Submit")

    # Handling form submission
    if submit_button:
        with st.spinner('Fetching data...'):
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
                st.error("Error fetching data. Please try again.")

# About Me Page
elif selection == "About Me":
    st.title("About Me")
    st.markdown("""
        ## About the Developer
        Hi, I'm [Your Name], the developer of this Travel Query App. I am passionate about travel and technology. 
        This app is designed to help users find information about hotels, places, and attractions for their trips.

        ### Contact Information
        - **Email**: [your.email@example.com](mailto:your.email@example.com)
        - **GitHub**: [YourGitHubProfile](https://github.com/YourGitHubProfile)
        - **LinkedIn**: [YourLinkedInProfile](https://linkedin.com/in/YourLinkedInProfile)
    """)

# Custom CSS to improve UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        color: #333333;
    }
    .sidebar .sidebar-content {
        background-color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)
