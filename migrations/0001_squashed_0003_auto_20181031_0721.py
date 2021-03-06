# Generated by Django 2.1.2 on 2018-11-01 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('profiles', '0001_initial'), ('profiles', '0002_auto_20181030_1444'), ('profiles', '0003_auto_20181031_0721')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bio', models.TextField(blank=True)),
                ('image', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-created_by', '-updated_by'],
                'abstract': False,
            },
        ),
    ]
