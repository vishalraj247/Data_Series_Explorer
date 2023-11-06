import streamlit as st
from tab_date.logics import DateColumn

def display_tab_date_content(file_path):
    """
    --------------------
    Description
    --------------------
    -> display_tab_date_content (function): Function that will instantiate tab_date.logics.DateColumn class, save it into Streamlit session state and call its tab_date.logics.DateColumn.find_date_cols() method in order to find all datetime columns.
    Then it will display a Streamlit select box with the list of datetime columns found.
    Once the user select a datetime column from the select box, it will call the tab_date.logics.DateColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_date.logics.DateColumn.get_summary() as a Streamlit Table
    - the graph from tab_date.logics.DateColumn.histogram using Streamlit.altair_chart()
    - the results of tab_date.logics.DateColumn.frequent using Streamlit.write
 
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

    dataset2 = DateColumn(file_path)
    dataset2.find_date_cols()
    
    column_selected = st.selectbox('Which datetime column do you want to explore', dataset2.cols_list)
    dataset2.set_data(column_selected)

    if dataset2.is_of_valid_datetime() == False:
        st.warning(f'WARNING: the selected column "{column_selected}" does not appear to be of datetime data type, as a result, some statistics may not be available. These statistics have been flagged as "N/A"', icon="⚠️")

    # Display datetime stats
    with st.expander("Date Column", expanded=True):
        st.table(dataset2.get_summary())

    # Display bar chart
    with st.expander("Bar Chart", expanded=True):
        st.altair_chart(dataset2.barchart, use_container_width=True)

    # Display top 20 dates
    with st.expander("Most Frequent Values", expanded=True):
        st.dataframe(dataset2.frequent)

    