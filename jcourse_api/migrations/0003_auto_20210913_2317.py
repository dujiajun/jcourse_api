# Generated by Django 3.2.3 on 2021-09-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jcourse_api', '0002_report_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='formercode',
            name='old_code',
            field=models.CharField(max_length=32, unique=True, verbose_name='旧课号'),
        ),
        migrations.AddConstraint(
            model_name='action',
            constraint=models.UniqueConstraint(fields=('user', 'review'), name='unique_action'),
        ),
    ]
