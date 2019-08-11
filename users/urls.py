from django.urls import include, path
from .views import CreateNewUserView

urlpatterns = [
    path('api/create_user/', CreateNewUserView.as_view()),
]
