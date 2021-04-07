from django.urls import include, path
from .views import (CreateNewUserView, GetUserInfo, AllowedObtainJSONWebToken, 
                    AllowedRefreshJSONWebToken, AllowedVerifyJSONWebToken,
                    AddNewValidEmail)
from rest_framework.authtoken import views

urlpatterns = [
    path('api/login/', views.obtain_auth_token),
    path('api/create_user/', CreateNewUserView.as_view()),
    path('api/get_user_info/', GetUserInfo.as_view()),
    path('api/submit_email/', AddNewValidEmail.as_view()),
]
