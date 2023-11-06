import pandas as pd
import altair as alt
from datetime import datetime

class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column from a dataframe of datetime data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are text type (default set to empty list)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a serie (optional)
    -> n_missing (int): Number of missing values of a serie (optional)
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> n_weekend (int): Number of times a serie has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a serie has dates not falling during weekend (optional)
    -> n_future (int): Number of times a serie has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a serie has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a serie has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Dataframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
        self.find_date_cols()


    def find_date_cols(self):
        """
        --------------------
        Description
        --------------------
        -> find_date_cols (method): Class method that will load the uploaded CSV file as Pandas DataFrame and store it as attribute (self.df) if it hasn't been provided before.
        Then it will find all columns of datetime data type. If it can't find any datetime then it will look for all columns of text time. Then it will store the results in the relevant attribute (self.cols_list).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if self.file_path is not None:
            self.file_path.seek(0)
            data_df = pd.read_csv(self.file_path, low_memory=False)

        list_of_dt_txt_columns = []
        for col in data_df.columns:
            if data_df[col].dtype == 'object':
                try:
                    data_df[col] = pd.to_datetime(data_df[col], format='mixed')
                    list_of_dt_txt_columns.append(col)
                except ValueError as error:
                    pass
        
        if len(list_of_dt_txt_columns) == 0:
            for col in data_df.columns:
                if data_df[col].dtype == 'object':
                    print(col)
                    list_of_dt_txt_columns.append(col)

        self.df = data_df
        self.cols_list = list_of_dt_txt_columns



    def set_data(self, col_name):
        """
        --------------------
        Description
        --------------------
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that sets the self.serie attribute with the relevant column from the dataframe and then computes all requested information from self.serie to be displayed in the Date section of Streamlit app 

        --------------------
        Parameters
        --------------------
        -> col_name (str): Name of the text column to be analysed

        --------------------
        Returns
        --------------------
        -> None
        """
        self.serie = self.df[col_name]
        self.convert_serie_to_date()

        if self.is_serie_none():
            self.serie = self.df[col_name]

        self.set_unique()
        self.set_missing()
        self.set_min()
        self.set_max()
        self.set_weekend()
        self.set_weekday()
        self.set_future()
        self.set_empty_1900()
        self.set_empty_1970()
        self.set_barchart()
        self.set_frequent()


    def is_of_valid_datetime(self):
        try:
            res = pd.to_datetime(self.serie)
            return True
        except ValueError:
            return False


    def convert_serie_to_date(self):
        """
        --------------------
        Description
        --------------------
        -> convert_serie_to_date (method): Class method that convert a Pandas Series to datetime data type and store the results in the relevant attribute (self.serie).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            self.serie = pd.to_datetime(self.serie)
        except ValueError:
            self.serie = None

        

    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none 

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (bool): Flag stating if the serie is empty or not

        """
        if self.serie is None or self.serie.empty:
            return True
        else:
            return False
        

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie and store the results in the relevant attribute(self.n_unique).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_unique = self.serie.nunique()
        

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie and store the results in the relevant attribute(self.n_missing).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        self.n_missing = self.serie.isnull().sum()
        

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_min).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.col_min = 'N/A'
            else:
                self.col_min = self.serie.min()
        except:
            self.col_min = 'N/A'

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_max).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.col_max = 'N/A'
            else:
                self.col_max = self.serie.max()
        except:
            self.col_max = 'N/A'

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a serie has dates falling during weekend and store the results in the relevant attribute(self.n_weekend).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.n_weekend = 'N/A'
            else:
                df = pd.DataFrame({'date_column': self.serie})
                df['day_of_week'] = df['date_column'].dt.dayofweek
                self.n_weekend  = len(df[df['day_of_week'].isin([5, 6])])
        except:
            self.n_weekend = 'N/A'

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend and store the results in the relevant attribute(self.n_weekday).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.n_weekday = 'N/A'
            else:
                df = pd.DataFrame({'date_column': self.serie})
                df['day_of_week'] = df['date_column'].dt.dayofweek
                self.n_weekday = len(df[df['day_of_week'].isin([0, 1, 2, 3, 4])])
        except:
            self.n_weekday = 'N/A'

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a serie has dates falling in the future and store the results in the relevant attribute(self.n_future).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.n_future = 'N/A'
            else:
                df = pd.DataFrame({'date_column': self.serie})
                self.n_future = len(df[df['date_column'] > datetime.now()])
        except:
             self.n_future = 'N/A'
        
    
    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' and store the results in the relevant attribute(self.n_empty_1900).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.n_empty_1900 = 'N/A'
            else:
                df = pd.DataFrame({'date_column': self.serie})
                self.n_empty_1900 = len(df[df['date_column'] == pd.to_datetime('1900-01-01')])
        except:
            self.n_empty_1900 = 'N/A'

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a serie has only digit characters and store the results in the relevant attribute(self.n_empty_1970).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        try:
            if self.is_serie_none():
                self.n_empty_1970 = 'N/A'
            else:
                df = pd.DataFrame({'date_column': self.serie})
                self.n_empty_1970 = len(df[df['date_column'] == pd.to_datetime('1970-01-01')])
        except:
            self.n_empty_1970 = 'N/A'

    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie and store the results in the relevant attribute(self.barchart).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        axis = "date"
        if self.is_of_valid_datetime() == False:
            axis = "value"

        df = pd.DataFrame({axis: self.serie})
        df2 = df.groupby(axis).size().reset_index(name='number_of_records')
        self.barchart = alt.Chart(df2).mark_bar().encode(x=axis, y="number_of_records")

        
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie and store the results in the relevant attribute(self.frequent).

        --------------------
        Parameters
        --------------------
        -> end (int):
            Parameter indicating the maximum number of values to be displayed

        --------------------
        Returns
        --------------------
        -> None

        """
        df = pd.DataFrame({'value': self.serie})
        df2 = df.groupby('value').size().reset_index(name='occurrance')
        total_count = df2['occurrance'].sum()
        df2['percentage'] = df2['occurrance'] / total_count
        df2 = df2.sort_values(by='percentage', ascending=False)
        self.frequent = df2.head(end)
        

    def get_summary(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (pd.DataFrame): Formatted dataframe to be displayed on the Streamlit app

        """
        summary_data = {
            "Description": ["Number of Unique Values",
                            "Number of Rows with Missing Values",
                            "Number of Weekend Dates",
                            "Number of Weekday Dates",
                            "Number of Dates in the Future",
                            "Number of Rows with 1900-01-01",
                            "Number of Rows with 1970-01-01",
                            "Minimum Value",
                            "Maximum Value"
                            ],

            "Value": [self.n_unique,
                      self.n_missing,
                      self.n_weekend,
                      self.n_weekday,
                      self.n_future,
                      self.n_empty_1900,
                      self.n_empty_1970,
                      self.col_min,
                      self.col_max
                      ]
        }
        return pd.DataFrame(summary_data)
