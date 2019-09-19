from django.urls import include, path
from .views import GetGamesView

urlpatterns = [
    path('api/get_games/', GetGamesView.as_view()),
]
