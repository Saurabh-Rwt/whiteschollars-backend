from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)
    meta_og_image = models.ImageField(upload_to='seo_images/', blank=True, null=True)
    brochure_pdf = models.FileField(upload_to='brochures/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.name


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    section_heading = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    list_text = models.JSONField(blank=True, null=True)
    collaboration_logo = models.JSONField(blank=True, null=True)
    youtube_video = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'course_intro'

    def __str__(self):
        return f"{self.course.name} - {self.section_heading}"


class KeyHighlight(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='key_highlights')
    logo = models.ImageField(upload_to='key_highlights/', blank=True, null=True)
    logo_alt = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'key_highlight'

    def __str__(self):
        return f"{self.course.name} - {self.text[:30] if self.text else 'No text'}"


class AccreditationsAndCertification(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='accreditations_certifications'
    )
    certification_logo = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'accreditationsandcertification'


class AccreditationLogo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='accreditation_logos')
    image = models.ImageField(upload_to='accreditations_certifications/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'accreditation_logos'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Accreditation Logo"

class WhyChoose(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='why_choose_items'
    )
    icon = models.ImageField(upload_to='why_choose_icons/', blank=True, null=True)
    icon_alt = models.CharField(max_length=255, blank=True)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.name} - {self.heading}"

    class Meta:
        db_table = 'why_choose'

class Mentor(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='mentors'
    )
    mentor_image = models.ImageField(upload_to='mentors/', blank=True, null=True)
    mentor_image_alt = models.CharField(max_length=255, blank=True)
    mentor_name = models.CharField(max_length=255)
    designation_name = models.CharField(max_length=255)
    experience_text = models.TextField()
    company_logo = models.ImageField(upload_to='mentor_company_logos/', blank=True, null=True)
    company_logo_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.mentor_name} ({self.designation_name})"

    class Meta:
        db_table = 'mentors'

class ProgramHighlight(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='program_highlights')
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    text = models.JSONField(default=list, blank=True)
    description_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='program_highlights/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'program_highlights'

    def __str__(self):
        return self.title

class CareerAssistance(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='career_assistances')
    title = models.CharField(max_length=255)
    description = models.TextField()  # long text
    description_list = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='career_assistance/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_assistance'

    def __str__(self):
        return self.title

class CareerTransition(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='career_transitions')
    profile_image = models.ImageField(upload_to='career_transitions/', blank=True, null=True)
    profile_image_alt = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    achievement_text = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    placed_company = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    from_role = models.CharField(max_length=255, blank=True)
    to_role = models.CharField(max_length=255, blank=True)
    story_label = models.CharField(max_length=100, blank=True)
    youtube_testimonial_link = models.URLField(max_length=500, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_transitions'

    def __str__(self):
        return f"{self.name} - {self.placed_company}"

class OurAlumni(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='our_alumni')
    alumni_logo = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'our_alumni'

    def __str__(self):
        return f"Our Alumni - {self.course.name}"

class OnCampusClass(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='on_campus_classes')
    class_title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField()
    time = models.CharField(max_length=100)
    batch_type = models.CharField(max_length=100)
    seats_left_text = models.CharField(max_length=100, blank=True)
    cta_label = models.CharField(max_length=100, blank=True)
    cta_url = models.URLField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'on_campus_classes'

    def __str__(self):
        return f"{self.course.name} - {self.class_title} ({self.batch_type})"
        
class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='fee_structures')
    title = models.CharField(max_length=255)
    mode_of_training = models.CharField(max_length=255) 
    list_text = models.JSONField(default=list, blank=True)
    batch_date = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, blank=True, default='INR')
    cta_label = models.CharField(max_length=100, blank=True)
    cta_url = models.URLField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'fee_structures'

    def __str__(self):
        return f"{self.title} - {self.mode_of_training}"


class ProgramFor(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='program_for'
    )
    image = models.ImageField(upload_to='program_for_images/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'program_for'

    def __str__(self):
        return f"{self.course.name} - {self.title}"

class WhyWhiteScholars(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='why_white_scholars'
    )
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'why_white_scholars'

    def __str__(self):
        return f"{self.course.name} - Why WhiteScholars"

class ListenOurExpert(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='listen_our_experts')
    title = models.CharField(max_length=255)
    youtube_links = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'listen_our_expert'

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class CourseSection(models.Model):
    SECTION_CHOICES = [
        ('hero', 'Hero'),
        ('key_highlights', 'Key Highlights'),
        ('accreditations', 'Accreditations'),
        ('why_choose', 'Why Choose'),
        ('live_demo', 'Live Demo CTA'),
        ('course_overview', 'Course Overview'),
        ('mentors', 'Mentors'),
        ('program_highlights', 'Program Highlights'),
        ('learner_journey', 'Learner Journey'),
        ('curriculum', 'Curriculum'),
        ('career_assistance', 'Career Assistance'),
        ('career_transitions', 'Career Transitions'),
        ('alumni', 'Our Alumni'),
        ('on_campus', 'On Campus Classes'),
        ('fee_structure', 'Fee Structure'),
        ('program_for', 'Program For'),
        ('why_white_scholars', 'Why WhiteScholars'),
        ('expert_talks', 'Expert Talks'),
        ('salary_trends', 'Salary Trends'),
        ('scope', 'Scope'),
        ('related_articles', 'Related Articles'),
        ('certifications', 'Certifications'),
        ('reviews', 'Reviews'),
        ('faqs', 'FAQs'),
        ('cta_ready', 'CTA Ready'),
        ('cta_discover', 'CTA Discover'),
        ('cta_confused', 'CTA Confused'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='section_order')
    key = models.CharField(max_length=50, choices=SECTION_CHOICES)
    is_enabled = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'course_sections'
        unique_together = ('course', 'key')
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.key}"


class CourseHero(models.Model):
    MEDIA_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='hero')
    badge_text = models.CharField(max_length=100, blank=True)
    badge_icon = models.ImageField(upload_to='hero_badges/', blank=True, null=True)
    badge_icon_alt = models.CharField(max_length=255, blank=True)
    award_text = models.CharField(max_length=255, blank=True)
    award_logo = models.ImageField(upload_to='hero_awards/', blank=True, null=True)
    award_logo_alt = models.CharField(max_length=255, blank=True)
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255, blank=True)
    description_html = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_CHOICES, default='image')
    hero_image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    hero_image_alt = models.CharField(max_length=255, blank=True)
    hero_video_url = models.URLField(max_length=500, blank=True)
    hero_video_thumbnail = models.ImageField(upload_to='hero_videos/', blank=True, null=True)
    hero_video_thumbnail_alt = models.CharField(max_length=255, blank=True)
    collaboration_heading = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'course_hero'

    def __str__(self):
        return f"{self.course.name} - Hero"


class HeroHighlight(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='hero_highlights')
    text = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'hero_highlights'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.text[:40]}"


class HeroCollaborationLogo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='hero_collaboration_logos')
    image = models.ImageField(upload_to='collaboration_logos/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'hero_collaboration_logos'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Collaboration Logo"


class CourseHeroButton(models.Model):
    STYLE_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('ghost', 'Ghost'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='hero_buttons')
    label = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='primary')
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'hero_buttons'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.label}"


class LiveDemoCta(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='live_demo_cta')
    heading = models.CharField(max_length=255)
    button_label = models.CharField(max_length=100)
    button_url = models.URLField(max_length=500)

    class Meta:
        db_table = 'live_demo_cta'

    def __str__(self):
        return f"{self.course.name} - Live Demo"


class CourseOverview(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='course_overview')
    intro_html = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'course_overview'

    def __str__(self):
        return f"{self.course.name} - Overview"


class CourseOverviewItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_overview_items')
    question = models.CharField(max_length=255)
    answer_html = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'course_overview_items'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.question[:40]}"


class LearnerJourney(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='learner_journey')
    image = models.ImageField(upload_to='learner_journey/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'learner_journey'

    def __str__(self):
        return f"{self.course.name} - Learner Journey"


class CurriculumSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='curriculum_section')
    call_us_title = models.CharField(max_length=255, blank=True)
    call_us_phone = models.CharField(max_length=50, blank=True)
    call_us_button_label = models.CharField(max_length=100, blank=True)
    call_us_button_url = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'curriculum_section'

    def __str__(self):
        return f"{self.course.name} - Curriculum"


class CurriculumModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculum_modules')
    title = models.CharField(max_length=255)
    content_html = models.TextField(blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'curriculum_modules'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class CareerTransitionStat(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='career_transition_stats')
    icon = models.ImageField(upload_to='career_transition_stats/', blank=True, null=True)
    icon_alt = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'career_transition_stats'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.text}"


class AlumniLogo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='alumni_logos')
    image = models.ImageField(upload_to='alumni_logos/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'alumni_logos'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Alumni Logo"


class OnCampusSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='on_campus_section')
    bottom_cta_text = models.CharField(max_length=255, blank=True)
    bottom_cta_label = models.CharField(max_length=100, blank=True)
    bottom_cta_url = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'on_campus_section'

    def __str__(self):
        return f"{self.course.name} - On Campus Section"


class WhyWhiteScholarsBullet(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='why_white_scholars_bullets')
    text = models.CharField(max_length=500)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'why_white_scholars_bullets'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Bullet"


class WhyWhiteScholarsImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='why_white_scholars_images')
    image = models.ImageField(upload_to='why_white_scholars_images/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'why_white_scholars_images'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Image"


class ExpertTalkVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='expert_talk_videos')
    youtube_url = models.URLField(max_length=500)
    thumbnail = models.ImageField(upload_to='expert_talks/', blank=True, null=True)
    thumbnail_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'expert_talk_videos'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Expert Talk"


class SalaryTrendSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='salary_trend_section')
    source_label = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'salary_trend_section'

    def __str__(self):
        return f"{self.course.name} - Salary Trends"


class SalaryDesignationGroup(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='salary_designations')
    name = models.CharField(max_length=255)
    labels = models.JSONField(default=list, blank=True)
    min_values = models.JSONField(default=list, blank=True)
    max_values = models.JSONField(default=list, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'salary_designations'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class HiringLogo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='hiring_logos')
    image = models.ImageField(upload_to='hiring_logos/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'hiring_logos'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Hiring Logo"


class ScopeSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='scope_section')
    intro_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='scope_images/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'scope_section'

    def __str__(self):
        return f"{self.course.name} - Scope"


class ScopeBullet(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='scope_bullets')
    text = models.CharField(max_length=500)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'scope_bullets'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Scope Bullet"


class RelatedArticlesSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='related_articles_section')
    load_more_label = models.CharField(max_length=100, blank=True)
    load_more_url = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'related_articles_section'

    def __str__(self):
        return f"{self.course.name} - Related Articles"


class RelatedArticle(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='related_articles')
    title = models.CharField(max_length=255)
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='related_articles/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    link = models.URLField(max_length=500, blank=True)
    cta_label = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'related_articles'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class CertificationItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certifications')
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'certifications'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - Certification"


class ReviewSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='review_section')
    rating_value = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    total_reviews = models.PositiveIntegerField(blank=True, null=True)
    summary_title = models.CharField(max_length=255, blank=True)
    summary_text = models.CharField(max_length=500, blank=True)
    cta_label = models.CharField(max_length=100, blank=True)
    cta_url = models.URLField(max_length=500, blank=True)

    class Meta:
        db_table = 'review_section'

    def __str__(self):
        return f"{self.course.name} - Reviews"


class ReviewItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='review_items')
    name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(default=5)
    text = models.TextField()
    avatar = models.ImageField(upload_to='reviews/', blank=True, null=True)
    avatar_alt = models.CharField(max_length=255, blank=True)
    review_url = models.URLField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'review_items'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class FaqSection(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='faq_section')
    intro_text = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = 'faq_section'

    def __str__(self):
        return f"{self.course.name} - FAQ"


class FaqItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faq_items')
    question = models.CharField(max_length=255)
    answer_html = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'faq_items'
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.course.name} - {self.question[:40]}"


class LeadCta(models.Model):
    CTA_CHOICES = [
        ('ready', 'Ready to Start'),
        ('discover', 'Discover Secrets'),
        ('confused', 'Still Confused'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lead_ctas')
    key = models.CharField(max_length=20, choices=CTA_CHOICES)
    heading = models.CharField(max_length=255, blank=True)
    description_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='lead_ctas/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'lead_ctas'
        unique_together = ('course', 'key')

    def __str__(self):
        return f"{self.course.name} - {self.key}"
