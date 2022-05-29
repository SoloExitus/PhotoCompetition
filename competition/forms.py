from django import forms
from django.urls import reverse_lazy

from competition.models import PhotoPost


class PostForm(forms.ModelForm):
    class Meta:
        model = PhotoPost
        fields = ['title', 'description', 'full_image']