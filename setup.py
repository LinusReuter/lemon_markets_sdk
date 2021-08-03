from lemon_markets import __version__
from setuptools import setup, find_packages

if __name__ == '__main__':
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

    setup(
        name='lemon_markets_sdk',
        version=__version__,
        description='SDK for Lemon Markets API',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        python_requires='>=3.7',
        author='Linus Reuter',
        url="https://github.com/LinusReuter/lemon-markets-api-access",
        download_url='https://github.com/LinusReuter/lemon-markets-api-access/archive/refs/tags/v0.2.1.tar.gz',
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'pandas == 1.3.1',
            'dataclasses == 0.6',
            'requests == 2.26.0'
        ],
    )
