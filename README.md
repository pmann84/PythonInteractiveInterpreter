# README #

An graphical interactive Python interpreter with module introspection.

* Version: 1.0.0
* Author: Peter Mann

## How do I get set up? ##

### Dependencies ###
This application has the following package dependencies (see requirements.txt for versions):
	* Python 3.4+
	* PyQt5
	* PyInstaller 

You can install these dependencies using pip, preferably in a virtual environment.

### Setting up a Virtual ###
Setup a virtual environment by running

`python -m venv env`

Activate the environment with 

`env\Scripts\activate`

Install dependencies with `pip`

`pip install -r requirements.txt`

### Generating Executable ###
You can generate an exe for the interactive interpreter that makes it easier to run/distribute you can do this by running

`pyinstaller -F -w pii\pii.py` 

this generates an exe in the `dist` folder. Note this has only been tested on Windows :D

### Running the application manually ###
To run the application manually without generating an exe everytime, you can just run 

`python <path_to_pii_checkout>/bin/pii.py`

this will launch the application and will be ready for use immediately.

### Running the tests ###
The tests can simply be run by 

`python <path_to_pii_checkout>/unittests/unittests.py`
