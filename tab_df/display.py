import streamlit as st

from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    # Create the Dataset object and set data
    dataset = Dataset(file_path)

    # Check if the dataframe is empty and display a message if so
    if dataset.df is None or dataset.df.empty:
        st.write("No columns to display. Please upload a dataset with data.")
        return  # Exit the function if the dataframe is empty

    # If the dataframe is not empty, proceed to display the data
    with st.expander("Dataset Summary", expanded=True):
        st.table(dataset.get_summary())

    # Display the columns, data types, and memory usage
    with st.expander("Columns Information", expanded=True):
        st.table(dataset.table)

    # Data exploration section
    with st.expander("Data Exploration", expanded=True):
        row_count = st.slider("Select number of rows to display", 5, 50, value=5)  # Added default value for slider
        display_option = st.radio("Choose rows to display", ["head", "tail", "sample"])
        
        # Display the dataframe based on the user selection
        if display_option == "head":
            st.dataframe(dataset.get_head(row_count))
        elif display_option == "tail":
            st.dataframe(dataset.get_tail(row_count))
        elif display_option == "sample":
            st.dataframe(dataset.get_sample(row_count))
