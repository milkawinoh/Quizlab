
from django.urls import include, path
from .views import QuizDeleteView, QuizUpdateView, login_view, register, quiz_list, take_quiz, quiz_result, create_quiz, add_question, quiz_detail, QuestionUpdateView, my_quizzes, user_quiz_results



urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', take_quiz, name='take_quiz'),
    path('quiz/<int:result_id>/result/', quiz_result, name='quiz_result'),
    path('quiz/create/', create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/add-questions/', add_question, name='add_question'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/edit-question/', QuestionUpdateView.as_view(), name='edit_question'),
    #path('quiz/<int:pk>/delete/', QuestionDeleteView.as_view(), name='delete_question'),
    path('login/', login_view, name='login'),
    path('signup/', register, name='signup'),
    path('my_quizzes/', my_quizzes, name='my_quizzes'),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='delete_quiz'),
    path('quiz/<int:pk>/edit/', QuizUpdateView.as_view(), name='edit_quiz'),
    path('my_results/', user_quiz_results, name='user_quiz_results'),

]

