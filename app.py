"""
Date: 17/8/2025
Description: Streamlit app to interpret MongoDB and classify
"""
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from src import *
import pandas as pd

if "client" not in st.session_state:
    client = Database()

# st.write(df)
if "df" not in st.session_state:
    st.session_state.df = client.getDb()

st.title("Leads")
st.set_page_config(layout="wide")   # make the page use the full width
st.write("Select any incorrectly classified columns")

if st.button("Reload Data"):
    st.session_state.df = client.getDb()
    # st.session_state.pop("selected_qual", None)
    # st.session_state.pop("selected_unqual", None)

# Columns
col1, col2 = st.columns(2)
# st.write(st.session_state.df)

def display_table(df, key: str):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        wrapText=True,
        autoHeight=True,
        resizable=True,
        flex=1
    )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        key=key,
        update_mode=GridUpdateMode.SELECTION_CHANGED,  # reacts to cell edits
        allow_unsafe_jscode=True,
        reload_data=False
    )

    updated_df = pd.DataFrame(grid_response["data"])
    selected_rows = pd.DataFrame(grid_response["selected_rows"])

    return updated_df, selected_rows

with col1:
    st.header("Good leads")
    updated_qual, selected_qual = display_table(
        st.session_state.df[st.session_state.df["actual"] == True],
        "qualified"
    )

with col2:
    st.header("Bad leads")
    updated_unqual, selected_unqual = display_table(
        st.session_state.df[st.session_state.df["actual"] == False],
        "unqualified"
    )

# Merge edits back into session_state
st.session_state.df.update(updated_qual)
st.session_state.df.update(updated_unqual)

# Show selected rows on button press
if st.button("Update actual classification"):
    selected_all = pd.concat([selected_qual, selected_unqual], ignore_index=True)

    # if st.button("Change actual classification"):
        # Change the actual classification here
    for item in selected_all.to_dict(orient="records"):
        count = client.update(
            {"link": item["link"]}, 
            {
                "name": item["name"],
                "headline": item["headline"],
                "location": item["location"],
                "link": item["link"],
                "model": item["model"],
                "actual": not item["actual"]
            })
    st.session_state.df = client.getDb()
    st.write(st.session_state.df)
