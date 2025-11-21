from setuptools import setup, find_packages
import os

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), "org_analyze", "__init__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

version = read_version()
setup(
    name="org_analyze",
    version=read_version(),
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
    ],
    #scripts=["export_html.py"],  # Add your script(s) here
    entry_points={
        'console_scripts': [
            'roam-export-html=org_analyze.export_html:main', # module:function
            'roam-export-md=org_analyze.export_md:main'
          ],
      },
    
)
