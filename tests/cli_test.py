"""Testing out the cli functionality of pystall

There is no way to do real installations without causing issues, so the only resources used are:
    1. StaticResource
    2. ZIPResource
    3. TarballResource
    4. Resource (base class)

Test Variables
--------------
DESKTOP : (str)
    This is the path to the current user desktop folder, it is OS independant

DOWNLOAD_FOLDER : (str)
    This is the path to the current user downloads folder, it is OS independant
"""

# Standard library dependencies
import os                                      # Used to validate paths, and remove files
from shutil import rmtree as remove_directory  # Used to remove test directories

# Internal Dependencies
from pystall.cli import *                      # Imports the pystall cli functionality to test

# Setting up default downloads folder based on OS
if os.name == "nt":
    DESKTOP = f"{os.getenv('USERPROFILE')}\\Desktop"
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
else: # PORT: Assuming variable is there for MacOS and Linux installs
    DESKTOP = f"{os.getenv('HOME')}/Desktop" #TODO: Verify this is the right directory
    DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads" #TODO: Verify this is the right directory

def test_file_build():
    # 1. Create resource file
    file_text = """
Resources:
  'Micro Zip':
    type: 'zip'
    location: 'https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip'
    remove: True
    overwrite_agreement: True
  'Micro Tarball':
    type: 'tarball'
    location: 'https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-linux64.tar.gz'
    remove: True
    overwrite_agreement: True
  'Wallpaper':
    type: 'static'
    location: 'https://images.unsplash.com/photo-1541599468348-e96984315921?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=500&q=60'
    extension: '.png'
    overwrite_agreement: True
    """

    with open("resource.yml", "w") as resource_file:
        resource_file.write(file_text)

    # 2. Build resource file
    build_from_file("resource.yml")

    # Verify files downloaded and extracted/"installed"
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Zip")
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Tarball")
    assert os.path.isfile(f"{DOWNLOAD_FOLDER}{os.sep}Wallpaper.png")

    # Remove downloaded files
    remove_directory(f"{DOWNLOAD_FOLDER}{os.sep}Micro Zip")
    remove_directory(f"{DOWNLOAD_FOLDER}{os.sep}Micro Tarball")
    os.remove(f"{DOWNLOAD_FOLDER}{os.sep}Wallpaper.png")
    os.remove(f"resource.yml")

    pass
