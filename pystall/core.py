"""Contains core functionality of Pystall.

This module contains core functionality of Pystall including:
    - Base Resource class
    - The included basic Resource subclasses
    - The build() method

Module Variables
----------------
DESKTOP : (str)
    This is the path to the current user desktop folder, it is OS independant

DOWNLOAD_FOLDER : (str)
    This is the path to the current user downloads folder, it is OS independant

agreement_text : (str)
    The agreement users must make on each run to use pystall

Classes
-------
Resource: 
    Base class to be inherited from and extended to suit specific resource

EXEResource(Resource):
    Used to download and install .exe files

MSIResource(Resource):
    Used to download and install .msi files

StaticResource(Resource):
    Used to download static files (images, videos etc.)

ZIPResource(Resource):
    Used to download and extract .zip files

DEBResource(Resource):
    Used to download and install .deb files

CUSTOMPPAResource:
    Used to download files that are from a third party PPA's

TARBALLResource(Resource):
    Used to download and extract .tar.gz files

APTResource:
    Installs resources that are part of an exsiting APT repository

Methods
-------
build(*resources):
    Downloads and installs specified resources. 
    NOTE: Pass an arbitrary number of Resource instances (comma delimited)

show_logs():
    When called sets up a logger to display script logs

Examples
--------
```
from pystall.core import EXEResource, MSIResource, StaticResource, build

python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

logo = StaticResource("Wallpaper", ".png", "https://canadiancoding.ca/static/img/post-banners/python-post-banner.9bf19b390832.png")

build(python, go, logo)
```

"""



"""
Code maintenance
TODO
----
  * Logging
  * Error Catching

"""

# Standard lib dependencies
import os                           # Path validation and checking which OS script is being run on
import logging                      # Used to grab logs from functions and classes
import sys                          # Used to exit cleanly from scripts
import subprocess                   # Used to install/run binaries once downloaded
from zipfile import ZipFile         # Used to extract files from .zip archives
import tarfile                      # Used to extract tarball archives
from abc import ABC, abstractmethod # Used to enforce subclassing from base Resource class

# Third party dependencies
import requests                     # Used to download files from the web
from tqdm import tqdm               # Used to create installation/download progress bars

# Setting up default downloads folder based on OS
if os.name == "nt":
    DESKTOP = f"{os.getenv('USERPROFILE')}\\Desktop"
    DOWNLOAD_FOLDER = f"{os.getenv('USERPROFILE')}\\Downloads"
else: # PORT: Assuming variable is there for MacOS and Linux installs
    DESKTOP = f"{os.getenv('HOME')}/Desktop" #TODO: Verify this is the right directory
    DOWNLOAD_FOLDER = f"{os.getenv('HOME')}/Downloads" #TODO: Verify this is the right directory

# The agreement users must make on each run to use pystall
agreement_text = """By using pystall you are also agreeing that:
    1. There is no responsibility or accountability on the part of the creator for how this library is used
    2. You agree to any and all required software liscences for the software you install using pystall

If you agree type y and hit enter, if you disagree type n and hit enter to exit: """

def show_logs():
    """When called sets up a logger to display script logs"""
    LOG_FORMAT = "%(levelname)s | : %(message)s "
    formatter = logging.Formatter(LOG_FORMAT)
    logger = logging.getLogger("pystall")
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout).setFormatter(formatter))


def _add_to_path(program_path:str):
    """Takes in a path to a program and adds it to the sytem path

    Parameters
    ----------
    program_path : str
        The path to the installation folder of the application

    Notes
    -----
    * All paths must be absolute paths

    * The linux version of the command assumes you're using ~/.bashrc

    * Because there are so many possible ways this can fail, there are no catches in place

    Examples
    --------
    ```
    program_path = f"{os.environ['USERPROFILE']}\\Downloads\\micro editor\\micro-1.4.1" # Path that contains the executeable
    _add_to_path(program_path) # Adds the program_path to the path variable
    ```
    """

    if os.name == "nt": # Windows systems
        import winreg # Allows access to the windows registry
        import ctypes # Allows interface with low-level C API's

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root: # Get the current user registry
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key: # Go to the environment key
                existing_path_value = winreg.EnumValue(key, 3)[1] # Grab the current path value
                new_path_value = existing_path_value + program_path + ";" # Takes the current path value and appends the new program path
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value) # Updated the path with the updated path

            # Tell other processes to update their environment
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
            SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(result),) 
    else: # If system is *nix
        execution_string = f'printf \'\\nexport PATH="{program_path}:$PATH"\' >> ~/.bashrc && source ~/.bashrc' # TODO: Verify this works
        subprocess.Popen(execution_string)
    print(f"Added {program_path} to path, please restart shell for changes to take effect")


