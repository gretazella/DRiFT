import pandas as pd
import os
from tqdm import tqdm

def create_diachronic_corpora(input_path, f, output_path):
    # Extract category and year from the filename
    subreddit, year = f.split('_')[0], f.split('_')[1].split('.')[0]

    # Create one file for each community
    for key, value in communities.items():
        if subreddit in value:
            if key == 'Generic':
                if 2010 <= int(year) <= 2014:
                    # Construct output filename
                    output_filename = f"{key}_t0.json"
                if 2021 <= int(year) <= 2022:
                    # Construct output filename
                    output_filename = f"{key}_t1.json"
            elif key == 'Sustainable':
                if 2010 <= int(year) <= 2016:
                    # Construct output filename
                    output_filename = f"{key}_t0.json"
                if 2021 <= int(year) <= 2022:
                    # Construct output filename
                    output_filename = f"{key}_t1.json"
                    
        # Check if the merged file already exists
            if os.path.isfile(output_path+output_filename):
                # Community corpus already exists, append data to the existing file
                with open(output_path+output_filename, 'a') as output_file:
                  
                    # Read and append data to the merged file
                    try:
                        df = pd.read_json(input_path+f, lines=True)
                        df.to_json(output_file, orient='records', lines=True)
                    except pd.errors.EmptyDataError:
                        print(f"Warning: Empty file encountered: {input_path+f}")
            else:
                # Community corpus doesn't exist, create a new file
                try:
                    df = pd.read_json(input_path+f, lines = True)
                    with open(output_path+output_filename, 'w', encoding='utf-8') as output_file:
                        df.to_json(output_file, orient='records', lines=True)
                except pd.errors.EmptyDataError:
                    print(f"Warning: Empty file encountered: {input_path+f}")

# Iterate through each file in the input directory
def create_diastratic_corpora(input_path, f, output_path):
    # Extract category and year from the filename
    subreddit = f.split('_')[0]

    # Create one file for each community
    for key, value in communities.items():
        if subreddit in value:
    
            # Construct output filename
            output_filename = f"{key}.json"
            # Check if the merged file already exists
            if os.path.isfile(output_path+output_filename):
                # Community corpus already exists, append data to the existing file
                with open(output_path+output_filename, 'a') as output_file:
                  
                    # Read and append data to the merged file
                    try:
                        df = pd.read_json(input_path+f, lines=True)
                        df.to_json(output_file, orient='records', lines=True)
                    except pd.errors.EmptyDataError:
                        print(f"Warning: Empty file encountered: {input_path+f}")
            else:
                # Community corpus doesn't exist, create a new file
                try:
                    df = pd.read_json(input_path+f, lines = True)
                    with open(output_path+output_filename, 'w', encoding='utf-8') as output_file:
                        print(df)
                        exit()
                        df.to_json(output_file, orient='records', lines=True)
                except pd.errors.EmptyDataError:
                    print(f"Warning: Empty file encountered: {input_path+f}")

def main(input_path, output_path):

    list_of_sub_files = [sub_file for sub_file in os.listdir(input_path)]
    os.makedirs(output_path, exist_ok=True)  
    for f in tqdm(list_of_sub_files):   
        print(f)
        create_diastratic_corpora(input_path, f, output_path)
        create_diachronic_corpora(input_path, f, output_path)

# Retrieve selected subreddits
df = pd.read_csv("selected_subreddits.csv")

# Create the dictionary with community as key and list of subreddits as values
communities = {}

for index, row in df.iterrows():
    community = row['Community']
    subreddit = row['Subreddit']
    if community not in communities:
        communities[community] = []
    communities[community].append(subreddit.strip('r/'))

if __name__ == '__main__':   
    
    input_path = '[path to directory with one unique json file for each subreddit-year]'
    output_path = '[path to directory where corpora are stored]'
  
    main(input_path, output_path)



