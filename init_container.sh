    #!/bin/bash
    set -e
    echo "Starting init_container.sh"
    # Ensure DB env vars exist (basic check)
    if [ -z "$DB_HOST" ]; then
      echo "Warning: DB_HOST not set. You should set DB_* env vars in Render."
    fi

    # Run migrations & collectstatic
    echo "Running migrations..."
    python backend/manage.py migrate --noinput || true
    echo "Collecting static..."
    python backend/manage.py collectstatic --noinput || true

    # Create sample superuser if not exists (username: admin, password: adminpass)
    echo "from django.contrib.auth import get_user_model; User=get_user_model();    username='admin';    password='adminpass';    email='admin@example.com';    u=User.objects.filter(username=username).first();    u and print('superuser exists') or User.objects.create_superuser(username, email, password)" | python - <<'PY'
import sys
from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py','shell'])
PY || true

    # Create sample repo via Django ORM if not exists
    echo "Creating sample repository..."
    python - <<'PY'
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
django.setup()
from django.contrib.auth import get_user_model
from apps.gitserver.models import Repository
User=get_user_model()
user=User.objects.filter(username='admin').first()
if user:
    if not Repository.objects.filter(owner=user,name='hello-world').exists():
        repo=Repository.objects.create(owner=user,name='hello-world',description='Sample repo',is_private=False)
        print('Created repo record')
        # initialize bare repo on disk using git_utils
        from apps.gitserver.git_utils import init_bare_repo
        init_bare_repo(user.username, 'hello-world')
        print('Initialized bare git repo')
else:
    print('admin user missing')
PY

    echo "Initialization complete. Starting supervisord..."
    /usr/bin/supervisord -n -c /app/supervisord.conf
