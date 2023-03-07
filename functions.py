def visualize_subplots_boxplots(df: DataFrame, columns: List[str], nrows: int, ncols: int) -> None:
    """
    Creates a grid of subplots containing boxplots of Daily average energy consumption.

    Args:
        df: A Pandas DataFrame containing energy consumption data.
        columns: A list of column names to include in the boxplots.
        nrows: The number of rows in the subplot grid.
        ncols: The number of columns in the subplot grid.

    Returns:
        None. Displays a grid of subplots containing boxplots of daily average energy consumption.

    Example:
        >>> visualize_subplots_boxplots(my_df, ['Consumption', 'Generation'], 3, 4)
    """
    from typing import List
    from pandas import DataFrame
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 12))
    fig.suptitle('Daily Average Energy Consumption', weight='bold', fontsize=25)

    # We just need 11 figures, so we delete the last one
    if nrows*ncols > len(columns):
        fig.delaxes(axes[nrows-1][ncols-1])

    for i, col in enumerate(columns): 
        sns.boxplot(data=df, x='Day', y=col, ax=axes.flatten()[i], color='#cc444b')

    plt.tight_layout()
    plt.show()
    fig.savefig("Images/Daily_Average_Energy_Consumption.png", dpi=300, bbox_inches='tight')

def moving_average(data: pd.DataFrame, window: int, savepath) -> None:
    """
    Calculates and visualizes the moving average of a time series data.

    Args:
        data: A Pandas DataFrame containing the time series data.
        window: An integer representing the window size for calculating the moving average.

    Returns:
        None. Visualizes the actual data and the moving average.

    Example:
        >>> moving_average(my_data, 5)
    """
    # calculate the moving average
    data['Moving Average'] = data['DAYTON_MW'].rolling(window).mean()
    actual = data['DAYTON_MW'][-(window+30):]
    ma = data['Moving Average'][-(window+30):]

    # plot the actual data and moving average
    plt.figure(figsize=(20,8))
    actual.plot(label='Actual', lw=4)
    ma.plot(label='MA-{}'.format(str(window)), ls='--', lw=2)
    plt.title('{}-Days Moving Average'.format(str(window)), weight='bold', fontsize=25)
    plt.legend()
    plt.savefig(savepath, dpi=300, bbox_inches='tight')
    plt.show()
    
def plot_data_splitting(train, test):
    """
    Plots the training and test sets of a time series.

    Args:
    train (pandas.DataFrame): DataFrame containing the training set with a DatetimeIndex and a 'DAYTON_MW' column.
    test (pandas.DataFrame): DataFrame containing the test set with a DatetimeIndex and a 'DAYTON_MW' column.

    Returns:
    None
    """
    plt.figure(figsize=(20,8))

    plt.plot(train.index, train['DAYTON_MW'], label='Training Set')
    plt.plot(test.index, test['DAYTON_MW'], label='Test Set')
    # plt.text('2015-10-01', 3700, 'Split', fontsize=20, fontweight='bold') 

    plt.title('Data Splitting', weight='bold', fontsize=25)
    plt.legend()
    plt.show()

def plot_prophet_forecast(prophet_test, prophet_pred, savepath):
    """
    Plots the actual and predicted values of a Prophet test set, along with the mean absolute error (MAE).

    Parameters:
    prophet_test (pandas.DataFrame): The Prophet test set containing columns 'ds' and 'y'.
    prophet_pred (pandas.DataFrame): The Prophet predictions containing columns 'ds' and 'yhat'.

    Returns:
    None
    """
    mae = round(mean_absolute_error(prophet_test['y'], prophet_pred['yhat']), 3)
    plt.figure(figsize=(20,8))
    plt.plot(prophet_test['ds'], prophet_test['y'], label='Actual')
    plt.plot(prophet_pred['ds'], prophet_pred['yhat'], label='Predicted')
    plt.title('Test Forecasting', weight='bold', fontsize=40)
    plt.text(16770, 3250, 'MAE: {}'.format(mae), fontsize=20, color='red')
    plt.title('Testing Set Forecast', weight='bold', fontsize=25)
    plt.savefig(savepath,  dpi=300, bbox_inches='tight')
    plt.legend()


def evaluate_prophet_model(model, test_set):
    """
    Evaluate a Prophet model using mean absolute error (MAE), root mean squared error (RMSE), and mean absolute percentage error (MAPE).
    
    Parameters:
    -----------
    model : Prophet object
        Fitted Prophet model
    test_set : DataFrame
        DataFrame containing the test set with columns 'ds' and 'y'
        
    Returns:
    --------
    mae : float
        Mean absolute error
    rmse : float
        Root mean squared error
    mape : float
        Mean absolute percentage error
    """
    
    # Make predictions on test set
    forecast = model.predict(test_set)
    y_true = test_set['y'].values
    y_pred = forecast['yhat'].values
    
    # Calculate evaluation metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return mae, rmse, mape

