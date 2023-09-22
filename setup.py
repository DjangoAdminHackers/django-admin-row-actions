from setuptools import find_packages
from setuptools import setup

setup(
    name='django-admin-row-actions',
    version='0.10.0',
    description='Add action buttons to individual rows in the Django Admin',
    author='Andy Baker',
    author_email='andy@andybak.net',
    url='https://github.com/DjangoAdminHackers/django-admin-row-actions',
    packages=find_packages(),
    package_data={
        'django_admin_row_actions': [
            'static/css/*.css',
            'static/js/*.js',
            'templates/django_admin_row_actions/*.html',
        ]
    },
    include_package_data=True,
)
