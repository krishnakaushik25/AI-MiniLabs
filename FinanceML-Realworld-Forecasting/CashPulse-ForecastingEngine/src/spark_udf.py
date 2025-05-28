%%time 
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import *
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import StructType, StructField, TimestampType, IntegerType, DoubleType

import pandas as pd
from darts import TimeSeries
from darts.models import Prophet

# Initialize a Spark session
spark = SparkSession.builder.appName("LiquidityForecasting").getOrCreate()

schema = StructType([
StructField('date', TimestampType(), True),
StructField('forecast_net_cash_flow', DoubleType(), True)
])

# Define the pandas_udf function
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def forecast_timeseries(df):
  # Convert the data into a Darts TimeSeries object
  train_series = TimeSeries.from_dataframe(df, time_col='date', value_cols='net_cash_flow', fill_missing_dates=True, freq='M')

  # Create and fit the Prophet model
  model = Prophet(seasonality_mode='multiplicative', yearly_seasonality=4)
  model.fit(train_series)

  # Forecast the future liquidity
  forecast_horizon = 30  # Adjust the forecast horizon as needed
  forecast = model.predict(n=forecast_horizon)

  # Prepare the forecast DataFrame to match the specified schema
  forecast_df = forecast.pd_dataframe()
  forecast_df.reset_index(inplace=True)
  forecast_df.columns = ['date', 'forecast_net_cash_flow']
  #forecast_df['total_mean_forecasted_net_cash_flow'] = forecast_df.filter(regex='^total_mean_forecasted_net_cash_flow_s').mean(axis=1)

  # Return the forecast as a Pandas DataFrame
  return forecast_df

# Assuming 'sdf' is a Spark DataFrame with 'date' and 'net_cash_flow' columns. Apply the pandas_udf function to the DataFrame
total_liquidity = cash_flow_df.groupby('date')['net_cash_flow'].sum().reset_index()
sdf = spark.createDataFrame(total_liquidity)
forecast_sdf = sdf.groupby().apply(forecast_timeseries)
