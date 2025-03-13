import pandas as pd
import os

# Retrieve classified selected subreddits
df = pd.read_csv("selected_subreddits.csv")

# Create the dictionary with community as key and list of subreddits as values
communities = {}

for index, row in df.iterrows():
    community = row['Community']
    subreddit = row['Subreddit']
    
    if community not in communities:
        communities[community] = []
    
    communities[community].append(subreddit)

# Iterate through each file in the input directory
def merge_communities(input_folder):
  for filename in os.listdir(input_folder):
      #print(filename)
      file_path = os.path.join(input_folder, filename)
      if os.path.isfile(file_path) and filename.endswith('.json'):
          # Extract category and year from the filename
          subreddit, year_with_extension = filename.split('_')
          year = year_with_extension.split('.')[0]
          print(subreddit, year)
          #exit()
          
          for key, value in communities.items():
              if subreddit in value:
          
                  # Construct output filename
                  output_filename = key+'_'+year+'.json'
                  output_path = os.path.join(output_folder, output_filename)
                  #print(output_path)
                  
                  # Check if the merged file already exists
                  if os.path.isfile(output_path):
                      # File already exists, append data to the existing file
                      with open(output_path, 'a') as outfile:
                          # Print lines causing DtypeWarning
                          
                          # Read and append data to the merged file
                          try:
                              df = pd.read_json(file_path, lines=True)
                              df.to_json(outfile, orient='records', lines=True)
                          except pd.errors.EmptyDataError:
                              print(f"Warning: Empty file encountered: {file_path}")
                  else:
                      # File doesn't exist, create a new file
                      try:
                          df = pd.read_json(file_path, lines = True)
                          with open(output_path, 'w', encoding='utf-8') as outfile:
                              df.to_json(outfile, orient='records', lines=True)
                      except pd.errors.EmptyDataError:
                          print(f"Warning: Empty file encountered: {file_path}")
input_folder=""
merge_communities(input_folder)
