from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register(r'courses', CourseViewSet, 'course')
router.register(r'tees', TeeViewSet, 'tee')
router.register(r'scorecards', ScorecardViewSet, 'scorecard')
router.register(r'rounds', RoundViewSet, 'round')
urlpatterns = router.urls

urlpatterns += [
    path('api/handicap/', HandicapView.as_view()),
    path('api/handicap/serializer/<str:serializer_name>/',
         SerializerToForm.as_view())
]
