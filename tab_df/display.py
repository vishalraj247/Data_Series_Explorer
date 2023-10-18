import streamlit as st
from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    # Create the Dataset object and set data
    dataset = Dataset(file_path)
    dataset.set_data()

    # Display the basic information
    with st.expander("Dataset Summary", expanded=True):
        st.table(dataset.get_summary())

    # Display the columns, data types, and memory usage
    with st.expander("Columns Information", expanded=True):
        st.table(dataset.table)

    # Data exploration section
    with st.expander("Data Exploration", expanded=True):
        row_count = st.slider("Select number of rows to display", 5, 50)
        display_option = st.radio("Choose rows to display", ["head", "tail", "sample"])
        
        if display_option == "head":
            st.dataframe(dataset.get_head(row_count))
        elif display_option == "tail":
            st.dataframe(dataset.get_tail(row_count))
        elif display_option == "sample":
            st.dataframe(dataset.get_sample(row_count))
