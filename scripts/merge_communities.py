import pandas as pd
import os
from tqdm import tqdm

# Iterate through each file in the input directory
def merge_communities(input_path, f, output_path):
    # Extract category and year from the filename
    subreddit, year = filename.split('_')[0], filename.split('_')[1].split('.')[0]

    # Create one file for each community
    for key, value in communities.items():
        if subreddit in value:
    
            # Construct output filename
            output_filename = f"{key}_{year}.json"
            
            # Check if the merged file already exists
            if os.path.isfile(output_path+output_filename):
                # File already exists, append data to the existing file
                with open(output_path+output_filename, 'a') as output_file:
                  
                    # Read and append data to the merged file
                    try:
                        df = pd.read_json(input_path+f, lines=True)
                        df.to_json(output_file, orient='records', lines=True)
                    except pd.errors.EmptyDataError:
                        print(f"Warning: Empty file encountered: {file_path}")
            else:
                # File doesn't exist, create a new file
                try:
                    df = pd.read_json(input_path+f, lines = True)
                    with open(output_path+output_filename, 'w', encoding='utf-8') as output_file:
                        df.to_json(output_file, orient='records', lines=True)
                except pd.errors.EmptyDataError:
                    print(f"Warning: Empty file encountered: {file_path}")

def main(input_path, output_path):
  
    # Retrieve selected subreddits
    df = pd.read_csv("../data/selected_subreddits.csv")
    
    # Create the dictionary with community as key and list of subreddits as values
    communities = {}
    
    for index, row in df.iterrows():
        community = row['Community']
        subreddit = row['Subreddit']
        if community not in communities:
            communities[community] = []
        communities[community].append(subreddit)

    list_of_sub_files = [sub_file for sub_file in os.listdir(input_path)]
    os.makedirs(output_path, exist_ok=True)  
    for f in tqdm(list_of_sub_files):
        merge_communities(input_path, f, output_path)


if __name__ == '__main__':   
    
    input_path = '[path to directory containing one unique json file for each subreddit-year combination]'
    output_path = '[path to directory where diachronic and diastratic corpora are stored]'
  
    main(input_path, output_path)
