from django import forms
from .models import Quiz, Question, Choice
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {
            'text': 'Write Question',
        }
        error_messages = {
            'text': {
                'required': 'Question should not be blank',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.pop('placeholder', None)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        labels = {
            'text': 'Add Choice',
            'is_correct': 'Is Correct',
        }
        error_messages = {
            'text': {
                'required': 'Choice should not be blank',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.pop('placeholder', None)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

ChoiceFormSet = forms.modelformset_factory(Choice, form=ChoiceForm, extra=1)

class Quizform(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_public']


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
