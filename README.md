# Stock Price Increase Predictor
## Motivation
I was interested in analyzing certain properties of stock prices (custom and well known momentum creators) to increase weekly stock price gains over the course of a week.

## Process
### Obtaining the Data
I used a stock screener on Yahoo Finance to find all the current stock tickers that met a certain criteria. For this project, I filtered the screen to stock tickers with a price between $20-$200 on the day of data retrievel that are in the "Technology" category and had an average volume over the past 30 days of at least 100,000. I then used BeautifulSoup/HTML to scrape and create a list of all these tickers.

From there, I used the yfinance library to obtain the daily data for each of these stock tickers for the past 300 calendar days. As I knew I was going to be using or creating features based on previous day's data, I only kepts those which had at least 30 days worth of data.

### Data Cleaning and Feature Engineering
After the data was obtained, I created custom features (a custom volatility and volume indicator) and use the talib to analyze some well known features. Initially, I analyzed a few (RSI, MACD, SMA), but upon analyzing each of these, I noticed that the only one that gave any interesting insights compared to the custom features was RSI, so this is all I kept.

I also created a target column measuring the maximum 4-day change in stock price (as a proportion), called SP_change_Target, and used this to create a "Yes/No" for classification called Target. The "Yes" was if the SP_change_Target >= 0.0225 (2.25%) and "No" otherwise.

With how the data was created, many null values popped up from the feature engineering step, so I removed the nulls after fully feature engineering (otherwise consecutive rows may not be consecutive days).

### Data Mining, Visualization, and Analysis
I then used Pandas, Numpy, Seaborn, and Matplotlib to look into the data. Discovering many extreme outliers in the dataset (some due to the "memestocks" on Reddit), I realized removing these outliers, not only for analysis but also to put in a pipeline for modeling/future analysis when choosing weekly stock tickers would be a good idea as they heavily swayed the target columns.

I split the data into a train and test data sets at the beginning of analysis to avoid any data leakage.

### Results
After analyzing the average stock price change based on some of my created features and creating many classification models (trying to predict yes with a certain probability using Logistic Regression, Random Forest Regression, KNN Regression), I found that restricting to looking at a couple of features did just as well as the best model. 

Overall, the average SP_change_Target for the training set was ~ 0.03 with a 95% CI of ~(0.029, 0.031). By restricting the dataset to have a 20-day average volatility of 0.03 and have lost at least 5% of it's stock price over the 10 days, the test data had a 95% CI of ~(0.048, 0.066). Moreso, the when combining the entire dataset back together, the overall 95% CI was ~(0.049, 0.054), which is about a 60% increase in looking at the data without these restrictions.

Most importantly, roughly 5% of the data met the two restricted criteria, and since there are ~300 tickers that meet the filtered criteria described above, this means we can expect to have ~15 tickers per week to meet the criteria. Of course, if this restriction was such that there was no way to guarantee we would get any tickers to meet these criteria, then the results would not be meaningful.

### Predictions
Of course, after doing all this, I wanted to be able to implement it and see what tickers it would suggest, so I created a script to get the daily "Yes" predictions, in this case, Yes meaning the stock tickers that meet the two restrictions above.

## Requirements
[Requirements](https://github.com/EWiliams0590/StockPredictor/blob/main/requirements.txt)
## Notebooks and .py Scripts
  * [Scrape for Stock Tickers and Data](https://github.com/EWiliams0590/StockPredictor/blob/main/GetTickersAndDataForModelTraining.py)
  * [Functions for Feature Engineering](https://github.com/EWiliams0590/StockPredictor/blob/main/FunctionsForFeatureAdding.py)
  * [Pipeline for Converting Data](https://github.com/EWiliams0590/StockPredictor/blob/main/ConvertData.py)
  * [Data Visualization and Analysis](https://github.com/EWiliams0590/StockPredictor/blob/main/Stock%20EDA.ipynb)
  * [Model Creation and Evaluation](https://github.com/EWiliams0590/StockPredictor/blob/main/Model%20Evaluation.ipynb)
  * [Get the Daily "Yes" Predictions](https://github.com/EWiliams0590/StockPredictor/blob/main/GetDailyYesPredictions.py)
  * [Evaluating the Picks](https://github.com/EWiliams0590/StockPredictor/blob/main/EvaluationOfModelPicks.py)
  
## Python Libraries
  * [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/), [requests](https://pypi.org/project/requests/) - Web scraping
  * [yfinance](https://pypi.org/project/yfinance/) - Obtaining Daily Data
  * [talib](http://mrjbq7.github.io/ta-lib/doc_index.html) - Traditional technical analysis library for stocks
  * [Pandas](https://pandas.pydata.org/), [Numpy](https://numpy.org/), [Scipy](https://www.scipy.org/) - Data Analysis
  * [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/index.html) - Data Visualization
  * [Sci-kit Learn](https://scikit-learn.org/stable/index.html) - Feature engineering, Pipelines, Preprocessing, and Model Creation
