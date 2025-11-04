from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, KeyHighlight
from .forms import CourseForm, SectionForm, KeyHighlightForm
from .models import Section
import json, os
from django.conf import settings


def dashboard(request):
    courses = Course.objects.all()
    selected_course = None
    existing_highlight = None
    form = None

    # Handle form submission
    if request.method == 'POST':
        course_id = request.POST.get('course')
        if not course_id:
            return render(request, 'dashboard.html', {
                'courses': courses,
                'error': 'Please select a course first.'
            })

        selected_course = get_object_or_404(Course, id=course_id)
        existing_highlight = KeyHighlight.objects.filter(course=selected_course).first()
        form = KeyHighlightForm(request.POST, request.FILES, instance=existing_highlight)

        if form.is_valid():
            highlight = form.save(commit=False)
            highlight.course = selected_course
            highlight.save()
            return redirect('dashboard')
        else:
            print(form.errors)

    # Handle GET (initial load or course selection)
    else:
        course_id = request.GET.get('course')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            existing_highlight = KeyHighlight.objects.filter(course=selected_course).first()
            form = KeyHighlightForm(instance=existing_highlight)
        else:
            form = KeyHighlightForm()

    return render(request, 'dashboard.html', {
        'courses': courses,
        'selected_course': selected_course,
        'existing_highlight': existing_highlight,
        'form': form
    })

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Add Course'})

def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Edit Course'})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list')


def add_section(request):
    if request.method == 'POST':
        list_text = request.POST.getlist('list_text[]')
        post_data = request.POST.copy()
        post_data['list_text'] = json.dumps(list_text)

        form = SectionForm(post_data, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)
            uploaded_files = []
            if request.FILES.getlist('collaboration_logo[]'):
                for file in request.FILES.getlist('collaboration_logo[]'):
                    file_path = os.path.join('collaboration_logos', file.name)
                    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    with open(full_path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)
                    uploaded_files.append(file_path)
            section.collaboration_logo = uploaded_files 
            section.save()
            return redirect('add_section')
        else:
            print(form.errors)
    else:
        form = SectionForm()
    return render(request, 'dashboard.html', {'form': form})


def add_key_highlight(request):
    courses = Course.objects.all()  # for dropdown
    selected_course = None
    existing_highlight = None

    if request.method == 'POST':
        course_id = request.POST.get('course')
        if not course_id:
            return render(request, 'key_highlight.html', {
                'courses': courses,
                'error': 'Please select a course first.'
            })

        selected_course = get_object_or_404(Course, id=course_id)

        # check if KeyHighlight already exists for this course
        existing_highlight = KeyHighlight.objects.filter(course=selected_course).first()

        form = KeyHighlightForm(request.POST, request.FILES, instance=existing_highlight)
        if form.is_valid():
            highlight = form.save(commit=False)
            highlight.course = selected_course
            highlight.save()
            return redirect('add_key_highlight')
        else:
            print(form.errors)

    else:
        course_id = request.GET.get('course')
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            existing_highlight = KeyHighlight.objects.filter(course=selected_course).first()
            form = KeyHighlightForm(instance=existing_highlight)
        else:
            form = KeyHighlightForm()

        return render(request, 'dashboard.html', {
            'form': form,
            'courses': courses,
            'selected_course': selected_course,
            'existing_highlight': existing_highlight,
        })

