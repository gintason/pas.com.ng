from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Question
 
class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password'] 
 
class addQuestionform(ModelForm):
    class Meta:
        model=Question
        fields="__all__"

class EssayAnswerForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput())
    user_answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your answer here...'}),
        required=True
    )

