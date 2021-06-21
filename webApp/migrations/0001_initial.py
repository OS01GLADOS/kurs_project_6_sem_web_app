# Generated by Django 3.2.2 on 2021-05-13 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.CharField(max_length=100)),
                ('header', models.CharField(max_length=100)),
                ('Message', models.CharField(max_length=1000)),
                ('Is_replyed', models.BooleanField(default=False)),
                ('Reply_header', models.CharField(blank=True, max_length=200)),
                ('Reply_text', models.CharField(blank=True, max_length=2000)),
                ('Replyed_by', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=100)),
                ('Preambule', models.CharField(max_length=100)),
                ('Text', models.CharField(max_length=4000)),
                ('Photo', models.ImageField(upload_to='images')),
                ('Liked', models.IntegerField(default=0)),
                ('Disliked', models.IntegerField(default=0)),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now_add=True)),
                ('Hidden', models.BooleanField(default=False)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
