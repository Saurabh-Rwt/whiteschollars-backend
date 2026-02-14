from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_careerassistance_image_alt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseherobutton',
            name='url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='livedemocta',
            name='button_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='courseherobutton',
            name='action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='livedemocta',
            name='button_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='curriculumsection',
            name='call_us_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='oncampusclass',
            name='cta_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='oncampussection',
            name='bottom_cta_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='feestructure',
            name='cta_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='relatedarticlessection',
            name='load_more_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='relatedarticle',
            name='cta_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.AddField(
            model_name='reviewsection',
            name='cta_action_type',
            field=models.CharField(choices=[('link', 'Link'), ('modal', 'Modal')], default='link', max_length=20),
        ),
        migrations.CreateModel(
            name='CoursePopup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_popups/')),
                ('image_alt', models.CharField(blank=True, max_length=255)),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='popup_modal', to='dashboard.course')),
            ],
            options={
                'db_table': 'course_popups',
            },
        ),
    ]
