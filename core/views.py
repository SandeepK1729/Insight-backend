from django.shortcuts   import render
from django.http        import JsonResponse

from rest_framework.decorators  import api_view
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework             import viewsets

from .serializers   import DatasetSerializer, ModelFileSerializer
from .models        import Dataset, ModelFile
from .helper        import get_trained_model, give_analysis_report

from django.core.files.base         import File, ContentFile
from django.utils.decorators        import method_decorator
from django.views.decorators.cache  import cache_page
from django.core.cache              import cache

@cache_page(60 * 60 * 30)
@api_view(['GET'])
def apiOverview(request):
    """
        List of API routes
    """
    host = request.get_host()
    return Response({
        'datasets'          : f"http://{host}/api/datasets",
        'dataset detail'    : f"http://{host}/api/datasets/pk:int",
        
        'models'            : f"http://{host}/api/models",
        'model detail'      : f"http://{host}/api/models/pk:int",
        'supported models'  : f"http://{host}/api/supported-models/",

        'analysis'           : f"http://{host}/api/analyze",
        
    })

class DatasetView(APIView):
    """ 
        List of all Datasets available, and upload a dataset
    """
    @method_decorator(cache_page(60))
    def get(self, request):
        """Get all datasets

        Args:
            request (client request): contains client data

        Returns:
            JSON: list of all datasets
        """
        try:
            res = DatasetSerializer(
                    Dataset.objects.all(),
                    many = True
                ).data
        except Exception as e:
            res = f"Unable to load datasets, beacuase {e}"
        
        return Response(res)

    def post(self, request):
        """Upload a dataset

        Args:
            request (client request): contains client data

        Returns:
            JSON: message about transaction
        """
        try:
            name        = request.data.get('name')
            features    = request.data.get('features')
            targets     = request.data.get('targets')
            path        = request.data.get('path')

            if Dataset.objects.filter(name = name).count() > 0:
                return Response("Unable to upload dataset, because name already exist")
            
            dataset     = Dataset(
                            name        = name,
                            features    = features,
                            targets     = targets,
                            path        = path
                        )
            dataset.save()
            res = "Dataset uploaded successfully"

        except Exception as e:
            res = f"Unable to upload dataset, because {e}"
        
        return Response(res)

class DatasetDetailView(APIView):
    """
        Perform put, delete, update operations on particular dataset 
    """
    def get(self, request, pk):
        """Give Detailed view of particular dataset based on ID

        Args:
            request (client request): contains data from client
            pk (int): primary key or id of dataset

        Returns:
            JSON: returns view of dataset in JSON i.e, Java Script Object Notation format
        """
        try:
            res = DatasetSerializer(
                    Dataset.objects.get(id = pk)
                ).data
        except Exception as e:
            res = f"Unable to load dataset details, beacuase {e}"

        return Response(res)

    def delete(self, request, pk):
        """delete a particular dataset

        Args:
            request (client request): contains client info
            pk (int): primary key of dataset

        Returns:
            JSON: message about transaction
        """
        try:
            dataset = Dataset.objects.get(id = pk)
            dataset.delete()

            res = "Dataset deleted Succefully"
        except Exception as e:
            res = f"Unable to delete dataset, because {e}"
        
        return Response(res)

    def put(self, request, pk):
        """updates the specific dataset, if exist
           creates new, if not exit

        Args:
            request (client request): contains client data
            pk (int): primary key of dataset

        Returns:
            JSON: acknowledgement message
        """
        res = ""
        try:
            dataset = Dataset.objects.filter(id = pk)
            
            serializer = DatasetSerializer(dataset.first(), data = request.data)

            if serializer.is_valid():
                serializer.save()
                
                res = "Dataset updated successfully"
            else:
                res = "Unable to update dataset"
                
        except Exception as e:
            res = f"Unable to update dataset, because {e}"
    
        return Response(res)

    def patch(self, request, pk):
        """updates the specific dataset

        Args:
            request (client request): contains client data
            pk (int): primary key of dataset

        Returns:
            JSON: acknowledgement message
        """
        res = ""
        try:
            dataset = Dataset.objects.get(id = pk)
            serializer = DatasetSerializer(dataset, data = request.data, partial = True)

            if serializer.is_valid():
                serializer.save()
                
                res = "Dataset updated successfully"
            else:
                res = "Unable to update dataset"

        except Exception as e:
            res = f"Unable to update dataset, because {e}"
    
        return Response(res)

