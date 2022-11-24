import pandas as pd

df = pd.read_csv('../data/raw/data.csv',encoding="ISO-8859-1")

# Processing the outliers for Age
def find_outliers_IQR(df):

    """This function calculates the outliers of a df"""

    q1=df.quantile(0.25)

    q3=df.quantile(0.75)

    IQR=q3-q1

    outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]

    return outliers

outliers = find_outliers_IQR(df['Age'])


def drop_outliers_IQR(df):

   """This function replaces outliers with null value"""

   q1=df.quantile(0.25)

   q3=df.quantile(0.75)

   IQR=q3-q1

   not_outliers = df[~((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]

   outliers_dropped = outliers.dropna().reset_index()

   return not_outliers

# Testing out my method chain function
def load_and_process(url_or_path_to_csv_file):
    
    # Method Chain 1 - Need to create new columns first because we need to do dropna on the newly created column + (Load Data, Create new columns, and drop others)
    df1 = (
        pd.read_csv(url_or_path_to_csv_file,encoding="ISO-8859-1")
        .assign(Year=lambda x:pd.DatetimeIndex(df['Date']).year)
        .assign(Month=lambda x:pd.DatetimeIndex(df['Date']).month)
        .assign(filtered_age = lambda df_: pd.to_numeric(drop_outliers_IQR(df['Age'])))
        .drop(['Age'],axis=1)
    )
    
    # Method Chain 2 (Deal with missing data)
    df2 = (
        df1.dropna(subset = ['filtered_age'])
        .dropna(subset=['Race'])
        .dropna(subset=['City'])
        .dropna(subset=['Gender'])
    )
    
    
    # Return the latest dataframe
    return df2

# Use function with the path to data csv file
load_and_process('../data/raw/data.csv')
