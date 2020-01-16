# Contribution Guide

If you are interested in contributing to Pystall (thanks by the way) then this guide should give you all you need to get started. There will be info about pystalls' structure, guiding principles, code style information, and more.



## Code style

Here is everything you need to know about writing code that matches the style of the existing codebase.



#### Variable names

There is really only 1 rule for variable names:



**DO NOT INCLUDE SINGLE CHARACTER VARIABLE NAMES!**



This makes things so much more difficult to debug that it often ends up being better to just re-implement, keep things short, simple, readable and idiomatic. 



#### Linting

Curently there is no strict linting enforced, but be reasonable. [PEP-8](https://www.python.org/dev/peps/pep-0008/) is a good source to follow, but not required. In the future something like [black](https://black.readthedocs.io/en/stable/) or [flake8](http://flake8.pycqa.org/en/latest/) may be implemented, but not yet.



#### In-Line Documentation

At a minimum your code must include docstrings for any functions, and inline code for any module global variables (though these should be avoided anyway). The typical format followed is the [numpystyle docstrings](https://numpydoc.readthedocs.io/en/latest/format.html#class-docstring) with at least the attributes, methods, examples, returns/yields and notes sections (where applicable) for both classes and functions.



Ideally you should also include an in-line comment if you are doing any nested iteration, conditionals, or combinations of both, that just quickly explains what's going on.



## Guiding principles

Here are some of the principles that pystall is built on, before submitting a pull request make sure your feature is in line with them (you can also submit an issue to ask before writing it).



#### Goals

1. Make setting up fresh OS installs easier.
2. Create an extensible framework that can be expanded upon to meet custom dependency installation management.
3. Simple to use, with minimal boilerplate.
4. Automation of tedious configuration and downloading.



Also take a look at the [what is pystall?](/#what-is-pystall?) section of the homepage.



#### Bug Tracking & Roadmap

The bug tracking and overall roadmap can be found in the [project page on github](https://github.com/Descent098/pystall/projects/1). If you are looking to submit a bug report, feature request, or pull request please go through [the github issues page](https://github.com/Descent098/pystall/issues).



## Source File/Folder Structure

Here is the layout and functions for all the files/folders in the project. I have split it up between functionality, testing/documentation, and Metadata/Manifest files.



### Functionality

All the code that comprises pystalls' functionality is found in /pystall and in the following files:



#### /pystall/cli.py

Includes the code for the ```pystall``` command (which will be implemented at a later date).



#### /pystall/core.py

Includes all 'core' functionality of the package such as:

- The base Resource class
- All of the officially supported Resource subclasses
- The build() method used to install Resources



#### /pystal/library.py

Contains all the code for the resource library (a set of preconfigured installers to make things easier). This is also a good way to check out examples of setups for popular applications.



### Testing & Documentation

These files comprise the testing suite (implemented in [pytest](https://docs.pytest.org/en/latest/)) and the documentation source files (implemented with [mkdocs](https://www.mkdocs.org/)).



#### /tests

This folder contains all the testing files, currently there is only one ```primary_test.py``` which runs a slough of functionality tests.



#### /docs

Includes all the source documentation files for this website (written in markdown and built to HTML using [mkdocs](https://www.mkdocs.org/)).



#### CHANGELOG.md

A chronological list of changes made in various versions of pystall, along with their respective **public** release dates.



#### README.md

A file used by github to give a bit of a blurb about using pystall for those who don't want to read the real documentation (good on you by the way).



### Metadata/Manifest files

These are files for doing various maintenence tasks, and storing configurations for different development utilities.



#### .github/workflows/pythonpackage.yml

This file is used to drive the github actions CI/CD system.



#### .gitignore

This file is used to specify which files should not include



#### LICENSE

This file contains the licensing information about the project, which in this case is [GNU GPL V3.0](https://choosealicense.com/licenses/gpl-3.0/).



#### noxfile.py

Used to configure various automated processes using [nox](https://nox.readthedocs.io/en/stable/), these include:

- Building release distributions
- Releasing distributions on PyPi
- Running test suite agains a number of python versions (3.5-current)



If anything to do with deployment or releases is failing, this is likely the suspect.



#### setup.py

Manifest information for defining pystall as a python package. Includes metadata about the package such as version number, the CLI entrypoint, specification of standard installation (and development installation) dependencies, and other metadata required by PyPi.



If you need to modify how python installs pystall, this is the file to start with.



#### /pystall/\_\_init\_\_.py

This file is used by python to define the /pystall folder as a python package. You should never need to modify it.