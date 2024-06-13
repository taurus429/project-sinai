from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1.0',
    description='A simple Excel viewer using PyQt and Pandas',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'PyQt5'
    ],
    entry_points={
        'console_scripts': [
            'excel_viewer = main:main',
        ],
    },
)
