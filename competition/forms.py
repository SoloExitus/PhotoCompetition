from django import forms

import os
import photocompetition.settings as settings

from django.utils.safestring import mark_safe

from competition.models import PhotoPost


class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            img_html = mark_safe(
                f'<img src="{os.path.join(settings.MEDIA_URL, str(value))}" width="200" /><br><br>')
            return f'{img_html}{input_html}'
        return input_html


class UpdatePostForm(forms.ModelForm):

    class Meta:
        model = PhotoPost
        fields = ['title', 'description', 'full_image']

        widgets = {
            'full_image': PictureWidget
        }


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = PhotoPost
        fields = ['title', 'description', 'full_image']