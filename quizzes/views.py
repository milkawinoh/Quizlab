from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import ChoiceForm, ChoiceFormSet, QuestionForm, Quizform, TakeQuizForm
from .models import Quiz, Question, Choice, Result, UserAnswer
from django.views.generic.edit import DeleteView, UpdateView

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
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()

            valid_choices = True
            for form in formset.forms:
                if not form.cleaned_data.get('text'):
                    valid_choices = False
                    form.add_error('text', 'Choice should not be blank.')

            if valid_choices:
                choices = formset.save(commit=False)
                for choice in choices:
                    choice.question = question
                    choice.save()

                if 'action' in request.POST:
                    if request.POST['action'] == 'add_another':
                        messages.success(request, "Question and choices saved. Add another question.")
                        return redirect('add_question', quiz_id=quiz_id)
                    elif request.POST['action'] == 'save_exit':
                        messages.success(request, "Question and choices saved.")
                        return redirect('quiz_list')
            else:
                question.delete()  # Delete the question if choices are invalid
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet(queryset=Choice.objects.none())

    return render(request, 'quizzes/add_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'formset': formset
    })

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = TakeQuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            score = 0
            user_answers = []

            for question in quiz.questions.all():
                selected_choice_id = int(form.cleaned_data[f'question_{question.id}'])
                selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                user_answers.append(UserAnswer(user=request.user, quiz=quiz, question=question, choice=selected_choice))

                if selected_choice.is_correct:
                    score += 1

            UserAnswer.objects.bulk_create(user_answers)

            result = Result.objects.create(
                quiz=quiz,
                user=request.user,
                score=score
            )
            return redirect('quiz_result', result_id=result.id)
    else:
        form = TakeQuizForm(quiz=quiz)
    
    return render(request, 'quizzes/take_quiz.html', {'quiz': quiz, 'form': form})

@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    user_answers = UserAnswer.objects.filter(quiz=result.quiz, user=result.user)
    
    results = []
    score = result.score
    total = result.quiz.questions.count()
    
    for user_answer in user_answers:
        correct_choice = user_answer.question.choices.filter(is_correct=True).first()
        correct_answer_text = correct_choice.text if correct_choice else "No correct answer provided"

        results.append({
            'question': user_answer.question,
            'user_answer': user_answer.choice.text,
            'correct_answer': correct_answer_text,
            'is_correct': user_answer.choice.is_correct
        })
    
    context = {
        'quiz': result.quiz,
        'results': results,
        'score': score,
        'total': total
    }
    return render(request, 'quizzes/quiz_result.html', context)

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.filter(created_by=request.user) | Quiz.objects.filter(is_public=True)
    return render(request, 'quizzes/quiz_list.html', {'quizzes': quizzes})

@login_required
def my_quizzes(request):
    user_quizzes = Quiz.objects.filter(created_by=request.user)
    return render(request, 'quizzes/my_quizzes.html', {'quizzes': user_quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['text']
    template_name = 'quizzes/edit_question.html'

    def get_success_url(self):
        return reverse_lazy('quiz_detail', args=[self.object.quiz.id])

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'quizzes/delete_question.html'

    def get_success_url(self):
        return reverse_lazy('quiz_detail', args=[self.object.quiz.id])
class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'quizzes/delete_quiz.html'

    def get_success_url(self):
        return reverse_lazy('quiz_list')

class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = Quizform 
    template_name = 'quizzes/edit_quiz.html'

    def get_success_url(self):
        return reverse_lazy('my_quizzes')

@login_required
def user_quiz_results(request):
    results = Result.objects.filter(user=request.user)
    return render(request, 'quizzes/user_quiz_results.html', {'results': results})