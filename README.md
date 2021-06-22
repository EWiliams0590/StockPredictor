# Stock Price Increase Predictor
The purpose of this project was to create a model to predict when the closing price of a stock would increase by at least 2.25% over the next four days.

The stocks used for training and testing were all the stocks in the "Technology" category (as defined by Yahoo Finance) with a stock price between $20-$200 with a 30-day average volume of at least 100,000. I went back 300 days to get the data and only kept the tickers with at least 30 days worth of data

### Obtaining the Data
To obtain the data, I used yfinance and BeautifulSoup to get all the tickers meeting my desired criteria described above.

### Transforming the Data
I created functions and a pipeline based on analysis done (both historical and of my own creation) to create features to help make predictions. After thorough analysis, I decided on which features to keep.

I got rid of many data points that were extreme outliers (only kept with 3 std of the mean since all distributions were roughly normal).

### EDA/Visualization
The EDA was done using Jupyter Notebooks. I cleaned it up after going through all the features I was interested in analyzing. This is in the "Stock EDA" notebook. I used a RandomForestClassifier to get feature importances and noticed a huge improvement by limiting the training data to the following requirements: The stock must maintain a certain volatility (0.03) on average over the past 20 days and must have lost at least 5% of it's value over the past 10 days.

The analysis on the training set, confirmed on the testing set, showed an average increase 95% confidence interval of (0.049, 0.054) (4.9%-5.4% increase) in closing stock price.

Note that the volatility is defined by the (high-close)/close price on a given day.

### Model
I performed GridSearch on a number of models including Random Forest Classification, Logistic Regression, and KNN Regressor, then validated the results. The best model, Logistic Regression, showed that, when a prediction of "Yes" with probability of at least 60% had an average increase 95% confidence interval of (0.047, 0.051) (4.7%-5.1% increase) in closing stock price

### Final Result
In comparison, limiting the data as described above performed just as well as the models on the test set. Due to this, I decided against using a model and just looking at these two features.
