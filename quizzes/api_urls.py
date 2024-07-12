from django.urls import path, include
from rest_framework.routers import DefaultRouter

from quizzes.api_views import ChoiceViewSet, QuestionViewSet, QuizViewSet


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]