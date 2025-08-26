import streamlit as st
import pandas as pd
from src import *

st.set_page_config(layout="wide", page_title="Customer Relationship Manager")

if "client" not in st.session_state:

    st.session_state.client = Database()
    st.session_state.df = st.session_state.client.getDb()
# db = df["name", "location", "headline", "link"]

# st.write(st.session_state.df)

tab1, tab2, tab3 = st.tabs(["Good leads", "Bad leads", "Unclassified"])

def render_table(df, bool, key):
    return st.data_editor(
        df[df["actual"] == bool].reset_index(drop=True),
        key = key,
        column_config={
            "headline": st.column_config.TextColumn("Headline", width="small", disabled=True),  # "small" | "medium" | "large"
            "link": st.column_config.LinkColumn("Profile", disabled=True, width="small"),
            "name": st.column_config.TextColumn("Name", width="auto", disabled=True),
            "model": st.column_config.CheckboxColumn("Model Prediction", disabled=True),
            "actual": st.column_config.CheckboxColumn("Real Classification")
            },
        hide_index=True,
        use_container_width=True
        )
with tab1:
    update = render_table(st.session_state.df, key="table1", bool=True)
    if st.button("Commit to database"):
        new = update.to_dict(orient="records")
        # st.write(new)
        for item in new:
            st.session_state.client.update({"link": item["link"]}, item)
        del st.session_state["client"]
        st.rerun()

with tab2:
    update = render_table(st.session_state.df, key="table2", bool=False)
    if st.button("Commit to a database"):
        new = update.to_dict(orient="records")
        for item in new:
            st.session_state.client.update({"link": item["link"]}, item)
        del st.session_state["client"]
        st.rerun()


with tab3:
    db = st.session_state.df[st.session_state.df["actual"].isna()].reset_index(drop=True)
    st.data_editor(
        db,
        key = "unclassified",
        column_config={
            "headline": st.column_config.TextColumn("Headline", width="small", disabled=True),  # "small" | "medium" | "large"
            "link": st.column_config.LinkColumn("Profile", disabled=True, width="small"),
            "name": st.column_config.TextColumn("Name", width="auto", disabled=True)
            },
        hide_index=True,
        use_container_width=True
        )
    
    if st.button("Run Classification"):
        tmp_df = st.session_state.client.getDb(
            ["name", "headline", "location", "link", "model", "actual", "full"]
        ).copy()
        # mask of rows that need classification
        mask = tmp_df["actual"].isna()
        dataf = tmp_df[mask]  # optional, just for convenience

        series = dataf["full"]

        model = Model()
        classes = model.run(series)
        # st.write(classes)
        # write results back into the original df
        tmp_df.loc[mask, "actual"] = classes.values
        tmp_df.loc[mask, "model"] = classes.values

        # st.write(st.session_state.df)
        classified = tmp_df.loc[mask].to_dict(orient="records")
        # st.write(classified)
        # st.write(dataf["full"])
        for item in classified:
            st.session_state.client.update({"link": item["link"]}, item)
        # st.write(classified)
        del st.session_state["client"]
        st.rerun()
