from rest_framework import generics, permissions
from .serializers import CourseSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Course, Section, KeyHighlight, AccreditationsAndCertification, WhyChoose, Mentor, ProgramHighlight, CareerAssistance, CareerTransition, OurAlumni, OnCampusClass, FeeStructure, ProgramFor, WhyWhiteScholars, ListenOurExpert
from .forms import CourseForm, SectionForm, KeyHighlightForm, AccreditationsAndCertificationForm, WhyChooseForm, MentorForm, ProgramHighlightForm, CareerAssistanceForm, CareerTransitionForm, OurAlumniForm, OnCampusClassForm
import json, os

# -------------------- API View --------------------
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

# -------------------- DASHBOARD --------------------
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

# -------------------- COURSE CRUD --------------------
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


# -------------------- SECTION --------------------
def add_section(request):
    if request.method == 'POST':
        list_text = request.POST.getlist('list_text[]')
        post_data = request.POST.copy()
        post_data['list_text'] = json.dumps(list_text)

        form = SectionForm(post_data, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)

            course_id = request.POST.get('course')
            if not course_id:
                return render(request, 'dashboard.html', {
                    'form': form,
                    'error': 'Please select a course first.'
                })
            selected_course = get_object_or_404(Course, id=course_id)
            section.course = selected_course

            # ✅ Handle collaboration logos
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
            return redirect('/')
        else:
            print("Form errors:", form.errors.as_json())
    else:
        form = SectionForm()
    return render(request, 'dashboard.html', {'form': form})


# -------------------- KEY HIGHLIGHT --------------------
def add_key_highlight(request):
    courses = Course.objects.all()
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


# -------------------- ACCREDITATIONS & CERTIFICATIONS --------------------
def add_accreditation_and_certification(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)

        files = request.FILES.getlist('certification_logo')

        uploaded_files = []
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'accreditations_certifications'))

        for file in files:
            filename = fs.save(file.name, file)
            file_url = fs.url(os.path.join('accreditations_certifications', filename))
            uploaded_files.append(file_url)

        AccreditationsAndCertification.objects.create(
            course=course,
            certification_logo=uploaded_files
        )

        return redirect('dashboard')

