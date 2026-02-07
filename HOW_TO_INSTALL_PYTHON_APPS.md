Installation
============

Operating systems and Python version
------------------------------------

The library/tool is designed to work with Python 3 (3.9 and greater), from the official Python 
implementation [CPython](https://www.python.org/), and is systematically tested on Windows. 
It should also support any other operating systems which has a decent Python 3 support.

Dependencies
------------

All Required packages are listed in requirements.txt, which is further bifurcated in 4 categories:
1. ```requirements_build.txt```Required Build Tools / Libraries 
2. ```requirements_external.txt```Required External Tools / Libraries
3. ```requirements_internal_lib.txt```Required Internal Libraries
4. ```requirements_internal_tool.txt```Required Internal Tools

Few dedciated Basic Scripts are also present under <i>scripts</i> directory.
   - Currently, Scripts are targeting <i>venv</i> (virtual environment directory, Present in parallel of <i>scripts</i> directory)
   - However, the same can be modified as per user choice.
    
   **Note:** installing library/tool in virtual environment is optional but preferred.

Automatic installation using dedicated scripts (Recommended)
----------------------

An installation script is (requirements_install.bat / requirements_install.sh) available in <i>scripts</i> directory.
As soon as you have cloned or downloaded the repository, you can use it to install
the tool/library within your Python package directory.

Manual installation using pip commands
----------------------

The usual pip command(s) can be used for manual installation.

```
Sample Command(s):

pip install playhelpers
pip install git+https://github.com/AmenityPj/playhelpers@v6.0.0.git
pip install -r requirements.txt
pip install -r requirements_internal_lib.txt
```

An installation script is (requirements_install.bat / requirements_install.sh) available.
As soon as you have cloned or downloaded the repository, you can use it to install
the tool/library within your Python package directory.

Manual installation using setup.py
----------------------

Setup File can also be executed manully.

```
Sample Command(s): 

python setup.py install
```

Installation Troubleshoot
----------------------

If requirements Installation is failed due to *ModuleNotFoundError: No Module named 'incremental'*
Try installing build requirements using dedicated script (requirements_install_build.bat / requirements_install_build.sh) prior to actual Installation.
