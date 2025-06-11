from setuptools import setup, find_packages

setup(
    name="code-complexity-analyzer",
    version="1.0.0",
    description="A comprehensive code complexity analysis tool",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "radon>=6.0.1",
        "click>=8.1.0",
        "tabulate>=0.9.0",
        "colorama>=0.4.6",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "complexity-analyzer=interfaces.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
