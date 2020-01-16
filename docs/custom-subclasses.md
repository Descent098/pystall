# Custom Subclasses

If the file format you are looking for is not available you do have the option to create a custom subclass (also if you think it's useful please upstream it back to the project).



## Base class

First let's take a look at the base Resource class:

```python
class Resource(ABC):
    """Base class to be inherited from and extended to suit specific resource.
    
    Attributes
    ----------
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
    def __init__(self, label, extension, location, arguments = False, downloaded = False):
        
        self.label = label
        self.extension = extension
        self.location = location
        self.arguments = arguments
        self.downloaded = downloaded

    def download(self, file_path = False):
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

        logging.info("Starting binary download")
        file_content = requests.get(self.location)
        open(file_path, 'wb').write(file_content.content) # Save file
        # TODO: Error catching
        self.downloaded = True
        self.location = file_path

    @abstractmethod
    def install(self) -> None:
        """installation steps after all necessary downloads are completed"""
        raise NotImplementedError
```

As we can see it is an abstract class with a few attributes, and one abstract method that **must** be implemented in any sub-classes to work.



## Minimum requirements for subclass

The convention for sub-classes is to use the capitalized extension + Resource for the name (i.e. for ".exe" use EXEResource etc.), also classes are documented using a modified [numpy style docstring](https://numpydoc.readthedocs.io/en/latest/format.html#class-docstring). There are a few things that you should do minimally to create the subclass:
1. Create a \_\_init\_\_() method. You can add any valuable extra attributes here such as whether the file should be removed after installation with a remove flag etc.
2. Override the install() method; this is where you will put any logic that needs to run to install/modify the downloaded resources.



## Example Subclass

Let's take a look at the ZIPResource subclass as an example. The intention with this subclass is to download a .zip file and extract all the files into the folder it was downloaded in:
```python
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
    def __init__(self, label, location, arguments = False, downloaded = False, remove = True):
        super().__init__(label, ".zip", location, arguments, downloaded)
        self.remove = remove

    def extract(self):
        """Extracts the .zip file."""
        extract_path = self.location[:-3:]
        logging.info(f"Extracting Zip archive {self.location} to {extract_path}")
        with ZipFile(self.location, "r") as archive:
                archive.extractall(extract_path) # Strip extension and extract to folder

    def install(self):
        """Extracts the .zip file and runs necessary installation steps. NOTE: Not yet implemented"""
        if self.downloaded:
            logging.info(f"Installing {self.label}")
            self.extract()
            
        else:
            logging.error(f"{self.name} failed to install due to not being downloaded")

        if self.remove:
            logging.info(f"Removing installer {self.label}")
            os.remove(self.location)
```



When someone creates an instance of the ZIPResource class and runs the build() method on it, it will call the download() and install() methods. The download method is rarely needed to be overridden, but the install() method is an abstract method and **MUST** be overridden.