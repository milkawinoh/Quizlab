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


class TakeQuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        quiz = kwargs.pop('quiz')
        super().__init__(*args, **kwargs)
        for question in quiz.questions.all():
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=True
            )
