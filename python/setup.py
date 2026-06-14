from setuptools import setup, find_packages

setup(
    name="fuseiq-agent",
    version="0.1.0",
    description="Connect any AI agent to FuseIQ in 3 lines of code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nexgen Trading LLC",
    author_email="hello@fuseiq.io",
    url="https://github.com/abbasi8586/fuseiq-agent-sdk",
    packages=find_packages("python"),
    package_dir={"": "python"},
    install_requires=["requests>=2.28"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="fuseiq ai agent orchestration dashboard",
)
