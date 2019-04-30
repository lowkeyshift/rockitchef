# Run gunicorn from Linux server
gunicorn --access-logfile - --workers 3 --bind unix:/home/rockitchef/django_rockitchef/rockitchef_project/rockitchef_project.sock rockitchef_project.wsgi:application
