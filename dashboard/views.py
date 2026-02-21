from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .serializers import CourseSerializer, CourseFullDetailSerializer, CoursePageSerializer
from .models import (
    Course,
    Section,
    KeyHighlight,
    AccreditationsAndCertification,
    AccreditationLogo,
    WhyChoose,
    Mentor,
    ProgramHighlight,
    CareerAssistance,
    CareerTransition,
    CareerTransitionStat,
    OurAlumni,
    AlumniLogo,
    OnCampusClass,
    OnCampusSection,
    FeeStructure,
    ProgramFor,
    WhyWhiteScholars,
    WhyWhiteScholarsBullet,
    WhyWhiteScholarsImage,
    ListenOurExpert,
    CourseSection,
    CourseHero,
    HeroHighlight,
    HeroCollaborationLogo,
    CourseHeroButton,
    LiveDemoCta,
    CourseOverview,
    CourseOverviewItem,
    LearnerJourney,
    CurriculumSection,
    CurriculumModule,
    ExpertTalkVideo,
    SalaryTrendSection,
    SalaryDesignationGroup,
    HiringLogo,
    ScopeSection,
    ScopeBullet,
    RelatedArticlesSection,
    RelatedArticle,
    CertificationItem,
    ReviewSection,
    ReviewItem,
    FaqSection,
    FaqItem,
    LeadCta,
    CoursePopup,
)
from .forms import (
    CourseForm, SectionForm, KeyHighlightForm, AccreditationsAndCertificationForm, 
    WhyChooseForm, MentorForm, ProgramHighlightForm, CareerAssistanceForm, 
    CareerTransitionForm, OurAlumniForm, OnCampusClassForm
)
from .utils import sanitize_html
from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode
import json, os
import logging

logger = logging.getLogger(__name__)

SECTION_CONFIG = [
    {
        'key': 'hero',
        'label': 'Hero + Primary CTA',
        'description': 'Top banner with heading, media, highlights, and CTA buttons.',
        'template': 'components/editor_sections/hero.html',
    },
    {
        'key': 'key_highlights',
        'label': 'Key Highlights',
        'description': 'Small highlight cards under the hero section.',
        'template': 'components/editor_sections/key_highlights.html',
    },
    {
        'key': 'accreditations',
        'label': 'Accreditations & Certifications',
        'description': 'Logo strip for accrediting partners.',
        'template': 'components/editor_sections/accreditations.html',
    },
    {
        'key': 'why_choose',
        'label': 'Why Choose WhiteScholars',
        'description': 'Icon cards explaining why to choose this course.',
        'template': 'components/editor_sections/why_choose.html',
    },
    {
        'key': 'live_demo',
        'label': 'Live Demo CTA',
        'description': 'Full-width CTA banner for live demos/workshops.',
        'template': 'components/editor_sections/live_demo.html',
    },
    {
        'key': 'course_overview',
        'label': 'Course Overview',
        'description': 'Intro text plus expandable overview questions.',
        'template': 'components/editor_sections/course_overview.html',
    },
    {
        'key': 'mentors',
        'label': 'Mentors',
        'description': 'Mentor cards with photo, role, and company logo.',
        'template': 'components/editor_sections/mentors.html',
    },
    {
        'key': 'program_highlights',
        'label': 'Program Highlights',
        'description': 'Tabbed highlights with rich text and image.',
        'template': 'components/editor_sections/program_highlights.html',
    },
    {
        'key': 'learner_journey',
        'label': 'Learner Journey',
        'description': 'Journey infographic image and caption.',
        'template': 'components/editor_sections/learner_journey.html',
    },
    {
        'key': 'curriculum',
        'label': 'Curriculum & Modules',
        'description': 'Module list plus call-us box.',
        'template': 'components/editor_sections/curriculum.html',
    },
    {
        'key': 'career_assistance',
        'label': 'Career Assistance',
        'description': '360-degree career assistance content blocks.',
        'template': 'components/editor_sections/career_assistance.html',
    },
    {
        'key': 'career_transitions',
        'label': 'Career Transitions',
        'description': 'Success story slider + stats panel.',
        'template': 'components/editor_sections/career_transitions.html',
    },
    {
        'key': 'alumni',
        'label': 'Our Alumni Works Here',
        'description': 'Alumni company logo carousel.',
        'template': 'components/editor_sections/alumni.html',
    },
    {
        'key': 'on_campus',
        'label': 'On Campus Classes',
        'description': 'Upcoming class schedule and CTA.',
        'template': 'components/editor_sections/on_campus.html',
    },
    {
        'key': 'fee_structure',
        'label': 'Fee Structure',
        'description': 'Pricing cards for online/offline/hybrid.',
        'template': 'components/editor_sections/fee_structure.html',
    },
    {
        'key': 'program_for',
        'label': 'Who Is This Program For?',
        'description': 'Audience cards with images.',
        'template': 'components/editor_sections/program_for.html',
    },
    {
        'key': 'why_white_scholars',
        'label': 'Why WhiteScholars Is the Best',
        'description': 'Bullet list and image slider.',
        'template': 'components/editor_sections/why_white_scholars.html',
    },
    {
        'key': 'expert_talks',
        'label': 'Expert Talks',
        'description': 'Embedded expert talk videos.',
        'template': 'components/editor_sections/expert_talks.html',
    },
    {
        'key': 'salary_trends',
        'label': 'Salary & Hiring Trends',
        'description': 'Salary trend chart and hiring logos.',
        'template': 'components/editor_sections/salary_trends.html',
    },
    {
        'key': 'scope',
        'label': 'Scope of the Course',
        'description': 'Scope intro, bullet list, and image.',
        'template': 'components/editor_sections/scope.html',
    },
    {
        'key': 'related_articles',
        'label': 'Related Articles',
        'description': 'Article cards and load more CTA.',
        'template': 'components/editor_sections/related_articles.html',
    },
    {
        'key': 'certifications',
        'label': 'Certifications',
        'description': 'Certification image cards.',
        'template': 'components/editor_sections/certifications.html',
    },
    {
        'key': 'reviews',
        'label': 'Reviews',
        'description': 'Review summary plus cards.',
        'template': 'components/editor_sections/reviews.html',
    },
    {
        'key': 'faqs',
        'label': 'FAQs',
        'description': 'Frequently asked questions.',
        'template': 'components/editor_sections/faqs.html',
    },
    {
        'key': 'cta_ready',
        'label': 'CTA: Ready to Start',
        'description': 'Lead capture CTA block for ready-to-start users.',
        'template': 'components/editor_sections/cta.html',
    },
    {
        'key': 'cta_discover',
        'label': 'CTA: Discover Secrets',
        'description': 'Lead capture CTA block for discovery users.',
        'template': 'components/editor_sections/cta.html',
    },
    {
        'key': 'cta_confused',
        'label': 'CTA: Still Confused',
        'description': 'Lead capture CTA block for confused users.',
        'template': 'components/editor_sections/cta.html',
    },
]

SECTION_INDEX = {item['key']: idx for idx, item in enumerate(SECTION_CONFIG)}
SECTION_META = {item['key']: item for item in SECTION_CONFIG}

EDITABLE_MAP = {
    'hero_highlight': HeroHighlight,
    'hero_logo': HeroCollaborationLogo,
    'hero_button': CourseHeroButton,
    'key_highlight': KeyHighlight,
    'accreditation_logo': AccreditationLogo,
    'why_choose': WhyChoose,
    'mentor': Mentor,
    'program_highlight': ProgramHighlight,
    'career_assistance': CareerAssistance,
    'career_transition': CareerTransition,
    'career_transition_stat': CareerTransitionStat,
    'alumni_logo': AlumniLogo,
    'on_campus_class': OnCampusClass,
    'fee_structure': FeeStructure,
    'program_for': ProgramFor,
    'why_white_bullet': WhyWhiteScholarsBullet,
    'why_white_image': WhyWhiteScholarsImage,
    'expert_talk': ExpertTalkVideo,
    'salary_designation': SalaryDesignationGroup,
    'hiring_logo': HiringLogo,
    'scope_bullet': ScopeBullet,
    'related_article': RelatedArticle,
    'certification': CertificationItem,
    'review_item': ReviewItem,
    'faq_item': FaqItem,
    'course_overview_item': CourseOverviewItem,
    'curriculum_module': CurriculumModule,
}


def _dashboard_url(tab=None, course_id=None, section=None, edit_key=None, edit_id=None, **extra_params):
    base = reverse('dashboard')
    params = {}
    if tab:
        params['tab'] = tab
    if course_id:
        params['course'] = course_id
    if section:
        params['section'] = section
    if edit_key:
        params['edit_key'] = edit_key
    if edit_id:
        params['edit_id'] = edit_id
    for key, value in extra_params.items():
        if value not in (None, ''):
            params[key] = value
    if not params:
        return base
    return f"{base}?{urlencode(params)}"


