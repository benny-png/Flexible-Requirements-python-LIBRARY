from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flexible-requirements",
    version="0.1.3",
    author="benny-png",
    author_email="mazikuben2@gmail.com",
    description="A library for generating flexible Python requirements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benny-png/Flexible-Requirements-python-LIBRARY",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "packaging",
        "requests",
    ],
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'flexible-requirements=main:main',
        ],
    },
)