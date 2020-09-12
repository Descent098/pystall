"""Contains all the configuration for the package on pip"""
import setuptools

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string

    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "pystall",
    version = "0.3.0",
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "A system to automate configuration and setup of fresh Operating systems.",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls={
        'Docs': 'http://pystall.readthedocs.io/',
        'Bug Reports': 'https://github.com/Descent098/pystall',
        'Source': 'https://github.com/Descent098/pystall',
        'Roadmap': 'https://github.com/Descent098/pystall/projects/1',
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    # entry_points = { # Waiting on implementation to uncomment
    #       'console_scripts': ['pystall = pystall.cli:main']
    #   },
    install_requires = [
    "requests",
    "docopt",
    "tqdm",
    "colored",
    "pyinstaller",
    "distro",
        ],
    extras_require = {
        "dev" : [
            "nox", 
            "pytest", 
            "mkdocs"
            ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
