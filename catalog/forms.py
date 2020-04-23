from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Question


class QuestionForm(forms.Form):
    header = forms.CharField(label="Title")
    body_quest = forms.CharField(label="Text", widget=forms.Textarea(attrs={'rows':'3'}))
    tags = forms.CharField(label="Tags", required=False)

    def clean_header(self):
        header = self.cleaned_data['header']
        if Question.objects.filter(header=header).exists():
            print("kek")
            raise forms.ValidationError('This question already exist')
        return header


    def clean_body_quest(self):
        body_quest = self.cleaned_data['body_quest']
        return body_quest

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            tags = tags.split()
        return tags


class AnswerForm(forms.Form):
    body_answer = forms.CharField(label='Your anwer', widget=forms.Textarea(attrs={'rows':'3'}))

    def clean_body_answer(self):
        body_answer = self.cleaned_data['body_answer']
        return body_answer