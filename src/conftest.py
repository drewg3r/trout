import pytest

from django.conf import settings
from django.core.management import call_command


@pytest.fixture
def example_data(db):
    """Use this fixture to populate database with fixture data"""
    call_command('loaddata', settings.BASE_DIR / 'trout/fixtures/test_data.json')