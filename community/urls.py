from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCommunitiesInformation.as_view(), name='list_create_information'),
    path('community/all/', views.ListCommunity.as_view(), name='list_communities'),
    path('create-info/', views.CreateInformation.as_view(), name='create-info'),
    path('join-community/<str:community_id>/', views.JoinCommunity.as_view(), name='join-community'),
    path('<str:communityId>/create-message', views.RetrieveCreateMessages.as_view(), name='create_community_message'),
]
