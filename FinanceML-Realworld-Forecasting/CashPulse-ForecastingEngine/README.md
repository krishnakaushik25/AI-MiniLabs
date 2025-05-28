# Cash Liquidity Forecasting
<div align="justify">
Suppose there are 100 bank accounts for a group of companies out of 100 business units and a central account. Now let's say those individual accounts that receive variable cash amounts daily (e.g., from stores or other businesses) will deposit the net cash (net cash inflow) into a central account (e.g., after paying out salaries for employees (cash outflow), service charges, and other depreciation costs). Also, since those 100 accounts might be within a country or spread across several countries, e.g., the central account will have all the liquid money in US Dollars. How can we model this situation as a cash or liquidity forecasting problem such that we can forecast how much liquid cash will still be in their individual or central account so that the organization can make intelligent decisions about investing the liquid money in profitable businesses? This is crucial because, otherwise that money will just be sitting idle. 
  </div>

## Time series forecasting: standard Python libraries vs. PySpark
<div align="justify">
  
When comparing PySpark with its standard Python library counterparts for time series forecasting capabilities, the key points of comparison are performance, features, scalability and computational efficiency, especially in the case of large-scale datasets. The following are the most widely used Python libraries for time series forecasting:

  - [**Darts**](https://github.com/unit8co/darts): Darts is the **most comprehensive and resourceful** Python library for time series forecasting. It provides a variety of models, from classical to deep learning (e.g., from ARIMA, XGBoost, LightGBM, Time-Series Mixer, exponential smoothing, and Prophet to transformers). Darts also supports both **univariate and multivariate** (e.g., contain multiple time-varying dimensions instead of a single scalar value), probabilistic forecasting**, can be used to explain some forecasting models, supports a wide variety of evaluating for the goodness of fit, and supports **back-testing via moving time windows**. Besides, it contains a collection of anomaly scorers, detectors and aggregators, which can all be combined to **detect anomalies** in time series. 
  - [**Skforecast**](https://github.com/JoaquinAmatRodrigo/skforecast/): Skforest is a Python library that eases using scikit-learn regressors as single and multi-step forecasters. It also works with any regressor compatible with the scikit-learn API such as LightGBM, XGBoost, and CatBoost. Besides, it has a **backtesting process** consisting of generating a forecast for each observation in the test set and then comparing the predicted value with the actual value.  
  - **[Prophet](https://github.com/facebook/prophet) and [NeuralProphet](https://github.com/ourownstory/neural_prophet)**: Prophet is designed for forecasting time series data. It's **good for data with strong seasonal effects and several seasons of historical data**. NeuralProphet, on the other hand, is a framework for interpretable time series forecasting. It is built on PyTorch and combines Neural Networks and traditional time-series algorithms, inspired by Facebook Prophet and AR-Net. It is designed for iterative human-in-the-loop model building. This allows building a first model quickly, interpreting the results, improving, and repeating. However, it may not be the most accurate model out of the box. It is **best suited for time series data involving higher frequency** (e.g., sub-daily) and longer duration (e.g., two full periods/years).
  - [**Tsfresh**](https://github.com/blue-yonder/tsfresh): provides systematic **time-series feature extraction** by combining established algorithms from statistics, time-series analysis, signal processing, and nonlinear dynamics with a robust feature selection algorithm. 
  - [**AutoTS**](https://github.com/winedarksea/AutoTS): all models support forecasting **multivariate and probabilistic forecasts**. Most **models can readily scale to tens to hundreds of thousands of input series**. Also, these models can be integrated with AutoML feature search that automatically finds the best models and performs ensemble forecasting through genetic algorithms.
  - [**AutoGluon**](https://github.com/autogluon/autogluon): combines various forecasting algorithms, including well-known statical methods like ETS and ARIMA from StatsForecast, efficient tree-based forecasters like LightGBM, deep learning models like DeepAR and Temporal Fusion Transformer from GluonTS, and pretrained zero-shot forecasting model to produce **multi-step ahead probabilistic forecasts**. It also has **automatic model selection and hyperparameter tuning** functionalities.

These Python libraries are naturally specialised, well-maintained, and based on scientific studies, and hence are widely used for time series forecasting. They support model development, diagnostics, validation, and even back-testing functions. However, they are primarily designed for single-machine (e.g., they don't parallelize computations), hence they work well for datasets that fit into the memory of a single machine. Therefore, they can face significant slowdowns or memory issues when dealing with large datasets, leading to potential OOM issues. 

**PySpark** can handle large-scale data processing, allowing parallel processing across multiple nodes in a cluster. This significantly improves scalability and computational speed for large datasets. PySpark's MLlib library provides tools for ML and time series forecasting. The main advantage is its ability to scale horizontally by adding more nodes to the Spark cluster and its ability to handle complex, thus overcoming the computational bottlenecks faced by standard Python libraries. However, PySpark has no specialized time series functions or algorithms. 
</div>

## Workarounds to recommendations? 
I provide my recommendations in 3-folds: i) using standard libraries in small data settings, ii) using regression algorithms from PySpark, and iii) forecasting at scale with any libraries and by leveraging PySpark's pandas_udf. 

<div align="justify">

### Forecasting with standard libraries in Python in small data settings
For small to medium-sized datasets, standard Python libraries may be sufficient and easier to use due to their specialized time series functions. They're worth exploring and experimenting with because specialised, well-maintained, and based on scientific studies. 
  
### Forecasting using PySpark's regression algorithms   
PySpark's regression models such as random forest and gradient-boosted trees can be used for time series forecasting, albeit they are not the best option. A workaround could be: i) either compute or re-engineer features that capture time series characteristics, e.g. [lag features, rolling windows](https://medium.com/analytics-vidhya/time-series-forecasting-using-spark-ml-part-2-31506514c643) and use them in these models, ii) implement specialised algorithms in PySpark like Prophet. 
</div>

### Forecasting at scale with PySpark's pandas_udf
<div align="justify">
  
Although standard time series forecasting libraries in Python do not have inherent PySpark support, there are several ways to scale things up still. For example, standard Python libraries can be used for time series forecasting by leveraging *pandas_udf* of PySpark and Python UDFs. Like Apache Spark and Arrow, *pandas_udf* uses Pandas for data manipulation to allow writing more performant UDFs than Python UDFs. They bring the power of Pandas and allow its capabilities to be used in PySpark code. More specifically, *pandas_udf* and *applyInPandas* are two powerful functions that can be used for working with grouped data in PySpark. However, their performance and efficiency can largely vary depending on the use case, e.g., pandas_udf is optimized for grouped operations and can leverage vectorized operations, making it faster than row-at-a-time UDFs: 

- **Scalar pandas_udf**: operates element-wise
- **Grouped map pandas_udf**: it is designed for more complex operations on grouped data.
- **applyInPandas**: allows for arbitrary operations on grouped data and allows for more complex transformations. Hence, it can be more efficient for execution with large datasets. Although similar to grouped map pandas_udf, the efficiency of applyInPandas depends on the specific transformation and the context.

Even though these functions can be employed while performing time series forecasting with **any specialized Python libraries in PySpark** (see examples in Darts and AutoTS), the overhead of applying these depends on various factors, e.g., complexity and data size. A sample aggregation operation on 1M rows took 50–55 seconds with Python UDF, whereas pandas_udfs took 40–45 seconds. This is a 25% performance improvement in local mode. Conversely, I noticed the advantage diminishes with smaller data, yet it is a good advantage indicator of using *pandas_udf* in PySpark compared to Python UDFs. 

</div>

**Warnings**: 
<div align="justify">
  
  - both applyInPandas and grouped map pandas_udf may lead to **OOM** if the data within a group is too large.
  - both pandas_udf and applyInPandas in PySpark can potentially produce inconsistent results if not used carefully: i) **non-deterministic operations** -if the function applied is non-deterministic, results may vary between runs, ii) **order of execution** - in distributed setting the order in which data is processed may not be guaranteed, which can affect results in order-sensitive operations, iii) **data partitioning** - how data is partitioned across the cluster can influence the results, especially if the function assumes a certain data distribution or order. To ensure consistent results, it's important to write deterministic functions and check data partitioning, and sanity checking is crucial to confirm that the results are stable and reliable across different runs and cluster configurations.

</div>

## Final verdict
<div align="justify">
  
Taking into consideration several features such as back-testing, probabilistic forecasting, uni- and multivariate support, higher frequency (e.g., sub-daily) & longer duration (e.g., two full periods/years), support for seasonal effects or several seasons, specialised feature extraction, scalability, automatic model selection & hyperparameter tuning, explainability, and anomaly detection capability, we should go with forecasting at scale using Dart library in PySpark to achieve massive scalability and to avoid potential computational bottleneck. 

</div>

<img src="https://github.com/rezacsedu/cash_liquidity_forecasting/blob/main/images/lib_recommendation.png" width="930" height="450">


## Toy proof-of-concept 
<div align="justify">
We did some quick POC based on synthetic data to assess the technical feasibility. The overall workflow of the methods employed can be described as follows: 

  1. **Data generation:** Generating the data by incorporating real-life scenarios.
  2. **Splitting data into a training- and a calibration set**: The calibration set is used to determine the conformity scores, which are essential for conformal prediction.
  3. **Model training**: train the model on the train set by considering factors like seasonality if needed. 
  4. **Generating predictions on a calibration set and calculating the conformity scores**: The conformity score is calculated w.r.t absolute error between the predicted and actual values. 
  5. **Setting a significance level**: Set a confidence level, e.g., 0.05 for 95% confidence and use the conformity scores to determine the prediction intervals for new data points. 
  6. **Prediction:** Predict future data points for a given forecast horizon using the trained model and calculate the upper and lower bounds of the prediction intervals w.r.t conformity scores and the significance level.
</div>

### Data generation
<div align="justify">
We generate synthetic time series data for 1000 accounts over a specified date that ranges with monthly frequency. The dataset includes simulated cash inflows and outflows with seasonal patterns, seasonality, and external economic indicators such as adjusted inflation factors to comply with a real-world scenario.
</div>

```
  # Set the random seed for reproducibility
  np.random.seed(0)
  
  # Generate month-end dates
  dates = pd.date_range(start=start_date, end=end_date, freq='M')
  
  # Number of accounts
  num_accounts = 1000
  
  # Create a MultiIndex with dates and account IDs
  multi_index = pd.MultiIndex.from_product([dates, range(num_accounts)], names=['date', 'account_id'])
  
  # Initialize an empty DataFrame with the MultiIndex
  df = pd.DataFrame(index=multi_index)
  
  # Define the number of periods (months)
  num_periods = len(dates)
  
  # Simulate seasonal patterns for cash inflows and outflows. Assuming a yearly seasonality with a sinusoidal pattern
  seasonality_inflows = np.sin(np.linspace(0, 2 * np.pi, num_periods))
  seasonality_outflows = np.sin(np.linspace(0, 2 * np.pi, num_periods))
  
  # Generate random cash inflows and outflows for each account on each date and add the seasonality effect
  df['cash_inflows'] = (np.random.normal(loc=100000, scale=20000, size=len(df)) + np.tile(seasonality_inflows, num_accounts))
  df['cash_outflows'] = (np.random.normal(loc=50000, scale=10000, size=len(df)) + np.tile(seasonality_outflows, num_accounts))
  
  # Simulate external economic factors (e.g., inflation rates). Let's assume we have inflation rates for 10 countries
  inflation_rates = [0.03, 0.025, 0.04, 0.02, 0.05, 0.03, 0.045, 0.025, 0.035, 0.03]  # Example rates
  df['inflation_factors'] = np.random.choice(inflation_rates, size=len(df))
  
  # Adjust cash flows based on inflation rates
  df['adjusted_cash_inflows'] = df['cash_inflows'] * (1 + df['inflation_factors'])
  
  # Calculate net cash flow
  df['net_cash_flow'] = df['adjusted_cash_inflows'] - df['cash_outflows']
  
  # Reset the index to turn the MultiIndex into columns
  df.reset_index(inplace=True)
```
<img src="https://github.com/rezacsedu/cash_liquidity_forecasting/blob/main/images/sample_data.png" width="900" height="400">

### Standalone forecasting using Prophet model from Darts library 
```
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

model, train_series = standalone_model_training_for_liquidity_forecasting(cash_flow_df)

forecast_horizon = 30
forecast, lower_quantile, upper_quantile = standalone_liquidity_forecasting(model, forecast_horizon)
# Sum all net_cash_flow columns for each date
forecast_pdf = forecast.pd_dataframe()
     
forecast_pdf['forecasted_net_cash_flow'] = forecast_pdf.filter(regex='^net_cash_flow_s').mean(axis=1)
forecast_pdf['date'] = forecast_pdf.index
forecast_pdf = forecast_pdf.reset_index(drop=True)
forecast_pdf = forecast_pdf[['date', 'forecasted_net_cash_flow']]    
```
<img src="https://github.com/rezacsedu/cash_liquidity_forecasting/blob/main/images/sample_forecast_pdf.png" width="400" height="300">

### Distributed cash liquidity forecasting with Darts library in PySpark
```
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
```
<img src="https://github.com/rezacsedu/cash_liquidity_forecasting/blob/main/images/sample_forecast_sdf.png" width="250" height="350">

### Distributed cash liquidity forecasting with AutoTS library in PySpark
```
  from autots import AutoTS
  import pandas as pd
  from pyspark.sql.functions import pandas_udf, PandasUDFType
  from pyspark.sql.types import *
  
  df_spark = spark.createDataFrame(df1)  
  schema = StructType([StructField('series_id', StringType(), True),
                       StructField('datetime', DateType(), True),
                       StructField('value', LongType(), True)])
  
  @pandas_udf(df_spark.schema, PandasUDFType.GROUPED_MAP)  
  def forecast_func(df_long):      
    model = AutoTS(
      forecast_length=18,
      frequency='MS',
      model_list= "fast_parallel",
        transformer_list='all',
      ensemble='all',
      validation_method="even",
      max_generations=5,
      num_validations=3,
      no_negatives=True,
      constraint=2.0)

    model = model.fit(df_long, date_col='datetime', value_col='value', id_col='series_id')
    prediction = model.predict()
    forecasts_df = prediction.forecast
    forecasts_df.reset_index(inplace = True)
    forecasts_df.insert(2, "series_id", forecasts_df.columns.values[1])
    forecasts_df.columns = ['datetime', 'value', 'series_id']

    return(forecasts_df)
  
  out_df = df_spark.repartitionByRange(2000, 'series_id').groupby(['series_id']).apply(forecast_func)
```

### Conformal prediciton interval for better uncertanity quantification
```
def plot_liquidity_forecast(series, forecast, lower_quantile, upper_quantile):
  # Plot the forecast alongside the actual data
  plt.figure(figsize=(13, 6))
  ax = plt.gca()  # Get the current Axes instance

  # Plot actual and forecast series
  actual_plot, = ax.plot(series.time_index, series.values(), label='Actual', color='black')
  forecast_plot, = ax.plot(forecast.time_index, forecast.values(), label='Forecast', color='blue')
  lower_quantile_plot, = ax.plot(lower_quantile.time_index, lower_quantile.values(), label='5th percentile', color='green')
  upper_quantile_plot, = ax.plot(upper_quantile.time_index, upper_quantile.values(), label='95th percentile', color='red')

  # Add vertical dashed lines for important dates
  campaign_start = pd.Timestamp('2022-01-01')
  campaign_end = pd.Timestamp('2022-06-01')
  product_launch = pd.Timestamp('2023-06-01')
  plt.axvline(x=campaign_start, color='red', linestyle='--', linewidth=1, label='Campaign Start')
  plt.axvline(x=campaign_end, color='red', linestyle='--', linewidth=1, label='Campaign End')
  plt.axvline(x=product_launch, color='green', linestyle='--', linewidth=1, label='Product Launch')

  # Annotate with arrows
  plt.annotate('Horizon', xy=(forecast.time_index[-1], forecast.values()[-1]),
  xytext=(forecast.time_index[-30], forecast.values()[-1] + 50000),
  arrowprops=dict(facecolor='orange', shrink=0.05), fontsize=9)
  plt.annotate('Period Focus', xy=(campaign_start, ax.get_ylim()[0]),
  xytext=(campaign_start, ax.get_ylim()[1] - 50000),  # Move the text up by using the upper y-limit
  arrowprops=dict(facecolor='purple', shrink=0.05), fontsize=9)
  plt.annotate('Cut-off', xy=(campaign_end, ax.get_ylim()[0]),
  xytext=(campaign_end, ax.get_ylim()[0] + 50000),
  arrowprops=dict(facecolor='brown', shrink=0.05), fontsize=9)

  # Set title, labels, and legend
  plt.title('Liquidity Forecast with Confidence Intervals')
  plt.xlabel('Date')
  plt.ylabel('Net Cash Flow')
  plt.legend(ncol=len(ax.lines), loc='upper center', bbox_to_anchor=(0.5, -0.1))

  # Improve date formatting on the x-axis
  ax.xaxis.set_major_locator(mdates.YearLocator())
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
  ax.xaxis.set_minor_locator(mdates.AutoDateLocator())
  ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

  # Rotate date labels for better readability
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
  plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)

  # Show gridlines
  plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)

  # Use mplcursors to add interactive hover tooltips
  cursor = mplcursors.cursor(hover=True)
  cursor.connect("add", lambda sel: sel.annotation.set_text(
  'Date: {}\nNet Cash Flow: ${:.2f}'.format(pd.to_datetime(sel.target[0]).strftime('%Y-%m-%d'), sel.target[1])))

  # Show the plot
  plt.tight_layout()
  plt.show()

plot_liquidity_forecast(train_series, forecast, lower_quantile, upper_quantile)  
```
<img src="https://github.com/rezacsedu/cash_liquidity_forecasting/blob/main/images/sample_forecast.png" width="900" height="400">

  - **Cut-off**: This is a point in time at which the data is divided into two parts: the historical data used for training the model, and the future period for which predictions are made. The cut-off date is crucial because it determines the dataset that will be used to train the forecasting model.  
  - **Period Focus**: As previously mentioned, this refers to the granularity of the forecast, such as hourly, daily, or monthly forecasts. It's about choosing the right time interval that aligns with the specific needs of the forecast.
