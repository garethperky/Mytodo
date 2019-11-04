from django import forms
from .models import Todo, UserProfile
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["user", 'title', 'due_date', 'description', 'value']
        widgets = {
            "due_date": DatePicker(
                attrs={"placeholder": "Select a due date and time for this task"},
                options={
                    "format": "DD/MM/YYYY HH:mm",
                    "locale": "en-gb",
                },
            ),
            'description': forms.Textarea(attrs={'rows':4})
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]
        widget = {
            'image' : forms.FileInput(attrs={'class': 'form-control',
                                             'id' : 'input-file'}),
            }
