"""
Date: 17/8/2025
Description: Streamlit app to interpret MongoDB and classify
"""
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from src import *
import pandas as pd

st.title("Leads")

client = Database()
database = client.getDb()
st.set_page_config(layout="wide")   # make the page use the full width

# Wrap text and render table
def render(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapText=True,       # Enable text wrapping
        autoHeight=True,     # Adjust row height automatically
        resizable=True
    )
    gridOptions = gb.build()
    return gridOptions


# Columns
col1, col2 = st.columns(2)
with col1:
    st.header("Qualified")
    qual: pd.DataFrame = database[database["qualified"] == True]
    gb1 = GridOptionsBuilder.from_dataframe(qual)
    gb1.configure_default_column(
        wrapText=True,       # Enable text wrapping
        autoHeight=True,     # Adjust row height automatically
        resizable=True,
        flex=1
    )
    gridOptions1 = gb1.build()
    AgGrid(qual, gridOptions=gridOptions1, enable_enterprise_modules=False, fit_columns_on_grid_load=True, key="table1")

with col2:
    st.header("Not qualified")
    nqual: pd.DataFrame = database[database["qualified"] == False]
    gb2 = GridOptionsBuilder.from_dataframe(qual)
    gb2.configure_default_column(
        wrapText=True,       # Enable text wrapping
        autoHeight=True,     # Adjust row height automatically
        resizable=True,
        flex=1
    )
    gridOptions2 = gb2.build()
    AgGrid(nqual, gridOptions=gridOptions2, enable_enterprise_modules=False, fit_columns_on_grid_load=True, key="table2")


