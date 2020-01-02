"""
Description:
    Contains all the configuration for the package on pip
"""
import setuptools

def get_content(filename):
    """ Gets the content of a file and returns it as a string
    Args:
        filename(str): Name of file to pull content from
    Returns:
        str: Content from file
    """
    with open(filename, "r") as full_description:
        content = full_description.read()
    return content

setuptools.setup(
    name="Pystall",
    version="0.0.1",
    author="Kieran Wood",
    author_email="kieran@canadiancoding.ca",
    description="A system to automate configuration and setup of fresh Operating systems.",
    long_description=get_content("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Descent098/pystall",
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={
          'console_scripts': ['pystall = pystall.cli:main']
      },
    install_requires=[
    "requests",
    "docopt",
    "tqdm",
    "colored",
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)