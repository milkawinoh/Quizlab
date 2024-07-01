from django import forms
from .models import Quiz, Question, Choice

class Quizform(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_public']
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']