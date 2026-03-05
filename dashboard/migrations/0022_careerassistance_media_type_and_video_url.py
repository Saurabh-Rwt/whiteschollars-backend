from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_courseherobutton_icon_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerassistance',
            name='media_type',
            field=models.CharField(
                choices=[('image', 'Image'), ('video', 'Video')],
                default='image',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='careerassistance',
            name='youtube_video_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
