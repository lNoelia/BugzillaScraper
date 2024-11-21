from setuptools import setup, find_packages

setup(
    name='issuex',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'python-dotenv',
    ],
    author='David Romero',
    author_email='drorganvidez@us.es',
    entry_points={
        'console_scripts': [
            'issuex=issuex.cli:cli'
        ],
    },
)
