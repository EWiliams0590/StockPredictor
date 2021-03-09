# StockPredictor

The goal of this project was to data from Yahoo Finance to know which stock tickers in the Healthcare field to invest.

### Stock Scraper
The first thing to do was to get the data. I did this using BeautifulSoup4 and Python. I imposed certain conditions on the stock tickers to download the data from. Specifically, the stocks had to be in the Healthcare field and their current stock price had to be between 10 and 50 dollars. There was about 160 tickers that met the criteria, which I then used to download daily data for each stock ticker from the previous calendar year.

### Stock Predictor
After obtaining and saving the data above in a csv file, I fixed it up, applied relevant changes and trained a model. The final choice of model was a Logistic Regression model, since it not only performed best, but it outputs probabilities, which I found to be a useful tool. The hyperparameters were chosen from an exhaustive grid search.

The goal was to find a model that could predict when a 3% increase was to be expected from a ticker's next day high price vs open price, with the idea that if you can buy a stock for it's open price the next day, you can expect a 3% increase on your purchase. After some thinking, I realized that the usefulness of probabilities was more useful instead of just a simple yes/no, which led me to the below.

In this Jupyter Notebook, I also performed some basic visualization of how the model performed on the entire set. Ultimately, we saw a statistically significant improvement from using our model compared to choosing any random ticker, assuming the choice of ticker(s) to use had a probability of >53.5%. I chose this probability based on a visual in the notebook.

### Pulling Data and Transform for Stock Model
This notebook was specifically for using the model to make predicts. The final product is being able to put in a list of tickers, and the output is those that had a certain probability threshold. I only used 0.535 (53.5%); however, this could be easily changed to make it an input the user wants. One important thing to consider here is that the model's probability distribution on the dataset had around a mean of 0.45 with a rather small standard deviation, so someone using something like 0.8 would probably not get any results on a daily basis.
