# Generated from pyproject.toml - do not edit directly
from setuptools import find_packages, setup

setup(
    name="fida",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "loguru>=0.7.0",
        "lxml>=4.9.0",
        "matplotlib>=3.8.0",
        "nest-asyncio>=1.5.0",
        "numpy>=1.26.0",
        "pandas>=2.2.0",
        "pandas-datareader>=0.10.0",
        "pyrate-limiter==2.6.0",
        "requests-cache>=1.1.0",
        "requests-ratelimiter>=0.4.0,<0.8.0",
        "scipy>=1.12.0",
        "setuptools>=69.0.0",
        "tqdm>=4.66.0",
        "tiingo>=0.14.0",
        "yfinance>=0.2.0",
    ],
    extras_require={
        "test": [
            "coveralls>=3.3.1",
            "freezegun>=1.2.0",
            "requests-mock>=1.11.0",
            "pytest>=7.0.0",
        ],
        "dev": [
            "better-exceptions>=0.3.3",
            "ruff>=0.2.0",
            "ipython>=8.12.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
            "pre-commit>=3.5.0",
            "terminaltables>=3.1.10",
            "tabulate>=0.9.0",
            "types-ujson>=5.9.0",
        ],
    },
)
