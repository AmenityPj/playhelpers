Installation
============

Operating systems and Python version
------------------------------------

The library/tool is designed to work with Python 3 (3.9 and greater), from the official Python
implementation [CPython](https://www.python.org/), and is systematically unit tested on Windows, Linux & macOS.
It should also support any other operating systems which has a decent Python 3 support.

Scripts
-------

Multiple scripts are designed for various purposes, which are present in <i>scripts</i> directory.
e.g.:
- ```activate_vir_env.sh / activate_vir_env.bat``` Can be used to activate a virtual environment (venv/.venv) .
- ```install_requirements.sh / install_requirements.bat``` Can be used to install all the required dependencies (libraries/tools) for the library/tool.

<h3>Shell Scripts:</h3>

- Dedicated **Shell Scripts (*.sh)** are designed for Linux/macOS, but can also be used on Windows with a decent support for Shell Scripts (like Git Bash, Cygwin, WSL, etc.). 
However, they may require execution permission to be set before use.

You can set the execution permission using chmod command in terminal. Sample: 
```
cd scripts
chmod +x *.sh
```

<h3>Windows Scripts:</h3>
- Dedicated **Windows scripts (*.bat)** are also designed for Windows, but can also be used on Linux/macOS with a decent support for Batch Scripts (like Wine, etc.).

Dependencies
------------

All Required packages are listed in requirements.txt, which is further bifurcated in 4 categories:

1. ```requirements_build.txt```Required Build Tools / Libraries
2. ```requirements_external.txt```Required External Tools / Libraries
3. ```requirements_internal_lib.txt```Required Internal Libraries
4. ```requirements_internal_tool.txt```Required Internal Tools

Few dedicated Basic Scripts are also present under <i>scripts</i> directory.
- Currently, Scripts are targeting <i>venv</i> (virtual environment directory, Present in parallel of <i>scripts</i>
directory)
- However, the same can be configured in ```config_vir_env.ini``` as per user choice.
  **Note:** installing library/tool in virtual environment is optional but preferred.

Automatic installation using dedicated scripts (Recommended)
----------------------

An installation script (install_requirements.sh / install_requirements.bat) is available in <i>scripts</i> directory.
As soon as you have cloned or downloaded the repository, you can use it to install
the tool/library within your Python package directory.

Refer "Scripts" section for details about the script and its usage.

Automatic installation using IDE (Recommended)
----------------------

Modern IDEs like PyCharm also offers to install Package Requirements automatically.
Once the project is open in IDE, same can be used.

Manual installation using pip commands
----------------------

The usual pip command(s) can be used for manual installation.

Sample Command(s) (Recommended):
```
pip install playhelpers

pip install -r requirements.txt

pip install -r requirements_internal_lib.txt
```

Sample Command(s) (Unwise):
```
# Directly from Git (Main Branch)
pip install git+https://github.com/AmenityPj/playhelpers

# Directly from Git using Specific Tag
pip install git+https://github.com/AmenityPj/playhelpers@v7.0.0

# Directly from Local Cloned Copy (Shell)
pip install /Users/amenitypj/github/playhelpers
pip install ../playhelpers

# Directly from Local Cloned Copy (Windows)
pip install C:\Users\amenitypj\github\playhelpers
pip install ..\playhelpers
```

Manual installation using setup.py
----------------------

Setup File can also be executed manually.

```
Sample Command(s): 

python setup.py install
```

Manual upgrade using pip commands
----------------------

The usual pip command(s) can be used for manual upgrade.

```
Sample Command(s) (Recommended):

pip install --upgrade playhelpers
pip install -r requirements.txt --upgrade
pip install -r requirements_internal_lib.txt --upgrade
```

Installation Troubleshoot
----------------------

If requirements Installation is failed due to *ModuleNotFoundError: No Module named 'incremental'*
Try installing build requirements using dedicated script (install_requirements_build.bat /
install_requirements_build.sh) prior to actual Installation.
