import pandas as pd
import altair as alt


class NumericColumn:
    """
    --------------------
    Description
    --------------------
    -> NumericColumn (class): Class that manages a column of numeric data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are numeric type (default set to empty list)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a serie (default set to None)
    -> n_missing (int): Number of missing values of a serie (default set to None)
    -> col_mean (int): Average value of a serie (default set to None)
    -> col_std (int): Standard deviation value of a serie (default set to None)
    -> col_min (int): Minimum value of a serie (default set to None)
    -> col_max (int): Maximum value of a serie (default set to None)
    -> col_median (int): Median value of a serie (default set to None)
    -> n_zeros (int): Number of times a serie has values equal to 0 (default set to None)
    -> n_negatives (int): Number of times a serie has negative values (default set to None)
    -> histogram (alt.Chart): Altair histogram displaying the count for each bin value of a serie (default set to empty)
    -> frequent (pd.DataFrame): Datframe containing the most frequest value of a serie (default set to empty)

    """
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    
    def find_num_cols(self):
        if self.file_path is not None:
            self.file_path.seek(0)
            data_df = pd.read_csv(self.file_path, low_memory=False)

        list_of_num_txt_columns = []
        for col in data_df.columns:
            if data_df[col].dtype in ['float64', 'int64']:
                list_of_num_txt_columns.append(col)
            elif data_df[col].dtype == 'object':
                temp_series = pd.to_numeric(data_df[col], errors='coerce')
                # Check if all values are numeric after conversion
                if not temp_series.isnull().all():  # Ensure not all values are NaN after conversion
                    data_df[col] = temp_series
                    list_of_num_txt_columns.append(col)

        self.df = data_df
        self.cols_list = list_of_num_txt_columns

    def set_data(self, col_name):
        self.serie = self.df[col_name]
        self.convert_serie_to_num()
        self.set_unique()
        self.set_missing()
        self.set_zeros()
        self.set_negatives()
        self.set_mean()
        self.set_std()
        self.set_min()
        self.set_max()
        self.set_median()
        self.set_histogram()
        self.set_frequent()

    def convert_serie_to_num(self):
        self.serie = pd.to_numeric(self.serie, errors='coerce')

    def is_serie_none(self):
        return self.serie is None or self.serie.empty

    def set_unique(self):
        if not self.is_serie_none():
            self.n_unique = self.serie.nunique()

    def set_missing(self):
        if not self.is_serie_none():
            self.n_missing = self.serie.isnull().sum()

    def set_zeros(self):
        if not self.is_serie_none():
            self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        if not self.is_serie_none():
            self.n_negatives = (self.serie < 0).sum()

    def set_mean(self):
        if not self.is_serie_none():
            self.col_mean = self.serie.mean()

    def set_std(self):
        if not self.is_serie_none():
            self.col_std = self.serie.std()

    def set_min(self):
        if not self.is_serie_none():
            self.col_min = self.serie.min()

    def set_max(self):
        if not self.is_serie_none():
            self.col_max = self.serie.max()

    def set_median(self):
        if not self.is_serie_none():
            self.col_median = self.serie.median()

    def set_histogram(self):
        if not self.is_serie_none():
            # Convert series to DataFrame for Altair
            data_for_histogram = self.serie.reset_index(drop=True).to_frame('value')

            # Create an Altair histogram chart
            self.histogram = alt.Chart(data_for_histogram).mark_bar().encode(
                alt.X("value:Q", bin=True),
                y='count()',
            ).interactive()  # making it interactive

    def set_frequent(self, end=20):
        if not self.is_serie_none():
            value_counts = self.serie.value_counts().head(end).reset_index()
            value_counts.columns = ['value', 'occurrence']
            value_counts['percentage'] = (value_counts['occurrence'] / len(self.serie)) * 100
            
            # Check if the value_counts DataFrame is empty before styling
            self.frequent_empty = value_counts.empty
            
            # Using pandas' Styler to format the percentage column
            self.frequent = value_counts.style.format({
                'percentage': '{:,.2f}%'
            })

    def get_summary(self):
        data = {
            'Description': ['Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Rows with 0', 'Number of Rows with Negative Values',
                            'Average value', 'Standard Deviation Value', 'Minimum Value', 'Maximum Value', 'Median Value'],
            'Value': [self.n_unique, self.n_missing, self.n_zeros, self.n_negatives, "{:.2f}".format(self.col_mean), 
                            "{:.2f}".format(self.col_std), self.col_min, self.col_max, "{:.2f}".format(self.col_median)]
        }
        return pd.DataFrame(data)