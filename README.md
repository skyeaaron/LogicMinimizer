## Run the script ##
Example:
cd logic_minimizer
python logic_minimizer.py ../SampleFiles/SampleLogicFile_Config.yml

The main script to run is logic_minimizer/logic_minimizer.py.
It requires specifying a config file as a command line argument.
The config file can have an absolute path or relative to current directory.

## Inputs required from the user ##
1. Save a config file
    * required arguments:
        * path to input_file
		* output_file where output should be saved
		* log_file where log should be saved
    * optional arguments: 
	    * input_encoding (defaults to utf-8 if not specified) for the encoding of the input_file
		* max_variables so that the script will ignore any logic statements that exceed the number of variables specified. (espresso minimization is very fast even with many variables, so I would try without this first.)
2. Save an input file
    * Text delimited file with at least 2 columns
	* First column is a unique identifier for each logic statement
	* Second column is the logic statement with variables specified by numbers and logical operators specified with words, e.g. 1 AND 2 OR 3
	    * It will work if second column is already in format a & b | c, but the script will convert back to numbers and words in the output.
	* Any other columns are irrelevant but will be included in the output as additional columns
	
	
## Dependencies ##
Listed in dependencies.txt
Notes:
* The pyeda package containing the espresso minimization algorithm requires a python C++ extension.
    * An easy way to install this package without worrying about the extension is to download the wheel from Christoph Gohlke's website:
    * https://www.lfd.uci.edu/~gohlke/pythonlibs/
    * My version is Windows 32-bit, with python 3.7.
    * It needs to match the OS and python version.
* The other dependencies should be straightforward to install
    * pip install -r dependencies.txt

## What does it do? ##
Given a text file with a bunch of logic statements, it applies the espresso minimization algorithm to minimize each statement.
It returns the minimized form and a list of redundant variables (variables that are not present in the reduced statement).
There is no guarantee that the espresso algorithm returns the global minimum, but usually it does, and it is good enough for finding most redundancies.