from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README for long description
with open('README.md') as f:
    long_description = f.read()

setup(
    name='pi_sdk',
    version='0.1.0',
    description='Python SDK for PI API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alex Foster',
    author_email='alexfosterinvisible@gmail.com',
    url='https://github.com/alexfosterinvisible/pi_sdk',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='pi, sdk, api',
)
