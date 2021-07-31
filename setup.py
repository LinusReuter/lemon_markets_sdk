from lemon_markets import __version__
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='lemon_markets',
        version=__version__,
        description='Lemon Markets API Access SDK',
        license='MIT',
        python_requires='>=3.7',
        author='Linus Reuter',
        packages=find_packages(),
        install_requires=[
            'pandas == 1.3.1',
            'dataclasses == 0.6',
            'requests == 2.26.0'
        ],
    )
