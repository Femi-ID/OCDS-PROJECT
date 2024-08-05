from django.urls import path
from .views import CreateAdminUser

urlpatterns = [
    path('admin-signup/', CreateAdminUser.as_view(), name='sign-up'),
]