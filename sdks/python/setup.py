from setuptools import setup, find_packages

setup(
    name="craite-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "craite=craite.cli:main",
        ],
    },
    python_requires=">=3.8",
)
