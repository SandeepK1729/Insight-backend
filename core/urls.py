from django.urls import path, include

from .views import *

urlpatterns = [
    path('', apiOverview, name = "documentation"),
    path('docs', apiOverview, name = "documentation"),
]

# Auth URL patterns
urlpatterns += [
    path('api/login', UserLogin.as_view(), name = "login"),
    path('api/logout', UserLogout.as_view(), name = "logout"),
    path('api/register', UserRegister.as_view(), name = "register"),
    path('api/user', UserView.as_view(), name = "user detail"),
    path('api/user/api_key', UserAPIKeyGenerate.as_view(), name = "user api"),
]

# API URL patterns
urlpatterns += [
    path('api/supported-models', SupportedModelsView.as_view(), name = "supported models"),

    path('api/models', ModelFileView.as_view(), name = "models"),
    path('api/model/<str:project_name>', ModelFileDetailView.as_view(), name = "model detail"),

    path('api/public-models', publicModels, name = "public models"),
    path('<str:project_name>', ProjectView.as_view(), name = "project"),

]
