# Compare two energy level files
This Python script take two energy level files and compares the energy levels and then combines the output.

As per request the filenames, directories, and column numbers are all defined in the script. This can easily be added to a command line argument instead. To run simply do:

`python3 match_energy.py`

There are tests included in test_match_energy.py. To run the tests do `pytest` in the same directory as the script and the tests. Youmust ahve pytest installed for this.

There is a requirements.txt with the required packages inside. To install these automatically with pip run:

`pip install -r requirements.txt`