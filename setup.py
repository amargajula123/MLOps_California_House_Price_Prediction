from setuptools import setup,find_packages
from typing import List


PROJECT_NAME = "housing-predictor"
VERSION = "0.0.4"
AUTHOR = "Amar Gajula"
DESCRIPTION = "This is 2025/5th month ML project, its about California house price prediction using regression on housing dataset."
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list() -> List[str]:
    """
    Description: Returns a list of dependencies/libraries from requirements.txt, excluding '-e .'"""
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirements = requirement_file.read().splitlines()  # Read lines properly
        
    if "-e ." in requirements:
        requirements.remove("-e .")  # Remove "-e ." safely
    return requirements



setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),  # Finds all Python packages with __init__.py for installing
    install_requires=get_requirements_list()  # Installs dependencies
)
# Your own packages/modules (find_packages())

# External libraries (install_requires)

# find_packages() will search all the packages that you are created, and its going to
#  return that names in the list where ever "__init__.py" file is there only that folder
# /package its going to return ex:- ['housing']

# install_requires=get_requirements_list() to install External Libraries which is required
# for this project its libraries are available in the requirements.txt 

# why we are removing -e . ?
# we have packages=find_packages() this is for all the package where ever there is __init__ file
# this will return packages/folders as a list we say this is for to install our own custome/user/internal pakages  
# similarly we have for External libraries install we use install_requires=get_requirements_list()
# so here in requirements.txt "-e ." will also search for all the files for the instalation
# that is the ression we removed (-e.) from requirements.txt so that External will install