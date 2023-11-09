import pandas as pd
import altair as alt


class TextColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_text_cols(self):
        if self.file_path is not None:
            self.file_path.seek(0)
            data = pd.read_csv(self.file_path)

            list_of_text_columns = []
            for col in data.columns:
                try:
                    if data[col].dtype == 'object':
                        list_of_text_columns.append(col)
                except Exception as e:
                    print(f"Error processing column {col}: {str(e)}")

            if list_of_text_columns:
                self.df = data
                self.cols_list = list_of_text_columns
            else:
                print('No Text Columns found')
        else:
            print('No file path provided')

    def set_data(self, col_name):
        if col_name in self.cols_list:
            self.serie = self.df[col_name]
            if isinstance(self.serie, pd.Series):
                self.convert_serie_to_text()
                self.set_unique()
                self.set_missing()
                self.set_empty()
                self.set_mode()
                self.set_whitespace()
                self.set_lowercase()
                self.set_uppercase()
                self.set_alphabet()
                self.set_digit()
                self.set_barchart()
                self.set_frequent()
            else:
                self.serie = None

    def convert_serie_to_text(self):
        self.serie = self.serie.astype(str)

    def is_serie_none(self):
        return self.serie is None

    def set_unique(self):
        self.n_unique = self.serie.nunique()

    def set_missing(self):
        if not self.is_serie_none():
            n_missing_nan = self.serie.isna().sum()
            n_missing_nan_str = self.serie.apply(lambda x: x == 'nan').sum()
            self.n_missing = n_missing_nan + n_missing_nan_str

    def set_empty(self):
        if self.serie is not None:
            self.n_empty = len(self.serie[self.serie.str.strip() == ''])
        else:
            self.n_empty = 0

    def set_mode(self):
        self.n_mode = self.serie.mode().iloc[0]

    def set_whitespace(self):
        self.n_space = len(self.serie[self.serie.str.isspace()])

    def set_lowercase(self):
        if not self.is_serie_none():
            self.n_lower = self.serie[self.serie.str.islower()].count()

    def set_uppercase(self):
        if not self.is_serie_none():
            self.n_upper = self.serie[self.serie.str.isupper()].count()

    def set_alphabet(self):
        self.n_alpha = len(self.serie[self.serie.str.isalpha()])

    def set_digit(self):
        self.n_digit = len(self.serie[self.serie.str.isdigit()])

    def set_barchart(self):
        value_counts = self.serie.value_counts().reset_index()
        value_counts.columns = ['value', 'occurrence']
        zoom = alt.selection_interval(bind='scales', encodings=['x'])
        self.barchart = alt.Chart(value_counts).mark_bar().encode(
            y='occurrence:Q',
            x=alt.Y('value:N', sort='-x')
        ).properties(
            width=600  # Adjust the width as needed
        ).add_selection(zoom).transform_filter(zoom)

    def set_frequent(self, end=20):
        self.serie.dropna()
        value_counts = self.serie.value_counts().reset_index()
        value_counts.columns = ['value', 'occurrence']
        total = len(self.serie)
        value_counts['percentage'] = (value_counts['occurrence'] / total) * 100
        self.frequent = value_counts.head(end)

    def get_summary(self):
        summary_df = pd.DataFrame({
            'Description': ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Empty Rows',
                            'Mode Value', 'Number of Rows with Only Whitespace', 'Number of Rows with only Lowercases',
                            'Number of Rows with Only Uppercases', 'Number of Rows with Only Alphabet',
                            'Number of Rows with Only Digit'],
            'Value': [self.n_unique, self.n_missing, self.n_empty, self.n_mode, self.n_space, self.n_lower,
                      self.n_upper, self.n_alpha, self.n_digit]
        })
        return summary_df
