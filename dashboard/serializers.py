from rest_framework import serializers
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
    OurAlumni,
    OnCampusClass,
    FeeStructure,
    ProgramFor,
    WhyWhiteScholars,
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
    CareerTransitionStat,
    AlumniLogo,
    OnCampusSection,
    WhyWhiteScholarsBullet,
    WhyWhiteScholarsImage,
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

# ----------------- Basic Serializers -----------------

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class KeyHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyHighlight
        fields = '__all__'

class AccreditationsAndCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditationsAndCertification
        fields = '__all__'

class AccreditationLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditationLogo
        fields = '__all__'

class WhyChooseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChoose
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'

class ProgramHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramHighlight
        fields = '__all__'

class CareerAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAssistance
        fields = '__all__'

class CareerTransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTransition
        fields = '__all__'

class OurAlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurAlumni
        fields = '__all__'

class OnCampusClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnCampusClass
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class ProgramForSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramFor
        fields = '__all__'

class WhyWhiteScholarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyWhiteScholars
        fields = '__all__'

class ListenOurExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListenOurExpert
        fields = '__all__'


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = '__all__'


class CourseHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseHero
        fields = '__all__'


class HeroHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroHighlight
        fields = '__all__'


class HeroCollaborationLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroCollaborationLogo
        fields = '__all__'


class CourseHeroButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseHeroButton
        fields = '__all__'


class LiveDemoCtaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveDemoCta
        fields = '__all__'


class CourseOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOverview
        fields = '__all__'


class CourseOverviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOverviewItem
        fields = '__all__'


class LearnerJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerJourney
        fields = '__all__'


class CurriculumSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumSection
        fields = '__all__'


class CurriculumModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumModule
        fields = '__all__'


class CareerTransitionStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerTransitionStat
        fields = '__all__'


class AlumniLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniLogo
        fields = '__all__'


class OnCampusSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnCampusSection
        fields = '__all__'


class WhyWhiteScholarsBulletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyWhiteScholarsBullet
        fields = '__all__'


class WhyWhiteScholarsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyWhiteScholarsImage
        fields = '__all__'


class ExpertTalkVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertTalkVideo
        fields = '__all__'


class SalaryTrendSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryTrendSection
        fields = '__all__'


class SalaryDesignationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDesignationGroup
        fields = '__all__'


class HiringLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringLogo
        fields = '__all__'


class ScopeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeSection
        fields = '__all__'


class ScopeBulletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeBullet
        fields = '__all__'


class RelatedArticlesSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedArticlesSection
        fields = '__all__'


class RelatedArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedArticle
        fields = '__all__'


class CertificationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificationItem
        fields = '__all__'


class ReviewSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewSection
        fields = '__all__'


class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewItem
        fields = '__all__'


class FaqSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqSection
        fields = '__all__'


class FaqItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqItem
        fields = '__all__'


class LeadCtaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadCta
        fields = '__all__'


class CoursePopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePopup
        fields = '__all__'

# ----------------- Course Serializers -----------------

class CourseSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='meta_description',
        allow_blank=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'slug', 'description', 'created_at']


# ----------------- Full Course Detail Serializer -----------------

class CourseFullDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='meta_description',
        allow_blank=True,
        allow_null=True,
        required=False
    )
    sections = SectionSerializer(many=True, read_only=True)
    key_highlights = KeyHighlightSerializer(many=True, read_only=True)
    accreditations_certifications = AccreditationsAndCertificationSerializer(many=True, read_only=True)
    why_choose_items = WhyChooseSerializer(many=True, read_only=True)
    mentors = MentorSerializer(many=True, read_only=True)
    program_highlights = ProgramHighlightSerializer(many=True, read_only=True)
    career_assistances = CareerAssistanceSerializer(many=True, read_only=True)
    career_transitions = CareerTransitionSerializer(many=True, read_only=True)
    our_alumni = OurAlumniSerializer(many=True, read_only=True)
    on_campus_classes = OnCampusClassSerializer(many=True, read_only=True)
    fee_structures = FeeStructureSerializer(many=True, read_only=True)
    program_for = ProgramForSerializer(many=True, read_only=True)
    why_white_scholars = WhyWhiteScholarsSerializer(many=True, read_only=True)
    listen_our_experts = ListenOurExpertSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description',
            'sections', 'key_highlights', 'accreditations_certifications',
            'why_choose_items', 'mentors', 'program_highlights',
            'career_assistances', 'career_transitions', 'our_alumni',
            'on_campus_classes', 'fee_structures', 'program_for',
            'why_white_scholars', 'listen_our_experts'
        ]


