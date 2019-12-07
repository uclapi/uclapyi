import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uclapyi-uclapi", # Replace with your own username
    version="0.0.1",
    author="UCLAPI",
    author_email="isd.apiteam@ucl.ac.uk",
    description="A python wrapper for UCL API's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uclapi/uclapyi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
