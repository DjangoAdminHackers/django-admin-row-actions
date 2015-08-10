from setuptools import find_packages
from setuptools import setup

setup(
    name='django admin row actions',
    version='0.0.1',
    description='django admin row actions',
    author='Andy Baker',
    author_email='andy@andybak.net',
    packages=find_packages(),
    package_data={
        'django_admin_row_actions': [
            'static/css/*.css',
            'static/js/*.js',
        ]
    },
    include_package_data=True,
)