class CoursePageSerializer(serializers.ModelSerializer):
    description = serializers.CharField(
        source='meta_description',
        allow_blank=True,
        allow_null=True,
        required=False
    )

    section_order = CourseSectionSerializer(many=True, read_only=True)
    hero = CourseHeroSerializer(read_only=True)
    hero_highlights = HeroHighlightSerializer(many=True, read_only=True)
    hero_collaboration_logos = HeroCollaborationLogoSerializer(many=True, read_only=True)
    hero_buttons = CourseHeroButtonSerializer(many=True, read_only=True)
    key_highlights = KeyHighlightSerializer(many=True, read_only=True)
    accreditation_logos = AccreditationLogoSerializer(many=True, read_only=True)
    why_choose_items = WhyChooseSerializer(many=True, read_only=True)
    live_demo_cta = LiveDemoCtaSerializer(read_only=True)
    course_overview = CourseOverviewSerializer(read_only=True)
    course_overview_items = CourseOverviewItemSerializer(many=True, read_only=True)
    mentors = MentorSerializer(many=True, read_only=True)
    program_highlights = ProgramHighlightSerializer(many=True, read_only=True)
    learner_journey = LearnerJourneySerializer(read_only=True)
    curriculum_section = CurriculumSectionSerializer(read_only=True)
    curriculum_modules = CurriculumModuleSerializer(many=True, read_only=True)
    career_assistances = CareerAssistanceSerializer(many=True, read_only=True)
    career_transitions = CareerTransitionSerializer(many=True, read_only=True)
    career_transition_stats = CareerTransitionStatSerializer(many=True, read_only=True)
    alumni_logos = AlumniLogoSerializer(many=True, read_only=True)
    on_campus_section = OnCampusSectionSerializer(read_only=True)
    on_campus_classes = OnCampusClassSerializer(many=True, read_only=True)
    fee_structures = FeeStructureSerializer(many=True, read_only=True)
    program_for = ProgramForSerializer(many=True, read_only=True)
    why_white_scholars_bullets = WhyWhiteScholarsBulletSerializer(many=True, read_only=True)
    why_white_scholars_images = WhyWhiteScholarsImageSerializer(many=True, read_only=True)
    expert_talk_videos = ExpertTalkVideoSerializer(many=True, read_only=True)
    salary_trend_section = SalaryTrendSectionSerializer(read_only=True)
    salary_designations = SalaryDesignationGroupSerializer(many=True, read_only=True)
    hiring_logos = HiringLogoSerializer(many=True, read_only=True)
    scope_section = ScopeSectionSerializer(read_only=True)
    scope_bullets = ScopeBulletSerializer(many=True, read_only=True)
    related_articles_section = RelatedArticlesSectionSerializer(read_only=True)
    related_articles = RelatedArticleSerializer(many=True, read_only=True)
    certifications = CertificationItemSerializer(many=True, read_only=True)
    review_section = ReviewSectionSerializer(read_only=True)
    review_items = ReviewItemSerializer(many=True, read_only=True)
    faq_section = FaqSectionSerializer(read_only=True)
    faq_items = FaqItemSerializer(many=True, read_only=True)
    lead_ctas = LeadCtaSerializer(many=True, read_only=True)
    popup_modal = CoursePopupSerializer(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'slug',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'meta_og_image',
            'brochure_pdf',
            'description',
            'section_order',
            'hero',
            'hero_highlights',
            'hero_collaboration_logos',
            'hero_buttons',
            'key_highlights',
            'accreditation_logos',
            'why_choose_items',
            'live_demo_cta',
            'course_overview',
            'course_overview_items',
            'mentors',
            'program_highlights',
            'learner_journey',
            'curriculum_section',
            'curriculum_modules',
            'career_assistances',
            'career_transitions',
            'career_transition_stats',
            'alumni_logos',
            'on_campus_section',
            'on_campus_classes',
            'fee_structures',
            'program_for',
            'why_white_scholars_bullets',
            'why_white_scholars_images',
            'expert_talk_videos',
            'salary_trend_section',
            'salary_designations',
            'hiring_logos',
            'scope_section',
            'scope_bullets',
            'related_articles_section',
            'related_articles',
            'certifications',
            'review_section',
            'review_items',
            'faq_section',
            'faq_items',
            'lead_ctas',
            'popup_modal',
        ]