class Resource(ABC):
    """Base class to be inherited from and extended to suit specific resource.

    Attributes
    ----------

    agreement : (bool)
        A class variable to confirm that users

    label : (str)
        Human readable name for resource and used with extension in files name.

    extensions : (str)
        The extension of the filetype being downloaded

    location : (str)
        The path or URL to the resource that needs to be downloaded & installed

    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.

    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 

    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install (abstract):
        Subclass implemented function for how to install/configure resource once downloaded.

    Examples
    --------
    Subclassing a static resource class to download static assets (images, videos etc.)
    ```
    class StaticResource(Resource):
        def __init__(self, label, extension, location, arguments = False, downloaded = False):
            super().__init__(label, extension, location, arguments, downloaded)

        def install(self):
            logging.info("No installation necessary for StaticResources")
            pass
    ```
    """
    # Software liscence agreement that runs on import
    agreement = False

    def __init__(self, label:str, extension:str, location:str, arguments:list = False, downloaded:bool = False, overwrite_agreement:bool = False, dependencies:tuple = ()):
        if not overwrite_agreement:
            while not Resource.agreement:  # Continuously ask user to agree to software terms, this only runs once per script as this is a class variable
                response = input(agreement_text).lower().strip()

                if response == "y":
                    Resource.agreement = True
                elif response == "n":  # If someone does not agree to liscence then terminate script
                    sys.exit()
                else:
                    # Clear the terminal and re-ask
                    if os.name == 'nt':  # PORT: Windows
                        os.system('cls')
                    else:  # PORT: *nix
                        os.system('clear')
                    continue

        self.label = label
        self.extension = extension
        self.location = location
        self.arguments = arguments
        self.downloaded = downloaded
        self.dependencies = dependencies

    def download(self, file_path:str = False):
        """Downloads Resource from location specified in self.location of the instance.

        Attributes
        ----------
        file_path : (str|bool)
            The path to where the resource should download to. 
            Leave as false for download folder + name + extension.
            NOTE: Custom paths MUST include extension.

        Examples
        --------
        ```
        python = EXEResource('python-installer', 'https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe')

        python.download() # Downloads python installer exe to OS downloads folder
        ```
        """
        logging.info(f"Downloading {self.label}")

        if not file_path:
            file_path = f"{DOWNLOAD_FOLDER}{os.sep}{self.label}{self.extension}"

        if os.path.exists(file_path): # If file already exists
            self.downloaded = True
            self.location = file_path
            return

        if self.location.startswith("https://") or self.location.startswith("http://"): # If URL is provided start download
            logging.info("Starting binary download")

            # Setting up necessary download variables
            file_stream = requests.get(self.location, stream=True) # The open http request for the file
            chunk_size = 1024 # Setting the progress bar chunk size to measure in kb
            total_length = int(file_stream.headers.get('content-length')) # Getting file size

            # Setting up the download progress bar
            progress_bar = tqdm(total=total_length, unit='iB', unit_scale=True)
            progress_bar.set_description(f"Download progress for {self.label}:")

            # Write the incoming data stream to a file and update progress bar as it downloads
            with open(file_path, 'wb') as download_file: 
                for chunk in file_stream.iter_content(chunk_size): 
                    if chunk:
                        progress_bar.update(len(chunk))
                        download_file.write(chunk)
            progress_bar.close()
            # TODO: Error catching
            self.downloaded = True
            self.location = file_path
        
        else: # No need to download it since it's already downloaded
            self.downloaded = True

    @abstractmethod
    def install(self) -> None:
        """installation steps after all necessary downloads are completed"""
        raise NotImplementedError


