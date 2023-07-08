from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sklearn.model_selection    import train_test_split
from sklearn.metrics            import accuracy_score, confusion_matrix, precision_score, recall_score 
from sklearn.datasets           import *

from pickle                     import load, dumps

from django.conf                import settings

from pathlib                    import Path
from django.core.files.base     import File, ContentFile

import numpy    as np 
import pandas   as pd
import matplotlib.pyplot as plt
import io
from seaborn                    import heatmap



models_list = [
    ("Decision Tree Classifier"         , "Decision Tree Classifier"),
    ("K-Nearest Neighbors Classifier"   , "K-Nearest Neighbors Classifier"),
    ("Logistic Regression"              , "Logistic Regression"),
    ("Gaussian Naive Bayes Classifier"  , "Gaussian Naive Bayes Classifier"),
    ("Random Forest Classifier"         , "Random Forest Classifier"),
    ("Support Vector Machine"           , "Support Vector Machine"),
    ("Custom Model"                     , "Upload Model")
]

class User(AbstractUser):
    mobile_number   = models.CharField(
                        blank = False,
                        unique = True, 
                        max_length = 10,
                        help_text = "Enter 10 digit phone number only"
                    )
    dob         = models.DateField(
                    _("date of birth"),
                    null = True,
                    blank = True,
                    help_text="Please use the following format: <em>YYYY-MM-DD</em>."
                )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    api_key     = models.CharField(_("API key"), unique = True, null = True, max_length = 24)
    
    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

    def generate_api_key(self):
        timestamp = str(timezone.now())
        key = ""
        for c in timestamp:
            if c.isalnum():
                key += c
            
        key = key[:-4]
        key += self.username[:6] if len(self.username) > 6 else self.username.rjust(6, 's')
        
        self.api_key = key
        self.save()
    
    # def save(self, *args, **kwargs):
    #     self.api_key = generate_api_key()

    #     super(User, self).save(*args, **kwargs)

class ModelFile(models.Model):
    """Model File model Schema

    
        project_name(str) : name of the project
        model_name(str)   : name of the classifier used
        model_obj(file)   : file path of model
        created_by(user)  : created by user
        created_on(DateTime) : time model created
        last_trained_on : time model last trained
    """
    project_name = models.TextField(
                    unique = True,
                    blank = False,
                    max_length = 30,
                    db_index = True
                )
    model_name  = models.CharField(
                    choices = models_list,
                    default = models_list[1][1],
                    max_length = 50,
                    null = False
                )
    is_public   = models.BooleanField(verbose_name = "Is public model", default = False)
    model_obj   = models.FileField(upload_to = 'saved_models', null= True)
    created_by  = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "models")
    created_on  = models.DateTimeField(default = timezone.now)
    last_trained_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.project_name = '_'.join([word.strip() for word in self.project_name.split()])
        self.last_trained_on   = timezone.now()

        super(ModelFile, self).save(*args, **kwargs)    

    def delete(self, *args, **kwargs):
        if self.model_obj:
            self.model_obj.delete()

        super(ModelFile, self).delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.project_name} - {self.model_name} by {self.created_by}"

    def give_analysis_report(self, dataset):
        """gives the report of model on analysis of dataset

        Args:
            model_file_path (str): file path of the model
            dataset (file): dataset file

        Returns:
            dict: gives report of dictionary
        """
        
        X, y = get_dataset(dataset)
        
        model = load(self.model_obj.open('rb'))
        
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

    def add_model_obj(self, data, user):
        """adds model object to the modelFileRecord

        Args:
            data (dict): data of the model
            user (User): user who created the model
        """
        
        # delete existing model object file if exists
        if self.model_obj:
            self.model_obj.delete()

        file_name = f"{self.project_name} - {self.model_name} created by {user.username} .pkl"

        if self.model_name == "Custom Model":
            model_obj = data.get('model_obj')
            self.model_obj.save(
                file_name,
                model_obj
            )
        else:
            self.model_obj.save(
                file_name,
                ContentFile(
                    get_model(
                        self.model_name,
                        int(data.get('knn_val', '0')),
                    )
                )
            )

        self.save()

    def train(self, train_set):
        """trains the model

        Args:
            train_set (file): file of the dataset
        """
        model = load(self.model_obj.open('rb'))
        features, target = train_set

        model.fit(features, target)           # model training 

        trained_model = dumps(model)

        self.model_obj.delete()          # delete existing model
        self.model_obj.save(             # create new model
                f"{self.project_name} - {self.model_name} created by {self.created_by.username}.pkl",
                ContentFile( trained_model )
            )
        self.save()

    def get_data(self, data, is_predict = False):
        """
        get_data function

        Args:
            data (file): file object
            is_predict (bool, optional): is predict or not. Defaults to False.

        Returns:
            (pd.DataFrame, pd.DataFrame): tuple of features dataframe and target dataframe or series
        """
        data_type = data.get("data_type", "plain_text")

        if data_type == "plain_text":
            df_dict, i = {}, 0

            while str(i) in data:
                v = data.get(str(i))
                # if v.isnumeric():
                v = float(v)
                
                df_dict[i] = [v]
                i += 1

            df = pd.DataFrame(df_dict)

        elif data_type == "csv":
            df = pd.read_csv(io.StringIO(data.get('dataset').read().decode('utf-8')), delimiter = ",")

        if is_predict:
            return df

        target  = data.get('target', '').strip()
        features = [feature.strip() for feature in data.get('features').split(",")]

        y       = df[target]
        X       = df.drop(
                    target,
                    axis = 1
                )
        
        if features != ["*"]:
            X = X[features]

        return (X, y)

    def predict(self, data):
        """predicts the output of the data

        Args:
            data (dict): data to be predicted

        Returns:
            str: predicted output
        """
        dataset = self.get_data(data, is_predict = True)

        model = load(self.model_obj.open('rb'))

        X = dataset

        return model.predict(X)