from django.urls import path, include

from .views import *

urlpatterns = [
    path('', apiOverview, name = "documentation"),
    path('docs/', apiOverview, name = "documentation"),
    
    path('datasets/', DatasetView.as_view(), name = "datasets"),
    path('datasets/<int:pk>', DatasetDetailView.as_view(), name = "dataset detail"),
    
    path('supported-models/', SupportedModelsView.as_view(), name = "supported models"),

    path('models/', ModelFileView.as_view(), name = "models"),
    path('models/<int:pk>', ModelFileDetailView.as_view(), name = "model detail"),

    path('analyze/', ModelResponseView.as_view(), name = "analyze"),
]
