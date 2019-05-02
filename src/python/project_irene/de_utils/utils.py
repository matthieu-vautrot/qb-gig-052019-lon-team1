import re
import pandas as pd
#from pyxlsb import open_workbook
#from pyspark.sql import SparkSession, functions as F


def clean_column_name(column_name):
    """
    Refactor pandas column names including lower casing,
    and replacement of non-alpha characters with underscores or words.

    Args:
        column_name(str): a 'dirty' column name
    Returns:
        column_name(str): a 'clean' column name
    """
    column_new = column_name.lower()
    column_new = re.sub('[ :_\-]+', '_', column_new)
    column_new = re.sub('#', 'number', column_new)
    column_new = re.sub('%', 'percent', column_new)
    column_new = re.sub('[&+]+', 'and', column_new)
    column_new = re.sub('[|,/;]+', 'or', column_new)
    column_new = column_new.replace("?", "")
    column_new = column_new.replace("(", "")
    column_new = column_new.replace(")", "")
    column_new = column_new.replace("\r", "")
    column_new = re.sub('>=', 'greater_than_or_equal_to_', column_new)
    column_new = re.sub('<=', 'less_than_or_equal_to_', column_new)

    return column_new


def clean_pandas_column_names(pandas_df):
    """
    Refactor pandas column names including lower casing,
    and replacement of non-alpha characters with underscores or words.

    Args:
        pandas_df(pandas.DataFrame): a dataframe
    Returns:
        pandas_df(pandas.DataFrame): dataframe with column names in lowercase and non-alpha characters substituted
    """

    column_dict = {}
    for i, column in enumerate(pandas_df):
        column_dict[column] = clean_column_name(column)

    return pandas_df.rename(columns=column_dict)


def clean_spark_column_names(spark_df):
    """
    Refactor spark column names including lower casing,
    and replacement of non-alpha characters with underscores or words.

    Args:
        spark_df(pyspark.sql.dataframe.DataFrame): a dataframe
    Returns:
        spark_df(pyspark.sql.dataframe.DataFrame): dataframe with column names in lowercase and non-alpha characters substituted
    """

    return spark_df.toDF(*[clean_column_name(column) for column in spark_df.columns])


def convert_pandas_object_to_string_columns(pandas_df):
    """
    Refactor pandas dataframe and convert any 'object data type' into string
    data type

    In pandas a single column can have different data types for each line,
    and if you try to convert it into spark data frame it fails, because spark
    requires one data type.


    Args:
        pandas_df(pandas.DataFrame): a dataframe
    Returns:
        pandas_df(pandas.DataFrame): dataframe with mixed-typed columns as string
    """

    columns_to_fix = [col for col, type in pandas_df.dtypes.to_dict().items() if
                      str(type) == 'object']

    pandas_df[columns_to_fix] = pandas_df[columns_to_fix].astype(str)

    return pandas_df


def convert_pandas_to_spark(pandas_df):
    """
    Convert pandas Dataframe to Spark Dataframe

    Converting pandas dataframe to Spark dataframe, by converting all the objects of pandas
    dataframe to string also cleans the column names.


    Args:
        pandas_df(pandas.DataFrame): a dataframe
    Returns:
        spark_df(pyspark.sql.dataframe.DataFrame): spark dataframe
    """

    df_new = clean_pandas_column_names(pandas_df)
    df_str = convert_pandas_object_to_string_columns(df_new)
    spark = SparkSession.builder.getOrCreate()
    df_spark = spark.createDataFrame(df_str)
    return df_spark.coalesce(10)


def retype_df(pdf):
    """
    Modify column type contextually based on column name.

    Args:
        pdf(pandas.DataFrame): a dataframe
    Returns:
        pdf(pandas.DataFrame): dataframe with column retyped for column names containing matching strings in column name
    """

    date_columns = []
    string_columns = []
    float_columns = []
    int_columns = []

    string_list = ['name', 'address', 'city', 'state', 'suffix', 'prefix', 'email']
    date_list = ['date']
    float_list = ['cost', 'usd', 'rate', 'percent']
    int_list = ['number']

    string_re = re.compile('|'.join(string_list))
    date_re = re.compile('|'.join(date_list))
    float_re = re.compile('|'.join(float_list))
    int_re = re.compile('|'.join(int_list))

    pdf_dtypes = pdf.dtypes
    for i, column in enumerate(pdf):
        column_type = pdf_dtypes.loc[column].name
        if (column_type == 'object'):

            if (date_re.search(column)):
                # this is a date
                date_columns.append(column)
            elif (int_re.search(column)):
                # cast int
                int_columns.append(column)
            elif (float_re.search(column)):
                # cast float
                float_columns.append(column)
            elif (string_re.search(column)):
                # cast string
                string_columns.append(column)
            else:
                # to cast to str
                string_columns.append(column)

    pdf[string_columns] = pdf[string_columns].astype(str)
    pdf[float_columns] = pdf[float_columns].astype(float)
    pdf[int_columns] = pdf[int_columns].astype(int)

    return pdf


def xlsb_sheet_to_pandas(sheet):
    """
    Convert a pyxlsb sheet to a pandas dataframe.
    Rows that have no value in the first column are assumed part of an empty row and the row excluded.

    Args:
        sheet(pyxlsb.Worksheet): a pyxlsb worksheet
    Returns:
        pdf(pandas.DataFrame): pandas dataframe representation of the pyxlsb worksheet
    """

    rows = []

    # using sparse=True to skip blank rows
    for row in sheet.rows(sparse=True):
        if (len((''.join(['' if c.v is None else c.v for c in row])).strip()) > 0):
            rows.append(['None' if item.v is None else item.v for item in row])

    pdf = pd.DataFrame(rows[1:], columns=rows[0])

    return pdf


def trim_all_columns(df):
    """
    Trim values of all columns

    Args:
        df(pyspark.sql.dataframe.DataFrame): input dataframe
    Returns:
        df(pyspark.sql.dataframe.DataFrame): dataframe with values trimmed of whitespaces
    """

    trim_columns = [F.trim(F.col(column)).alias(column) if type == 'string' else column for column, type in iter(df.dtypes)]
    return df.select(trim_columns)


def prefix_columns(df, prefix, exclude_list=[]):
    """
    prefix all columns

    Args:
        df(pyspark.sql.dataframe.DataFrame): input dataframe
        prefix: string : The prefix string
        exclude_list: list[string] : List of columns to exclude
    Returns:
        df(pyspark.sql.dataframe.DataFrame): dataframe with prefixed columns
    """
    df_out = df.toDF(*(prefix + c if c not in exclude_list else c for c in df.columns ))
    return df_out

