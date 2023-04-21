from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.auth import get_user_model


def test_superuser_creation(db):
    call_command('set_superuser', username='admin', password='password')
    admin: User = get_user_model().objects.get(username='admin')
    assert admin.is_staff
    assert admin.is_superuser
    assert admin.check_password('password')


def test_superuser_password_update(db):
    admin: User = get_user_model().objects.create_superuser(
        username='admin', email='admin@admin.com', password='password'
    )
    call_command('set_superuser', username='admin', password='password2')
    admin.refresh_from_db()
    assert admin.check_password('password2')
