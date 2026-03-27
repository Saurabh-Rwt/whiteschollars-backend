from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_toolscoveredlogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsCovered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects_covered/')),
                ('image_alt', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects_covered', to='dashboard.course')),
            ],
            options={
                'db_table': 'projects_covered',
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
                    ('projects_covered', 'Projects Covered'),
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
