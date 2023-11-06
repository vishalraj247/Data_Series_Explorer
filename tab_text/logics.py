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

        self.df = data
        self.cols_list = list_of_text_columns

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
        self.n_missing = self.serie.isnull().sum()

    def set_empty(self):
        self.n_empty = len(self.serie[self.serie == ''])

    def set_mode(self):
        self.n_mode = self.serie.mode().iloc[0]

    def set_whitespace(self):
        self.n_space = len(self.serie[self.serie.str.isspace()])

    def set_lowercase(self):
        self.n_lower = len(self.serie[self.serie.str.islower()])

    def set_uppercase(self):
        self.n_upper = len(self.serie[self.serie.str.isupper()])

    def set_alphabet(self):
        self.n_alpha = len(self.serie[self.serie.str.isalpha()])

    def set_digit(self):
        self.n_digit = len(self.serie[self.serie.str.isdigit()])

    def set_barchart(self):
        value_counts = self.serie.value_counts().reset_index()
        value_counts.columns = ['value', 'occurrence']
        self.barchart = alt.Chart(value_counts).mark_bar().encode(
            y='occurrence:Q',
            x=alt.Y('value:N', sort='-x')
        )

    def set_frequent(self, end=20):
        value_counts = self.serie.value_counts().reset_index()
        value_counts.columns = ['value', 'occurrence']
        total = len(self.serie)
        value_counts['percentage'] = (value_counts['occurrence'] / total) * 100
        self.frequent = value_counts.head(end)

    def get_summary(self):
        summary_df = pd.DataFrame({
            'Description': ['Number of Unique Values', 'Number of Missing Values', 'Number of Empty Strings',
                            'Mode Value', 'Number of Whitespace Strings', 'Number of Lowercase Strings',
                            'Number of Uppercase Strings', 'Number of Alphabetic Strings', 'Number of Digit Strings'],
            'Value': [self.n_unique, self.n_missing, self.n_empty, self.n_mode, self.n_space, self.n_lower,
                      self.n_upper, self.n_alpha, self.n_digit]
        })
        return summary_df
