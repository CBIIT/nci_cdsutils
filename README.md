# Repository for CDS Related Utilties

## File cdsutils_srr_pathgetter.py
This function reads a file which contains a list of NCBI SRR lists and retrieves the filenames and S3 path locations.
### Usage
python cdsutils_srr_pathgetter.py --inputFile phs001554.txt --token prj_12345_A123456.ngc --outputFile test
### Inputs
inputFile: The CSV file with the list of SRR.

token: The NGC file from dBGap

outputFile: The prefix the output CSV file. 

### Outputs
The final output in the above example would be test_MM_DD_YY_HH_MM_SS.csv which would contain the S3 filepaths and filenames along with the rest of the info for each SRR.


