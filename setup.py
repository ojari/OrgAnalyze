from setuptools import setup, find_packages

setup(
    name="OrgAnalyze",
    version="0.0.1",
    description="Collect data from org-mode/org-roam pages and do some simple analyzing it.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jari Ojanen",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.9",
    url="https://github.com/ojari/OrgAnalyze",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ]
)
