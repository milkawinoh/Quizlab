from django.urls import path
from .views import register, login_view
from django.urls import path
from .views import (
    create_quiz, add_questions, add_choices, quiz_detail, take_quiz, quiz_result, quiz_list,
    QuizUpdateView, QuizDeleteView, QuestionUpdateView, QuestionDeleteView
)

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/result/', quiz_result, name='quiz_result'),
    path('quiz/create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-questions/', add_questions, name='add_questions'),
    path('question/<int:question_id>/add-choices/', add_choices, name='add_choices'),
    path('quiz/<int:pk>/edit/', QuizUpdateView.as_view(), name='edit_quiz'),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='delete_quiz'),
    path('question/<int:pk>/edit/', QuestionUpdateView.as_view(), name='edit_question'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete_question'),
     path('login/', login_view, name='login'),
    path('signup/', register, name='signup'),
]
