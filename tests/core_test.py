"""Testing out the core functionality of pystall

There is no way to do real installations without causing issues, so the only resources used are:
    1. StaticResource
    2. ZIPResource
    3. TarballResource
    4. Resource (base class)
"""

# Standard library dependencies
import os                                      # Used to validate paths, and remove files
from shutil import rmtree as remove_directory  # Used to remove test directories

# Internal Dependencies
from pystall.core import *                     # Imports the primary pystall functionality to test

def test_download():
    """Tests that download function from EXEResource class works properly"""
    # Define resource
    python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe", overwrite_agreement=True)

    # Download resource
    python.download("python-installer.exe")

    # Check that file was downloaded
    assert os.path.isfile("python-installer.exe")

    # Remove downloaded resource
    os.remove("python-installer.exe")


def test_archive_extract():
    """Tests that archive resources are downloaded and extracted properly"""
    # Define resources
    micro_zip = ZIPResource("Micro Zip", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip",  overwrite_agreement=True)
    micro_tar = TARBALLResource("Micro Tarball", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-linux64.tar.gz", overwrite_agreement=True)

    # Try to build resources
    build(micro_zip, micro_tar)

    # Verify files downloaded and extracted/"installed"
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Zip")
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Tarball")


def test_build():
    """Tests that resources are built properly"""
    # Define resources
    logo = StaticResource("Wallpaper", ".png", "https://canadiancoding.ca/static/img/post-banners/python-post-banner.9bf19b390832.png", overwrite_agreement=True)
    micro_zip = ZIPResource("Micro Zip", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip",  overwrite_agreement=True)
    micro_tar = TARBALLResource("Micro Tarball", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-linux64.tar.gz", overwrite_agreement=True)

    # Try to build resources
    build(logo, micro_zip, micro_tar)

    # Verify files downloaded and extracted/"installed"
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Zip")
    assert os.path.isdir(f"{DOWNLOAD_FOLDER}{os.sep}Micro Tarball")
    assert os.path.isfile(f"{DOWNLOAD_FOLDER}{os.sep}Wallpaper.png")

    # Remove downloaded files
    remove_directory(f"{DOWNLOAD_FOLDER}{os.sep}Micro Zip")
    remove_directory(f"{DOWNLOAD_FOLDER}{os.sep}Micro Tarball")
    os.remove(f"{DOWNLOAD_FOLDER}{os.sep}Wallpaper.png")
