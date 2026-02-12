from django import forms
from django.utils.text import slugify
from .utils import sanitize_html
from .models import (
    Course,
    Section,
    KeyHighlight,
    AccreditationsAndCertification,
    WhyChoose,
    Mentor,
    ProgramHighlight,
    CareerAssistance,
    CareerTransition,
    OurAlumni,
    OnCampusClass
)

class CourseForm(forms.ModelForm):
    slug = forms.SlugField(required=False)

    class Meta:
        model = Course
        fields = [
            'name',
            'slug',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'meta_og_image',
            'brochure_pdf',
        ]

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '')
        name = self.cleaned_data.get('name', '')
        if not slug and name:
            slug = slugify(name)
        if not slug:
            return slug
        qs = Course.objects.filter(slug=slug)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if not qs.exists():
            return slug
        # Ensure uniqueness by appending a counter
        base = slug
        counter = 2
        while Course.objects.filter(slug=f"{base}-{counter}").exists():
            counter += 1
        return f"{base}-{counter}"

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class SanitizedHtmlField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        return sanitize_html(value) if value else ''

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['logo', 'section_heading', 'text', 'youtube_video']


class KeyHighlightForm(forms.ModelForm):
    class Meta:
        model = KeyHighlight
        fields = ['logo', 'text']


class AccreditationsAndCertificationForm(forms.ModelForm):
    certification_logo = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=True
    )

    class Meta:
        model = AccreditationsAndCertification
        fields = ['course', 'certification_logo']


class WhyChooseForm(forms.ModelForm):
    class Meta:
        model = WhyChoose
        fields = ['course', 'icon', 'heading', 'text']

class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = [
            'course',
            'mentor_image',
            'mentor_name',
            'designation_name',
            'experience_text',
            'company_logo'
        ]

class ProgramHighlightForm(forms.ModelForm):
    text = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = ProgramHighlight
        fields = ['course', 'title', 'heading', 'text', 'image']

class CareerAssistanceForm(forms.ModelForm):
    class Meta:
        model = CareerAssistance
        fields = ['course', 'title', 'description', 'description_list', 'image']

    widgets = {
        'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter detailed description'}),
    }

class CareerTransitionForm(forms.ModelForm):
    class Meta:
        model = CareerTransition
        fields = ['course', 'name', 'designation', 'description', 'placed_company', 'job_type', 'youtube_testimonial_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Enter long description'}),
        }

class OurAlumniForm(forms.ModelForm):
    alumni_logo = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False
    )

    class Meta:
        model = OurAlumni
        fields = ['course', 'alumni_logo']

class OnCampusClassForm(forms.ModelForm):
    class Meta:
        model = OnCampusClass
        fields = ['course', 'class_title', 'date', 'time', 'batch_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'batch_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Batch Type'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }
