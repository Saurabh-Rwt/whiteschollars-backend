from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=500, blank=True, null=True)
    meta_og_image = models.ImageField(upload_to='seo_images/', blank=True, null=True)

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
    text = models.TextField(blank=True, null=True)
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

class WhyChoose(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='why_choose_items'
    )
    icon = models.ImageField(upload_to='why_choose_icons/', blank=True, null=True)
    heading = models.CharField(max_length=255)
    text = models.TextField()

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
    mentor_name = models.CharField(max_length=255)
    designation_name = models.CharField(max_length=255)
    experience_text = models.TextField()
    company_logo = models.ImageField(upload_to='mentor_company_logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.mentor_name} ({self.designation_name})"

    class Meta:
        db_table = 'mentors'

class ProgramHighlight(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='program_highlights')
    title = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    text = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='program_highlights/', blank=True, null=True)

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

    class Meta:
        db_table = 'career_assistance'

    def __str__(self):
        return self.title

class CareerTransition(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='career_transitions')
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    description = models.TextField()
    placed_company = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    youtube_testimonial_link = models.URLField(max_length=500, blank=True, null=True)

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

    class Meta:
        db_table = 'on_campus_classes'

    def __str__(self):
        return f"{self.course.title} - {self.class_title} ({self.batch_type})"
        
class FeeStructure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='fee_structures')
    title = models.CharField(max_length=255)
    mode_of_training = models.CharField(max_length=255) 
    list_text = models.JSONField(default=list, blank=True)
    batch_date = models.CharField(max_length=255)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)

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
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'program_for'

    def __str__(self):
        return f"{self.course.title} - {self.title}"

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
        return f"{self.course.title} - Why WhiteScholars"

class ListenOurExpert(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='listen_our_experts')
    title = models.CharField(max_length=255)
    youtube_links = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'listen_our_expert'

    def __str__(self):
        return f"{self.course.title} - {self.title}"