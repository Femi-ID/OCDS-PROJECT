from django.urls import path
from . import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('<str:community_id>/', views.ListQuestionByCommunity.as_view(), name='question_list'),
] 
 