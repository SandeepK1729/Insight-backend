from django.shortcuts   import render, get_object_or_404
from django.http        import JsonResponse
from json               import loads

from rest_framework.decorators      import api_view
from rest_framework.response        import Response
from rest_framework                 import status, permissions
from rest_framework.views           import APIView
from rest_framework                 import viewsets
from rest_framework.authentication  import SessionAuthentication, BasicAuthentication

from .authenicators import CsrfExemptSessionAuthentication
from .serializers   import ModelFileSerializer, UserSerializer
from .models        import ModelFile, User
from .helper        import *

from django.utils.decorators        import method_decorator
from django.views.decorators.cache  import cache_page
from django.views.decorators.csrf   import csrf_exempt
from django.core.cache              import cache
from django.core.files.storage      import FileSystemStorage

from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.models     import AnonymousUser

@cache_page(60 * 60 * 30)
@api_view(['GET'])
def apiOverview(request):
    """
        List of API routes
    """
    host = request.get_host()
    return Response({
        'models'            : f"http://{host}/api/models",
        'model detail'      : f"http://{host}/api/model/<str:project_name>",
        'supported models'  : f"http://{host}/api/supported-models",
        'public models'  : f"http://{host}/api/public-models",
        
        'project'           : f"http://{host}/api/project/<str:project_name>",
        
    }, status = status.HTTP_200_OK)

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
        return Response(res, status = status.HTTP_200_OK)

@api_view(["GET", "POST"])
def publicModels(request):
    """List of public models

    Returns:
        JSON : public models list
    """
    public_models = ModelFile.objects.filter(is_public = True)
    res = ModelFileSerializer(public_models, many = True).data

    return Response(res, status.HTTP_200_OK)


