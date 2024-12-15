"""
Streamlit app to wrap around backend
"""
import streamlit as st
import pandas as pd
import csv
import os
from src.google import Google
from src.dataUpdate import DataUpdate
st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 1])

def load_data():
    return pd.read_csv("data.csv")


# Define your processing function here
def process_input(user_input, num_results):
    # Example processing: just return the input for demonstration
    tmp = Google(user_input).search(num_results)
    DataUpdate("data.csv", tmp.Links(), user_input).run()
    return user_input

df = load_data()

if 'df' not in st.session_state:
    st.session_state.df = df

with col1:
    st.title('Morts&More')
    col3, col4 = st.columns([7, 3])
    with col3:
        user_input = st.text_input("Search for Profiles:")
    with col4:
        num_results = st.number_input("Number of Results:", min_value=1, max_value=100, value=10)

    if st.button('Submit'):
        processed_data = process_input(user_input, num_results)
        st.success(f'Input "{processed_data}" has been saved!')
        df = pd.read_csv('data.csv')

# Display the contents of the CSV file
if os.path.isfile('data.csv'):
    with col2:
        st.write("Current Database:")
        
        edited_df = st.data_editor(
            df,
            column_config={
                "url": st.column_config.LinkColumn("url"),
                "Select": st.column_config.CheckboxColumn("Select"),   
                },
            num_rows="dynamic",
            key="my_data_editor",
        )
        
        
        
        
st.session_state.edited_df = edited_df
if not st.session_state.df.equals(edited_df):  # Check if there are changes
    edited_df.to_csv("data.csv", index=False)  # Save updated DataFrame to CSV
    
    