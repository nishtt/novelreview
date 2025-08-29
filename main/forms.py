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
        fields = ['rating', 'comment']
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise forms.ValidationError("Please select a rating.")
        return rating
    
    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()
        if not comment:
            raise forms.ValidationError("Review comment cannot be empty.")
        return comment
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }