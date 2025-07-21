from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="craite-sdk",
    version="1.0.2",
    author="CRAITE Team",
    author_email="support@craite.ai",
    description="CRAITE Python SDK - AI-powered Web3 code generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CRAITE-CODE/craite",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "craite=craite.cli:main",
        ],
    },
)
