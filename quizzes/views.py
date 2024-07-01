# quizzes/views.py
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import ChoiceForm, QuestionForm, Quizform, TakeQuizForm
from .models import Quiz, Question, Choice, Result
from django import forms


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quiz_list')
        else:
            return render(request, 'templates/registration/login.html', {'error': 'Invalid username or password'})
    return render(request, 'templates/registration/login.html')


@login_required
def create_quiz(request):
    if request.method == 'POST':
        quiz_form = Quizform(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        quiz_form = Quizform()
    return render(request, 'quizzes/create_quiz.html', {'quiz_form': quiz_form})

@login_required
def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form .is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_choice', question_id = question.id)
    else:
        question_form = QuestionForm()
        return render(request, 'quizzes/add_questions.html', {'quiz': quiz, 'question_form': question_form})

@login_required
def add_choices(request, question_id):
    question = Question.objects.get(id=question_id)
    ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, extra=3)
    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            return redirect('add_questions', quiz_id=question.quiz.id)
    else:
        formset = ChoiceFormSet(instance=question)
    return render(request, 'quizzes/add_choices.html', {'question': question, 'formset': formset})


@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = TakeQuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = 0
            for question in quiz.questions.all():
                selected_choice_id = int(form.cleaned_data[f'question_{question.id}'])
                selected_choice = Choice.objects.get(id=selected_choice_id)
                if selected_choice.is_correct:
                    score += 1
            result = Result.objects.create(
                quiz=quiz,
                user=request.user,
                score=score
            )
            return redirect('quiz_result', result_id=result.id)
    else:
        form = TakeQuizForm(quiz=quiz)
    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})

@login_required
def quiz_result(request, result_id):
    result = Result.objects.get(id=result_id)
    return render(request, 'quiz_result.html', {'result': result})
