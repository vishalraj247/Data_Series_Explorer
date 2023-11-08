import streamlit as st

from text_logics import TextColumn


def display_tab_text_content(file_path=None, df=None):
    text_column = TextColumn(file_path=file_path, df=df)
    text_column.find_text_cols()

    selected_text_column = st.selectbox('Which text column do you want to explore', text_column.cols_list)
    if text_cols_list is not None:
        selected_text_column = st.selectbox('Which text column do you want to explore', text_cols_list)

        if selected_text_column:
            text_column.set_data(selected_text_column)

            with st.expander('Text Column', expanded=True):
                st.table(text_column.get_summary())

            with st.expander('Bar Chart', expanded=True):
                st.altair_chart(text_column.barchart, use_container_width=True)

            with st.expander('Most Frequent Values', expanded=True):
                st.table(text_column.frequent)

    else:
        st.error('No text columns available')
