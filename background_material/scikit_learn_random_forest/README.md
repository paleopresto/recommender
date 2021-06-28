### Scikit-learn RandomForestClassifier Implementation on Iris Dataset

#### Requirements

1. You need to use python 3.8
2. You would need to upgrade sklearn and ensure version is greater than 0.21.

    ```
    pip install --upgrade sklearn
    ```

3. Run the notebook scikit-random-forest-classifier.ipynb

#### What we understood

RandomForestClassifier will be selecting bagged samples(choosing samples with replacement) and a random number of features(max_features = None means all features are selected).
This generates different number of decision trees. The final score is a max vote of all the predictions from all the decison trees, thus improving the overall prediction process.

#### What are we trying to achieve

1. Get the predictions from each of the decision trees separately.
2. Get the accuracy of each individual decision tree.
3. Visualize the decision trees to understand the features the data is split on.
