# Generated by Django 4.2.7 on 2024-06-20 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0056_alter_animalform_status_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalform',
            name='feedback_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='animalform',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
