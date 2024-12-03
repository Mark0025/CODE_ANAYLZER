"""
Setup configuration for CODE_ANALYZER package.

This module handles package configuration, dependencies,
and entry points for the CODE_ANALYZER project.
"""
from setuptools import setup, find_packages

setup(
    name="code_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "crewai>=0.11.0",  # AI crew management
        "click>=8.0.0",     # CLI interface
        "rich>=10.0.0",     # Rich terminal output
        "loguru>=0.7.0",    # Logging
        "pendulum>=2.0.0",  # Time handling
        "pyyaml>=6.0.0",    # YAML processing
    ],
    entry_points={
        'console_scripts': [
            'analyze=code_analyzer.cli.main:cli',
        ],
    },
    python_requires='>=3.9',
) 