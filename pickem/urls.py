from django.urls import include, path
from .views import GetGamesView, GetPicksView, UpdateWinnersView, GetPickSummaryView

urlpatterns = [
    path('api/get_games/', GetGamesView.as_view()),
    path('api/get_picks/', GetPicksView.as_view()),
    path('api/update_results/', UpdateWinnersView.as_view()),
    path('api/get_pick_summary/', GetPickSummaryView.as_view()),
]
