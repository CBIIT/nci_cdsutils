from urllib.parse import urlparse
import csv,argparse,os,pandas as pd
from datetime import datetime
import requests
import json

# This function gets a presigned url path and returns a valid s3 path
def get_s3_path_from_presignedurl(presigned_url):
    parsed_result = urlparse(presigned_url, allow_fragments=False)
    s3_path = 's3://'+parsed_result.netloc.split('.')[0]+parsed_result.path
    #print(s3_path)
    return s3_path



# This function returns the an array of tuples for a given SRR from the NCBI API
def get_s3_path_from_srr(srr,ngc_location,aws_region):
    print(f'Processing {srr}...')
    BASE_URL='https://www.ncbi.nlm.nih.gov/Traces/sdl/1/retrieve?acc='
    url = BASE_URL+srr+'&location=s3.'+aws_region
    files = {'ngc': open(ngc_location,'rb')}
    response = requests.post(url, files=files)
    #Returns a list of dictionaries and extracting the first item
    data = response.json()[0]
    # Initializing an Empty List
    list_of_files_paths=[]
    # If there are any files for this SRR, then return an array of tuples
    if 'files' in data.keys():
        for item in data['files']:
            presigned_url =((item['link']))
            filename = item['name']
            # Call the function to get the S3 path
            s3_path=get_s3_path_from_presignedurl(presigned_url)
            list_of_files_paths.append((srr,filename,s3_path))

    #print(list_of_files_paths)
    return list_of_files_paths

#Returns the current date-time in a specific format
def get_time():
    return datetime.now().strftime("%m-%d-%Y-%H-%M-%S")    



    
#Adding desired arguments to the script    
parser = argparse.ArgumentParser(description='Script to populate NCBI file')
parser.add_argument("--inputFile", required=True, type=str, help="Name of  NCBI SRR File")
parser.add_argument("--token",required=True, type=str, help="Location of NGC File from dBGap with extension .ngc")
parser.add_argument("--awsRegion",default='us-east-1', type=str, help="AWS Region of interest")
parser.add_argument("--outputFile", required=True, type=str, help="Name of  Output CSV formatted file")

#Parsing the provided arguments
args = parser.parse_args()

try:
    #Storing the input file
    ncbi_metadata_file=args.inputFile

    #Read the file into a Pandas DataFrame
    df = pd.read_csv(ncbi_metadata_file,sep=',',header = 0)
     
    #Store the token NGC file
    ngc_token=args.token

    # Generates a List of Lists of Tuples with (SRR, FilePath, Filename)
    list_of_tuples=[get_s3_path_from_srr(srr,ngc_token,'us-east-1') for srr in df['Run']]

    # Flatten to a single list of tuples
    flat_list_tuples = [item for sublist in list_of_tuples for item in sublist]
    #print(flat_list_tuples)

    #Convert the list of tuples to a Dataframe
    df_filepaths_srr = pd.DataFrame(flat_list_tuples, columns =['Run', 'Filename', 'FilePath']) 

    #Merging the dataframes
    df_merged= df_filepaths_srr.merge(df,how='left',on='Run')

    # Write to CSV with the filename_timestamp.csv format
    final_output_file=f'{args.outputFile}_{get_time()}.csv'

    #Write the Dataframe to CSV
    df_merged.to_csv(final_output_file, sep=',', index=False)
except Exception as e:
    print(e)



