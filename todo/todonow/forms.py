from django import forms
from .models import Todo, UserProfile

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["user", 'title', 'due', 'description', 'value']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]
        widget = {
            'image' : forms.FileInput(attrs={'class': 'form-control',
                                             'id' : 'input-file'}),
            }
