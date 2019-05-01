# Generated by Django 2.1.7 on 2019-05-01 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0003_auto_20190501_0323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RemoveField(
            model_name='direction',
            name='directions_json',
        ),
        migrations.RemoveField(
            model_name='direction',
            name='recipe',
        ),
        migrations.AddField(
            model_name='direction',
            name='direction_text',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.ManyToManyField(to='recipes_app.Direction'),
        ),
    ]
