from django.urls import path
from . import views

urlpatterns = [
    path('community/all/', views.ListCommunity.as_view(), name='list_communities'),
    path('', views.ListCreateInformation.as_view(), name='list_create_information'),
]