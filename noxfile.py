import nox

@nox.session
def build(session):
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