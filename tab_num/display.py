import streamlit as st
from tab_num.logics import NumericColumn

def display_tab_num_content(file_path=None, df=None):
    num_col_instance = NumericColumn(file_path=file_path, df=df)
    num_col_instance.find_num_cols()
    
    if not num_col_instance.cols_list:
        st.write("No numeric columns found.")
        return
    
    selected_num_col = st.selectbox("Select Numeric Column", num_col_instance.cols_list)
    
    if selected_num_col:
        num_col_instance.set_data(selected_num_col)
        with st.expander("Numeric Column", expanded=True):
            summary_df = num_col_instance.get_summary()
            if not summary_df.empty:
                st.table(summary_df)
            else:
                st.write("No data to display in the summary table.")
        with st.expander("Histogram", expanded=True):
            if num_col_instance.histogram:
                st.altair_chart(num_col_instance.histogram)
            else:
                st.write("No histogram to display.")
        with st.expander("Most Frequent Values", expanded=True):
            if not num_col_instance.frequent_empty:
                st.write(num_col_instance.frequent)
            else:
                st.write("No frequent values to display.")
