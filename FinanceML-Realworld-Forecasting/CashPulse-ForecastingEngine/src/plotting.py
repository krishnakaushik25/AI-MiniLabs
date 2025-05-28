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
