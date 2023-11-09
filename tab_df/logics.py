import pandas as pd

class Dataset:
    """
    --------------------
    Description
    --------------------
    -> Dataset (class): Class that manages a dataset loaded

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (mandatory)
    -> df (pd.Dataframe): Pandas dataframe (default set to None)
    -> cols_list (list): List of columns names of dataset (default set to empty list)
    -> n_rows (int): Number of rows of dataset (default set to 0)
    -> n_cols (int): Number of columns of dataset (default set to 0)
    -> n_duplicates (int): Number of duplicated rows of dataset (default set to 0)
    -> n_missing (int): Number of missing values of dataset (default set to 0)
    -> n_num_cols (int): Number of columns that are numeric type (default set to 0)
    -> n_text_cols (int): Number of columns that are text type (default set to 0)
    -> table (pd.Series): Pandas DataFrame containing the list of columns, their data types and memory usage from dataframe (default set to None)
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None
        # Automatically populate the attributes by calling set_data
        self.set_data()

    def set_data(self):
        self.set_df()
        self.set_columns()
        self.set_dimensions()
        self.set_duplicates()
        self.set_missing()
        self.set_numeric()
        self.set_text()
        self.set_table()

    def set_df(self):
        # If the DataFrame is already set or not empty, we don't need to read the file again
        if not self.df is None and not self.df.empty:
            return

        # Try to read the uploaded file directly using pandas
        try:
            # Check if file_path is an UploadedFile object
            if hasattr(self.file_path, "read"):
                # Read the file from the buffer
                self.df = pd.read_csv(self.file_path)
            else:
                # It's a file path; proceed with the usual method
                self.df = pd.read_csv(self.file_path)
        except pd.errors.EmptyDataError:
            # If the CSV is empty, set the DataFrame to None or an empty DataFrame
            self.df = pd.DataFrame()

        # Update the rest of the data
        self.set_columns()
        self.set_dimensions()
        self.set_duplicates()
        self.set_missing()
        self.set_numeric()
        self.set_text()
        self.set_table()

    def is_df_none(self):
        return self.df is None or self.df.empty

    def set_columns(self):
        if not self.is_df_none():
            self.cols_list = self.df.columns.tolist()

    def set_dimensions(self):
        if not self.is_df_none():
            self.n_rows, self.n_cols = self.df.shape

    def set_duplicates(self):
        if not self.is_df_none():
            self.n_duplicates = self.df.duplicated().sum()

    def set_missing(self):
        if not self.is_df_none():
            self.n_missing = self.df.isnull().sum().sum()

    def set_numeric(self):
        if not self.is_df_none():
            self.n_num_cols = self.df.select_dtypes(include=['float64', 'int64']).shape[1]

    def set_text(self):
        if not self.is_df_none():
            self.n_text_cols = self.df.select_dtypes(include=['object']).shape[1]

    def get_head(self, n=5):
        if not self.is_df_none():
            return self.df.head(n)
        return None

    def get_tail(self, n=5):
        if not self.is_df_none():
            return self.df.tail(n)
        return None

    def get_sample(self, n=5):
        if not self.is_df_none():
            return self.df.sample(n)
        return None

    def set_table(self):
        if not self.is_df_none():
            self.table = pd.DataFrame({
                "Column Name": self.df.columns,
                "Data Type": [str(dtype) for dtype in self.df.dtypes],
                "Memory Usage (Bytes)": self.df.memory_usage(deep=True).values[1:]  # Excluding the memory usage of the index
            })

    def get_summary(self):
        summary_data = {
            "Description": ["Number of Rows", "Number of Columns", "Duplicated Rows", "Missing Values", "Numeric Columns", "Text Columns"],
            "Value": [self.n_rows, self.n_cols, self.n_duplicates, self.n_missing, self.n_num_cols, self.n_text_cols]
        }
        return pd.DataFrame(summary_data)