import streamlit as st

from tab_num.logics import NumericColumn

def display_tab_num_content(file_path=None, df=None):
    num_col_instance = NumericColumn(file_path=file_path, df=df)
    num_col_instance.find_num_cols()
    selected_num_col = st.selectbox("Select Numeric Column", num_col_instance.cols_list)
    
    if selected_num_col:
        num_col_instance.set_data(selected_num_col)
        with st.expander("Numeric Column", expanded=True):
            st.table(num_col_instance.get_summary())
        with st.expander("Histogram", expanded=True):
            st.altair_chart(num_col_instance.histogram)
        with st.expander("Most Frequent Values", expanded=True):
            st.write(num_col_instance.frequent)