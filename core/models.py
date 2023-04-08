from django.db import models
from django.conf import settings

models_list = [
    ("Decision Tree Classifier"         , "Decision Tree Classifier"),
    ("K-Nearest Neighbors Classifier"   , "K-Nearest Neighbors Classifier"),
    ("Logistic Regression"              , "Logistic Regression"),
    ("Gaussian Naive Bayes Classifier"  , "Gaussian Naive Bayes Classifier"),
    ("Random Forest Classifier"         , "Random Forest Classifier"),
    ("Support Vector Machine"           , "Support Vector Machine"),
]

class Dataset(models.Model):
    """
        Dataset Model schema

        columns : 
            name : str
            path : str
            features : json
            targets  : json
    """
    name        = models.CharField(max_length = 30, unique = True, blank = False)
    path        = models.FileField(upload_to = "datasets")
    features    = models.JSONField(default = dict)
    targets     = models.JSONField(default = dict)

    def __str__(self):
        return f"{self.name} dataset {self.id}"

class ModelFile(models.Model):
    """ 
        ModelFile Schema

        model_name : str
        dataset_id : int
        model_obj  : str path of saved model
    """
    model_name  = models.CharField(
                    choices = models_list,
                    default = models_list[1][1],
                    max_length = 50,
                    null = False
                )
    dataset     = models.ForeignKey(Dataset, on_delete = models.CASCADE)
    model_obj   = models.FileField(upload_to = settings.MODEL_PATH_FIELD_DIRECTORY, null= True)
    # author      = models.CharField(max_length = 30)
    features    = models.JSONField(default = dict)
    targets     = models.JSONField(default = dict)

    def __str__(self):
        return f"{self.model_name} trained on {self.dataset}"

