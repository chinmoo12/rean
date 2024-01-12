from django import forms
from .models import Rean

class PostForm(forms.ModelForm):

    class Meta:
        model = Rean
        fields = ('title_file', 'title_dif', 'title_ru', 'title_th', 'title_is', 'text_note', 'text_ph', 'text_ex')
