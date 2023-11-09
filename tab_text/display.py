import streamlit as st
from text_logics import TextColumn


def display_tab_text_content(file_path=None, df=None):
    text_column = TextColumn(file_path=file_path, df=df)
    text_column.find_text_cols()

    if not text_column.cols_list:
        st.error('No text columns available')
    else:
        text_cols_list = [col for col in text_column.cols_list if text_column.df[col].dtype == 'object']

        if not text_cols_list:
            st.error('No text columns available')
        else:
            selected_text_column = st.selectbox('Which text column do you want to explore', text_cols_list)

            if selected_text_column:
                text_column.set_data(selected_text_column)

                with st.expander('Text Column', expanded=True):
                    summary = text_column.get_summary()
                    if summary is not None:
                        st.table(text_column.get_summary())
                    else:
                        st.write('No summary table to display')

                with st.expander('Bar Chart', expanded=True):
                    if text_column.barchart:
                        st.altair_chart(text_column.barchart, use_container_width=True)
                    else:
                        st.write('No Bar Chart')

                with st.expander('Most Frequent Values', expanded=True):
                    frequent = text_column.frequent
                    if not frequent.empty:
                        st.table(text_column.frequent)
                    else:
                        st.write('No frequency table to display')
