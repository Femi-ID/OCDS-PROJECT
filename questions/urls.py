from django.urls import path
from . import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('<str:community_id>/', views.ListQuestionByCommunity.as_view(), name='question_list'),
    path('details/<str:question_id>/', views.QuestionDetails.as_view(), name='question_detail'),
] 
 