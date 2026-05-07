# imbit-abm-test
Tests for the output of IMBIT ABM

To setup, run the ABM and copy the output file to the `data` folder.
Adjust the variable `OUTPUT_DIR` in the `test_output.py` file and then run the tests.

Currently only two tests are written:

1. Test to check that sum of SEIR is constant. 
This needs to be adjusted with the birth and death rates.

2. Test that SEIR populations is never negative
