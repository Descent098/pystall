from docopt import docopt


usage = """
    Usage: 
        pystall [-h] [-v] [-f FILE_PATH] [-l] [-d]

    A system to automate fresh OS installs

    Options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -f FILE_PATH, --file FILE_PATH
                            Specify the path to the JSON file with section
                            information
    -l, --log             If present will output logs to sys.stdout
    -d, --doc             If present will open up the pystall docs
    """

arguments = docopt(usage, version="Pystall V 0.0.1")

print(arguments)