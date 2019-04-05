## Run the script ##
Example:

cd logic_minimizer

python logic_minimizer.py ../SampleFiles/SampleLogicFile_Config.yml

The main script to run is logic_minimizer/logic_minimizer.py.

It requires specifying a config file as a command line argument.

The config file can have an absolute path or a path relative to current directory.

## Inputs required from the user ##
1. Save a config file
    * required arguments:
        * path to input_file
		* output_file where output should be saved
		* log_file where log should be saved
		* temp_file where the results of any big statements can be temporarily stored during processing
    * optional arguments: 
	    * input_encoding (defaults to utf-8 if not specified) for the encoding of the input_file
		* timeout (defaults to unlimited if not specified) to specify the maximum seconds to spend when trying to minimize a big statement 
2. Save an input file
    * Tab-delimited text file with at least 2 columns
	* First column is a unique identifier for each logic statement
	* Second column is the logic statement with variables specified by numbers and logical operators specified with words, e.g. 1 AND 2 OR 3
	    * It will work if second column is already in format a & b | c, but the script will convert back to numbers and words in the output.
	* Any other columns are irrelevant but will be included in the output as additional columns
	
	
## Dependencies ##

python 3.3+ required, and 3.5+ recommended

Dependencies are listed in requirements.txt

pip install -r requirements.txt

Notes:
* The pyeda package containing the espresso minimization algorithm requires a C extension for python.
    * An easy way to install this package on Windows without worrying about the extension is to download the wheel from Christoph Gohlke's website:
    * https://www.lfd.uci.edu/~gohlke/pythonlibs/
    * My version is Windows 32-bit, with python 3.7.
    * It needs to match the OS and python version.
	* pip install pyeda-0.28.0-cp37-cp37m-win32.whl
	* To install on Linux, download the egg from github and install
* The other dependencies should be straightforward to install

## What does it do? ##
Given a text file with a bunch of logic statements in the form "1 AND 2 OR 3", it applies the espresso minimization algorithm, as implemented by PyEDA, to minimize each statement.

It returns a text file containing columns with a list of redundant variables (variables that are not present in the reduced statement) and a classification.

There is no guarantee that the espresso algorithm returns the global minimum, but usually it does, and it is good enough for finding most redundancies.

It might even be guaranteed that espresso produces an expression with no redundant variables--if anyone knows, please let me know--saaron at bwh dot harvard dot edu.

## Warning ##
Very large statements can cause a lot of memory to be used and may segfault because of an unknown problem with espresso.

Big statements are thus run in a child process so that if the child process is killed, the parent process can continue. It is expected that some very large statements can not be minimized even with large amounts of memory.

When running the minimizer on Windows, if a child process is killed, the Windows debugger may issue a pop-up. This requires the user to respond to the dialogue box in order for the script to continue.
