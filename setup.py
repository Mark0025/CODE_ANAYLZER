from setuptools import setup, find_packages

setup(
    name="code_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pathlib",
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        'console_scripts': [
            'code_analyzer=code_analyzer.analyzer:main',
        ],
    },
    python_requires='>=3.6',
    author="Mark Carpenter",
    author_email="Mark@theairealestateinvestor.com",
    description="A tool for analyzing code directories",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code_analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 