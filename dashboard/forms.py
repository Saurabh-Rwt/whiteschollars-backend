from django import forms
from .models import Section
from .models import KeyHighlight
from .models import Course
from .models import AccreditationsAndCertification


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'slug', 'description']

class SectionForm(forms.ModelForm):
    list_text = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Section
        fields = ['logo', 'section_heading', 'text', 'list_text', 'collaboration_logo', 'youtube_video']

class KeyHighlightForm(forms.ModelForm):
    class Meta:
        model = KeyHighlight
        fields = ['logo', 'text']


class AccreditationsAndCertificationForm(forms.ModelForm):
    certification_logo = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=True
    )

    class Meta:
        model = AccreditationsAndCertification
        fields = ['course', 'certification_logo']
