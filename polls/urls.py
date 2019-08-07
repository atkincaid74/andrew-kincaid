from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'polls', views.IndexView, 'polls')
# router.register(r'polls', views.DetailView, 'detail')
# router.register(r'polls', views.ResultsView, 'results')

app_name = 'polls'
urlpatterns = [
    path('api/', include(router.urls)),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
