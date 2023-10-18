# Import packages
import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Set Python path
current_dir = os.path.dirname(__file__)
parent_dir = str(Path(current_dir).resolve().parents[0])
sys.path.append(parent_dir)

# Import custom functions
from tab_df.display import display_tab_df_content
from tab_num.display import display_tab_num_content
from tab_text.display import display_tab_text_content
from tab_date.display import display_tab_date_content

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="CSV Explorer",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Set objects in Streamlit session state
st.session_state["file_path"] = None
st.session_state["df"] = None
st.session_state["dataset"] = None
st.session_state["selected_num_col"] = None
st.session_state["num_column"] = None
st.session_state["selected_text_col"] = None
st.session_state["text_column"] = None
st.session_state["selected_date_col"] = None
st.session_state["date_column"] = None

# Display Title
st.title("CSV Explorer")

# Add Window to upload CSV file
with st.expander("ℹ️ - Streamlit application for performing data exploration on a CSV", expanded=True):
    st.session_state.file_path = st.file_uploader("Choose a CSV file")

# If a CSV file is uploaded, display the different tabs
if st.session_state.file_path is not None:
    tab_df, tab_num, tab_text, tab_date = st.tabs(["DataFrame", "Numeric Serie", "Text Serie", "Datetime Serie"])
    with tab_df:
        display_tab_df_content(file_path=st.session_state.file_path)
    with tab_num:
        display_tab_num_content(df=st.session_state.dataset.df)
    with tab_text:
        display_tab_text_content(df=st.session_state.dataset.df)
    with tab_date:
        display_tab_date_content(df=st.session_state.dataset.df)