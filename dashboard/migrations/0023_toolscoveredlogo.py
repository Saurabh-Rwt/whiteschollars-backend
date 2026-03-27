from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_careerassistance_media_type_and_video_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolsCoveredLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='tools_covered/')),
                ('image_alt', models.CharField(blank=True, max_length=255)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tools_covered_logos', to='dashboard.course')),
            ],
            options={
                'db_table': 'tools_covered_logos',
                'ordering': ['sort_order'],
            },
        ),
        migrations.AlterField(
            model_name='coursesection',
            name='key',
            field=models.CharField(
                choices=[
                    ('hero', 'Hero'),
                    ('key_highlights', 'Key Highlights'),
                    ('accreditations', 'Accreditations'),
                    ('why_choose', 'Why Choose'),
                    ('live_demo', 'Live Demo CTA'),
                    ('course_overview', 'Course Overview'),
                    ('tools_covered', 'Tools Covered'),
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
                ],
                max_length=50,
            ),
        ),
    ]