def _get_selected_course(course_id):
    if not course_id:
        return None
    try:
        return Course.objects.get(id=course_id)
    except (Course.DoesNotExist, ValueError, TypeError):
        return None


def _ensure_course_sections(course):
    existing = {section.key for section in CourseSection.objects.filter(course=course)}
    new_sections = []
    for idx, config in enumerate(SECTION_CONFIG):
        key = config['key']
        if key not in existing:
            new_sections.append(CourseSection(course=course, key=key, sort_order=idx * 10))
    if new_sections:
        CourseSection.objects.bulk_create(new_sections)


def _next_sort_order(model, course):
    last = model.objects.filter(course=course).order_by('-sort_order').first()
    if not last:
        return 1
    return last.sort_order + 1


def _clean_list(values):
    return [value.strip() for value in values if value and value.strip()]


def _get_decimal(value, fallback=None):
    if value in (None, ''):
        return fallback
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def _rich_text(value):
    return sanitize_html(value or '')


def _build_dashboard_context(request, selected_course=None, active_section=None, edit_key=None, edit_id=None):
    context = {
        'courses': Course.objects.all().order_by('name'),
        'selected_course': selected_course,
        'section_config': SECTION_CONFIG,
        'section_meta': SECTION_META,
        'active_section': active_section,
        'edit_key': edit_key,
        'edit_id': edit_id,
    }

    if not selected_course:
        return context

    _ensure_course_sections(selected_course)
    section_records = CourseSection.objects.filter(course=selected_course).order_by('sort_order')
    course_sections = []
    for section in section_records:
        meta = SECTION_META.get(section.key, {})
        course_sections.append({
            'key': section.key,
            'label': meta.get('label', section.key),
            'description': meta.get('description', ''),
            'template': meta.get('template', ''),
            'is_enabled': section.is_enabled,
        })

    editing = {}
    if edit_key and edit_id and edit_key in EDITABLE_MAP:
        model = EDITABLE_MAP[edit_key]
        editing[edit_key] = model.objects.filter(id=edit_id, course=selected_course).first()

    hero_highlights = HeroHighlight.objects.filter(course=selected_course).order_by('sort_order')
    hero_buttons = CourseHeroButton.objects.filter(course=selected_course).order_by('sort_order')

    context.update({
        'course_sections': course_sections,
        'editing': editing,
        'hero': getattr(selected_course, 'hero', None),
        'hero_highlights': hero_highlights,
        'hero_highlights_text': '\n'.join(item.text for item in hero_highlights),
        'hero_logos': HeroCollaborationLogo.objects.filter(course=selected_course).order_by('sort_order'),
        'hero_buttons': hero_buttons,
        'key_highlights': KeyHighlight.objects.filter(course=selected_course).order_by('sort_order'),
        'accreditation_logos': AccreditationLogo.objects.filter(course=selected_course).order_by('sort_order'),
        'why_choose_items': WhyChoose.objects.filter(course=selected_course).order_by('sort_order'),
        'live_demo_cta': getattr(selected_course, 'live_demo_cta', None),
        'course_overview': getattr(selected_course, 'course_overview', None),
        'course_overview_items': CourseOverviewItem.objects.filter(course=selected_course).order_by('sort_order'),
        'mentors': Mentor.objects.filter(course=selected_course).order_by('sort_order'),
        'program_highlights': ProgramHighlight.objects.filter(course=selected_course).order_by('sort_order'),
        'learner_journey': getattr(selected_course, 'learner_journey', None),
        'curriculum_section': getattr(selected_course, 'curriculum_section', None),
        'curriculum_modules': CurriculumModule.objects.filter(course=selected_course).order_by('sort_order'),
        'career_assistances': CareerAssistance.objects.filter(course=selected_course).order_by('sort_order'),
        'career_transitions': CareerTransition.objects.filter(course=selected_course).order_by('sort_order'),
        'career_transition_stats': CareerTransitionStat.objects.filter(course=selected_course).order_by('sort_order'),
        'alumni_logos': AlumniLogo.objects.filter(course=selected_course).order_by('sort_order'),
        'on_campus_section': getattr(selected_course, 'on_campus_section', None),
        'on_campus_classes': OnCampusClass.objects.filter(course=selected_course).order_by('sort_order'),
        'fee_structures': FeeStructure.objects.filter(course=selected_course).order_by('sort_order'),
        'program_for_items': ProgramFor.objects.filter(course=selected_course).order_by('sort_order'),
        'why_white_bullets': WhyWhiteScholarsBullet.objects.filter(course=selected_course).order_by('sort_order'),
        'why_white_images': WhyWhiteScholarsImage.objects.filter(course=selected_course).order_by('sort_order'),
        'expert_talks': ExpertTalkVideo.objects.filter(course=selected_course).order_by('sort_order'),
        'salary_trend_section': getattr(selected_course, 'salary_trend_section', None),
        'salary_designations': SalaryDesignationGroup.objects.filter(course=selected_course).order_by('sort_order'),
        'hiring_logos': HiringLogo.objects.filter(course=selected_course).order_by('sort_order'),
        'scope_section': getattr(selected_course, 'scope_section', None),
        'scope_bullets': ScopeBullet.objects.filter(course=selected_course).order_by('sort_order'),
        'related_articles_section': getattr(selected_course, 'related_articles_section', None),
        'related_articles': RelatedArticle.objects.filter(course=selected_course).order_by('sort_order'),
        'certifications': CertificationItem.objects.filter(course=selected_course).order_by('sort_order'),
        'review_section': getattr(selected_course, 'review_section', None),
        'review_items': ReviewItem.objects.filter(course=selected_course).order_by('sort_order'),
        'faq_section': getattr(selected_course, 'faq_section', None),
        'faq_items': FaqItem.objects.filter(course=selected_course).order_by('sort_order'),
        'lead_ctas': {cta.key: cta for cta in LeadCta.objects.filter(course=selected_course)},
        'popup_modal': getattr(selected_course, 'popup_modal', None),
    })
    return context


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


# -------------------- API View: Get course page payload --------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_course_page(request, slug):
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CoursePageSerializer(course)
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


