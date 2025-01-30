from setuptools import setup, find_packages

setup(
    name='profiler_framework',
    version='1.0.1',
    description='A Python framework for memory and CPU profiling.',
    author='Ajay Khanna',
    author_email='ajaykhanna123ak@gmail.com',
    packages=find_packages(),
    url="https://github.com/ajaykhanna123/profiler_framework",
    install_requires=[
        'psutil',
        'seaborn',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        '..',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)