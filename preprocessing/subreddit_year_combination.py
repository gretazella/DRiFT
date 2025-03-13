import pandas as pd
import json
import gzip
import os
    
# Dictionary to keep track of the number of files written for each subreddit-year combination
file_count = {}

def create_sub_year_files(input_folder):
    # Iterate through each file in the input directory
    for filename in sorted(os.listdir(input_folder)):
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path) and filename.endswith('.jsonl.gz'):
            # Read the JSONL.gz file
            with gzip.open(file_path, 'rt', encoding='utf-8') as file:
                df = pd.read_json(file, lines=True)
            
            # Convert 'created_utc' from epoch time to datetime
            df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
            
            # Convert datetime to year
            df['year'] = df['created_utc'].dt.year
            
            # Group by subreddit and year
            grouped = df.groupby(['subreddit', 'year'])
            
            # Output each group to a separate jsonl file
            for (subreddit, year), group in grouped:
                # Increment file count for the category-year combination
                file_count[(subreddit, year)] = file_count.get((subreddit, year), 0) + 1
                
                # counter
                counter_str = str(file_count[(subreddit, year)]).zfill(3)
                
                # Naming output file
                output_filename = f"{subreddit}_{year}_{counter_str}.jsonl.gz"
                
                # Write group to jsonl file
                output_path = os.path.join(output_folder, output_filename)
                with gzip.open(output_path, 'wt', encoding='utf-8') as out_file:
                    group.to_json(out_file, orient='records', lines=True)

create_sub_year_files(input_folder)
