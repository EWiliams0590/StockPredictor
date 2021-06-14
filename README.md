# Stock Price Increase Predictor
The purpose of this project was to create a model to predict when the closing price of a stock would increase by at least 2.25% over the next four days.

The stocks used for training and testing were all the stocks in the "Technology" category (as defined by Yahoo Finance) with a stock price between $20-$200 with a 30-day average volume of at least 100,000. I went back 300 days to get the data and only kept the tickers with at least 30 days worth of data

Due to the desired result of probabilities, I used a LogisticRegression model.

### Obtaining the Data
To obtain the data, I used yfinance and BeautifulSoup to get all the tickers meeting my desired criteria described above.

### Transforming the Data
I created functions and a pipeline based on analysis done (both historical and of my own creation) to create features to help make predictions. After thorough analysis, I decided on which features to keep.

I got rid of many data points that were extreme outliers. When I ran a sample model on the training set without this, I got extremely strange results.

### EDA/Visualization
The EDA was done using Jupyter Notebook. I cleaned it up after going through all the features I was interested in analyzing. This is in the "Stock EDA" notebook.

### Model
As stated above, I chose a LogisticRegression model due to not only wanting a classifier, but also wanting the probabilities.
The model transforms the data by scaling all the features (all features are numerical).
When predicting, the model does not consider the data points containing any outliers defined by the EDA I did.

### Performance
When evaluating the model, the average "Yes" prediction had stock price increase of about 3.5% compared to 2.25% with the No's. You can also see from the notebook on "Model Evaluation" that there is over twice as many predicted "No" than "Yes", but each has a substantial amount and the 95% confidence intervals of each are extremely far apart.

The model performed just as well on the test data as the training data. I am going to update this once I have some more data as far as how the stock's my model predicts is performing. I will obtain the stock tickers that have a "Yes" prediction (along with their probabilities) prior to opening on each Monday and will keep track of the maximum closing price over the next four days to see how well it is performing.

I will be using the same criteria for predicting with the model as it was trained on. Although some tickers will certainly change by virtue of changing stock prices and volumes, the point of making the restrictions on the training/testing data was to have an adequate amount of data to use each day with the same properties.

### Future Considerations
I would like to learn more about neural networks/deep learning and try to a neural network to apply to this data. From much of my EDA, I noticed that many of the data features had clear trends as far as when Yes or No was more predicted; however, it was never a drastic sway. When I added in a polynomial features (up to degree 2 for computational reasons), the model performed almost exactly the same.
