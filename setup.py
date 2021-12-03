from setuptools import setup, find_packages

setup(
    name='fida',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/pablomitchell/fida',
    license='MIT',
    author='Pablo Mitchell',
    author_email='pablo.mitchell@gmail.com',
    description='Financial Data Accessor Code in Python',
    install_requires=[
        'lxml',
        'matplotlib',
        'numba',
        'pandas',
        'pandas-datareader',
        'pyarrow',
        'scipy',
        'setuptools',
        'tqdm',
        'tiingo',
    ],
)
