from setuptools import setup, find_packages

setup(
    name="datascience",
    version="0.1",
    packages=find_packages(exclude=["tests*"]),
    license="MIT",
    description="EDSA example python package",
    long_description=open("README.md").read(),
    install_requires=["numpy"],
    url="https://github.com/Ultra-Code/datascience_exploration.git",
    author="Ultra Code",
    author_email="mega.alpha100@gmail.com",
)
