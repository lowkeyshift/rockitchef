# Generated by Django 2.1.7 on 2019-05-29 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chef_url', models.URLField(blank=True, default='', max_length=500)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Crawled',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crawled_url', models.URLField(blank=True, default='', max_length=500)),
                ('source', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction_text', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_item', models.CharField(max_length=200)),
                ('qty', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, help_text='User bio of themselves.', max_length=500)),
                ('diet', models.CharField(blank=True, max_length=100)),
                ('saved_recipes', models.IntegerField(blank=True)),
                ('subscribed_chefs', models.IntegerField(blank=True)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('connected_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('inventory', models.ManyToManyField(blank=True, to='recipes_app.Inventory')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('recipe_url', models.URLField(blank=True, default='', max_length=500, unique=True)),
                ('prep_time', models.CharField(max_length=10)),
                ('cook_time', models.CharField(max_length=10)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_app.Chef')),
                ('directions', models.ManyToManyField(to='recipes_app.Direction')),
                ('ingredients', models.ManyToManyField(to='recipes_app.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='TaggedFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes_app.Recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_app_taggedfood_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='recipes_app.TaggedFood', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
