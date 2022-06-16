from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='s3-endpoint-parse',
    version='1.1.0',
    python_requires=">=3.6",
    description='Flexibly extract information from S3 endpoint URL/URI strings',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pckilgore/s3_endpoint_parse",
    author='Patrick C. Kilgore',
    author_email="pypy-contact-s3-endpoint-parse@pck.email",
    project_urls={
        "Bug Tracker": "https://github.com/pckilgore/s3_endpoint_parse/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
