
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["python>=3"]

setup(
    name="Gamma restful api",
    version="0.0.1",
    author="Gergo Belinszky",
    description="Test task for Gamma",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/KicsiG/Gamma",
    packages=find_packages(),
    install_requires=requirements_dev,
)