class EXEResource(Resource):
    """Used to download and install .exe files.

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.

    location : (str)
        The path or URL to the resource that needs to be downloaded & installed

    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.

    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    remove: (bool)
        Whether to delete the .exe after installation, by default True.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 

    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Runs the .exe file with specified arguments.
        NOTE: assumes you have already downloaded the file or set the self.location to correct file path.

    Examples
    --------
    ```
    from pystall.core import EXEResource, build

    python = EXEResource("python-installer", "https://www.python.org/ftp/python/3.8.1/python-3.8.1.exe")

    build(python) # Runs the download() and install() methods on the 'python' instance
    ```
    """
    def __init__(self, label:str, location:str, arguments:list = False, downloaded:bool = False, remove:bool = True, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, ".exe", location, arguments, downloaded, overwrite_agreement, dependencies)
        self.remove = remove

    def install(self):
        """Runs the .exe specified in self.location"""
        print(f"Installing {self.label}")

        # install dependencies
        if self.dependencies:
            print(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        # Check if already downloaded
        if self.downloaded:
            installer = subprocess.Popen(self.location, shell=True)
        else:
            logging.error(f"{self.label} failed to install due to not being downloaded")

        # Wait until installation is complete
        while installer.poll() == None:
            """loop runs until process has terminated"""

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)


class MSIResource(Resource):
    """Used to download and install .msi files.

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.
    
    location : (str)
        The path or URL to the resource that needs to be downloaded & installed
    
    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.
    
    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    remove: (bool)
        Whether to delete the .msi after installation, by default True.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Runs the .msi file with specified arguments.
        NOTE: assumes you have already downloaded the file or set the self.location to correct file path.

    Examples
    --------
    ```
    from pystall.core import MSIResource, build

    go = MSIResource("Golang", "https://dl.google.com/go/go1.13.5.windows-amd64.msi")

    build(go) # Runs the download() and install() methods on the 'go' instance
    ```
    """
    def __init__(self, label:str, location:str, arguments:list = False, downloaded:bool = False, remove:bool = True, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, ".msi", location, arguments, downloaded, overwrite_agreement, dependencies)
        self.remove = remove

    def install(self):
        """Runs the .msi file with specified arguments."""
        print(f"Installing {self.label}")

        # install dependencies
        print(f"Installing {self.label} dependencies")
        if self.dependencies:
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        # Check if already downloaded
        if self.downloaded:
            installer = subprocess.Popen(self.location, shell=True)
        else:
            logging.error(f"{self.name} failed to install due to not being downloaded")

        # Wait until installation is complete
        while installer.poll() == None:
            """loop runs until process has terminated"""

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)


class StaticResource(Resource):
    """Used to download static files (images, videos etc.).

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.

    extensions : (str)
        The extension of the filetype being downloaded.
    
    location : (str)
        The path or URL to the resource that needs to be downloaded & installed
    
    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.
    
    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Does nothing since there are no installation/configuration steps for static files

    Examples
    --------
    ```
    from pystall.core import StaticResource, build

    wallpaper = StaticResource("Wallpaper", ".png", "https://images.unsplash.com/photo-1541599468348-e96984315921?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=500&q=60")

    wallpaper.download() # Since no install is necessary

    build(wallpaper) # Another option to download the Resource
    ```
    """
    def __init__(self, label:str, extension:str, location:str, arguments:list = False, downloaded:bool = False, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, extension, location, arguments, downloaded, overwrite_agreement, dependencies)

    def install(self):
        """Does nothing since there are no installation/configuration steps for static files"""
        # install dependencies
        logging.info(f"Installing {self.label}")
        if self.dependencies:
            print(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)


class ZIPResource(Resource):
    """Used to download and extract .zip files.

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.
    
    location : (str)
        The path or URL to the resource that needs to be downloaded & installed
    
    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.
    
    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    remove: (bool)
        Whether to delete the .zip after installation, by default True.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Extracts the .zip file.
        NOTE: assumes you have already downloaded the file or set the self.location to correct file path.

    Examples
    --------
    ```
    from pystall.core import ZIPResource, build

    micro = ZIPResource("micro editor", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip")

    build(micro)
    ```
    """
    def __init__(self, label:str, location:str, arguments:list = False, downloaded:bool = False, remove:bool = True, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, ".zip", location, arguments, downloaded, overwrite_agreement, dependencies)
        self.remove = remove

    def extract(self):
        """Extracts the .zip file."""
        extract_path = self.location[:-3:]
        logging.info(f"Extracting Zip archive {self.location} to {extract_path}")
        with ZipFile(self.location, "r") as archive:
                archive.extractall(extract_path) # Strip extension and extract to folder

    def install(self):
        """Extracts the .zip file and runs necessary installation steps."""
        print(f"Extracting {self.label}")

        # install dependencies
        if self.dependencies:
            logging.info(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        if self.downloaded:
            self.extract()
            
        else:
            logging.error(f"{self.name} failed to install due to not being downloaded")

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)


