from setuptools import setup

setup(
    name='stmt',
    version='0.1',
    py_modules=['remove_columns'],
    install_requires=[
        'Click',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        stmt=remove_columns:remove_columns
    ''',
)
