from setuptools import setup

setup(
    name='stmt',
    version='0.1',
    py_modules=['process_statement'],
    install_requires=[
        'Click',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        stmt=process_statement:process_statement
    ''',
)
