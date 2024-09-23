''' 
PyReports | Python Setup
'''

from setuptools import setup, find_packages, Extension

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "pyreports",
    version = '2024.09.24',
    description="Toolkit for Documentation and Reporting",
    long_description = "README.md",
    author = 'Pablo GP',
    author_email = "pablogonzalezpila@gmail.com",
    url = "https://github.com/PaulFilms/PyReports",
    license = "Apache License",
    # package_dir={'': 'src'},
    # packages = find_packages(where='src'), # con find_pachages no conseguir hacerlo funcionar
    # packages=find_packages(),
    packages=["pyreports"],
    include_package_data=True, # muy importante para que se incluyan archivos sin extension .py
    install_requires=requirements,
    # classifiers = [
    #     'Programming Language :: Python :: 3.12',
    #     "Intended Audience :: Developers",
    #     "Intended Audience :: System Administrators",
    #     # "Operating System :: OS Independent",
    #     "Topic :: Software Development",
    # ],
)