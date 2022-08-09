from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


def requirements():
    with open("requirements/requirements.txt") as f:
        return list(f.readlines())


setup(
    name="auto24_api",
    version="0.0.1",
    description="Python API wrapper for AutoScout24.ch",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=requirements(),
    url="https://github.com/leonardcser/auto24-api",
    author="Leonard C.",
    packages=["auto24_api", "auto24_api.utils", "auto24_api.search"],
    classifiers=[],
)
