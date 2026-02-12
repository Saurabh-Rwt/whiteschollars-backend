from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Course, CourseSection


@receiver(post_save, sender=Course)
def ensure_course_sections(sender, instance, created, **kwargs):
    if not created:
        return
    existing = set(
        CourseSection.objects.filter(course=instance).values_list('key', flat=True)
    )
    for index, (key, _label) in enumerate(CourseSection.SECTION_CHOICES):
        if key in existing:
            continue
        CourseSection.objects.create(
            course=instance,
            key=key,
            sort_order=index,
        )
