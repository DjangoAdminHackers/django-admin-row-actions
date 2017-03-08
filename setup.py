from setuptools import find_packages
from setuptools import setup

setup(
    name='django-admin-row-actions',
    version='0.0.2',
    description='django admin row actions',
    author='Andy Baker',
    author_email='andy@andybak.net',
    url='https://github.com/DjangoAdminHackers/django-admin-row-actions',
    packages=find_packages(),
    install_requires=[
        'six',
    ],
    package_data={
        'django_admin_row_actions': [
            'static/css/*.css',
            'static/js/*.js',
            'templates/django_admin_row_actions/*.html',
        ]
    },
    include_package_data=True,
)
