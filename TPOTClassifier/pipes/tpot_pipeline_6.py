import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.6429538681742378
exported_pipeline = make_pipeline(
    make_union(
        make_union(
            StackingEstimator(estimator=RandomForestClassifier(bootstrap=True, criterion="entropy", max_features=0.1, min_samples_leaf=13, min_samples_split=3, n_estimators=100)),
            FunctionTransformer(copy)
        ),
        FunctionTransformer(copy)
    ),
    SelectPercentile(score_func=f_classif, percentile=50),
    BernoulliNB(alpha=0.1, fit_prior=False)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
