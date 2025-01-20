from django import forms
from .models import Caption

class CaptionForm(forms.ModelForm):
    PLATFORM_CHOICES = [
        ('General', 'General'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Pinterest', 'Pinterest'),
    ]
    
    NUMBER_CHOICES = [(i, str(i)) for i in range(1, 11)]
    
    platform = forms.ChoiceField(choices=PLATFORM_CHOICES)
    num_captions = forms.ChoiceField(choices=NUMBER_CHOICES)
    
    class Meta:
        model = Caption
        fields = ['image', 'platform', 'num_captions']