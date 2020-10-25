import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE, SelectPercentile, f_classif
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import MaxAbsScaler
from sklearn.svm import LinearSVC
from tpot.builtins import StackingEstimator
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: 0.8318355333451303
exported_pipeline = make_pipeline(
    make_union(
        RFE(estimator=ExtraTreesClassifier(criterion="gini", max_features=0.45, n_estimators=100), step=0.05),
        FunctionTransformer(copy)
    ),
    StackingEstimator(estimator=ExtraTreesClassifier(bootstrap=False, criterion="entropy", max_features=0.8, min_samples_leaf=18, min_samples_split=11, n_estimators=100)),
    SelectPercentile(score_func=f_classif, percentile=67),
    MaxAbsScaler(),
    LinearSVC(C=0.5, dual=True, loss="squared_hinge", penalty="l2", tol=1e-05)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
