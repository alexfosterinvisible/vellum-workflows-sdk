from setuptools import setup, find_packages

setup(
    name="prompt_explorer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "vellum-ai>=0.11.7",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "rich>=13.0.0",
    ],
    entry_points={
        'console_scripts': [
            'vellum-explorer=src.cli:cli',
        ],
    },
)
