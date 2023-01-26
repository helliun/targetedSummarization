import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="targeted_sum",
    version="1.0.6",
    author="Henry Leonardi",
    author_email="leonardi.henry@gmail.com",
    description="A package for targeted summarization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/helliun/targetedSummarization",
    packages=setuptools.find_packages(),
    install_requires=['PyPDF2','sentence-transformers'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)