from setuptools import setup, find_packages

setup(
    name="markdown_to_confluence",
    version="0.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "md2conf=markdown_to_confluence.cli:main",
        ]
    },
    install_requires=[
        "requests",
        "markdown2",
        # any other dependencies you might have
    ],
)