class SupportedModelsView(APIView):
    """
        List of all supported models
    """
    def get(self, request):
        """invokes when get request

        Args:
            request (user request): contains all data of client

        Returns:
            Response: list of all models
        """
        from .models import models_list

        res = [{"id": idx, "name": val[0]} for idx, val in enumerate(models_list)]
        return Response(res)

class ModelFileView(APIView):
    """
        List of all Models, or create a model and save into file
    """
    @method_decorator(cache_page(60))
    def get(self, request):
        """invokes when get request

        Args:
            request (user request): contains all data of client

        Returns:
            Response: list of all models
        """
        return Response(
            ModelFileSerializer(
                ModelFile.objects.all(),
                many = True
            ).data
        )
    
    def post(self, request):
        """invokes post request called used to create model

        Args:
            request (user request): contains client info

        Returns:
            Response: answer about creation of model
        """
        try:
            model_name  = request.data.get('model_name')
            dataset_id  = request.data.get('dataset_id')
            dataset     = Dataset.objects.get(id = dataset_id)

            if ModelFile.objects.filter(model_name = model_name, dataset = dataset).count() > 0:
                return Response("Model already exist")
            
            modelFileRecord = ModelFile(
                                model_name = model_name,
                                dataset = dataset,
                                
                            )
            
            modelFileRecord.model_obj.save(
                f"{model_name} trained on {dataset.name} dataset - {dataset_id}.pkl",
                ContentFile(
                    get_trained_model(
                        model_name,
                        dataset_id,
                        request.data.get('knn_val', 0),
                    )
                )
            )

            modelFileRecord.save()

            response = "Successfully added dataset"
        except Exception as e:
            response = f"Unable to add dataset, due to Exception {e}"
        
        return Response(response)       

