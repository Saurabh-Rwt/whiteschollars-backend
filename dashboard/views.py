from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from .serializers import CourseSerializer, CourseFullDetailSerializer
from .models import (
    Course, Section, KeyHighlight, AccreditationsAndCertification, 
    WhyChoose, Mentor, ProgramHighlight, CareerAssistance, 
    CareerTransition, OurAlumni, OnCampusClass, FeeStructure, 
    ProgramFor, WhyWhiteScholars, ListenOurExpert
)
from .forms import (
    CourseForm, SectionForm, KeyHighlightForm, AccreditationsAndCertificationForm, 
    WhyChooseForm, MentorForm, ProgramHighlightForm, CareerAssistanceForm, 
    CareerTransitionForm, OurAlumniForm, OnCampusClassForm
)
import json, os


# -------------------- API View: List all courses --------------------
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------- API View: Get full course details by slug --------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_course_full_data(request, slug):
    """
    Retrieve complete course data including related sections, highlights,
    mentors, etc. by course slug.
    """
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseFullDetailSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------- AUTH --------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

# -------------------- DASHBOARD --------------------
@login_required(login_url='login')
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
@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Add Course'})

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list')


# -------------------- SECTION --------------------
@login_required(login_url='login')
def add_section(request):
    selected_course_id = request.POST.get('course')

    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)

        if form.is_valid():
            section = form.save(commit=False)
            section.course = Course.objects.get(id=selected_course_id)

            # ✅ Handle list_text correctly
            list_text = request.POST.getlist('list_text[]')
            section.list_text = list_text if list_text else []

            # ✅ text should remain plain text (don’t convert or JSON dump)
            section.text = request.POST.get('text', '').strip()

            # ✅ Handle collaboration logos
            collab_files = request.FILES.getlist('collaboration_logo[]')
            if collab_files:
                section.collaboration_logo = [file.name for file in collab_files]

            section.save()
            return redirect('dashboard')
    else:
        form = SectionForm()
    return render(request, 'add_section.html', {'form': form})

# -------------------- KEY HIGHLIGHT --------------------
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
def add_career_assistance(request):
    courses = Course.objects.all()
    selected_course = None
    
    course_id = request.GET.get('course')
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)

        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        description_list = request.POST.getlist('description_list[]')

        CareerAssistance.objects.create(
            course=course,
            title=title,
            description=description,
            description_list=description_list,
            image=image
        )
        return redirect('dashboard')
    return render(request, 'add_career_assistance.html', {
        'courses': courses,
        'selected_course': selected_course
    })
# -------------------- CAREER TRANSITION --------------------
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
def add_on_campus_class(request):
    courses = Course.objects.all()
    selected_course = request.GET.get('course')

    if request.method == 'POST':
        course_id = request.POST.get('course')
        class_title = request.POST.get('class_title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        batch_type = request.POST.get('batch_type')

        print("DEBUG:", course_id, class_title, date, time, batch_type)

        if course_id and class_title and date and time and batch_type:
            course = Course.objects.get(id=course_id)
            OnCampusClass.objects.create(
                course=course,
                class_title=class_title,
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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
@login_required(login_url='login')
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