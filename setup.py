from setuptools import setup, find_packages

setup(
    name='cdof',
    version='0.1',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    py_modules=["cdof", "parse_annotated"],
    entry_points={
        'console_scripts': [
            'cdof=cdof:main',
        ],
    },
)