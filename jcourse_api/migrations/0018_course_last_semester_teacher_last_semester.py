# Generated by Django 4.0.1 on 2022-01-07 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('jcourse_api', '0017_review_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='last_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='jcourse_api.semester', verbose_name='最后更新学期'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='last_semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='jcourse_api.semester', verbose_name='最后更新学期'),
        ),
    ]
