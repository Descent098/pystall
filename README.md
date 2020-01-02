# Pystall

A system to automate configuration and setup of fresh Operating systems.



## Quick-start



### API



Example installing exe files from website:

```python
from pystall.core import EXEAssets, Resource

python_installer = Resource("python-install", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe", None)

rustup = Resource("rustup", "https://win.rustup.rs/", None)

languages = EXEAssets("Languages", python_installer, rustup)
 
python_install.get() # Download and run the .exe's
```







## User requirements

What high-level goals you have:

1. Make setting up fresh OS installs easier
2. Create an extensible framework that can be expanded on.
3. Simple to use, with minimal boilerplate.
4. Automation of mass OS setups.



## Functional Requirements



1. Main python module that can be installed with pip through pypi
    1. Can be used in a python script.
    2. Can be used as a CLI. 
    3. Use pyinstaller to run as a direct binary.
2. Class that's inherited to setup dependencies
3. A way of supporting many filetypes (images, video files, installers etc.)
    1. Grab the files
    2. Put them in a particular path if necessary
    3. Run installers if necessary (make sure there is a flag not to run the binary, and that arguments can be passed)
4. A CLI interface
    1. Pass files with a JSON schema for installing dependencies.
5. Configuration of installations
    1. Handling PATH variables
    2. Handle running installers as admin.
6. Asynchronously download files. (V2)



### Unknowns

Anything you don't know implementation details of yet.



1. Not sure how to implement .dmg installation.
2. Don't know how to support unconventional installations. (Maybe out of scope)
3. don't necessarily know how to support varying linux installations. Particularly how to check what linux is installed. 





### Assumptions & Dependencies

**Assumptions**

- Python 3+ is installed
- Pip for python 3 is installed



**Dependencies**

- requests
- subprocess
- os
- sys
- docopt
- tqdm
- colored



### References

[Ansible](https://www.ansible.com/)



## Technical Detail

implementation details and challenges.



Language: Python

OS's: Windows & linux, Mac OS later (v2)

