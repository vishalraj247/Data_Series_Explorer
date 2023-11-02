import streamlit as st

from logics import TextColumn
import pandas as pd

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
