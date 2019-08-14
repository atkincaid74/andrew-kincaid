from django.urls import include, path
from .views import CreateNewUserView, GetUserInfo
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('api/create_user/', CreateNewUserView.as_view()),
    path('api/auth/', obtain_jwt_token),
    path('api/get_user_info/', GetUserInfo.as_view())
]
