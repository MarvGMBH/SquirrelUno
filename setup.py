from setuptools import setup, find_packages

setup(
    name='SquirrelUno',
    version='00.00.01',
    author='Dominik Krenn',
    author_email='i96774080@gmail.com',
    description='A project by Dominik Krenn to implement a unique version of the Uno game.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/SquirrelUno',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'squirreluno=uno.__main__:main',
        ],
    },
)
