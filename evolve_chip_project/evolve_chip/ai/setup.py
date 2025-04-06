from setuptools import setup, find_packages

setup(
    name="ai_common",
    version="0.1.0",
    description="汎用生成AIクライアントライブラリ",
    author="AI Team",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "openai": ["openai>=0.27.0"],
        "anthropic": ["anthropic>=0.2.0"],
        "all": [
            "openai>=0.27.0",
            "anthropic>=0.2.0",
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 