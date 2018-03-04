from setuptools import setup
setup(
    setup_requires=[
        'pytest-runner',
    ],
    packages= ["trading"],
    package_dir = {'': 'src'},
    tests_require=['pytest']
)
