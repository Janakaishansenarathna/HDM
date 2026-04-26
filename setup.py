from setuptools import setup, find_packages
import os

# Read version
version = {}
with open(os.path.join("hdm_optimizer", "__version__.py")) as f:
    exec(f.read(), version)

# Read long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hdm-optimizer",
    version=version['__version__'],
    author=version['__author__'],
    description=version['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=version['__url__'],
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="optimizer deep-learning pytorch gradient-descent momentum hdm",
    project_urls={
        "Bug Reports": f"{version['__url__']}/issues",
        "Source": version['__url__'],
        "Documentation": f"{version['__url__']}/wiki",
        "Author LinkedIn": "https://www.linkedin.com/in/janakaishansenarathna/",
    },
    entry_points={
        "console_scripts": [
            "hdm-optimizer=hdm_optimizer.__main__:main",
        ],
    },
)
