# Repository for CDS Related Utilties

## File cdsutils_srr_pathgetter.py
This function reads a file (or calls an API) which contains a list of NCBI SRR lists and retrieves the filenames and S3 path locations. Please make sure that the depenencies are installed before you use this file.

### Usage

#### File Mode
In file mode this utility, retrieves the s3 paths with a list of SRRs provided in a CSV file.\
python cdsutils_srr_pathgetter.py --fileOrApi file --inputFile phs001554.txt --token prj_12345_A123456.ngc --outputFile test


#### API Mode
In file mode this utility, retrieves the s3 paths for a specific study(phsId).\
python cdsutils_srr_pathgetter.py --fileOrApi api --phsId phs001554 --token prj_12345_A123456.ngc --outputFile test

### Inputs
inputFile: The CSV file with the list of SRR (File Mode)\
phsId: The study Id of interested Study (API Mode)\
token: The NGC file from dBGap\
outputFile: The prefix the output CSV file. 

### Outputs
The final output in the above example would be test_MM_DD_YY_HH_MM_SS.csv which would contain the S3 filepaths and filenames along with the rest of the info for each SRR.


