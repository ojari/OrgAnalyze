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

def read_requirements():
    res = []
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    with open(req_file, "r") as f:
        for line in f.readlines():
            res.append(line.strip())
    return res


version = read_version()
setup(
    name="org_analyze",
    version=read_version(),
    description="A toolkit for extracting, analyzing, and exporting data from org-mode/org-roam notes, with support for HTML and Markdown export. See https://ojari.github.io/OrgAnalyze/ for example HTML export.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jari Ojanen",
    packages=find_packages(),
    install_requires=['pandas'], # read_requirements(),
    python_requires=">=3.9",
    url="https://github.com/ojari/OrgAnalyze",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
        "Topic :: Text Editors :: Emacs"
    ],
    #scripts=["export_html.py"],  # Add your script(s) here
    entry_points={
        'console_scripts': [
            'roam-export-html=org_analyze.export_html:main', # module:function
            'roam-export-md=org_analyze.export_md:main'
        ],
    },
)
