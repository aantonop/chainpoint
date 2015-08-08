from setuptools import setup

setup(
    name='chainpoint', version='1.0',
    description='Federated server for building blockchain notarized Merkle trees.',
    author='Shawn Wilkinson', author_email='shawn+chainpoint@storj.io',
    url="http://chainpoint.io",

    #  Uncomment one or more lines below in the install_requires section
    #  for the specific client drivers/modules your application needs.
    install_requires=['Flask == 0.10.1', 'Flask-SQLAlchemy == 2.0', 'btctxstore == 4.0.0', 'jsonschema == 2.5.1'],
    tests_require=['coverage', 'coveralls'],
    test_suite="tests",
)
