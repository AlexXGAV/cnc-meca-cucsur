# Generated by Django 4.2.2 on 2023-08-01 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teammate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('second_name', models.CharField(blank=True, max_length=30, null=True)),
                ('first_last_name', models.CharField(max_length=40)),
                ('second_last_name', models.CharField(max_length=40)),
                ('career', models.CharField(max_length=40)),
                ('image', models.ImageField(upload_to='img/team')),
                ('twitter_url', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('instagram_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'compañero de equipo',
                'verbose_name_plural': 'compañeros de equipo',
            },
        ),
    ]
