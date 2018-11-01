from django.urls import path
from .views import ArticlesListCreateAPIView

urlpatterns = [
    # GET/POST api/articles
    path('', ArticlesListCreateAPIView.as_view(), name='list_create'),
]
