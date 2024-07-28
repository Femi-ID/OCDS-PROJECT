from django.urls import path
from . import views

# router = routers.DefaultRouter()

urlpatterns = [
    path('<str:communityId>/', views.QuestionListByCommunity.as_view(), name='question_list'),
] 
# + router.urls
 