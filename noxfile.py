import nox

def confirm(message, validators = ["y", "yes"]):
    valid_input = False

    while not valid_input:
        response = input(message + "(")
        if validators in response:
            valid_input = True

@nox.session
def build(session):
    confirm("Have you run the tests?")
    confirm("Have you updated inline docs?")
    confirm("Have you updated the wiki docs?")
    confirm("Have you updated the readme docs?")
    session.run("python", "setup.py", "sdist")
    session.install("wheel")
    session.run("python", "setup.py", "bdist_wheel", "--universal")

@nox.session
def release(session):
    session.install('twine')
    session.run("twine", "upload", "dist/*")

@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install('pytest')
    session.run('pytest')