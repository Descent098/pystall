import nox

def confirm(message, validators = ["y", "yes"]):
    valid_input = False

    while not valid_input:
        response = input(message + str(validators).replace(","," or").replace("[","(").replace("]",")").replace("'",""))
        if response in validators:
            valid_input = True
        else:
            raise ValueError(f"Failed to confirm; {message}")

@nox.session
def build(session):
    # Confirm all the essential release stuff has been done
    confirm("Have you run the tests?")
    confirm("Have you updated inline docs?")
    confirm("Have you updated the wiki docs?")
    confirm("Have you created the release page?")
    confirm("Have you updated the readme docs?")

    # Create source distribution
    session.run("python", "setup.py", "sdist")

    # Build Documentation
    session.install("mkdocs")
    session.run("mkdocs", "build")

    # Create wheelfile
    session.install("wheel")
    session.run("python", "setup.py", "bdist_wheel", "--universal")

@nox.session
def release(session):
    build(session)
    session.install('twine')
    session.run("twine", "upload", "dist/*")

@nox.session(python=["3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install('pytest')
    session.run('pytest')

@nox.session
def docs(session):
    # Serve documentation to verify it's how you want
    session.install("mkdocs")
    session.run("mkdocs", "serve")