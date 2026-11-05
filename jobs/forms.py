
from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': (
                    'Explain why you are interested in this job '
                    'and what skills you can bring...'
                ),
            }),
        }
        labels = {
            'cover_letter': 'Your cover letter',
        }
