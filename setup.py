from setuptools import setup, find_packages
package_dir = 'src'
setup(
    name='trading',
    version='0.0.1',
    setup_requires=[
        'pytest-runner',
    ],
    packages= find_packages(package_dir),
    package_dir = {'': package_dir},
    tests_require=['pytest'],
    install_requires = [
        'matplotlib==2.1.1',
        'PeakUtils==1.1.1'
    ]
)
