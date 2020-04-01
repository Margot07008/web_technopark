from django import forms

class QuestionForm(forms.Form):
    header = forms.CharField(label="Title")
    body_quest = forms.CharField(label="Text", widget=forms.Textarea(attrs={'rows':'3'}))
    tags = forms.CharField(label="Tags", required=False)

class AnswerForm(forms.Form):
    body_answer = forms.CharField(label='Your anwer', widget=forms.Textarea(attrs={'rows':'3'}))