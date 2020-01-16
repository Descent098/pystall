# Creating Binary Distributions

Because pyinstaller is one of the dependencies specified in setup.py it is possible to create a binary of a script that does not require the user to have python installed to use.

## Benefits:

1. Single click running
2. High portability
3. 0 Dependencies

## Downsides:

1. pyinstaller cannot cross-compile to non-native binaries, meaning you cannot compile for linux on windows and vice-versa.
2. If you are distributing just plain binaries people are less likely to be happy running your script.

---

## Example

Let's take a look at setting this up, let's assume this is the script we want to compile called *deployment.py*:

```python
from pystall.core import build, show_logs
from pystall.library import python, go, chrome, micro

show_logs()

build(python, go, chrome, micro)
```

To compile this to a single executable we can run ```pyinstaller --onefile deployment.py```, the script will run and at the end there will be a folder called dist and the executable will be inside the folder. You can now take that executable with you and run it on the target machine, in my case because I am on windows it will be called ```deployment.exe```.



## Pyinstaller Docs

If you want to see more customization options the docs for pyinstaller can be found here: https://pyinstaller.readthedocs.io/en/stable/



## Python 3.8 Bug with pyinstaller

One thing to note is that pyinstaller has a bug in python 3.8+ with creating distributions, the solution for now is to install the dev branch with the fix until the official build has been updated: https://github.com/pyinstaller/pyinstaller/issues/4265