class DEBResource(Resource):
    """Used to download and install .deb files.

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.

    location : (str)
        The path or URL to the resource that needs to be downloaded & installed
    
    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.

    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    remove: (bool)
        Whether to delete the .deb after installation, by default True.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Runs the .deb with specified arguments.
        NOTE: assumes you have already downloaded the file or set the self.location to correct file path.

    Examples
    --------
    ```
    from pystall.core import DEBResource, build

    atom = DEBResource("Atom", "https://atom.io/download/deb")

    build(atom) # Runs the download() and install() methods on the 'atom' instance
    ```
    """
    def __init__(self, label:str, location:str, arguments:list = False, downloaded:bool = False, remove:bool = True, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, ".deb", location, arguments, downloaded, overwrite_agreement, dependencies)
        self.remove = remove

    def install(self):
        """Runs the .msi file with specified arguments."""
        print(f"Installing {self.label}")

        # install dependencies
        if self.dependencies:
            logging.info(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        if self.downloaded:
            installer = subprocess.Popen(f"sudo apt install {self.location}", shell=True)
        else:
            logging.error(f"{self.name} failed to install due to not being downloaded")

        while installer.poll() == None:
            """loop runs until process has terminated"""

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)


class CUSTOMPPAResource:
    """Used to download files that are from a third party PPA's

    Attributes
    ----------

    label : (str)
        Human readable name for resource
    
    PPA : (str)
        The name of the ppa to add
    
    packages : (list|str)
        Specify either a list of packages to install, or a string with a package name.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Adds specified PPA and apt-get updates

    install:
        Installs specified packages after the PPA had been added.

    Examples
    --------
    ```
    from pystall.core import CUSTOMPPAResource, build

    python_linux = CUSTOMPPAResource("Python 3", "deadsnakes/ppa", ["python3.7", "python3.8"])

    build(python_linux)

    ```

    """
    def __init__(self, label:str, PPA:str, packages:list, overwrite_agreement:bool = False, dependencies:tuple = ()):
        self.label = label
        self.PPA = PPA
        self.packages = packages
        self.downloaded = False
        self.dependencies = dependencies
        if not overwrite_agreement:
            while not Resource.agreement:  # Continuously ask user to agree to software terms, this only runs once per script as this is a class variable
                response = input(agreement_text).lower().strip()

                if response == "y":
                    Resource.agreement = True
                elif response == "n":  # If someone does not agree to liscence then terminate script
                    sys.exit()
                else:
                    # Clear the terminal and re-ask
                    if os.name == 'nt':  # PORT: Windows
                        os.system('cls')
                    else:  # PORT: *nix
                        os.system('clear')
                    continue
        
    def download(self):
        """Adds PPA and apt updates"""

        logging.info(f"Adding PPA {self.PPA}")
        installer = subprocess.Popen(f"sudo add-apt-repository ppa:{self.PPA} && sudo apt-get update", shell=True)

        while installer.poll() == None:
            """loop runs until process has terminated"""

    def install(self):
        """Installs specified packages"""
        print(f"Installing {self.label}")

        # install dependencies
        if self.dependencies:
            logging.info(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        if type(self.packages) == str:
            logging.info(f"Installing{self.packages}")
            installer = subprocess.Popen(f"sudo apt install {self.packages}", shell=True)

            while installer.poll() == None:
                """loop runs until process has terminated"""

        elif (type(self.packages) == list) or (type(self.packages) == tuple):
            for package in self.packages:
                logging.info(f"Installing {package}")
                installer = subprocess.Popen(f"sudo apt install {package}", shell=True)

                while installer.poll() == None:
                    """loop runs until process has terminated"""


class TARBALLResource(Resource):
    """Used to download and extract .tar.gz files.

    Attributes
    ----------

    label : (str)
        Human readable name for resource and used with extension in files name.

    location : (str)
        The path or URL to the resource that needs to be downloaded & installed

    arguments : (list|bool)
        Specify any arguments to be passed on installation, False indicates no arguments.

    downloaded : (bool)
        Used to delineate if Resource is downloaded, if using local file set to True, else leave as False.

    remove: (bool)
        Whether to delete the .zip after installation, by default True.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 


    Methods
    -------
    download:
        Downloads Resource from location specified in self.location of the instance

    install:
        Extracts the .tar.gz file.
        NOTE: assumes you have already downloaded the file or set the self.location to correct file path.

    Examples
    --------
    ```
    from pystall.core import TARBALLResource, build

    micro = TARBALLResource("Micro editor", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-linux64.tar.gz")

    build(micro)
    ```
    """
    def __init__(self, label:str, location:str, arguments = False, downloaded = False, remove = True, overwrite_agreement:bool = False, dependencies:tuple = ()):
        super().__init__(label, ".tar.gz", location, arguments, downloaded, overwrite_agreement, dependencies)
        self.remove = remove

    def extract(self):
        """Extracts the .tar.gz file."""
        extract_path = self.location[:-7:]
        logging.info(f"Extracting Zip archive {self.location} to {extract_path}")
        with tarfile.open(name = self.location, mode = "r") as archive:
                archive.extractall(extract_path) # Strip extension and extract to folder

    def install(self):
        """Extracts the .zip file and runs necessary installation steps. NOTE: Not yet implemented"""
        print(f"Extracting {self.label}")

        # install dependencies
        if self.dependencies:
            logging.info(f"Installing {self.label} dependencies")

            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    
                    build(dependency)
            else:  # If single dependency is specified
                print(f"installing {self.dependencies.label}")
                build(self.dependencies)

        if self.downloaded:
            self.extract()

        else:
            logging.error(f"{self.name} failed to install due to not being downloaded")

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)


