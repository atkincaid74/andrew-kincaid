from django.urls import path
from .views import PicksView, PicksWithScoresView, LeaderboardView, StatusView

urlpatterns = [
    path('api/picks/', PicksView.as_view()),
    path('api/picks_scores/', PicksWithScoresView.as_view()),
    path('api/leaderboard/', LeaderboardView.as_view()),
    path('api/status/', StatusView.as_view()),
]
