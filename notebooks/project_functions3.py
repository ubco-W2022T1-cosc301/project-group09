import pandas as pd

df = pd.read_csv('../data/raw/data.csv',encoding="ISO-8859-1")


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



def load_and_process(url_or_path_to_csv_file):

    # Method Chain 1 

    df1 = (
         pd.read_csv('../data/raw/data.csv' ,encoding="ISO-8859-1")
         .assign(filtered_age = lambda df_: pd.to_numeric(drop_outliers_IQR(df['Age'])))
         .assign(Year=lambda x:pd.DatetimeIndex(df['Date']).year)
         .assign(Month=lambda x:pd.DatetimeIndex(df['Date']).month)
      )

    # Method Chain 2 

    df2 = (
          df1
          .dropna(subset = ['filtered_age'])
          .drop(['Age'], axis=1)
          .dropna(subset=['Race'])
          .dropna(subset=['City'])
          .dropna(subset=['Gender'])
    )


    # Make sure to return the latest dataframe

    return df2 



load_and_process('../data/raw/data.csv')