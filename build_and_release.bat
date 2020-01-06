python setup.py sdist
pip install wheel
python setup.py bdist_wheel --universal
pip install twine
twine upload dist/*