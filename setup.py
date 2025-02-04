from setuptools import setup, find_packages

setup(
    name='profiler_framework',
    version='1.0.3',
    description='A Python framework for memory and CPU profiling.',
    author='Ajay Khanna',
    author_email='ajaykhanna123ak@gmail.com',
    packages=find_packages(),
    url="https://github.com/ajaykhanna123/profiler_framework",
    install_requires=[
        "psutil>=5.8.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "tqdm>=4.60.0",
        "pathvalidate>=2.5.0",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        '..',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)