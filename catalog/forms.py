from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Question


class QuestionForm(forms.Form):
    header = forms.CharField(label="Title")
    body_quest = forms.CharField(label="Text", widget=forms.Textarea(attrs={'rows':'3'}))
    tags = forms.CharField(label="Tags", required=False)

    def clean_header(self):
        header = self.cleaned_data['header']
        try:
            Question.objects.get(header=header)
            raise ValidationError('This question already exist')
        except Exception as e:
            print(e)
            return header

    def clean_body_quest(self):
        body_quest = self.cleaned_data['body_quest']
        if not body_quest:
            raise ValidationError('Write the body of the question')
        return body_quest

    def clean_tags(self):
        tags = self.cleaned_data['tags'].split()
        return tags



        

class AnswerForm(forms.Form):
    body_answer = forms.CharField(label='Your anwer', widget=forms.Textarea(attrs={'rows':'3'}))