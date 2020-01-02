# README #

An graphical interactive Python interpreter with module introspection.

* Version: 1.0.0
* Author: Peter Mann

## How do I get set up? ##

### Dependencies ###
This application has the following package dependencies:
	* Python 3.4+
	* PyQt5 v5.14.0

You can install these dependencies using pip, preferably in a virtual environment.

### Setting up a Virtual ###
Setup a virtual environment by running

`python -m venv env`

Activate the environment with 

`env\Scripts\activate`

Install dependencies with `pip`

`pip install -r requirements.txt`

### Running the application ###
Setup is very manual at the moment. First checkout the source code from the repository. Then you can run the application, the script is setup so that you just have to run

`python <path_to_pii_checkout>/bin/pii.py`

this will launch the application and will be ready for use immediately.

### Running the tests ###
The tests can simply be run by 

`python <path_to_pii_checkout>/unittests/unittests.py`
