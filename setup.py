from setuptools import setup, find_packages

# README.mdの読み込み
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = "EvolveChip - AIチップを埋め込んで自己進化するPythonライブラリ"

setup(
    name="evolve-chip",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=0.19.0",
        "requests>=2.25.0",
    ],
    entry_points={
        'console_scripts': [
            'evolve-chip=evolve_chip:main',
        ],
    },
    author="EvolveChip Team",
    author_email="info@evolvechip.ai",
    description="AIチップを埋め込んで自己進化するPythonライブラリ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/evolve-chip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
) 