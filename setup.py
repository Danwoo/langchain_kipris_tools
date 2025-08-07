import os
from setuptools import setup, find_packages

setup(
    name="langchain_kipris_tools",
    version="0.1.0",
    author="Danwoo",
    author_email="tjeksdn173@gmail.com",
    description="KIPRIS patent search API tools for langchain",
    long_description=(
        open("README.md", encoding="utf-8").read()
        if os.path.exists("README.md")
        else ""
    ),
    long_description_content_type="text/markdown",
    url="https://github.com/Danwoo/langchain_kipris_tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "langchain",
        "langchain_core",
        "requests",
        "xmltodict",
        "pandas",
        "python-dotenv",
    ],
)
