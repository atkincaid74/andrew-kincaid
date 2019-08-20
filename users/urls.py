from django.urls import include, path
from .views import (CreateNewUserView, GetUserInfo, AllowedObtainJSONWebToken, 
                    AllowedRefreshJSONWebToken, AllowedVerifyJSONWebToken)

urlpatterns = [
    path('api/create_user/', CreateNewUserView.as_view()),
    path('api/auth/', AllowedObtainJSONWebToken.as_view()),
    # path('api/auth/refresh/', AllowedRefreshJSONWebToken.as_view()),
    # path('api/auth/verify/', AllowedVerifyJSONWebToken.as_view()),
    path('api/get_user_info/', GetUserInfo.as_view()),
]
