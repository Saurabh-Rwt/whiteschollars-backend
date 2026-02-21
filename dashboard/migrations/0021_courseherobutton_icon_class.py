from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_button_actions_and_course_popup'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseherobutton',
            name='icon_class',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
