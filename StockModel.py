import pandas as pd
from joblib import dump

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import make_scorer, precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Since I have already trained and evaluated in a Jupyter notebook,
# I will be finalizing the model by training it on the entire set.
df = pd.read_csv('TechStockDataForModelPreppedNoOutliers.csv')

X, y = df.drop(['Target', 'SP_change'], axis=1), df['Target']

preprocessing = ColumnTransformer([
    ('scaler', StandardScaler(), X.select_dtypes(include='number').columns),
])

custom_scorer = make_scorer(precision_score, greater_is_better=True, pos_label='Yes')


log_pipeline = Pipeline([
    ('preprocessing', preprocessing),
    ('log', LogisticRegression(max_iter=10000)),
])

log_param_grid = {'log__penalty': ['l2'],
                  'log__C': [0.005],
                  'log__solver': ['lbfgs']
                 }

custom_scorer = make_scorer(precision_score, 
                            greater_is_better=True, 
                            pos_label='Yes')

log_grid = GridSearchCV(estimator=log_pipeline, 
                        param_grid=log_param_grid, 
                        cv=5, 
                        scoring=custom_scorer, 
                        verbose=2)


log_grid.fit(X, y)

dump(log_grid, 'FinalStockModel.joblib')



