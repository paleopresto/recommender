### Scikit-learn RandomForestClassifier Implementation for LiPD Dataset

#### Requirements

1. You need to use python 3.8
2. You would need to upgrade sklearn and ensure version is greater than 0.21.

    ```
    pip install --upgrade sklearn
    ```

3. Run the notebook RF_paleodata.ipynb

#### What are we doing

1. Read the csv generated for the LiPD dataset in clean_lipdverse_datasets. ('master_lipd.csv')
2. Try to predict the proxyObservationType given the archiveType.
3. Try to predict the units given the proxyObservationType.

#### Steps

##### First Table - Predicted Archive Type, classVar = proxyObsType

1. We are using the predicted archiveType and the final proxyValue columns for prediction. For the meanings of the column refer the README from ../clean_lipdverse_datasets
2. Find the frequency of appearance of all the archiveTypes and the proxyValue. Remove all the ones whose frequency is less than 1. You can set the threshold in the notebook.
3. Since Scikit-learn RandomForest doesn't work on text data, we need to encode our columns.
4. We have tried 2 variations
    1. Enforcing an explicit ordering based on the frequency of appearance on the data.
    2. Random ordering of the data.
5. We used FeatureEncoding to number the archiveTypes and the proxyValues and replace them in the dataframes.
6. We fit a DummyClasssifier on the data to set a baseline which gave an accuracy of **13.236929922135707 %**.
7. We then fit a RandomForestClassifier on this data.
    1. For the explicit ordering feature encoding the model gave an accuracy of **37.04115684093437 %**.
    2. For the random ordering feature encoding the model gave an accuracy of **37.04115684093437 %**.
    This means that the ordering did not have an impact on the predictions.
8. We wanted to understand what was the prediction from each tree. We ran predict on each of the estimators of the model to get the same.
9. Visualized one of the trees using graphviz.


##### Second Table - proxyObsType, classVar = units

1. We are using the final proxyValue and units columns for prediction. For the meanings of the column refer the README from ../clean_lipdverse_datasets
2. Find the frequency of appearance of all the proxyValue and units. Remove all the ones whose frequency is less than 1. You can set the threshold in the notebook.
3. Since Scikit-learn RandomForest doesn't work on text data, we need to encode our columns.
4. We have tried to directly one-hot encode the entire data.
    Came across the curse of dimensionality : One-hot encoding results in a very sparse tree.
    https://towardsdatascience.com/one-hot-encoding-is-making-your-tree-based-ensembles-worse-heres-why-d64b282b5769 
6. We fit a DummyClasssifier on the data to set a baseline which gave an accuracy of **27.86343612334802 %**.
7. We then fit a RandomForestClassifier on this data.
   The model gave an accuracy of **86.12334801762115 %**.
   This result can be attributed to the distribution of the data across the classes. Since all the classes do not have equal number of samples, we cannot assume the model accuracy with certainty. 