class ModelFileDetailView(APIView):
    """
        Get details of particular model
    """
    def get(self, request, pk):
        """invokes for particular model

        Args:
            request (client request): contains client info
            pk (int): id of model

        Returns:
            JSON: model info
        """
        try:
            model = ModelFile.objects.get(id = pk)
            res = ModelFileSerializer(model).data
        except Exception as e:
            res = f"Unable to find model, because {e}"

        return Response(res)
    
    def delete(self, request, pk):
        """delete a particular model

        Args:
            request (client request): contains client info
            pk (int): primary key of model

        Returns:
            JSON: message about transaction
        """
        try:
            model = ModelFile.objects.get(id = pk)
            model.delete()

            res = "Model deleted Succefully"
        except Exception as e:
            res = f"Unable to delete model, because {e}"
        
        return Response(res)

    def put(self, request, pk):
        """updates the specific model, if exist
           creates new, if not exit

        Args:
            request (client request): contains client data
            pk (int): primary key of model

        Returns:
            JSON: acknowledgement message
        """
        res = ""
        try:
            model = ModelFile.objects.filter(id = pk)
            
            if model.count() == 0:
                ModelFileView().post(request)
                return Response("Model created successfully")

            model = model.first()
            model_name  = request.data.get('model_name')
            dataset_id  = request.data.get('dataset_id')
            dataset     = Dataset.objects.get(id = dataset_id)

            existing_model = ModelFile.objects.filter(model_name = model_name, dataset = dataset)
            if existing_model.count() > 0:
                ModelFileDetailView().delete(request, pk)
                return Response(f"Model with updated data, already exist with id: {existing_model.first().id}")

            if ModelFile.objects.filter(model_name = model_name, dataset = dataset).count() > 0:
                return Response("Model updated successfully")

            model.model_name = model_name
            model.dataset = dataset

            model.model_obj.save(
                f"{model_name} trained on {dataset.name} dataset - {dataset_id}.pkl",
                ContentFile(
                    get_trained_model(
                        model_name,
                        dataset_id,
                        request.data.get('knn_val', 0),
                    )
                )
            )

            model.save()

            res = "Model updated successfully"
        except Exception as e:
            res = f"Unable to update model, because {e}"
    
        return Response(res)

    def patch(self, request, pk):
        """updates the specific model

        Args:
            request (client request): contains client data
            pk (int): primary key of model

        Returns:
            JSON: acknowledgement message
        """
        res = {}
        try:
            model = ModelFile.objects.get(id = pk)

            model_name  = request.data.get('model_name', model.model_name)
            dataset_id  = request.data.get('dataset_id', model.dataset.id)

            dataset     = Dataset.objects.get(id = dataset_id)

            existing_model = ModelFile.objects.filter(model_name = model_name, dataset = dataset)
            if existing_model.count() > 0:
                ModelFileDetailView().delete(request, pk)
                return Response(f"Model with updated data, already exist with id: {existing_model.first().id}")

            model.model_name = model_name
            model.dataset = dataset

            model.model_obj.save(
                f"{model_name} trained on {dataset.name} dataset - {dataset_id}.pkl",
                ContentFile(
                    get_trained_model(
                        model_name,
                        dataset_id,
                        request.data.get('knn_val', 0),
                    )
                )
            )

            model.save()

            res = "Model updated successfully..."
        except Exception as e:
            res = f"Unable to update model, because {e}"
    
        return Response(res)

class ModelResponseView(APIView):
    """
        Get prediction from saved machine learning model
    """
    def get(self, request):
        """Prediction request if model exist

        Args:
            request (client request): client request info
                - model_name : str
                - dataset_id : int

        Returns:
            JSON: list of saved models
        """
        try:
            model_name  = request.data.get('model_name', None)
            dataset_id  = request.data.get('dataset_id')
            dataset     = Dataset.objects.get(id = dataset_id)
            
            modelFileRecord = ModelFile.objects.get(model_name = model_name, dataset = dataset)

            res = {
                "model_name"    : modelFileRecord.model_name,
                "dataset"       : modelFileRecord.dataset.name,
                "model_path"    : modelFileRecord.model_obj.url,
                **give_analyze_report(
                    modelFileRecord.model_obj.open('rb'), 
                    dataset_id
                )
            }
                
        except Exception as e:
            return Response(f"Unable to find model, due to Exception {e}")   

        return Response(res)

    def post(self, request):
        """Prediction request if model exist
        else creates model and gives prediction

        Args:
            request (client request): client request info
                - model_name : str
                - dataset_id : int

        Returns:
            JSON: list of saved models
        """
        try:
            model_name  = request.data.get('model_name', None)
            dataset_id  = request.data.get('dataset_id')
            dataset     = Dataset.objects.get(id = dataset_id)
            
        
            if ModelFile.objects.filter(model_name = model_name, dataset = dataset).count() == 0:
                ModelFileView().post(request)
            
            modelFileRecord = ModelFile.objects.get(model_name = model_name, dataset = dataset)

            res = {
                "model_name"    : modelFileRecord.model_name,
                "dataset"       : modelFileRecord.dataset.name,
                "model_path"    : modelFileRecord.model_obj.url,
                **give_analysis_report(
                    modelFileRecord.model_obj.open('rb'), 
                    dataset_id
                )
            }
                
        except Exception as e:
            return Response(f"Unable to find model, due to Exception {e}")   

        return Response(res)
