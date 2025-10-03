from django import forms
from .models import UntimedUserResponse

class UntimedQuizForm(forms.ModelForm):
    class Meta:
        model = UntimedUserResponse
        fields = ['user_answer']
        widgets = {
            'user_answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your answer here...'
            }),
        }