class APTResource:
    """Installs resources that are part of an exsiting APT repository

    Attributes
    ----------

    label : (str)
        Human readable name for resource
    
    packages : (list|str)
        Specify either a list of packages to install, or a string with a package name.

    overwrite_agreement : (bool)
        Used to overwrite software agreement, which should only be done for testing and integration purposes

    dependencies : (tuple[Resource])
        A tuple of the necessary Resources to install 

    Methods
    -------
    download:
        Adds specified PPA and apt-get updates

    install:
        Installs specified packages after the PPA had been added.

    Examples
    --------
    ```
    from pystall.core import APTResource, build

    nano = APTResource("Nano Editor", "nano")

    build(nano)

    ```

    """
    def __init__(self, label:str, packages:list, overwrite_agreement:bool = False, dependencies:tuple = ()):
        if not overwrite_agreement:
            while not Resource.agreement:  # Continuously ask user to agree to software terms, this only runs once per script as this is a class variable
                response = input(agreement_text).lower().strip()

                if response == "y":
                    Resource.agreement = True
                elif response == "n":  # If someone does not agree to liscence then terminate script
                    sys.exit()
                else:
                    # Clear the terminal and re-ask
                    if os.name == 'nt':  # PORT: Windows
                        os.system('cls')
                    else:  # PORT: *nix
                        os.system('clear')
                    continue
        self.label = label
        self.packages = packages
        self.downloaded = False
        self.dependencies = dependencies

    def download(self):
        """Updates apt packages using 'sudo apt-get update' """

        logging.info("Updating apt repositories")
        installer = subprocess.Popen("sudo apt-get update", shell=True)

        while installer.poll() == None:
            """loop runs until process has terminated"""

    def install(self):
        """Installs specified packages"""
        print(f"Installing {self.label}")

        # install dependencies
        if self.dependencies:
            logging.info(f"Installing {self.label} dependencies")
            if type(self.dependencies) == tuple or type(self.dependencies) == list:
                for dependency in self.dependencies:
                    build(dependency)
            else:  # If single dependency is specified
                build(self.dependencies)

        if type(self.packages) == str:
            logging.info(f"Installing{self.packages}")
            installer = subprocess.Popen(f"sudo apt install {self.packages}", shell=True)

            while installer.poll() == None:
                """loop runs until process has terminated"""

        elif (type(self.packages) == list) or (type(self.packages) == tuple):
            for package in self.packages:
                logging.info(f"Installing {package}")
                installer = subprocess.Popen(f"sudo apt install {package}", shell=True)

                while installer.poll() == None:
                    """loop runs until process has terminated"""


def build(*resources):
    """Downloads and installs everything specified
    
    Parameters
    ----------
    resources : (*Resource)
        Takes in an arbitrary number of Resource python object instances
    """
    for resource in resources:
        if not resource.downloaded:
            resource.download()
        resource.install()


if __name__ == "__main__":  # Used to test out functionality while developing
    show_logs()

    wallpaper = StaticResource("Wallpaper", ".png", "https://images.unsplash.com/photo-1541599468348-e96984315921?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=500&q=60")

    micro = ZIPResource("micro editor", "https://github.com/zyedidia/micro/releases/download/v1.4.1/micro-1.4.1-win64.zip", dependencies=(wallpaper))

    build(micro)
