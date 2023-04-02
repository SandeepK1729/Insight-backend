import numpy    as np 
import pandas   as pd
import matplotlib.pyplot as plt

from seaborn                    import heatmap

from sklearn.linear_model       import LogisticRegression           # logistic regression for classification
from sklearn.naive_bayes        import GaussianNB                   # Gaussian Naive Bayes Classifier
from sklearn.tree               import DecisionTreeClassifier       # Decision Tree Classifier
from sklearn.neighbors          import KNeighborsClassifier         # K Nearest Neighbors Classifier
from sklearn.svm                import SVC                          # Support Vector Machine Classifier
from sklearn.ensemble           import AdaBoostClassifier           # Ensemble Technique i.e, Ada Boosting
from sklearn.ensemble           import RandomForestClassifier       # Ensemble Technique i.e, Random Forest

from sklearn.model_selection    import train_test_split
from sklearn.metrics            import accuracy_score, confusion_matrix, precision_score, recall_score 

from sklearn.datasets           import *

from pickle                     import load, dumps

from .models                    import Dataset, ModelFile
from django.conf                import settings

from pathlib                    import Path


def get_trained_model(model_name: str, dataset_id: int, knn_val: int):
    """gives the report of model on analysis of dataset

    Args:
        model_name (str): name of the model
        dataset_id (int): unique id of the dataset
        knn_val    (int): knearestneighbour val

    Returns:
        obj: returns the model trained object in some of file content
    """

    features, target = get_dataset(dataset_id)
    
    model = get_model(model_name, knn_val)
    model.fit(features, target)           # model training 

    return dumps(model)

def give_analysis_report(model_file, dataset_id):
    """gives the report of model on analysis of dataset

    Args:
        model_file (file): file of the model
        dataset_id (int): unique id of the dataset

    Returns:
        dict: gives report of dictionary
    """
    
    X, y = get_dataset(dataset_id)
    
    model = load(model_file)
    
    y_pred = model.predict(X)        # making prediction
    
    res = {
        "accuracy"              : f"{int(accuracy_score(y, y_pred) * 100)}",
        "Precision Score"       : f"{int(precision_score(y, y_pred, average = 'micro') * 100)}",
        "Recall Score"          : f"{int(recall_score(y, y_pred, average = 'micro') * 100)}",
    }
    
    # plt.title(f"Classfication using {model_name} on {dataset_name}")
    # heatmap(pd.DataFrame(confusion_matrix(y_test, y_pred)), annot = True)
    # plt.xlabel("Predicted Labels")
    # plt.ylabel("Actual Labels")
    # plt.savefig(f"Confusion Matrix of {model_name} on {dataset_name}.png")

    return res

def get_dataset(dataset_id: str):
    """returns the features and target columns of dataset

    Args:
        dataset_id (int): unique id of the dataset

    Returns:
        (pd.DataFrame, pd.DataFrame): tuple of features dataframe and target dataframe or series
    """

    dataset = Dataset.objects.get(id = dataset_id)
    df      = pd.read_csv(dataset.path)
    target  = dataset.targets.keys()

    y       = df[target]
    X       = df.drop(
                target,
                axis = 1
            )

    return (X, y)

def get_model(model_name, neighbors = 0):
    """
    get_model function

    Args:
        model_name (str): name of the model
        neighbors (int, optional): no of neighbours. Defaults to 0.

    Returns:
        model object: contains respective model object
    """

    models = {
        "Decision Tree Classifier"          : DecisionTreeClassifier(),
        "K-Nearest Neighbors Classifier"    : KNeighborsClassifier(n_neighbors = int(neighbors)),
        "Logistic Regression"               : LogisticRegression(random_state = 0),
        "Gaussian Naive Bayes Classifier"   : GaussianNB(),
        "Random Forest Classifier"          : RandomForestClassifier(n_estimators = 25),
        "Support Vector Machine"            : SVC(),
    }
    
    return models[model_name]