# user auth views
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        """Create new User"""
        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            if User.objects.filter(username = request.data.get("username")).count() != 0:
                return Response(status = status.HTTP_400_BAD_REQUEST)
                
            user = serializer.create_user(data = request.data)
        
            return Response(data = UserSerializer(instance = user).data, status = status.HTTP_201_CREATED)

        return Response(status = status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes      = (permissions.AllowAny, )
    authentication_classes  = (CsrfExemptSessionAuthentication, )

    def post(self, request):
        """Login user"""
        username = request.data.get("username")
        password = request.data.get("password")

        user     = authenticate(username = username, password = password)

        if user is None:
            return Response(status = status.HTTP_404_NOT_FOUND)

        login(request, user)

        return Response(UserSerializer(user).data, status = status.HTTP_200_OK)

class UserLogout(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (CsrfExemptSessionAuthentication, )

    # @csrf_exempt 
    def post(self, request):
        """Logouts user"""
        logout(request)
        return Response(status = status.HTTP_204_NO_CONTENT)

class UserView(APIView):
    authentication_classes  = (CsrfExemptSessionAuthentication, )
    permission_classes      = (permissions.IsAuthenticated, )

    def get(self, request):
        """Get user info"""
        return Response(UserSerializer(request.user).data, status = status.HTTP_200_OK)

    def put(self, request):
        """Update user info"""
        serializer = UserSerializer(instance = request.user, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete user"""
        request.user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class UserAPIKeyGenerate(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def get(self, request):
        return Response({"API Key" : request.user.api_key}, status.HTTP_200_OK)
    
    def post(self, request):
        request.user.generate_api_key()
        return Response({"API Key" : request.user.api_key}, status.HTTP_200_OK)

class ModelFileView(APIView):
    """
        List of all Models, or create a model and save into file
    """
    permission_classes      = (permissions.IsAuthenticated, )
    authentication_classes  = (CsrfExemptSessionAuthentication, )

    def get(self, request):
        """invokes when get request

        Args:
            request (user request): contains all data of client

        Returns:
            Response: list of all models
        """
        try:
            res = ModelFileSerializer(request.user.models.all(), many = True).data
            
            return Response(res, status.HTTP_200_OK)
        except Exception as e:
            res = f"Unable to load models, beacuase {e}"

        return Response(res, status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def post(self, request):
        """invokes post request called used to create model

        Args:
            request (user request): contains client info

        Returns:
            Response: answer about creation of model
        """
        try:
            project_name = request.data.get('project_name')
            model_name  = request.data.get('model_name')
            user = request.user
            
            modelFileRecord = ModelFile.objects.create(
                                project_name = project_name,
                                model_name = model_name,
                                created_by = user,
                                
                            )

            modelFileRecord.add_model_obj(request.data, user)

            response = ModelFileSerializer(modelFileRecord).data
            return Response(response, status.HTTP_201_CREATED)

        except Exception as e:
            response = f"{model_name} Unable to train model, due to Exception {e} "
        
        return Response(response, status.HTTP_503_SERVICE_UNAVAILABLE)       

class ModelFileDetailView(APIView):
    # how to get model details for non logged in user and edit access to only owner
    permission_classes      = (permissions.AllowAny, )
    authentication_classes  = (CsrfExemptSessionAuthentication, )

    """
        Get details of particular model
    """
    def get(self, request, project_name):
        """invokes for particular model

        Args:
            request (client request): contains client info
            project_name (int): name of the project

        Returns:
            JSON: model info
        """
        try:
            model = ModelFile.objects.get(project_name = project_name)
            
            if model.created_by != request.user and model.is_public == False:
                # no permission to view
                return Response("You don't have permission to view this model", status.HTTP_401_UNAUTHORIZED)

            res = ModelFileSerializer(model).data

            return Response(res, status.HTTP_200_OK)
        except Exception as e:
            res = f"Unable to find model, because {e}"

        return Response(res, status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_name):
        """delete a particular model

        Args:
            request (client request): contains client info
            project_name (str): primary key of model

        Returns:
            JSON: message about transaction
        """
        try:
            model = ModelFile.objects.get(project_name = project_name)

            if model.created_by != request.user:
                # no permission to delete
                return Response("You don't have permission to delete this model", status.HTTP_401_UNAUTHORIZED)

            model.delete()

            res = ModelFileSerializer(model).data
            res = f"Model {project_name} deleted successfully"
            return Response(res, status.HTTP_202_ACCEPTED)
        except Exception as e:
            res = f"Unable to delete model, because {e}"
        
        return Response(res, status.HTTP_404_NOT_FOUND)

    def put(self, request, project_name):
        """used to train the model

        Args:
            project_name (str): name of the project

        Returns:
            response: message about training of model
        """
        try:
            modelFileRecord   = ModelFile.objects.get(project_name = project_name)
            modelFileRecord.train(
                train_set = get_dataset(request.data)
            )

            if modelFileRecord.created_by != request.user:
                # no permission to train
                return Response("You don't have permission to train this model", status.HTTP_401_UNAUTHORIZED)

            # implement result generation of train data for user satifiscation
            # ....
            
            return Response("Model trained successfully", status.HTTP_202_ACCEPTED)
        except Exception as e:
            res = f"Unable to update model, because {e}"
    
        return Response(res, status = status.HTTP_204_NO_CONTENT)

    def patch(self, request, project_name):
        """updates the specific model

        Args:
            request (client request): contains client data
            pk (int): primary key of model

        Returns:
            JSON: acknowledgement message
        """
        try:
            modelFileRecord = get_object_or_404(ModelFile.objects.filter(project_name = project_name))
            
            if modelFileRecord.created_by != request.user:
                # no permission to update
                return Response("You don't have permission to update this model", status.HTTP_401_UNAUTHORIZED)

            modelFileRecord.model_name = request.data.get('model_name', modelFileRecord.model_name)
            modelFileRecord.is_public  = request.data.get('is_public', False)

            user = User.objects.get(username = 'admin')

            modelFileRecord = modelFileRecord.add_model_obj(request.data, user)

            res = "Model updated successfully..."
        except Exception as e:
            res = f"Unable to update model, because {e}"
    
        return Response(res)

    def post(self, request, project_name):
        """prediction of target for requested dataset if model exist

        Args:
            project_name (str): name of the project

        Returns:
            JSON: prediction result
        """
        try:
            if request.user != AnonymousUser():
                user = request.user
            else:
                if request.data.get("api_key") is None:
                    # no permission to update
                    return Response("You don't have permission to prediction from this model", status.HTTP_401_UNAUTHORIZED)
                
                api_key_user = User.objects.get(api_key = request.data.get("api_key"))

                if api_key_user is None:
                    # no permission to update
                    return Response("You don't have permission to prediction from this model", status.HTTP_401_UNAUTHORIZED)
                
                user = api_key_user

            modelFileRecord = get_object_or_404(ModelFile.objects.filter(project_name = project_name))

            prediction = modelFileRecord.predict(
                data = request.data
            )
            res = {
                **ModelFileSerializer(modelFileRecord).data,
                "prediction" : prediction,
                "user" : user.username
            }

            return Response(res, status.HTTP_200_OK)
        except Exception as e:
            res = f"Unable to load models, beacuase {e}"

        return Response(res, status.HTTP_503_SERVICE_UNAVAILABLE)

class ProjectView(APIView):
    pass


