from sklearn.linear_model       import LogisticRegression           # logistic regression for classification
from sklearn.naive_bayes        import GaussianNB                   # Gaussian Naive Bayes Classifier
from sklearn.tree               import DecisionTreeClassifier       # Decision Tree Classifier
from sklearn.neighbors          import KNeighborsClassifier         # K Nearest Neighbors Classifier
from sklearn.svm                import SVC                          # Support Vector Machine Classifier
from sklearn.ensemble           import AdaBoostClassifier           # Ensemble Technique i.e, Ada Boosting
from sklearn.ensemble           import RandomForestClassifier       # Ensemble Technique i.e, Random Forest


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
    
    return dumps(models[model_name])
