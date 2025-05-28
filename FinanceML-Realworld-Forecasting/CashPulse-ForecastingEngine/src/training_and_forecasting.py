%%time 
from darts import TimeSeries
from darts.models import Prophet
import matplotlib.pyplot as plt
from darts import TimeSeries
from darts.models import Prophet
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import pandas as pd
from darts import TimeSeries
from darts.models import Prophet

def standalone_model_training_for_liquidity_forecasting(df):
  # Aggregate the net cash flow for each date to get the total liquidity
  total_liquidity = df.groupby('date')['net_cash_flow'].sum().reset_index()

  # Convert the aggregated data into a Darts TimeSeries object
  train_series = TimeSeries.from_dataframe(total_liquidity, time_col='date', value_cols='net_cash_flow', fill_missing_dates=True, freq='M')

  # Create and fit the Prophet model
  model = Prophet(seasonality_mode='multiplicative', yearly_seasonality=4)
  model.fit(train_series)

  return model, train_series

def standalone_liquidity_forecasting(model, forecast_horizon): 
  # Forecast the future liquidity for the next 'n' periods
  forecast = model.predict(n=forecast_horizon, num_samples=1000)

  # Extract the quantiles to get the confidence intervals
  lower_quantile = forecast.quantile_timeseries(0.05)
  upper_quantile = forecast.quantile_timeseries(0.95)

  return forecast, lower_quantile, upper_quantile