def _is_ajax_request(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def _set_dashboard_ajax_data(request, action, **extra):
    request._dashboard_ajax_data = {
        'action': action,
        **extra,
    }


def _serialize_dashboard_message(message):
    tags = message.tags or 'info'
    if 'error' in tags:
        level = 'error'
    elif 'warning' in tags:
        level = 'warning'
    elif 'success' in tags:
        level = 'success'
    else:
        level = 'info'
    return {
        'level': level,
        'tags': tags,
        'text': str(message),
    }


def _ajax_dashboard_response(request, response=None, fallback_redirect=None):
    redirect_url = fallback_redirect or getattr(
        response,
        'url',
        _dashboard_url(course_id=request.POST.get('course') or request.POST.get('course_id')),
    )
    queued_messages = [
        _serialize_dashboard_message(message)
        for message in messages.get_messages(request)
    ]
    has_error = any(message['level'] == 'error' for message in queued_messages)
    return JsonResponse(
        {
            'ok': not has_error,
            'messages': queued_messages,
            'redirect_url': redirect_url,
            'data': getattr(request, '_dashboard_ajax_data', None),
        },
        status=400 if has_error else 200,
    )


# -------------------- DASHBOARD --------------------
@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        try:
            response = _handle_dashboard_post(request)
        except Exception as exc:
            fallback_course_id = request.POST.get('course') or request.POST.get('course_id')
            fallback_redirect = _dashboard_url(course_id=fallback_course_id)
            logger.exception(
                "Dashboard action failed",
                extra={"action": request.POST.get('action'), "course_id": request.POST.get('course')},
            )
            messages.error(request, f"Failed to save changes: {exc}")
            if _is_ajax_request(request):
                return _ajax_dashboard_response(request, fallback_redirect=fallback_redirect)
            return redirect(fallback_redirect)

        if _is_ajax_request(request):
            return _ajax_dashboard_response(request, response=response)
        return response

    course_id = request.GET.get('course')
    selected_course = _get_selected_course(course_id)
    if course_id and not selected_course:
        messages.error(request, 'The selected course was not found.')

    active_section = request.GET.get('section')
    edit_key = request.GET.get('edit_key')
    edit_id = request.GET.get('edit_id')

    context = _build_dashboard_context(
        request,
        selected_course=selected_course,
        active_section=active_section,
        edit_key=edit_key,
        edit_id=edit_id,
    )
    return render(request, 'dashboard.html', context)


def _handle_dashboard_post(request):
    action = request.POST.get('action')
    course_id = request.POST.get('course') or request.POST.get('course_id')
    selected_course = _get_selected_course(course_id)

    if not selected_course:
        messages.error(request, 'Please select a valid course before saving.')
        return redirect(_dashboard_url())

    if action == 'save_course_meta':
        form = CourseForm(request.POST, request.FILES, instance=selected_course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course settings updated.')
        else:
            messages.error(request, f"Please fix the errors: {form.errors.as_text()}")
        return redirect(_dashboard_url(course_id=selected_course.id))

    if action == 'save_popup_modal':
        popup, _created = CoursePopup.objects.get_or_create(course=selected_course)
        heading = request.POST.get('popup_heading', '').strip()
        image = request.FILES.get('popup_image')
        image_alt = request.POST.get('popup_image_alt', '').strip()

        if not heading:
            messages.error(request, 'Popup heading is required.')
            return redirect(_dashboard_url(course_id=selected_course.id))
        if not image and not popup.image:
            messages.error(request, 'Popup image is required.')
            return redirect(_dashboard_url(course_id=selected_course.id))

        popup.heading = heading
        if image:
            popup.image = image
        if image_alt:
            popup.image_alt = image_alt
        popup.save()
        messages.success(request, 'Popup modal saved.')
        return redirect(_dashboard_url(course_id=selected_course.id))

    if action == 'save_hero':
        hero, _created = CourseHero.objects.get_or_create(course=selected_course)
        def has_field(name):
            return name in request.POST or name in request.FILES

        if has_field('heading'):
            hero.heading = request.POST.get('heading', '').strip()
        if has_field('subheading'):
            hero.subheading = request.POST.get('subheading', '').strip()
        if has_field('description_html'):
            hero.description_html = _rich_text(request.POST.get('description_html'))
        if has_field('badge_text'):
            hero.badge_text = request.POST.get('badge_text', '').strip()
        if has_field('award_text'):
            hero.award_text = request.POST.get('award_text', '').strip()
        if has_field('collaboration_heading'):
            hero.collaboration_heading = request.POST.get('collaboration_heading', '').strip()
        if has_field('media_type'):
            hero.media_type = request.POST.get('media_type', 'image')
        if has_field('hero_video_url'):
            hero.hero_video_url = request.POST.get('hero_video_url', '').strip()

        badge_icon = request.FILES.get('badge_icon')
        if badge_icon:
            hero.badge_icon = badge_icon
        if has_field('badge_icon_alt'):
            hero.badge_icon_alt = request.POST.get('badge_icon_alt', '').strip()

        award_logo = request.FILES.get('award_logo')
        if award_logo:
            hero.award_logo = award_logo
        if has_field('award_logo_alt'):
            hero.award_logo_alt = request.POST.get('award_logo_alt', '').strip()

        hero_image = request.FILES.get('hero_image')
        if hero_image:
            hero.hero_image = hero_image
        if has_field('hero_image_alt'):
            hero.hero_image_alt = request.POST.get('hero_image_alt', '').strip()

        video_thumb = request.FILES.get('hero_video_thumbnail')
        if video_thumb:
            hero.hero_video_thumbnail = video_thumb
        if has_field('hero_video_thumbnail_alt'):
            hero.hero_video_thumbnail_alt = request.POST.get('hero_video_thumbnail_alt', '').strip()

        core_fields = {
            'heading',
            'subheading',
            'description_html',
            'badge_text',
            'badge_icon',
            'badge_icon_alt',
            'award_text',
            'award_logo',
            'award_logo_alt',
        }
        if any(has_field(field) for field in core_fields) and not hero.heading:
            messages.error(request, 'Hero heading is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

        hero.save()
        messages.success(request, 'Hero section saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'save_hero_highlights_bulk':
        raw_text = request.POST.get('highlights_text', '')
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        HeroHighlight.objects.filter(course=selected_course).delete()
        if lines:
            HeroHighlight.objects.bulk_create([
                HeroHighlight(
                    course=selected_course,
                    text=line,
                    sort_order=(idx + 1) * 10,
                )
                for idx, line in enumerate(lines)
            ])
            messages.success(request, 'Hero checklist points saved.')
        else:
            messages.success(request, 'Hero checklist points cleared.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'save_hero_highlight':
        text = request.POST.get('highlight_text', '').strip()
        item_id = request.POST.get('item_id')
        if not text:
            messages.error(request, 'Highlight text is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        if item_id:
            highlight = HeroHighlight.objects.filter(id=item_id, course=selected_course).first()
            if not highlight:
                messages.error(request, 'Highlight not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        else:
            highlight = HeroHighlight(course=selected_course, sort_order=_next_sort_order(HeroHighlight, selected_course))
        highlight.text = text
        highlight.save()
        messages.success(request, 'Hero highlight saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'delete_hero_highlight':
        item_id = request.POST.get('item_id')
        HeroHighlight.objects.filter(id=item_id, course=selected_course).delete()
        messages.success(request, 'Hero highlight removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'save_hero_logo':
        item_id = request.POST.get('item_id')
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        if not image and not item_id:
            messages.error(request, 'Please upload a collaboration logo.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        if item_id:
            logo = HeroCollaborationLogo.objects.filter(id=item_id, course=selected_course).first()
            if not logo:
                messages.error(request, 'Collaboration logo not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        else:
            logo = HeroCollaborationLogo(course=selected_course, sort_order=_next_sort_order(HeroCollaborationLogo, selected_course))
        if image:
            logo.image = image
        if image_alt:
            logo.image_alt = image_alt
        logo.save()
        _set_dashboard_ajax_data(
            request,
            'save_hero_logo',
            mode='updated' if item_id else 'created',
            item={
                'id': logo.id,
                'image_alt': logo.image_alt or 'Logo',
            },
        )
        messages.success(request, 'Collaboration logo saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'delete_hero_logo':
        item_id = request.POST.get('item_id')
        HeroCollaborationLogo.objects.filter(id=item_id, course=selected_course).delete()
        _set_dashboard_ajax_data(request, 'delete_hero_logo', item_id=str(item_id or ''))
        messages.success(request, 'Collaboration logo removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'save_hero_button':
        label = request.POST.get('label', '').strip()
        url = request.POST.get('url', '').strip()
        style = request.POST.get('style', 'primary')
        action_type = request.POST.get('action_type', 'link')
        item_id = request.POST.get('item_id')
        if not label:
            messages.error(request, 'Button label is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        if action_type == 'link' and not url:
            messages.error(request, 'A URL is required when the button action is set to Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        if item_id:
            button = CourseHeroButton.objects.filter(id=item_id, course=selected_course).first()
            if not button:
                messages.error(request, 'Button not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))
        else:
            button = CourseHeroButton(course=selected_course, sort_order=_next_sort_order(CourseHeroButton, selected_course))
        button.label = label
        button.url = url
        button.style = style
        button.action_type = action_type
        button.save()
        _set_dashboard_ajax_data(
            request,
            'save_hero_button',
            mode='updated' if item_id else 'created',
            item={
                'id': button.id,
                'label': button.label,
                'style': button.style,
                'action_type': button.action_type,
            },
        )
        messages.success(request, 'CTA button saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'delete_hero_button':
        item_id = request.POST.get('item_id')
        CourseHeroButton.objects.filter(id=item_id, course=selected_course).delete()
        _set_dashboard_ajax_data(request, 'delete_hero_button', item_id=str(item_id or ''))
        messages.success(request, 'CTA button removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='hero'))

    if action == 'save_key_highlight':
        text = request.POST.get('text', '').strip()
        logo = request.FILES.get('logo')
        logo_alt = request.POST.get('logo_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not text:
            messages.error(request, 'Highlight text is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='key_highlights'))
        if item_id:
            highlight = KeyHighlight.objects.filter(id=item_id, course=selected_course).first()
            if not highlight:
                messages.error(request, 'Key highlight not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='key_highlights'))
        else:
            highlight = KeyHighlight(course=selected_course, sort_order=_next_sort_order(KeyHighlight, selected_course))
        if logo:
            highlight.logo = logo
        highlight.logo_alt = logo_alt
        highlight.text = text
        highlight.save()
        messages.success(request, 'Key highlight saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='key_highlights'))

    if action == 'delete_key_highlight':
        KeyHighlight.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Key highlight removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='key_highlights'))

    if action == 'save_accreditation_logo':
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not image and not item_id:
            messages.error(request, 'Please upload an accreditation logo.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='accreditations'))
        if item_id:
            logo = AccreditationLogo.objects.filter(id=item_id, course=selected_course).first()
            if not logo:
                messages.error(request, 'Accreditation logo not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='accreditations'))
        else:
            logo = AccreditationLogo(course=selected_course, sort_order=_next_sort_order(AccreditationLogo, selected_course))
        if image:
            logo.image = image
        if image_alt:
            logo.image_alt = image_alt
        logo.save()
        messages.success(request, 'Accreditation logo saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='accreditations'))

    if action == 'delete_accreditation_logo':
        AccreditationLogo.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Accreditation logo removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='accreditations'))

    if action == 'save_why_choose':
        heading = request.POST.get('heading', '').strip()
        text = request.POST.get('text', '').strip()
        icon = request.FILES.get('icon')
        icon_alt = request.POST.get('icon_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not heading or not text:
            messages.error(request, 'Heading and description are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='why_choose'))
        if item_id:
            item = WhyChoose.objects.filter(id=item_id, course=selected_course).first()
            if not item:
                messages.error(request, 'Why choose item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='why_choose'))
        else:
            item = WhyChoose(course=selected_course, sort_order=_next_sort_order(WhyChoose, selected_course))
        item.heading = heading
        item.text = text
        if icon:
            item.icon = icon
        if icon_alt:
            item.icon_alt = icon_alt
        item.save()
        messages.success(request, 'Why choose item saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_choose'))

    if action == 'delete_why_choose':
        WhyChoose.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Why choose item removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_choose'))

    if action == 'save_live_demo':
        heading = request.POST.get('heading', '').strip()
        button_label = request.POST.get('button_label', '').strip()
        button_url = request.POST.get('button_url', '').strip()
        button_action_type = request.POST.get('button_action_type', 'link')
        if not heading or not button_label:
            messages.error(request, 'Heading and button label are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='live_demo'))
        if button_action_type == 'link' and not button_url:
            messages.error(request, 'A URL is required when the button action is set to Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='live_demo'))
        live_demo, _created = LiveDemoCta.objects.get_or_create(course=selected_course)
        live_demo.heading = heading
        live_demo.button_label = button_label
        live_demo.button_url = button_url
        live_demo.button_action_type = button_action_type
        live_demo.save()
        messages.success(request, 'Live demo CTA saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='live_demo'))

    if action == 'save_course_overview':
        overview, _created = CourseOverview.objects.get_or_create(course=selected_course)
        overview.intro_html = _rich_text(request.POST.get('intro_html'))
        overview.save()
        messages.success(request, 'Course overview intro saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='course_overview'))

    if action == 'save_course_overview_item':
        question = request.POST.get('question', '').strip()
        answer_html = _rich_text(request.POST.get('answer_html'))
        item_id = request.POST.get('item_id')
        if not question or not answer_html:
            messages.error(request, 'Question and answer are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='course_overview'))
        if item_id:
            item = CourseOverviewItem.objects.filter(id=item_id, course=selected_course).first()
            if not item:
                messages.error(request, 'Overview item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='course_overview'))
        else:
            item = CourseOverviewItem(course=selected_course, sort_order=_next_sort_order(CourseOverviewItem, selected_course))
        item.question = question
        item.answer_html = answer_html
        item.save()
        messages.success(request, 'Course overview item saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='course_overview'))

    if action == 'delete_course_overview_item':
        CourseOverviewItem.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Course overview item removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='course_overview'))

    if action == 'save_mentor':
        name = request.POST.get('mentor_name', '').strip()
        designation = request.POST.get('designation_name', '').strip()
        experience = request.POST.get('experience_text', '').strip()
        image = request.FILES.get('mentor_image')
        image_alt = request.POST.get('mentor_image_alt', '').strip()
        company_logo = request.FILES.get('company_logo')
        company_logo_alt = request.POST.get('company_logo_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not name or not designation or not experience:
            messages.error(request, 'Mentor name, designation, and experience are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='mentors'))
        if item_id:
            mentor = Mentor.objects.filter(id=item_id, course=selected_course).first()
            if not mentor:
                messages.error(request, 'Mentor not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='mentors'))
        else:
            mentor = Mentor(course=selected_course, sort_order=_next_sort_order(Mentor, selected_course))
        mentor.mentor_name = name
        mentor.designation_name = designation
        mentor.experience_text = experience
        if image:
            mentor.mentor_image = image
        mentor.mentor_image_alt = image_alt
        if company_logo:
            mentor.company_logo = company_logo
        mentor.company_logo_alt = company_logo_alt
        mentor.save()
        messages.success(request, 'Mentor saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='mentors'))

    if action == 'delete_mentor':
        Mentor.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Mentor removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='mentors'))

    if action == 'save_program_highlight':
        title = request.POST.get('title', '').strip()
        heading = request.POST.get('heading', '').strip()
        description_html = _rich_text(request.POST.get('description_html'))
        bullets = _clean_list(request.POST.getlist('bullets[]'))
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not title or not heading:
            messages.error(request, 'Tab title and heading are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='program_highlights'))
        if item_id:
            highlight = ProgramHighlight.objects.filter(id=item_id, course=selected_course).first()
            if not highlight:
                messages.error(request, 'Program highlight not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='program_highlights'))
        else:
            highlight = ProgramHighlight(course=selected_course, sort_order=_next_sort_order(ProgramHighlight, selected_course))
        highlight.title = title
        highlight.heading = heading
        highlight.description_html = description_html
        highlight.text = bullets
        if image:
            highlight.image = image
        highlight.image_alt = image_alt
        highlight.save()
        messages.success(request, 'Program highlight saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='program_highlights'))

    if action == 'delete_program_highlight':
        ProgramHighlight.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Program highlight removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='program_highlights'))

    if action == 'save_learner_journey':
        journey, _created = LearnerJourney.objects.get_or_create(course=selected_course)
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        if image:
            journey.image = image
        journey.image_alt = image_alt
        journey.save()
        messages.success(request, 'Learner journey saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='learner_journey'))

    if action == 'save_curriculum_settings':
        section, _created = CurriculumSection.objects.get_or_create(course=selected_course)
        section.call_us_title = request.POST.get('call_us_title', '').strip()
        section.call_us_phone = request.POST.get('call_us_phone', '').strip()
        section.call_us_button_label = request.POST.get('call_us_button_label', '').strip()
        section.call_us_button_url = request.POST.get('call_us_button_url', '').strip()
        section.call_us_action_type = request.POST.get('call_us_action_type', 'link')
        if section.call_us_button_label and section.call_us_action_type == 'link' and not section.call_us_button_url:
            messages.error(request, 'A URL is required when the Call Us button action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))
        section.save()
        messages.success(request, 'Curriculum settings saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))

    if action == 'save_curriculum_module':
        title = request.POST.get('title', '').strip()
        content_html = _rich_text(request.POST.get('content_html'))
        item_id = request.POST.get('item_id')
        if not title:
            messages.error(request, 'Module title is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))
        if item_id:
            module = CurriculumModule.objects.filter(id=item_id, course=selected_course).first()
            if not module:
                messages.error(request, 'Module not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))
        else:
            module = CurriculumModule(course=selected_course, sort_order=_next_sort_order(CurriculumModule, selected_course))
        module.title = title
        module.content_html = content_html
        module.save()
        messages.success(request, 'Curriculum module saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))

    if action == 'delete_curriculum_module':
        CurriculumModule.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Module removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='curriculum'))

    if action == 'save_career_assistance':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        bullets = _clean_list(request.POST.getlist('bullets[]'))
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='career_assistance'))
        if item_id:
            assistance = CareerAssistance.objects.filter(id=item_id, course=selected_course).first()
            if not assistance:
                messages.error(request, 'Career assistance item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='career_assistance'))
        else:
            assistance = CareerAssistance(course=selected_course, sort_order=_next_sort_order(CareerAssistance, selected_course))
        assistance.title = title
        assistance.description = description
        assistance.description_list = bullets
        if image:
            assistance.image = image
        assistance.image_alt = image_alt
        assistance.save()
        messages.success(request, 'Career assistance item saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_assistance'))

    if action == 'delete_career_assistance':
        CareerAssistance.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Career assistance item removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_assistance'))

    if action == 'save_career_transition':
        name = request.POST.get('name', '').strip()
        designation = request.POST.get('designation', '').strip()
        description = request.POST.get('description', '').strip()
        placed_company = request.POST.get('placed_company', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        from_role = request.POST.get('from_role', '').strip()
        to_role = request.POST.get('to_role', '').strip()
        story_label = request.POST.get('story_label', '').strip()
        achievement_text = request.POST.get('achievement_text', '').strip()
        youtube_link = request.POST.get('youtube_testimonial_link', '').strip()
        profile_image = request.FILES.get('profile_image')
        profile_image_alt = request.POST.get('profile_image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not name or not designation or not description:
            messages.error(request, 'Name, designation, and description are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))
        if item_id:
            transition = CareerTransition.objects.filter(id=item_id, course=selected_course).first()
            if not transition:
                messages.error(request, 'Career transition not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))
        else:
            transition = CareerTransition(course=selected_course, sort_order=_next_sort_order(CareerTransition, selected_course))
        transition.name = name
        transition.designation = designation
        transition.description = description
        transition.placed_company = placed_company
        transition.job_type = job_type
        transition.from_role = from_role
        transition.to_role = to_role
        transition.story_label = story_label
        transition.achievement_text = achievement_text
        transition.youtube_testimonial_link = youtube_link
        if profile_image:
            transition.profile_image = profile_image
        transition.profile_image_alt = profile_image_alt
        transition.save()
        messages.success(request, 'Career transition saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))

    if action == 'delete_career_transition':
        CareerTransition.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Career transition removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))

    if action == 'save_career_transition_stat':
        text = request.POST.get('text', '').strip()
        icon = request.FILES.get('icon')
        icon_alt = request.POST.get('icon_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not text:
            messages.error(request, 'Stat text is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))
        if item_id:
            stat = CareerTransitionStat.objects.filter(id=item_id, course=selected_course).first()
            if not stat:
                messages.error(request, 'Career stat not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))
        else:
            stat = CareerTransitionStat(course=selected_course, sort_order=_next_sort_order(CareerTransitionStat, selected_course))
        stat.text = text
        if icon:
            stat.icon = icon
        stat.icon_alt = icon_alt
        stat.save()
        messages.success(request, 'Career stat saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))

    if action == 'delete_career_transition_stat':
        CareerTransitionStat.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Career stat removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='career_transitions'))

    if action == 'save_alumni_logo':
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not image and not item_id:
            messages.error(request, 'Please upload an alumni logo.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='alumni'))
        if item_id:
            logo = AlumniLogo.objects.filter(id=item_id, course=selected_course).first()
            if not logo:
                messages.error(request, 'Alumni logo not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='alumni'))
        else:
            logo = AlumniLogo(course=selected_course, sort_order=_next_sort_order(AlumniLogo, selected_course))
        if image:
            logo.image = image
        if image_alt:
            logo.image_alt = image_alt
        logo.save()
        messages.success(request, 'Alumni logo saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='alumni'))

    if action == 'delete_alumni_logo':
        AlumniLogo.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Alumni logo removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='alumni'))

    if action == 'save_on_campus_settings':
        section, _created = OnCampusSection.objects.get_or_create(course=selected_course)
        section.bottom_cta_text = request.POST.get('bottom_cta_text', '').strip()
        section.bottom_cta_label = request.POST.get('bottom_cta_label', '').strip()
        section.bottom_cta_url = request.POST.get('bottom_cta_url', '').strip()
        section.bottom_cta_action_type = request.POST.get('bottom_cta_action_type', 'link')
        if section.bottom_cta_label and section.bottom_cta_action_type == 'link' and not section.bottom_cta_url:
            messages.error(request, 'A URL is required when the bottom CTA action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))
        section.save()
        messages.success(request, 'On campus CTA saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))

    if action == 'save_on_campus_class':
        class_title = request.POST.get('class_title', '').strip()
        date = request.POST.get('date', '').strip()
        time = request.POST.get('time', '').strip()
        batch_type = request.POST.get('batch_type', '').strip()
        seats_left_text = request.POST.get('seats_left_text', '').strip()
        cta_label = request.POST.get('cta_label', '').strip()
        cta_url = request.POST.get('cta_url', '').strip()
        cta_action_type = request.POST.get('cta_action_type', 'link')
        item_id = request.POST.get('item_id')
        if not date or not time:
            messages.error(request, 'Date and time are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))
        if cta_label and cta_action_type == 'link' and not cta_url:
            messages.error(request, 'A URL is required when the class CTA action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))
        if item_id:
            entry = OnCampusClass.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'On-campus class not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))
        else:
            entry = OnCampusClass(course=selected_course, sort_order=_next_sort_order(OnCampusClass, selected_course))
        entry.class_title = class_title
        entry.date = date
        entry.time = time
        entry.batch_type = batch_type
        entry.seats_left_text = seats_left_text
        entry.cta_label = cta_label
        entry.cta_url = cta_url
        entry.cta_action_type = cta_action_type
        entry.save()
        messages.success(request, 'On-campus class saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))

    if action == 'delete_on_campus_class':
        OnCampusClass.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'On-campus class removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='on_campus'))

    if action == 'save_fee_structure':
        title = request.POST.get('title', '').strip()
        mode_of_training = request.POST.get('mode_of_training', '').strip()
        batch_date = request.POST.get('batch_date', '').strip()
        list_text = _clean_list(request.POST.getlist('list_text[]'))
        original_price = _get_decimal(request.POST.get('original_price'))
        discount_price = _get_decimal(request.POST.get('discount_price'))
        currency = request.POST.get('currency', 'INR').strip() or 'INR'
        cta_label = request.POST.get('cta_label', '').strip()
        cta_url = request.POST.get('cta_url', '').strip()
        cta_action_type = request.POST.get('cta_action_type', 'link')
        item_id = request.POST.get('item_id')
        if not title or not mode_of_training or not batch_date:
            messages.error(request, 'Title, mode of training, and batch date are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))
        if original_price is None or discount_price is None:
            messages.error(request, 'Prices must be valid numbers.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))
        if cta_label and cta_action_type == 'link' and not cta_url:
            messages.error(request, 'A URL is required when the fee CTA action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))
        if item_id:
            entry = FeeStructure.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Fee structure not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))
        else:
            entry = FeeStructure(course=selected_course, sort_order=_next_sort_order(FeeStructure, selected_course))
        entry.title = title
        entry.mode_of_training = mode_of_training
        entry.batch_date = batch_date
        entry.list_text = list_text
        entry.original_price = original_price
        entry.discount_price = discount_price
        entry.currency = currency
        entry.cta_label = cta_label
        entry.cta_url = cta_url
        entry.cta_action_type = cta_action_type
        entry.save()
        messages.success(request, 'Fee structure saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))

    if action == 'delete_fee_structure':
        FeeStructure.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Fee structure removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='fee_structure'))

    if action == 'save_program_for':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='program_for'))
        if item_id:
            entry = ProgramFor.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Program audience item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='program_for'))
        else:
            entry = ProgramFor(course=selected_course, sort_order=_next_sort_order(ProgramFor, selected_course))
        entry.title = title
        entry.description = description
        if image:
            entry.image = image
        entry.image_alt = image_alt
        entry.save()
        messages.success(request, 'Program audience item saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='program_for'))

    if action == 'delete_program_for':
        ProgramFor.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Program audience item removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='program_for'))

    if action == 'save_why_white_bullet':
        text = request.POST.get('text', '').strip()
        item_id = request.POST.get('item_id')
        if not text:
            messages.error(request, 'Bullet text is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))
        if item_id:
            bullet = WhyWhiteScholarsBullet.objects.filter(id=item_id, course=selected_course).first()
            if not bullet:
                messages.error(request, 'Bullet not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))
        else:
            bullet = WhyWhiteScholarsBullet(course=selected_course, sort_order=_next_sort_order(WhyWhiteScholarsBullet, selected_course))
        bullet.text = text
        bullet.save()
        messages.success(request, 'Bullet saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))

    if action == 'delete_why_white_bullet':
        WhyWhiteScholarsBullet.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Bullet removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))

    if action == 'save_why_white_image':
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not image and not item_id:
            messages.error(request, 'Please upload an image.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))
        if item_id:
            entry = WhyWhiteScholarsImage.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Image not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))
        else:
            entry = WhyWhiteScholarsImage(course=selected_course, sort_order=_next_sort_order(WhyWhiteScholarsImage, selected_course))
        if image:
            entry.image = image
        entry.image_alt = image_alt
        entry.save()
        messages.success(request, 'Image saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))

    if action == 'delete_why_white_image':
        WhyWhiteScholarsImage.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Image removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='why_white_scholars'))

    if action == 'save_expert_talk':
        youtube_url = request.POST.get('youtube_url', '').strip()
        thumbnail = request.FILES.get('thumbnail')
        thumbnail_alt = request.POST.get('thumbnail_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not youtube_url:
            messages.error(request, 'YouTube URL is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='expert_talks'))
        if item_id:
            entry = ExpertTalkVideo.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Expert talk not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='expert_talks'))
        else:
            entry = ExpertTalkVideo(course=selected_course, sort_order=_next_sort_order(ExpertTalkVideo, selected_course))
        entry.youtube_url = youtube_url
        if thumbnail:
            entry.thumbnail = thumbnail
        entry.thumbnail_alt = thumbnail_alt
        entry.save()
        messages.success(request, 'Expert talk saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='expert_talks'))

    if action == 'delete_expert_talk':
        ExpertTalkVideo.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Expert talk removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='expert_talks'))

    if action == 'save_salary_trend_settings':
        section, _created = SalaryTrendSection.objects.get_or_create(course=selected_course)
        section.source_label = request.POST.get('source_label', '').strip()
        section.description = request.POST.get('description', '').strip()
        section.save()
        messages.success(request, 'Salary trend settings saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))

    if action == 'save_salary_designation':
        name = request.POST.get('name', '').strip()
        labels = _clean_list(request.POST.getlist('labels[]'))
        min_values = _clean_list(request.POST.getlist('min_values[]'))
        max_values = _clean_list(request.POST.getlist('max_values[]'))
        item_id = request.POST.get('item_id')
        if not name:
            messages.error(request, 'Designation name is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))
        if item_id:
            entry = SalaryDesignationGroup.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Designation group not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))
        else:
            entry = SalaryDesignationGroup(course=selected_course, sort_order=_next_sort_order(SalaryDesignationGroup, selected_course))
        entry.name = name
        entry.labels = labels
        entry.min_values = min_values
        entry.max_values = max_values
        entry.save()
        messages.success(request, 'Salary designation saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))

    if action == 'delete_salary_designation':
        SalaryDesignationGroup.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Salary designation removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))

    if action == 'save_hiring_logo':
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not image and not item_id:
            messages.error(request, 'Please upload a hiring logo.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))
        if item_id:
            entry = HiringLogo.objects.filter(id=item_id, course=selected_course).first()
            if not entry:
                messages.error(request, 'Hiring logo not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))
        else:
            entry = HiringLogo(course=selected_course, sort_order=_next_sort_order(HiringLogo, selected_course))
        if image:
            entry.image = image
        entry.image_alt = image_alt
        entry.save()
        messages.success(request, 'Hiring logo saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))

    if action == 'delete_hiring_logo':
        HiringLogo.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Hiring logo removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='salary_trends'))

    if action == 'save_scope_settings':
        scope, _created = ScopeSection.objects.get_or_create(course=selected_course)
        scope.intro_html = _rich_text(request.POST.get('intro_html'))
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        if image:
            scope.image = image
        scope.image_alt = image_alt
        scope.save()
        messages.success(request, 'Scope section saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='scope'))

    if action == 'save_scope_bullet':
        text = request.POST.get('text', '').strip()
        item_id = request.POST.get('item_id')
        if not text:
            messages.error(request, 'Bullet text is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='scope'))
        if item_id:
            bullet = ScopeBullet.objects.filter(id=item_id, course=selected_course).first()
            if not bullet:
                messages.error(request, 'Scope bullet not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='scope'))
        else:
            bullet = ScopeBullet(course=selected_course, sort_order=_next_sort_order(ScopeBullet, selected_course))
        bullet.text = text
        bullet.save()
        messages.success(request, 'Scope bullet saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='scope'))

    if action == 'delete_scope_bullet':
        ScopeBullet.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Scope bullet removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='scope'))

    if action == 'save_related_articles_settings':
        section, _created = RelatedArticlesSection.objects.get_or_create(course=selected_course)
        section.load_more_label = request.POST.get('load_more_label', '').strip()
        section.load_more_url = request.POST.get('load_more_url', '').strip()
        section.load_more_action_type = request.POST.get('load_more_action_type', 'link')
        if section.load_more_label and section.load_more_action_type == 'link' and not section.load_more_url:
            messages.error(request, 'A URL is required when the Load More action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))
        section.save()
        messages.success(request, 'Related articles settings saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))

    if action == 'save_related_article':
        title = request.POST.get('title', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        link = request.POST.get('link', '').strip()
        cta_label = request.POST.get('cta_label', '').strip()
        cta_action_type = request.POST.get('cta_action_type', 'link')
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not title:
            messages.error(request, 'Title is required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))
        if cta_label and cta_action_type == 'link' and not link:
            messages.error(request, 'A URL is required when the article CTA action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))
        if item_id:
            article = RelatedArticle.objects.filter(id=item_id, course=selected_course).first()
            if not article:
                messages.error(request, 'Article not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))
        else:
            article = RelatedArticle(course=selected_course, sort_order=_next_sort_order(RelatedArticle, selected_course))
        article.title = title
        article.excerpt = excerpt
        article.link = link
        article.cta_label = cta_label
        article.cta_action_type = cta_action_type
        if image:
            article.image = image
        article.image_alt = image_alt
        article.save()
        messages.success(request, 'Related article saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))

    if action == 'delete_related_article':
        RelatedArticle.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Related article removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='related_articles'))

    if action == 'save_certification':
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        caption = request.POST.get('caption', '').strip()
        item_id = request.POST.get('item_id')
        if not image and not item_id:
            messages.error(request, 'Please upload a certification image.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='certifications'))
        if item_id:
            cert = CertificationItem.objects.filter(id=item_id, course=selected_course).first()
            if not cert:
                messages.error(request, 'Certification item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='certifications'))
        else:
            cert = CertificationItem(course=selected_course, sort_order=_next_sort_order(CertificationItem, selected_course))
        if image:
            cert.image = image
        cert.image_alt = image_alt
        cert.caption = caption
        cert.save()
        messages.success(request, 'Certification saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='certifications'))

    if action == 'delete_certification':
        CertificationItem.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Certification removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='certifications'))

    if action == 'save_review_settings':
        review, _created = ReviewSection.objects.get_or_create(course=selected_course)
        rating_value = _get_decimal(request.POST.get('rating_value'))
        total_reviews = request.POST.get('total_reviews')
        review.rating_value = rating_value
        review.total_reviews = int(total_reviews) if total_reviews else None
        review.summary_title = request.POST.get('summary_title', '').strip()
        review.summary_text = request.POST.get('summary_text', '').strip()
        review.cta_label = request.POST.get('cta_label', '').strip()
        review.cta_url = request.POST.get('cta_url', '').strip()
        review.cta_action_type = request.POST.get('cta_action_type', 'link')
        if review.cta_label and review.cta_action_type == 'link' and not review.cta_url:
            messages.error(request, 'A URL is required when the review CTA action is Link.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))
        review.save()
        messages.success(request, 'Review summary saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))

    if action == 'save_review_item':
        name = request.POST.get('name', '').strip()
        rating = request.POST.get('rating', '').strip()
        text = request.POST.get('text', '').strip()
        review_url = request.POST.get('review_url', '').strip()
        avatar = request.FILES.get('avatar')
        avatar_alt = request.POST.get('avatar_alt', '').strip()
        item_id = request.POST.get('item_id')
        if not name or not text:
            messages.error(request, 'Reviewer name and review text are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))
        if item_id:
            item = ReviewItem.objects.filter(id=item_id, course=selected_course).first()
            if not item:
                messages.error(request, 'Review item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))
        else:
            item = ReviewItem(course=selected_course, sort_order=_next_sort_order(ReviewItem, selected_course))
        item.name = name
        item.text = text
        item.rating = int(rating) if rating else item.rating
        item.review_url = review_url
        if avatar:
            item.avatar = avatar
        item.avatar_alt = avatar_alt
        item.save()
        messages.success(request, 'Review saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))

    if action == 'delete_review_item':
        ReviewItem.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'Review removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='reviews'))

    if action == 'save_faq_settings':
        faq, _created = FaqSection.objects.get_or_create(course=selected_course)
        faq.intro_text = request.POST.get('intro_text', '').strip()
        faq.save()
        messages.success(request, 'FAQ intro saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='faqs'))

    if action == 'save_faq_item':
        question = request.POST.get('question', '').strip()
        answer_html = _rich_text(request.POST.get('answer_html'))
        item_id = request.POST.get('item_id')
        if not question or not answer_html:
            messages.error(request, 'Question and answer are required.')
            return redirect(_dashboard_url(course_id=selected_course.id, section='faqs'))
        if item_id:
            item = FaqItem.objects.filter(id=item_id, course=selected_course).first()
            if not item:
                messages.error(request, 'FAQ item not found.')
                return redirect(_dashboard_url(course_id=selected_course.id, section='faqs'))
        else:
            item = FaqItem(course=selected_course, sort_order=_next_sort_order(FaqItem, selected_course))
        item.question = question
        item.answer_html = answer_html
        item.save()
        messages.success(request, 'FAQ saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='faqs'))

    if action == 'delete_faq_item':
        FaqItem.objects.filter(id=request.POST.get('item_id'), course=selected_course).delete()
        messages.success(request, 'FAQ removed.')
        return redirect(_dashboard_url(course_id=selected_course.id, section='faqs'))

    if action == 'save_lead_cta':
        cta_key = request.POST.get('cta_key', '').strip()
        heading = request.POST.get('heading', '').strip()
        description_html = _rich_text(request.POST.get('description_html'))
        image = request.FILES.get('image')
        image_alt = request.POST.get('image_alt', '').strip()
        if cta_key not in dict(LeadCta.CTA_CHOICES):
            messages.error(request, 'Invalid CTA type.')
            return redirect(_dashboard_url(course_id=selected_course.id))
        cta, _created = LeadCta.objects.get_or_create(course=selected_course, key=cta_key)
        cta.heading = heading
        cta.description_html = description_html
        if image:
            cta.image = image
        cta.image_alt = image_alt
        cta.save()
        messages.success(request, 'CTA block saved.')
        return redirect(_dashboard_url(course_id=selected_course.id, section=f'cta_{cta_key}'))

    messages.error(request, 'Unsupported action requested.')
    return redirect(_dashboard_url(course_id=selected_course.id))



def _form_error_text(form):
    errors = []
    for field, field_errors in form.errors.items():
        label = field if field != '__all__' else 'General'
        errors.append(f"{label}: {'; '.join(field_errors)}")
    return ' | '.join(errors)
# -------------------- COURSE CRUD --------------------
@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/course_list.html', {'courses': courses})

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            next_url = request.POST.get('next')
            if next_url == 'dashboard':
                messages.success(request, 'Course created. You can now fill the content.')
                return redirect(_dashboard_url(course_id=course.id))
            return redirect('course_list')
        messages.error(request, f"Could not create course: {_form_error_text(form)}")
        if request.POST.get('next') == 'dashboard':
            return redirect(_dashboard_url())
    else:
        form = CourseForm()
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Add Course'})

@login_required(login_url='login')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            next_url = request.POST.get('next')
            if next_url == 'dashboard':
                messages.success(request, 'Course settings updated.')
                return redirect(_dashboard_url(course_id=course.id))
            return redirect('course_list')
        messages.error(request, f"Could not update course: {_form_error_text(form)}")
        if request.POST.get('next') == 'dashboard':
            return redirect(_dashboard_url(course_id=course.id))
    else:
        form = CourseForm(instance=course)
    return render(request, 'course/course_form.html', {'form': form, 'title': 'Edit Course'})

@login_required(login_url='login')
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('course_list')


# -------------------- SECTION ORDER / TOGGLE --------------------
@login_required(login_url='login')
@require_POST
def reorder_sections(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    course_id = payload.get('course_id')
    order = payload.get('order', [])
    course = _get_selected_course(course_id)
    if not course:
        return JsonResponse({'error': 'Course not found'}, status=404)

    for index, key in enumerate(order):
        CourseSection.objects.filter(course=course, key=key).update(sort_order=index * 10)

    return JsonResponse({'status': 'ok'})


@login_required(login_url='login')
@require_POST
def toggle_section(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    course_id = payload.get('course_id')
    key = payload.get('key')
    is_enabled = payload.get('is_enabled')
    course = _get_selected_course(course_id)
    if not course:
        return JsonResponse({'error': 'Course not found'}, status=404)

    if key not in SECTION_META:
        return JsonResponse({'error': 'Invalid section key'}, status=400)

    CourseSection.objects.filter(course=course, key=key).update(is_enabled=bool(is_enabled))
    return JsonResponse({'status': 'ok'})


# -------------------- SECTION --------------------
@login_required(login_url='login')
def add_section(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='course-intro', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before saving the intro section.')
        return redirect(_dashboard_url(tab='course-intro'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='course-intro'))

    section_id = request.POST.get('section_id')
    instance = None
    if section_id:
        instance = Section.objects.filter(id=section_id, course=course).first()

    form = SectionForm(request.POST, request.FILES, instance=instance)
    if not form.is_valid():
        messages.error(request, f"Please fix the errors: {form.errors.as_text()}")
        return redirect(_dashboard_url(tab='course-intro', course_id=course_id))

    section = form.save(commit=False)
    section.course = course
    section.text = request.POST.get('text', '').strip()

    list_text = [item.strip() for item in request.POST.getlist('list_text[]') if item.strip()]
    section.list_text = list_text

    existing_logos = list(section.collaboration_logo or [])
    collab_files = request.FILES.getlist('collaboration_logo[]')
    if collab_files:
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'collaboration_logos'))
        uploaded_logos = []
        for file in collab_files:
            filename = fs.save(file.name, file)
            uploaded_logos.append(f'collaboration_logos/{filename}')
        section.collaboration_logo = existing_logos + uploaded_logos
    elif instance:
        section.collaboration_logo = existing_logos

    section.save()
    if instance:
        messages.success(request, 'Course intro section updated successfully.')
    else:
        messages.success(request, 'Course intro section saved successfully.')
    return redirect(_dashboard_url(tab='course-intro', course_id=course_id))


@login_required(login_url='login')
def edit_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    return redirect(_dashboard_url(tab='course-intro', course_id=section.course_id, edit_section=section.id))


@login_required(login_url='login')
def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    course_id = section.course_id
    section.delete()
    messages.success(request, 'Course intro section deleted.')
    return redirect(_dashboard_url(tab='course-intro', course_id=course_id))

# -------------------- KEY HIGHLIGHT --------------------
@login_required(login_url='login')
def add_key_highlight(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='key-highlight', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before saving the key highlight.')
        return redirect(_dashboard_url(tab='key-highlight'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='key-highlight'))

    existing_highlight = KeyHighlight.objects.filter(course=course).first()
    form = KeyHighlightForm(request.POST, request.FILES, instance=existing_highlight)

    if not form.is_valid():
        messages.error(request, f"Please fix the errors: {form.errors.as_text()}")
        return redirect(_dashboard_url(tab='key-highlight', course_id=course_id))

    highlight = form.save(commit=False)
    highlight.course = course
    highlight.save()

    messages.success(request, 'Key highlight saved successfully.')
    return redirect(_dashboard_url(tab='key-highlight', course_id=course_id))

# -------------------- ACCREDITATIONS & CERTIFICATIONS --------------------
@login_required(login_url='login')
def add_accreditation_and_certification(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='accreditations-and-certification', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding accreditations.')
        return redirect(_dashboard_url(tab='accreditations-and-certification'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='accreditations-and-certification'))

    files = request.FILES.getlist('certification_logo')
    if not files:
        messages.error(request, 'Please add at least one accreditation logo.')
        return redirect(_dashboard_url(tab='accreditations-and-certification', course_id=course_id))

    uploaded_files = []
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'accreditations_certifications'))

    for file in files:
        filename = fs.save(file.name, file)
        file_url = fs.url(os.path.join('accreditations_certifications', filename))
        uploaded_files.append(file_url)

    record, _created = AccreditationsAndCertification.objects.get_or_create(course=course)
    existing = list(record.certification_logo or [])
    record.certification_logo = existing + uploaded_files
    record.save()

    messages.success(request, 'Accreditations updated successfully.')
    return redirect(_dashboard_url(tab='accreditations-and-certification', course_id=course_id))

# -------------------- WHY CHOOSE --------------------
@login_required(login_url='login')
def add_why_choose(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='why-choose', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before saving this section.')
        return redirect(_dashboard_url(tab='why-choose'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='why-choose'))

    heading = request.POST.get('heading', '').strip()
    text_value = request.POST.get('text', '').strip()
    icon = request.FILES.get('icon')

    if not heading or not text_value:
        messages.error(request, 'Heading and description are required.')
        return redirect(_dashboard_url(tab='why-choose', course_id=course_id))

    why_choose, _created = WhyChoose.objects.get_or_create(course=course)
    why_choose.heading = heading
    why_choose.text = text_value
    if icon:
        why_choose.icon = icon
    why_choose.save()

    messages.success(request, 'Why Choose section saved successfully.')
    return redirect(_dashboard_url(tab='why-choose', course_id=course_id))

# -------------------- MENTOR --------------------
@login_required(login_url='login')
def add_mentor(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='mentors', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding a mentor.')
        return redirect(_dashboard_url(tab='mentors'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='mentors'))

    mentor_name = request.POST.get('mentor_name', '').strip()
    designation_name = request.POST.get('designation_name', '').strip()
    experience_text = request.POST.get('experience_text', '').strip()
    mentor_image = request.FILES.get('mentor_image')
    company_logo = request.FILES.get('company_logo')

    if not mentor_name or not designation_name or not experience_text:
        messages.error(request, 'Mentor name, designation, and experience are required.')
        return redirect(_dashboard_url(tab='mentors', course_id=course_id))

    Mentor.objects.create(
        course=course,
        mentor_name=mentor_name,
        designation_name=designation_name,
        experience_text=experience_text,
        mentor_image=mentor_image,
        company_logo=company_logo
    )

    messages.success(request, 'Mentor saved successfully.')
    return redirect(_dashboard_url(tab='mentors', course_id=course_id))

# -------------------- PROGRAM HIGHLIGHTS --------------------
@login_required(login_url='login')
def add_program_highlight(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='program-highlights', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding a program highlight.')
        return redirect(_dashboard_url(tab='program-highlights'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='program-highlights'))

    form = ProgramHighlightForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, f"Please fix the errors: {form.errors.as_text()}")
        return redirect(_dashboard_url(tab='program-highlights', course_id=course_id))

    text_data = form.cleaned_data.get('text')
    if text_data:
        try:
            text_data = json.loads(text_data)
        except json.JSONDecodeError:
            text_data = [text_data]
    else:
        text_data = []

    highlight = form.save(commit=False)
    highlight.text = text_data
    highlight.save()

    messages.success(request, 'Program highlight saved successfully.')
    return redirect(_dashboard_url(tab='program-highlights', course_id=course_id))

# -------------------- CAREER ASSISTANCE --------------------
@login_required(login_url='login')
def add_career_assistance(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='career-assistance', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding career assistance.')
        return redirect(_dashboard_url(tab='career-assistance'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='career-assistance'))

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    description_list = [item.strip() for item in request.POST.getlist('description_list[]') if item.strip()]
    image = request.FILES.get('image')

    if not title or not description:
        messages.error(request, 'Title and description are required.')
        return redirect(_dashboard_url(tab='career-assistance', course_id=course_id))

    CareerAssistance.objects.create(
        course=course,
        title=title,
        description=description,
        description_list=description_list,
        image=image
    )

    messages.success(request, 'Career assistance saved successfully.')
    return redirect(_dashboard_url(tab='career-assistance', course_id=course_id))

# -------------------- CAREER TRANSITION --------------------
@login_required(login_url='login')
def add_career_transition(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='career-transitions', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding a career transition.')
        return redirect(_dashboard_url(tab='career-transitions'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='career-transitions'))

    form = CareerTransitionForm(request.POST)
    if not form.is_valid():
        messages.error(request, f"Please fix the errors: {form.errors.as_text()}")
        return redirect(_dashboard_url(tab='career-transitions', course_id=course_id))

    form.save()
    messages.success(request, 'Career transition saved successfully.')
    return redirect(_dashboard_url(tab='career-transitions', course_id=course_id))

# -------------------- OUR ALUMNI --------------------
@login_required(login_url='login')
def add_our_alumni(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='our-alumni', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding alumni logos.')
        return redirect(_dashboard_url(tab='our-alumni'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='our-alumni'))

    files = request.FILES.getlist('alumni_logo[]')
    if not files:
        messages.error(request, 'Please add at least one alumni logo.')
        return redirect(_dashboard_url(tab='our-alumni', course_id=course_id))

    logo_list = []
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'alumni_logos'))
    for file in files:
        filename = fs.save(file.name, file)
        logo_list.append(f'alumni_logos/{filename}')

    OurAlumni.objects.create(course=course, alumni_logo=logo_list)
    messages.success(request, 'Alumni logos saved successfully.')
    return redirect(_dashboard_url(tab='our-alumni', course_id=course_id))

# -------------------- on campus classes --------------------
@login_required(login_url='login')
def add_on_campus_class(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='on-campus-class', course_id=request.GET.get('course')))

    course_id = request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding a class.')
        return redirect(_dashboard_url(tab='on-campus-class'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='on-campus-class'))

    class_title = request.POST.get('class_title', '').strip()
    date = request.POST.get('date')
    time = request.POST.get('time')
    batch_type = request.POST.get('batch_type', '').strip()

    if not class_title or not date or not time or not batch_type:
        messages.error(request, 'Please fill in all class details before saving.')
        return redirect(_dashboard_url(tab='on-campus-class', course_id=course_id))

    OnCampusClass.objects.create(
        course=course,
        class_title=class_title,
        date=date,
        time=time,
        batch_type=batch_type
    )

    messages.success(request, 'On-campus class saved successfully.')
    return redirect(_dashboard_url(tab='on-campus-class', course_id=course_id))

# -------------------- fee structure --------------------
@login_required(login_url='login')
def add_fee_structure(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='fee-structure', course_id=request.GET.get('course')))

    course_id = request.POST.get('course_id') or request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding a fee structure.')
        return redirect(_dashboard_url(tab='fee-structure'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='fee-structure'))

    title = request.POST.get('title', '').strip()
    mode_of_training = request.POST.get('mode_of_training', '').strip()
    batch_date = request.POST.get('batch_date', '').strip()
    list_text = [item.strip() for item in request.POST.getlist('list_text[]') if item.strip()]
    original_price_raw = request.POST.get('original_price', '').strip()
    discount_price_raw = request.POST.get('discount_price', '').strip()

    if not title or not mode_of_training or not batch_date:
        messages.error(request, 'Title, mode of training, and batch date are required.')
        return redirect(_dashboard_url(tab='fee-structure', course_id=course_id))

    try:
        original_price = Decimal(original_price_raw)
        discount_price = Decimal(discount_price_raw)
    except (InvalidOperation, ValueError):
        messages.error(request, 'Prices must be valid numbers.')
        return redirect(_dashboard_url(tab='fee-structure', course_id=course_id))

    FeeStructure.objects.create(
        course=course,
        title=title,
        mode_of_training=mode_of_training,
        list_text=list_text,
        batch_date=batch_date,
        original_price=original_price,
        discount_price=discount_price
    )

    messages.success(request, 'Fee structure saved successfully.')
    return redirect(_dashboard_url(tab='fee-structure', course_id=course_id))

# --------------------  Program for --------------------
@login_required(login_url='login')
def add_program_for(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='program-for', course_id=request.GET.get('course')))

    course_id = request.POST.get('course_id') or request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding this section.')
        return redirect(_dashboard_url(tab='program-for'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='program-for'))

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    image = request.FILES.get('image')

    if not title or not description:
        messages.error(request, 'Title and description are required.')
        return redirect(_dashboard_url(tab='program-for', course_id=course_id))

    ProgramFor.objects.create(
        course=course,
        image=image,
        title=title,
        description=description
    )

    messages.success(request, 'Program audience section saved successfully.')
    return redirect(_dashboard_url(tab='program-for', course_id=course_id))

# -------------------- why white scholars --------------------
@login_required(login_url='login')
def add_why_white_scholars(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='why-white-scholars', course_id=request.GET.get('course')))

    course_id = request.POST.get('course_id') or request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding this section.')
        return redirect(_dashboard_url(tab='why-white-scholars'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='why-white-scholars'))

    description = request.POST.get('description', '').strip()
    images = request.FILES.getlist('images[]')

    if not description:
        messages.error(request, 'Description is required.')
        return redirect(_dashboard_url(tab='why-white-scholars', course_id=course_id))

    image_paths = []
    if images:
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'why_white_scholars_images'))
        for image in images:
            filename = fs.save(image.name, image)
            image_paths.append(f'why_white_scholars_images/{filename}')

    WhyWhiteScholars.objects.create(
        course=course,
        description=description,
        images=image_paths
    )

    messages.success(request, 'Why WhiteScholars section saved successfully.')
    return redirect(_dashboard_url(tab='why-white-scholars', course_id=course_id))

# -------------------- Listen Our Expert --------------------
@login_required(login_url='login')
def add_listen_our_expert(request):
    if request.method != 'POST':
        return redirect(_dashboard_url(tab='listen-our-expert', course_id=request.GET.get('course')))

    course_id = request.POST.get('course_id') or request.POST.get('course')
    if not course_id:
        messages.error(request, 'Select a course before adding expert videos.')
        return redirect(_dashboard_url(tab='listen-our-expert'))

    course = _get_selected_course(course_id)
    if not course:
        messages.error(request, 'The selected course was not found.')
        return redirect(_dashboard_url(tab='listen-our-expert'))

    title = request.POST.get('title', '').strip()
    youtube_links = [link.strip() for link in request.POST.getlist('youtube_links[]') if link.strip()]

    if not title or not youtube_links:
        messages.error(request, 'Title and at least one YouTube link are required.')
        return redirect(_dashboard_url(tab='listen-our-expert', course_id=course_id))

    ListenOurExpert.objects.create(
        course=course,
        title=title,
        youtube_links=youtube_links
    )

    messages.success(request, 'Expert videos saved successfully.')
    return redirect(_dashboard_url(tab='listen-our-expert', course_id=course_id))