# -------------------- WHY CHOOSE --------------------
def add_why_choose(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        heading = request.POST.get('heading')
        text = request.POST.get('text')
        icon = request.FILES.get('icon')

        why_choose, created = WhyChoose.objects.get_or_create(course=course)
        why_choose.heading = heading
        why_choose.text = text
        if icon:
            why_choose.icon = icon
        why_choose.save()

        return redirect('dashboard')

    courses = Course.objects.all()
    return render(request, 'add_why_choose.html', {'courses': courses})

# -------------------- MENTOR --------------------
def add_mentor(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        mentor_name = request.POST.get('mentor_name')
        designation_name = request.POST.get('designation_name')
        experience_text = request.POST.get('experience_text')
        mentor_image = request.FILES.get('mentor_image')
        company_logo = request.FILES.get('company_logo')

        Mentor.objects.create(
            course=course,
            mentor_name=mentor_name,
            designation_name=designation_name,
            experience_text=experience_text,
            mentor_image=mentor_image,
            company_logo=company_logo
        )

        return redirect('dashboard')

    courses = Course.objects.all()
    return render(request, 'add_mentor.html', {'courses': courses})

# -------------------- PROGRAM HIGHLIGHTS --------------------
def add_program_highlight(request):
    if request.method == 'POST':
        form = ProgramHighlightForm(request.POST, request.FILES)
        if form.is_valid():
            text_data = form.cleaned_data.get('text')
            if text_data:
                try:
                    text_data = json.loads(text_data)
                except json.JSONDecodeError:
                    text_data = [text_data]

            highlight = form.save(commit=False)
            highlight.text = text_data
            highlight.save()
            return redirect('dashboard')
    else:
        form = ProgramHighlightForm()

    courses = Course.objects.all()
    return render(request, 'add_program_highlight.html', {'form': form, 'courses': courses})


# -------------------- CAREER ASSISTANCE --------------------
def add_career_assistance(request):
    courses = Course.objects.all()
    selected_course = None
    existing_assistance = None

    course_id = request.GET.get('course')
    if course_id:
        selected_course = Course.objects.filter(id=course_id).first()
        existing_assistance = CareerAssistance.objects.filter(course=selected_course).first()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)

        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        description_list = request.POST.getlist('description_list[]')

        assistance, created = CareerAssistance.objects.update_or_create(
            course=course,
            defaults={
                'title': title,
                'description': description,
                'description_list': description_list,
                'image': image
            }
        )

        return redirect('dashboard')

    return render(request, 'add_career_assistance.html', {
        'courses': courses,
        'selected_course': selected_course,
        'existing_assistance': existing_assistance
    })

# -------------------- CAREER TRANSITION --------------------
def add_career_transition(request):
    if request.method == 'POST':
        form = CareerTransitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CareerTransitionForm()

    courses = Course.objects.all()
    return render(request, 'components/add_career_transition.html', {'form': form, 'courses': courses})

# -------------------- OUR ALUMNI --------------------
def add_our_alumni(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        files = request.FILES.getlist('alumni_logo[]')  # multiple files input
        logo_list = []

        for file in files:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'alumni_logos')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            logo_list.append(f'alumni_logos/{file.name}')

        OurAlumni.objects.create(course=course, alumni_logo=logo_list)
        return redirect('dashboard')

    courses = Course.objects.all()
    return render(request, 'components/add_our_alumni.html', {'courses': courses})

# -------------------- on campus classes --------------------
def add_on_campus_class(request):
    courses = Course.objects.all()
    selected_course = request.GET.get('course')

    if request.method == 'POST':
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        time = request.POST.get('time')
        batch_type = request.POST.get('batch_type')

        print("DEBUG:", course_id, date, time, batch_type)

        if course_id and date and time and batch_type:
            course = Course.objects.get(id=course_id)
            OnCampusClass.objects.create(
                course=course,
                date=date,
                time=time,
                batch_type=batch_type
            )
        return redirect('dashboard')

    return render(request, 'components/add_on_campus_class.html', {
        'courses': courses,
        'selected_course': selected_course
    })

# -------------------- fee structure --------------------
def add_fee_structure(request):
    courses = Course.objects.all()
    selected_course_id = request.GET.get('course') or request.POST.get('course_id')
    selected_course = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)

        if request.method == 'POST':
            title = request.POST.get('title')
            mode_of_training = request.POST.get('mode_of_training')
            batch_date = request.POST.get('batch_date')
            list_text = request.POST.getlist('list_text[]')
            original_price = request.POST.get('original_price')
            discount_price = request.POST.get('discount_price')

            FeeStructure.objects.create(
                course=selected_course,
                title=title,
                mode_of_training=mode_of_training,
                list_text=list_text,
                batch_date=batch_date,
                original_price=original_price,
                discount_price=discount_price
            )

            return redirect('dashboard')

    return render(request, 'components/add_fee_structure.html', {
        'courses': courses,
        'selected_course': selected_course
    })

# --------------------  Program for --------------------
def add_program_for(request):
    courses = Course.objects.all()
    selected_course_id = request.GET.get('course') or request.POST.get('course_id')
    selected_course = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)

        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if title and description:
                ProgramFor.objects.create(
                    course=selected_course,
                    image=image,
                    title=title,
                    description=description
                )
                return redirect('dashboard')

    return render(request, 'components/add_program_for.html', {
        'courses': courses,
        'selected_course': selected_course
    })

# -------------------- why white scholars --------------------
def add_why_white_scholars(request):
    courses = Course.objects.all()
    selected_course_id = request.GET.get('course') or request.POST.get('course_id')
    selected_course = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)

        if request.method == 'POST':
            description = request.POST.get('description')
            images = request.FILES.getlist('images[]')

            image_paths = []
            for image in images:
                image_path = os.path.join('why_white_scholars_images', image.name)
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)

                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                image_paths.append(image_path)

            WhyWhiteScholars.objects.create(
                course=selected_course,
                description=description,
                images=image_paths
            )

            return redirect('dashboard')

    return render(request, 'components/add_why_white_scholars.html', {
        'courses': courses,
        'selected_course': selected_course
    })

# -------------------- Listen Our Expert --------------------
def add_listen_our_expert(request):
    courses = Course.objects.all()
    selected_course = None
    experts = None

    course_id = request.GET.get('course')
    if course_id:
        selected_course = Course.objects.get(id=course_id)
        experts = ListenOurExpert.objects.filter(course=selected_course)

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        title = request.POST.get('title')
        youtube_links = request.POST.getlist('youtube_links[]')

        ListenOurExpert.objects.create(
            course_id=course_id,
            title=title,
            youtube_links=youtube_links
        )
        return redirect('dashboard')

    return render(request, 'listen_our_expert.html', {
        'courses': courses,
        'selected_course': selected_course,
        'experts': experts
    })