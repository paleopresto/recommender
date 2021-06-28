### Probabilistic Recommendation System

#### Requirements

1. You need to use python 3.8
2. https://ipywidgets.readthedocs.io/en/latest/user_install.html

    ```
    pip install ipywidgets
    jupyter nbextension enable --py widgetsnbextension
    ```

3. Run the notebook calculate_probabilities.ipynb
4. Annotating Paleoclimate Data - Final Presentation presents this work.

#### What are we trying to achieve:

1. Read the csv file created by reading all the lipd files.
2. Using Conditinal Probabilities and Bayesian rules to compute the value for ProxyObservationType and Inferred Variable Type given the ArchiveType.
3. Using ipywidgets to generate a simulation of the entire process.

#### Issues with current approach

1. The data needs a lot of cleaning for efficient predictions.
2. We are not learning anything from the data.
3. We expect the user to enter the 'archiveType' to start the process. This means we are dependent on the user to provide us an archiveType. We would like to have a reverse prediction process which will help us fill the missing values.
