import pytest
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

@pytest.fixture(scope='session')
def django_db_setup():
    """Ensure tests use database"""
    pass