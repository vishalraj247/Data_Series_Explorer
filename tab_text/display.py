import streamlit as st
import pandas as pd

from logics import TextColumn
def display_tab_text_content(file_path=None, df=None):
    if file_path is not None:
        df = pd.read_csv(file_path)
        text_column = TextColumn(df=df)
        text_column.find_text_cols()

        selected_column = st.selectbox('Which text column do you want to explore', text_column.cols_list)

        if selected_column:
            text_column.set_data(selected_column)

            with st.expander('Text Column'):
                st.table(text_column.get_summary())

                st.subheader('Bar Chart')
                st.altair_chart(text_column.barchart, use_container_width=True)

                st.subheader('Most Frequent Values')
                st.table(text_column.frequent)

st.title('Text Column Analysis')

uploaded_file =st.file_uploader('Choose a csv file', type=['csv'])
if uploaded_file is not None:
    display_tab_text_content(file_path=uploaded_file)
    """
    --------------------
    Description
    --------------------
    -> display_tab_text_content (function): Function that will instantiate tab_text.logics.TextColumn class, save it into Streamlit session state and call its tab_text.logics.TextColumn.find_text_cols() method in order to find all text columns.
    Then it will display a Streamlit select box with the list of text columns found.
    Once the user select a text column from the select box, it will call the tab_text.logics.TextColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_text.logics.TextColumn.get_summary() as a Streamlit Table
    - the graph from tab_text.logics.TextColumn.histogram using Streamlit.altair_chart()
    - the results of tab_text.logics.TextColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """
    
