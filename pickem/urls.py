from django.urls import include, path
from .views import GetGamesView, GetPicksView

urlpatterns = [
    path('api/get_games/', GetGamesView.as_view()),
    path('api/get_picks/', GetPicksView.as_view()),
]
