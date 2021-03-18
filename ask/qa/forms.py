from django import forms
from .models import Question, Answer
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        question = Question(self.cleaned_data['title'], self.cleaned_data['text'], author=self._user)
        question.save()

        return question


class AnswerForm(forms.Form):

    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(required=False)

    def save(self):
        question_obj = Question.objects.get(pk=self.cleaned_data['question'])
        answer = Answer(text=self.cleaned_data['text'], question=question_obj, author=self._user)
        answer.save()

        return answer


class SignupForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
