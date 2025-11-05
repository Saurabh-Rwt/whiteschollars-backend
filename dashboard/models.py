from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
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