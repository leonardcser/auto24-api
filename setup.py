from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


def requirements():
    with open("requirements.txt") as f:
        return list(f.readlines())


setup(
    name="auto24_api",
    version="0.1.0",
    description="Python API wrapper for autoscout24 (ch)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=requirements(),
    # url="https://github.com/shuds13/pyexample",
    # author="Stephen Hudson",
    # author_email="shudson@anl.gov",
    # license="BSD 2-clause",
    packages=["auto24_api"],
    classifiers=[],
)
