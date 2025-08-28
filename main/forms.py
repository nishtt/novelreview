from django import forms
from .models import *

#add novel
class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = ('name', 'author', 'description', 'release_date', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'rating')